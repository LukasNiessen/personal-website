---
title: "System Design: Choosing the Right Dataflow"
summary: "Explaining and discussing REST, SOAP, GraphQL and messaging."
date: "Feb 1 2025"
draft: false
repoUrl: "https://github.com/LukasNiessen/dataflow-in-system-design"
xLink: "https://x.com/iamlukasniessen/status/1924545483034198526"
linkedInLink: "https://www.linkedin.com/pulse/system-design-choosing-right-dataflow-lukas-nie%25C3%259Fen-83sse/"
tags:
  - REST
  - GraphQL
  - SOAP
  - Messaging
---

# System Design: Choosing the Right Dataflow

When building a system, a very important decision is how data moves between components. I will walk through

- Database dataflow,
- Service calls (REST, SOAP, GraphQL, RPC),
- Messaging (message queues).

## Dataflow Through Databases

First off: The DB is almost always deployed separately, that is, a different machine or container. This has many reasons, including the following:

- **Scalability**: You can scale your app and database independently. For example, spin up more app servers without touching the DB.
- **Fault Tolerance**: You can restart your app without risking the DB, or upgrade the DB without downtime.
- **Security**: You can isolate the DB behind a firewall or private subnet for tighter access control.

(An exception to this is obviously SQLite or other embedded DBs.)

So we communicate with our DB **over the network**.

### Protocols

Which protocols are used? Databases don't use HTTP. They rely on custom binary protocols for performance. In the transport layer we use TCP due to its reliability.

### Other Considerations

When storing data in a database, it is encoded into a format suitable for the database (eg. UTF-8 for text in PostgreSQL, BSON for documents in MongoDB). When retrieved, the data is decoded for use by the application.

Something that makes databases unique is that they often store data for decades, such as user profiles or posts from 10 years ago. And they store it in the original encoding or schema. This means the data must remain accessible even as applications evolve and is often summarized as _data outlives code_. So we need to ensure backward compatibility (new code can read old data) and forward compatibility (old code can work with new data formats or schemas). This is achieved through strategies like:

## Dataflow Through Services

While there are many more, I will cover mainly REST vs SOAP vs RPC and I will mention GraphQL without going deep there. Let's first get the terms straight.

### Service

`Service = An API exposed by a server`

The most common type of communication is: clients and servers. The server exposes an API and the clients can use that API to make requests to server over the network.

### Web Service

`Web Service = Service that uses HTTP`

Although web services are not exlusively in _the web_ this is still the name they received. Reminder of how the web works: clients (web browsers) send requests to web servers. For example HTTP GET requests to download HTML, CSS, JavaScript, images or scripts, or HTTP POST requests to submit data, such as a registering form.

### REST (Representational State Transfer)

REST is **not** a protocol. It's merely a way to design your service-client or service-service communication. The core ideas are:

- Use simple data formats
- Use URLs to identify **resources**

  - So strictly speaking `/profiles/lukas` is cool, but `profiles/get-profile` is not that much. The latter is an action, not a resource.

- Use HTTP features, for example for cache control, authentication, or content type negotiation.

REST responses are typically in JSON. There is much more to REST and interpretations also moved pretty far from what it actually was meant to be, but that's all topic for a separate article.

REST has been gaining popularity compared to SOAP, especially for cross-organizational service integration. The main reason is its simplicity, support and interoperability.

### SOAP (Simple Object Access Protocol)

SOAP is an XML-based protocol for making network API requests. Although most commonly used over HTTP, it aims to be independent from HTTP and avoids using most HTTP features. Instead, it comes with a complex set of related standards (the WS-\* framework) that add various features.

The API of a SOAP web service is described using an XML-based language called the Web Services Description Language (WSDL). WSDL is not designed to be human-readable. Also SOAP messages are often too complex to construct manually. So develops rely heavily on tool support, code generation, and IDEs. And that's the biggest problem. For programming languages not supported by SOAP vendors, integration is difficult. Although SOAP is standardized, interoperability between different vendors' implementations often causes problems.

So in a nutshell, SOAP is much more complex and requires tools and the like. This often causes problems and is the main reason SOAP lost popularity (however, it's still used at many places).

### RPC (Remote Procedure Call)

Now some clients are not a browser or native app or the like. In fact, applications or services can be clients as well. For example, when your service makes a call to another service, your service is a client in the context of this call. So how do we approach such communication?

RPC is intended for such remote calls and the idea is to make them look like local function calls. However, it's important to clarify that this will never _really_ work for a multitude of reasons, here are some.

- **Predictability**: Local function calls are predictable, succeeding or failing based on controlled parameters. Network requests are unpredictable due to potential network issues, requiring retries.

- **Outcomes**: Local calls return a result or throw an exception. Network requests may timeout without a result, leaving uncertainty about request success.

- **Retries**: Retrying network requests risks multiple executions if responses are lost (there are workarounds).

- **Response times**: Local calls have consistent execution times. Network requests are slower with variable latency, ranging from milliseconds to seconds based on network conditions.

- **Parameter Passing**: Local calls efficiently pass object references. Network requests require encoding parameters into bytes, which is problematic for large objects.

- **Language differences**: RPC frameworks must translate datatypes across languages (eg. from Java to TypeScript), which can be complex.

The most common RPC framework is gRPC (by Google). It uses _Protocol Buffers_ for encoding the transmitted data.

The main use of RPC is for requests between services owned by the same organization, usually within the same datacenter. For example between micro services. When done right, eg. by using gRPC in the right way, the requests are very fast (way faster than using a RESTful API). More to this later.

### GraphQL

GraphQL is a query language for APIs and a runtime for executing those queries. Unlike REST, where each endpoint returns a fixed data structure, GraphQL lets clients specify exactly what data they need.

In simple terms, GraphQL works like this:

- The client sends a single query describing the data it needs
- The server returns exactly that data, nothing more, nothing less
- Everything happens over a single endpoint (typically `/graphql`)

GraphQL was developed by Facebook in 2012 and released as open source in 2015. It arose from the need to efficiently fetch data for mobile applications with varying requirements and limited bandwidth.

Key advantages of GraphQL include:

- **Precise data fetching**: Clients get exactly what they ask for, reducing over-fetching or under-fetching of data
- **Single request**: Clients can retrieve multiple resources in a single request
- **Strong typing**: The schema defines what queries are possible, enabling better tooling and validation
- **Versioning**: Fields can be deprecated without breaking existing queries

The main trade-offs include:

- More complex server implementation than simple REST
- Potential performance issues with deeply nested queries
- Caching is more challenging than with REST
- Learning curve for teams new to the technology

GraphQL is particularly well-suited for complex UIs with changing data requirements and diverse clients with different needs - like Facebook or Instagram for example

## Serialization and De-serialization

> Serialization = converting data structures into a transmittable format`

> De-serialization = reconstructing data structures from the received format`

We clearly need serialization/de-serialization when communicating over the network. So it's important to get it right. There are studies, for example [this one](https://arxiv.org/abs/2204.03032), which show that often serialization/de-serialization accounts for 80% or more of the communication time in microservice architectures.

This shows the importance of using gRPC (or other frameworks). There we still have serialization/de-serialization but it's very efficient - much faster than typical JSON serialization/de-serialization with RESTful APIs for example.

## Dataflow Through Messaging

At its simplest, messaging is like leaving a note for someone when they're not immediately available. Rather than connecting directly, you drop a message in a queue and trust it will be delivered.

### Super Brief Explanation

Messaging systems operate with a few key components:

- **Producers**: Systems that generate messages
- **Consumers**: Systems that process messages
- **Brokers**: The middleware that stores and routes messages
- **Queues/Topics**: Named destinations for messages
- **Queues**: Where each message is consumed by a single recipient (point-to-point)
- **Topics/Exchanges**: Where messages can be broadcast to multiple subscribers (publish-subscribe)

When using a messaging system, the sender doesn't need to know about the recipient - it simply publishes a message and moves on. Also called _fire-and-forget_.

### Strengths and Trade-offs

**Strengths:**

- **Decoupling**: Services don't need to know about each other's location or implementation
- **Resilience**: System can continue functioning even if some components are down
- **Buffering**: Great for elasticity, we can handle traffic spikes by queuing messages before consuming them

**Trade-offs:**

- **Increased complexity**: Additional infrastructure to maintain and monitor
- **Eventual consistency**: Messages are processed asynchronously, so data may be temporarily inconsistent, however, there are workarounds
- **Debugging challenges**: Message flow can be harder to trace than direct calls, testing is difficult too
- **Ordering guarantees**: Most systems provide only limited message ordering guarantees

Some common messaging systems are RabbitMQ, Apache Kafka, ActiveMQ, and cloud offerings like AWS SQS/SNS, Google Pub/Sub, and Azure Service Bus.
