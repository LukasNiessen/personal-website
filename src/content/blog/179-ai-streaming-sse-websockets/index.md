---
title: "Streaming in AI Apps: REST, SSE, WebSockets, Polling, and the Backend Reality"
summary: "A high-level and practical explanation of polling, long polling, SSE, WebSockets, HTTP streaming, and how modern AI applications stream tokens, progress, tool calls, and agent state across horizontally scaled infrastructure."
date: "Jun 11 2026"
tags:
  - AI
  - Architecture
  - Streaming
  - Server-Sent Events
  - WebSockets
  - System Design
---

# Streaming in AI Apps: REST, SSE, WebSockets, Polling, and the Backend Reality

Let's talk about streaming. Consider this situation:

```text
User asks an AI agent something
  -> backend starts working
  -> model produces tokens
  -> tools are called
  -> progress events happen
  -> final answer appears maybe 30 seconds later
```

The simple version would be:

```text
POST /chat
  -> wait
  -> wait more
  -> wait maybe a minute
  -> return final answer
```

This works but is obviously a terrible user experience. So we need some way of showing the user progress. Modern AI applications usually stream something back to the client:

- partial tokens
- progress messages
- tool call status
- retrieved sources
- intermediate steps
- final answer
- errors
- cancellation status

Streaming has different flavors and approaches with tradeoffs.

How exactly is it streamed? Is this REST? Is this WebSockets? Is this Server-Sent Events? What happens with Kubernetes pods? What about horizontal scaling? Do we need sticky sessions? Can an AI worker on one pod stream to a browser connected to another pod? What if the user refreshes the page?

Let's go through it.

## The Four Common Patterns

There are four patterns you should know.

### 1. Polling

Polling means the client asks again and again.

```text
Client -> Server: any updates?
Server -> Client: no

5 seconds later

Client -> Server: any updates?
Server -> Client: no

5 seconds later

Client -> Server: any updates?
Server -> Client: yes, here is the new state
```

This is extremely simple.

For example:

```javascript
setInterval(async () => {
  const response = await fetch("/api/runs/123");
  const run = await response.json();
  render(run);
}, 3000);
```

The downside is obvious. You either poll often and waste resources, or you poll rarely and the UI feels delayed.

Polling is still not bad. If the thing updates every few minutes, polling is fine. A dashboard that refreshes every 30 seconds does not need WebSockets just because WebSockets sound more exciting.

### 2. Long Polling

Long polling is a better version of polling.

The client asks for updates, but the server does not answer immediately. It holds the request until something happens or a timeout is reached.

```text
Client -> Server: any updates?
Server waits...
Server waits...
Server -> Client: yes, event happened

Client immediately asks again
```

This gives near real-time behavior while still using plain HTTP requests.

It was very useful before WebSockets and SSE became common. It is still useful as a fallback, but in greenfield AI applications I usually would not start here.

### 3. Server-Sent Events

Server-Sent Events, or SSE, is an event-stream format delivered over HTTP. Browsers provide the `EventSource` API for consuming it. (`EventSource` is a Web API defined by the HTML standard, not part of JavaScript or ECMAScript itself. Outside browsers, support depends on the runtime and version; you may need a library or parse a streaming `fetch()` response yourself.)

Client:

```javascript
const events = new EventSource("/api/runs/123/events");

events.addEventListener("message", (event) => {
  const data = JSON.parse(event.data);
  render(data);
});

events.addEventListener("done", () => {
  events.close();
});
```

Server response:

```text
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache

event: token
data: {"text":"Hello"}

event: token
data: {"text":" world"}

event: done
data: {}
```

Small detour: `Content-Type` tells the client how to interpret the response body.

In normal JSON APIs you usually see:

```text
Content-Type: application/json
```

That means: "The body is JSON."

Other common values are:

```text
Content-Type: text/plain
```

Plain text.

```text
Content-Type: text/html
```

HTML page.

```text
Content-Type: application/octet-stream
```

Generic binary data, often used for downloads.

```text
Content-Type: multipart/form-data
```

Usually file uploads from forms.

```text
Content-Type: application/x-ndjson
```

Newline-delimited JSON. This is sometimes used for streaming because each line is its own JSON object.

And then there is:

```text
Content-Type: text/event-stream
```

This means: "The body is an SSE stream." It is not one finished JSON response. It is a sequence of small text frames that look like this:

```text
event: token
data: {"text":"Hello"}

```

So `text/event-stream` is not a random alternative to JSON. It is the media type for this specific streaming format.

### How Does The Server Know Where To Send Events?

This is a very natural question.

Is the client sending some callback URL to the server?

No.

That would be a webhook-style design:

```text
Client tells server:
  When something happens, call https://my-client.example.com/callback
```

SSE is not that.

With SSE, the client opens an HTTP request to the server:

```text
Client -> Server:
GET /api/runs/123/events
Accept: text/event-stream
```

The server answers with:

```text
Server -> Client:
HTTP/1.1 200 OK
Content-Type: text/event-stream
```

And then the important part:

> The server does not close the response.

The server keeps the HTTP connection open and keeps writing bytes into that same response.

So the server does not need a callback URL. It does not need to later "find" the client. The client is already connected. The open TCP connection is the path back to the client.

The mental model is:

```text
Client opens connection
Server keeps response open
Server writes event 1
Server writes event 2
Server writes event 3
Client reads events as they arrive
```

Not:

```text
Client sends callback address
Server later starts a new request to the client
```

In the browser, `EventSource` wraps this for you. In a mobile app, desktop app, CLI, or Node.js service, the same idea applies. You use an HTTP client that can read a streaming response, then parse the `event:` and `data:` lines as they arrive.

So the client technology changes, but the pattern stays the same:

```text
Open HTTP request
Keep response open
Read events incrementally
Reconnect if needed
```

That open connection can disappear at any time because the user closes the tab, changes networks, or simply loses connectivity. The server should detect that the request was aborted or the response was closed, stop writing to it, and release any subscription or stream reader attached to it. Whether that also stops the AI run is a separate decision. In a durable architecture, the run usually continues and only this particular reader disappears. The client can then reconnect and resume from the last event ID.

The important properties:

- server to client only
- uses normal HTTP
- simple browser API
- automatic reconnection
- supports event IDs with `Last-Event-ID`
- text-based, not binary

For many AI chat and agent UIs, SSE is the default good answer.

Why? Because the browser usually sends one request:

```text
Please start or observe this run.
```

And then the server streams updates back:

```text
token
token
tool_started
tool_finished
token
done
```

The client does not need to constantly send messages back over the same connection. If the user wants to cancel, you can call a normal HTTP endpoint:

```text
POST /runs/123/cancel
```

So one-way streaming is often enough.

### 4. WebSockets

WebSockets create a bidirectional communication channel.

```javascript
const socket = new WebSocket("wss://example.com/ws");

socket.onopen = () => {
  socket.send(JSON.stringify({
    type: "subscribe",
    runId: "123"
  }));
};

socket.onmessage = (event) => {
  const message = JSON.parse(event.data);
  render(message);
};
```

The server can send messages to the client, and the client can send messages to the server, all over the same connection.

This is useful when the interaction is truly bidirectional:

- collaborative editing
- multiplayer games
- live cursors
- audio or voice sessions
- interactive terminals
- applications where the client frequently sends control messages

For AI chat, WebSockets can make sense, but they are not automatically better.

They also bring operational complexity:

- connection lifecycle
- reconnect logic
- load balancing
- sticky sessions if connection state is local
- backpressure
- message ordering
- auth refresh
- gateway timeouts

So my simple rule is:

> Use SSE when the server mainly pushes progress to the client. Use WebSockets when both sides need to talk frequently during the same session.

## Quick Comparison

| Pattern | Direction | Good For | Main Problem |
| --- | --- | --- | --- |
| Polling | client asks repeatedly | simple status checks | waste or delay |
| Long polling | client asks, server waits | fallback real-time | timeout handling |
| SSE | server pushes over HTTP | AI tokens, progress, dashboards | one-way only |
| WebSockets | bidirectional | voice, collaboration, interactive apps | stateful ops complexity |

## What Is HTTP Streaming Actually?

At a lower level, HTTP streaming means the server starts sending the response before it knows the whole response.

Instead of:

```text
calculate full response
send response
close
```

it does:

```text
send headers
send chunk 1
send chunk 2
send chunk 3
close when done
```

With HTTP/1.1 this is often done using chunked transfer encoding. With HTTP/2, the framing is different, but the idea is similar: data arrives over time.

The server code usually looks conceptually like this:

```typescript
res.writeHead(200, {
  "Content-Type": "text/event-stream",
  "Cache-Control": "no-cache",
  "Connection": "keep-alive",
});

res.write(`event: token\ndata: {"text":"Hello"}\n\n`);
res.write(`event: token\ndata: {"text":" world"}\n\n`);
res.write(`event: done\ndata: {}\n\n`);
res.end();
```

There is no magic here. The server is writing bytes to an open response.

One important detail: calling `write()` only hands bytes to the next layer in the stack. A framework, compression layer, reverse proxy, or gateway may still buffer them. Where the stack exposes explicit flushing, you may need to flush headers or chunks, but the real test is whether small events arrive promptly through the complete production path.

The magic, or better said the engineering work, is everything around it:

- flushing data quickly
- preventing proxy buffering
- handling disconnects
- reconnecting safely
- not losing events
- scaling across many instances
- keeping the worker and stream connection coordinated

That is where the interesting part starts.

## So Is An SSE Endpoint REST?

Now that we know what the client and server are actually doing, we can clear up a common misconception.

People often phrase the choice like this:

```text
REST vs streaming
```

That is not quite right because these are two different concepts:

```text
REST:
  How does the API model and interact with resources?

SSE:
  How is this particular HTTP response delivered?
```

They can be used together, and often are. SSE uses HTTP, but using HTTP does not automatically make an API RESTful. An SSE endpoint can be part of a REST-style API, but it can just as easily be part of an RPC-style API. Whether the system follows REST depends on the broader API design, not on the stream format.

A common design combines both like this:

```text
POST /runs
  -> create a run

GET /runs/123
  -> get the current run state

GET /runs/123/events
Accept: text/event-stream
  -> observe the run as events happen
```

The first two responses finish normally. The third endpoint still uses HTTP and still represents something related to the `run` resource, but its response stays open.

When the client opens that SSE endpoint:

```text
GET /runs/123/events
Accept: text/event-stream
```

The `GET` happens once when the client opens the stream. It does not mean the client keeps sending `GET` requests whenever it wants another event.

The server starts the response, leaves it open, and writes new events into that same response when they become available:

```text
Client -> Server: GET /runs/123/events
Server -> Client: response headers
Server -> Client: event 1
Server -> Client: event 2
Server -> Client: event 3
Server -> Client: done
```

So this is still normal HTTP and it can fit into a REST-style API. The unusual part is only that the response is long-lived instead of one complete JSON document returned at once.

Conversely, you can stream the response to an RPC-style `POST` endpoint too:

```text
POST /chat
Accept: text/event-stream
```

That endpoint may not be particularly RESTful, but it can still use SSE. Again, these are separate dimensions.

The more useful distinction is therefore:

```text
short request/response
  vs
long-lived response
  vs
bidirectional connection
```

SSE uses a long-lived HTTP response. WebSockets go further and allow both sides to send messages whenever they want. So instead of asking "REST or streaming?", ask both questions: how should the API model its resources, and which interaction pattern does this particular operation need?

## The Simple AI Streaming Version

The simplest AI streaming architecture looks like this:

```text
+---------+        +-------------+        +-----------+
| Browser | -----> | API Backend | -----> | LLM API   |
|         | <----- |             | <----- | streaming |
+---------+        +-------------+        +-----------+
                         |
                         v
                  writes chunks to browser
```

The backend calls the model provider with streaming enabled. As the provider sends tokens to the backend, the backend forwards them to the browser.

In pseudocode:

```typescript
app.post("/chat", async (req, res) => {
  startSse(res);

  const stream = await llm.responses.stream({
    input: req.body.message,
  });

  for await (const event of stream) {
    if (event.type === "text_delta") {
      sendSse(res, "token", { text: event.text });
    }
  }

  sendSse(res, "done", {});
  res.end();
});
```

This is fine for a demo or a small product.

But it has one important limitation:

> The HTTP request is doing the work.

If the user disconnects, the request may be cancelled. If the pod dies, the work is gone. If the model call takes two minutes, one web request is open for two minutes. If you want retries, resumability, audit logs, tool steps, and background execution, this gets messy quickly.

So serious AI systems usually separate the user connection from the actual work.

## The More Serious AI Architecture

A more production-like architecture often looks like this:

```text
                start run
+---------+  ---------------->  +-------------+
| Browser |                     | API Backend |
+---------+  <----------------  +-------------+
                run_id                |
                                      | enqueue job
                                      v
                                +------------+
                                | Queue      |
                                +------------+
                                      |
                                      | consume
                                      v
                                +------------+
                                | AI Worker  |
                                +------------+
                                      |
                                      | writes events
                                      v
                                +------------+
                                | Event Log  |
                                +------------+
                                      ^
                                      |
+---------+  SSE /runs/123/events    |
| Browser | <------------------------+
+---------+
```

The flow:

1. The browser creates a run:

```text
POST /runs
```

2. The API returns a `run_id`.

3. The backend enqueues work for an AI worker.

4. The browser opens an SSE stream:

```text
GET /runs/{run_id}/events
```

5. The worker performs the task and writes events to an event log.

6. The stream endpoint reads events and sends them to the browser.

This is more complex, but it gives you very useful properties:

- the AI work can continue if the browser disconnects
- the user can reconnect and resume
- runs can be audited
- events can be replayed
- workers can scale independently from API pods
- long tasks do not depend on one HTTP request staying alive

This is the pattern I would usually prefer for agentic systems.

## What Are The Events?

In AI systems, streaming is not only about tokens.

Tokens are nice because they make the answer feel alive. But in agentic applications, progress events are often more important.

Example event stream:

```text
event: run_started
data: {"run_id":"123"}

event: step_started
data: {"step":"search_docs"}

event: tool_started
data: {"tool":"search_product_docs","query":"refund policy"}

event: tool_finished
data: {"tool":"search_product_docs","matches":4}

event: token
data: {"text":"According"}

event: token
data: {"text":" to"}

event: token
data: {"text":" the policy"}

event: source
data: {"title":"Refund Policy","url":"/docs/refunds"}

event: run_completed
data: {"status":"success"}
```

The UI can render this as:

- "Searching docs..."
- "Reading policy..."
- text appearing token by token
- sources appearing when known
- final answer

This is much better than a spinner.

However, it also means you should treat the stream as a product contract.

Do not just dump random internal logs into the stream. Define event types. Version them. Keep them stable enough that the frontend can rely on them.

Example:

```typescript
type RunEvent =
  | { type: "run_started"; runId: string }
  | { type: "step_started"; stepId: string; title: string }
  | { type: "tool_started"; toolCallId: string; toolName: string }
  | { type: "tool_finished"; toolCallId: string; status: "ok" | "error" }
  | { type: "token"; text: string }
  | { type: "source"; title: string; url: string }
  | { type: "run_completed"; status: "success" | "failed" | "cancelled" };
```

This looks boring. Good. Boring contracts are good.

## The Event Log Is The Center

For serious AI apps, I like thinking of the event log as the center of the streaming architecture.

Not necessarily Kafka. It could be Postgres, Redis Streams, NATS JetStream, Kafka, EventStore, or something else. The important thing is the concept:

```text
Run events are persisted somewhere.
```

Why?

Because without persistence, streaming is fragile.

Suppose you only stream directly from worker memory to the browser:

```text
Worker -> Browser
```

If the browser disconnects, events are gone. If the worker crashes, events are gone. If the user refreshes the page, you may not know what was already sent.

With an event log:

```text
Worker -> Event Log -> Browser
```

you can resume.

The client can say:

```text
GET /runs/123/events
Last-Event-ID: 42
```

and the server can continue from event `43`.

This is one of the reasons SSE is so nice: it has a built-in concept of event IDs and reconnection.

Example SSE frame:

```text
id: 42
event: token
data: {"text":"hello"}
```

If the connection drops, the browser can reconnect and send the last seen event ID.

Of course, you need to implement the backend side. The browser API helps, but it does not magically persist events for you.

## Do You Need Sticky Sessions?

This is one of the big DevOps questions.

Short answer:

> You only need sticky sessions if important connection state lives inside one specific pod.

Let's look at the bad version first.

```text
Browser connects to API Pod A
AI Worker sends events to API Pod A memory
API Pod A streams to browser
```

Now the browser reconnects and the load balancer sends it to API Pod B.

```text
Browser connects to API Pod B
API Pod B has no events
Oops
```

In that design, you either need sticky sessions, or you need to route messages specifically to the pod that owns the connection. This can work, but it is annoying. It makes pods more stateful. It makes deployments and scaling harder.

The better version:

```text
Browser connects to any API pod
API pod reads run events from shared event log
AI worker writes run events to shared event log
```

Diagram:

```text
                 +-------------+
Browser -------> | API Pod A   | ----+
                 +-------------+     |
                                     v
                                +----------+
                                | Event Log|
                                +----------+
                                     ^
                 +-------------+     |
Browser -------> | API Pod B   | ----+
                 +-------------+
```

Now reconnecting to another pod is fine. Any pod can read the run events.

In this design, you do not need sticky sessions for SSE.

What about WebSockets?

WebSocket connections are long-lived and attached to a specific server process. If you store subscription state only in that process, sticky sessions help. But again, the more scalable design is to externalize state:

```text
WebSocket Pod A subscribes to run 123
Worker publishes events to broker
Pod A receives and forwards them
If user reconnects to Pod B, Pod B subscribes to run 123
```

So sticky sessions are not always wrong. Sometimes they are a pragmatic choice. But as a default architecture for horizontally scaled AI apps, I would prefer shared state and resumable streams over sticky sessions.

## Kubernetes And Horizontal Scaling

Let's put this into Kubernetes terms.

You may have:

```text
Deployment: api
  replicas: 5

Deployment: ai-worker
  replicas: 20

Stateful/managed service: postgres or redis or kafka

Ingress / API Gateway
  routes browser traffic to api pods
```

The request flow:

```text
Browser
  -> Ingress
  -> API pod
  -> creates run
  -> queue
  -> worker pod
  -> event log
  -> API pod streams events
  -> Browser
```

Important:

The API pod streaming the response does not have to be the worker pod doing the AI work.

That separation is the whole point.

It lets you scale different things differently:

- API pods scale with concurrent connections and normal HTTP traffic
- worker pods scale with queue depth and model/tool workload
- event log scales with event throughput and retention

For example, if you have 5,000 users watching streams but only 200 active AI runs, you need enough API capacity for connections. If you have 200 users but each run fans out into heavy tool calls, you need more worker capacity.

These are different scaling dimensions.

## What About The Load Balancer And Proxies?

This part is less glamorous but very important.

Streaming can break because of infrastructure defaults.

Common issues:

### 1. Proxy Buffering

Some proxies buffer responses. That means your app writes tokens immediately, but the proxy waits until it has enough data before sending anything to the browser.

From the backend's perspective, streaming works.

From the user's perspective, nothing appears until the end.

Not good.

For nginx, for example, you often need to disable buffering for SSE routes.

Conceptually:

```text
proxy_buffering off;
```

The exact config depends on your ingress controller or gateway.

### 2. Idle Timeouts

Load balancers often close connections that are idle for too long.

If your agent spends 45 seconds inside a tool call and sends nothing during that time, the connection may be killed.

Solution: send heartbeat events.

```text
: heartbeat

```

In SSE, a line starting with `:` is a comment. It keeps the connection alive without changing application state.

### 3. Response Compression

Compression can accidentally add buffering. For small token chunks, the compression layer may wait before flushing.

For SSE, I would usually disable compression unless you have verified that your stack flushes correctly.

### 4. HTTP/2 And Gateway Behavior

SSE can work over HTTP/2, but your full stack must support it properly. Some gateways, CDNs, or service meshes have their own timeout and buffering behavior.

The practical advice is simple:

> Test streaming through the exact production path, not only locally.

Localhost streaming tells you very little about your ingress, CDN, API gateway, service mesh, and browser behavior.

## Backpressure

Backpressure means the receiver cannot consume as fast as the producer produces.

In AI token streaming, this is usually not a huge problem because token rates are modest. But in agent systems it can matter:

- many tool events
- large logs
- many sources
- long generated outputs
- slow mobile client
- bad network

If your worker writes events faster than the stream endpoint can deliver them, you need a buffer somewhere. If that buffer grows without limits, you have a memory problem.

This is another reason to use a durable event log. The worker writes events. The stream reader consumes at its own pace.

But even then, you need limits:

- maximum event size
- maximum number of events per run
- retention period
- rate limits per user or tenant
- cancellation
- compaction for old token events if needed

Streaming does not remove resource management. It just moves it around.

## Cancellation

Cancellation is easy to forget.

The user clicks "Stop generating". What should happen?

Bad version:

```text
Browser closes stream
Worker continues spending money for 60 seconds
```

Better version:

```text
Browser -> POST /runs/123/cancel
API marks run as cancelling
Worker observes cancellation
Worker cancels model/tool calls if possible
Worker writes run_cancelled event
Stream ends
```

The important part is that closing the stream is not enough in a decoupled architecture.

If the stream connection and worker execution are separated, cancellation must be part of the run state.

This is especially important for AI systems because inference and tool calls cost money.

## Reliability: At-Least-Once Shows Up Again

If workers write events to a queue or event log, you will see the same old distributed systems topics again:

- retries
- duplicate events
- ordering
- idempotency
- dead-letter queues
- exactly-once illusions

Suppose a worker writes:

```text
event 42: tool_finished
```

Then it crashes before marking the step as complete. Another worker retries and writes the same event again.

Your event handling should tolerate this.

The usual solutions:

- event IDs
- step IDs
- idempotency keys
- unique constraints
- sequence numbers per run
- client-side deduplication by event ID

Example:

```sql
CREATE TABLE run_events (
  run_id TEXT NOT NULL,
  sequence_number BIGINT NOT NULL,
  event_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMP NOT NULL,
  PRIMARY KEY (run_id, sequence_number)
);
```

Now the stream endpoint can read:

```sql
SELECT *
FROM run_events
WHERE run_id = $1
  AND sequence_number > $2
ORDER BY sequence_number;
```

Again, not glamorous. Very useful.

## WebSockets In AI Apps

So where do WebSockets fit in?

They are not obsolete. They are just not required for every AI chat.

I would consider WebSockets when:

- the client sends frequent control messages during the run
- the app has real-time collaboration
- the AI session is voice/audio based
- the server pushes many different channels of events
- the client and server maintain an interactive session state
- low-latency bidirectional control matters

Examples:

```text
Voice assistant:
  browser streams audio to server
  server streams partial transcript and audio back
  WebSocket or WebRTC makes sense
```

```text
AI coding environment:
  browser sends file edits, terminal input, cancellation, approvals
  server streams logs, diffs, diagnostics, model output
  WebSocket can make sense
```

```text
Simple chat completion:
  user sends prompt
  server streams answer
  SSE is usually enough
```

One thing to be careful about: WebSocket is a transport, not an architecture.

You still need:

- run state
- auth
- reconnection
- event IDs
- replay or recovery
- cancellation
- worker coordination
- observability

Switching from SSE to WebSockets does not solve those. It just gives you a different pipe.

## gRPC Streaming

There is another protocol worth mentioning: gRPC streaming.

gRPC supports:

- server streaming
- client streaming
- bidirectional streaming

This can be excellent for service-to-service communication.

For example:

```text
API Backend -> AI Orchestrator: bidirectional gRPC stream
AI Orchestrator -> Tool Runner: server streaming
```

However, browsers do not support native gRPC in the same straightforward way they support fetch, SSE, and WebSockets. There is gRPC-Web, but it adds constraints.

So in many systems you see:

```text
Browser <-> API edge: SSE or WebSocket
Internal services: gRPC streaming, message broker, or normal HTTP
```

That is perfectly reasonable.

The external protocol and internal protocol do not have to be the same.

## A Practical AI Streaming Architecture

If I were building a serious AI agent application, I would probably start with something like this:

```text
                           +----------------+
                           | Auth / Policy  |
                           +----------------+
                                   |
                                   v
+---------+   POST /runs     +-------------+      +-------------+
| Browser | ---------------> | API Backend | ---> | Run Store   |
+---------+                  +-------------+      +-------------+
      |                             |
      |                             v
      |                       +-------------+
      |                       | Queue       |
      |                       +-------------+
      |                             |
      |                             v
      |                       +-------------+
      |                       | AI Worker   |
      |                       +-------------+
      |                             |
      |       writes events         v
      |                       +-------------+
      |                       | Event Log   |
      |                       +-------------+
      |                             ^
      |                             |
      +--- GET /runs/{id}/events ---+
             SSE stream
```

The run store contains:

```text
run_id
user_id
tenant_id
status
created_at
started_at
completed_at
cancel_requested
model
route
cost estimate
error
```

The event log contains:

```text
run_id
sequence_number
event_type
payload
created_at
```

The queue contains work:

```text
run_id
task_type
attempt
```

The UI uses:

```text
POST /runs
GET /runs/{id}
GET /runs/{id}/events
POST /runs/{id}/cancel
```

This is boring in the best way.

It separates:

- starting work
- doing work
- observing work
- cancelling work
- storing work

That separation makes the system much easier to operate.

## Observability

Track each run from request to completion: queue time, worker and model latency, time to first token, total duration, disconnects, errors, and cost.

Time to first token is especially useful because it tells you whether the delay happened in the queue, model, proxy, or frontend. The backend can write a token immediately while the browser receives nothing for 20 seconds because a proxy buffered the response. Trace both sides.

## Security And Multi-Tenancy

Streaming endpoints are still API endpoints.

That means:

- authenticate them
- authorize the run
- verify tenant ownership
- avoid leaking event data across users
- do not expose internal tool logs blindly
- rate-limit connections
- handle token expiry

The authorization check for:

```text
GET /runs/123/events
```

is not optional.

The server must check:

```text
Can this user observe this run?
```

not:

```text
Does this run exist?
```

This matters a lot in multi-tenant SaaS.

Also be careful with debug events. Tool calls may contain sensitive data. Retrieval events may contain document snippets. Error events may contain stack traces. The stream is user-visible unless you explicitly separate internal and external events.

I would usually have two event categories:

```text
internal events:
  detailed tool logs, stack traces, routing decisions

external events:
  safe progress and user-visible content
```

Do not stream internal events to the browser just because it is convenient during development.

## Common Failure Modes

### 1. The Spinner Is Replaced With Fake Progress

Streaming should represent real progress.

If the UI says:

```text
Analyzing...
Thinking...
Almost there...
```

but the backend is not actually emitting meaningful state, users eventually notice.

Better:

```text
Searching documents
Reading 4 sources
Calling pricing tool
Drafting answer
```

### 2. The Stream Is Not Resumable

If a refresh loses the whole answer, the architecture is too fragile for long-running agents.

Use run IDs and event IDs.

### 3. The Worker Owns The User Connection

This couples execution and delivery too tightly. It may be fine for simple requests, but it becomes painful for agents.

Use workers for work and API pods for delivery.

### 4. Everything Is WebSocket Because It Sounds Real-Time

WebSockets are good. They are not automatically the right answer.

If the server is just sending tokens, SSE is simpler.

### 5. No Cancellation

This burns money and annoys users.

Cancellation should be part of the run model.

### 6. Proxy Buffering

This is the classic "works locally, not in production" streaming bug.

Test through the real gateway.

### 7. No Backpressure Or Limits

If users can start unlimited runs with unlimited event output, someone will eventually discover the expensive path.

Maybe accidentally.

## What I Would Choose

For a normal AI chat or agent UI, I would usually choose:

```text
External client streaming:
  SSE

Run execution:
  background worker

Coordination:
  queue

State:
  run store

Events:
  durable event log

Cancellation:
  explicit cancel endpoint

Scaling:
  stateless API pods + horizontally scaled workers
```

I would use WebSockets if the product really needs bidirectional interaction during the run.

I would use polling if the updates are infrequent or if I want a very simple first version.

I would avoid making sticky sessions a core requirement unless there is a very good reason.

This is the key architecture:

```text
Do not tie the AI work to the browser connection.
```

The browser connection is fragile. Users close tabs. Networks change. Mobile devices sleep. Proxies cut idle connections.

The run should be durable.

The stream is only one way to observe the run.

That mental model makes the whole design cleaner.

## Wrapping Up

Streaming in AI applications is not one thing.

At the protocol level, it may be:

- polling
- long polling
- SSE
- WebSockets
- gRPC streaming internally
- plain HTTP chunked responses

At the product level, it is:

- tokens
- progress
- sources
- tool status
- final answer

At the architecture level, it is:

- run state
- event logs
- queues
- workers
- reconnects
- cancellation
- scaling
- observability

So when someone says:

```text
We need streaming for the agent.
```

I would ask:

```text
Streaming what?
To whom?
Over which protocol?
Is the work durable?
Can the user reconnect?
Where are events stored?
Can any API pod serve the stream?
What happens when the worker crashes?
How do we cancel?
What does the load balancer do?
```

The protocol choice matters, but it is only one part.

For many modern AI applications, SSE plus a durable run/event architecture is the sweet spot. It is simple enough for browsers, observable enough for production, and flexible enough for long-running AI work.

WebSockets are excellent when the interaction is truly bidirectional.

Polling is fine when freshness requirements are low.

The wrong answer is not choosing the "uncool" protocol.

The wrong answer is pretending that streaming is just a UI detail.

It is not.

In agentic systems, streaming is part of the execution architecture. It is how the user observes a process that may involve models, tools, queues, workers, retries, and failures.

And as soon as you see it like that, the design becomes much clearer:

```text
The agent does durable work.
The stream reports what is happening.
The browser is allowed to disappear and come back.
```

That is the difference between a nice demo and a system you can actually operate.
