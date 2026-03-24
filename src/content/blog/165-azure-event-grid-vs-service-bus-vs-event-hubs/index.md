---
title: "Azure Event Grid vs Service Bus vs Event Hubs: Picking the Right One"
summary: "Azure has three messaging services that confuse almost everyone. Here is what each one does, how they differ, and how to pick the right one for your system."
date: "Mar 23 2026"
tags:
  - Azure
  - Messaging
  - Distributed Systems
  - Architecture
  - Cloud
---

# Azure Event Grid vs Service Bus vs Event Hubs: Picking the Right One

Azure has three messaging services and they can easily be confusing. Event Grid, Event Hubs, Service Bus - what's the difference? When do you use which one? Can you combine them?

I'll go through each one, explain what it does, compare them, and then give you a concrete way to decide. I'll also touch on some things that are often overlooked, like the "at least once delivery" pattern that all three share and what that means for your system design.

## First: Events vs Messages

Before we look at the services, there's an important distinction. Events and messages are not the same thing.

An **event** is a notification that something happened. "A file was uploaded." "A user signed up." The publisher doesn't care who receives it or what they do with it. It's fire-and-forget.

A **message** is a command or a piece of data that needs to be processed. "Process this order." "Send this email." The sender expects a specific consumer to handle it, and it matters that it gets handled correctly.

This distinction is key because Event Grid is built for events, Service Bus is built for messages, and Event Hubs is built for streams of events at massive scale. If you understand this, you already understand 80% of when to use which.

## Event Grid

Event Grid is a pub-sub service. Publishers emit events, subscribers react to them. The publisher has no idea who the subscribers are and doesn't care. Subscribers decide which events they care about and what to do with them.

Think about it like this: a blob gets uploaded to Azure Storage. That's an event. Maybe an Azure Function processes the image. Maybe another service logs it. Maybe nothing happens at all. The storage account doesn't know and doesn't need to.

It's serverless, scales automatically, and since it uses a push model (no polling), it's cheap. Microsoft charges per operation, and for many workloads the cost is almost negligible.

The closest equivalents on other clouds: **AWS EventBridge** and **GCP Eventarc**. On GCP, **Pub/Sub** can also fill this role - GCP chose to have one unified messaging service rather than splitting it into three like Azure does.

### What Happens to Events?

Event Grid doesn't store events. It **pushes** them to subscribers, and if delivery fails, it retries with a configurable retry policy and expiration time. But if there's no subscriber, the event is gone. With the newer namespace topics and pull delivery there is some short-term retention, but Event Grid is fundamentally not designed as durable storage.

### Deployment Options

Event Grid exists in two forms. The standard **PaaS on Azure**, and a version that runs on **Kubernetes with Azure Arc**. The Kubernetes version is interesting for hybrid scenarios - you get Event Grid on your own cluster, on-prem or wherever. This is relatively newer and worth knowing about if you deal with data residency constraints.

### MQTT and HTTP

Event Grid supports both MQTT (Message Queuing Telemetry Transport) and HTTP. Why?

**MQTT** is designed for constrained environments. IoT devices, sensors, embedded systems. A thermostat sending temperature readings doesn't need the overhead of HTTP. MQTT is lightweight and efficient for that.

**HTTP** is for everything else. Webhooks, cloud-native integrations, reacting to Azure resource changes. When a new blob lands in storage or a resource gets created in a resource group, Event Grid pushes an HTTP event to your subscriber.

### Namespace Topics (2026)

A relatively recent addition to Event Grid are **namespace topics** with **pull delivery**. Traditionally, Event Grid pushes events to your endpoint. With namespace topics, consumers can pull events at their own pace instead. This gives you more control in scenarios where your consumer might be slow or bursty and you don't want to deal with the backpressure problem of push delivery.

Event Grid also now supports the **CloudEvents** specification (CNCF standard) as a first-class citizen, which is useful if you're building systems that need to work across cloud providers.

## Event Hubs

Event Hubs is a data streaming platform. It's designed for massive throughput - we're talking millions of events per second. The typical use cases are telemetry ingestion, log aggregation, and real-time analytics.

The mental model is different from Event Grid. With Event Grid, you react to individual events. With Event Hubs, you're dealing with a continuous **stream** of data. Think about IoT sensor data, application metrics, clickstream analytics, or security logs from thousands of servers.

The closest equivalent on AWS is **Kinesis**. On GCP, **Pub/Sub** covers this too (remember, GCP uses one service for what Azure splits into three).

### How It Works

Event Hubs uses a **partitioned consumer model**. Events go into partitions, and consumers read from those partitions. You get ordering within a partition but not across partitions. Multiple consumer groups can read the same stream independently, each at their own pace.

```
Producers ──► ┌───────────┐
              │ Partition 0│──► Consumer Group A
              │ Partition 1│──► Consumer Group A
              │ Partition 2│──► Consumer Group A
              └───────────┘
                    │
                    └──────────► Consumer Group B (independent)
```

This is powerful. Your real-time dashboard can read the same stream as your batch analytics pipeline, independently, without affecting each other.

### Capture

One feature that's genuinely useful: **Event Hubs Capture**. It automatically dumps your streaming data into Azure Blob Storage or Data Lake in Avro format. Your data team can run analytics on it later without touching the live stream. No code needed, just enable it.

### Kafka Compatibility

Event Hubs has a **Kafka-compatible endpoint**. If your team knows Kafka or you have existing Kafka producers and consumers, you can point them at Event Hubs without code changes. You get a managed service without running Kafka clusters yourself. By 2026 this has become quite mature and is a genuine migration path from self-managed Kafka. In fact, Event Hubs *is* Azure's managed Kafka offering - there's no separate service for it. So if someone asks "what's Azure's equivalent of AWS MSK?", the answer is Event Hubs.

### What Happens to Events?

Event Hubs uses a **retention window** - default 1 to 7 days, up to 90 days on Premium. Events sit in the partitioned log for that duration regardless of whether anyone consumed them. Consumers track their own position (offset) in the stream. After the retention period expires, events get deleted automatically. Consumption doesn't delete anything - it's purely time-based.

## Service Bus

Service Bus is a **message broker**. If Event Grid is "something happened, react if you want" and Event Hubs is "here's a firehose of data," then Service Bus is "here is a task, please handle it reliably."

Quick terminology note: a **queue** is a data structure - first in, first out, messages wait in line. A **broker** is bigger than that. A broker is a service that manages queues (and topics), handles routing, filtering, dead-lettering, transactions, and more. Service Bus is a broker that *has* queues inside it. AWS SQS is just a queue. That's why Service Bus has a much longer feature list - it's a different category.

The broker stores messages until the consumer is ready to process them. If the consumer is down, the messages wait. When it comes back up, it picks up where it left off. Messages only disappear when a consumer explicitly **acknowledges** them, or when their time-to-live expires. Unprocessable messages go to a dead-letter queue instead of being lost. This is fundamentally different from Event Grid (push and forget) and Event Hubs (time-based retention).

The closest equivalents: **AWS SQS/SNS** (though SQS is just a queue, not a full broker) and again **GCP Pub/Sub**.

### The Feature List

Service Bus has the longest feature list of the three:

- **FIFO ordering** (via sessions)
- **Transactions** - process multiple messages atomically
- **Duplicate detection** - built-in deduplication window
- **Dead-letter queues** - messages that can't be processed go here instead of being lost
- **Scheduled delivery** - send a message now, deliver it later
- **Message deferral** - receive a message but process it later
- **Batching and sessions** - group related messages together
- **Routing and filtering** - subscribers get only the messages they care about

Whether you need all of these is a different question. But when you do need transactions or strict ordering, Event Grid and Event Hubs simply don't offer them.

### Queues vs Topics

Service Bus has two patterns:

**Queues** - point to point. One sender, one receiver. Each message is processed by exactly one consumer.

```
Sender ──► Queue ──► Receiver
```

**Topics** - pub-sub. One sender, multiple subscribers. Each subscriber gets its own copy. Subscribers can filter which messages they receive.

```
Sender ──► Topic ──► Subscription A (filter: priority = high) ──► Receiver A
                 └──► Subscription B (filter: region = EU)    ──► Receiver B
```

### Premium Tier

For production workloads, the **Premium tier** gives you dedicated resources (no noisy neighbor issues), messages up to 100 MB, and geo-disaster recovery. The Standard tier shares resources with other tenants and limits messages to 256 KB. For enterprise applications where reliability matters, Premium is usually worth it.

## Side by Side

| | Event Grid | Event Hubs | Service Bus |
|---|---|---|---|
| **Model** | Pub-sub (events) | Streaming (partitioned log) | Message broker (queues/topics) |
| **Ordering** | No guarantee | Per partition | FIFO (with sessions) |
| **Throughput** | High | Millions/sec | High |
| **Replay** | No | Yes (retention window) | No (but dead-letter, deferral) |
| **Transactions** | No | No | Yes |
| **Dead-lettering** | No | No | Yes |
| **Duplicate detection** | No | No | Yes |
| **When deleted** | After push + retry expiry | After retention window (time) | After consumer acknowledgment |
| **Typical latency** | Sub-second | Low (ms) | Low (ms) |
| **Cost model** | Per operation | Throughput units | Per operation + tier |

## "At Least Once" Delivery

All three services guarantee **at least once delivery**. This is not a coincidence. It's the pattern Microsoft uses across their entire distributed systems stack. Azure Function activity executions? At least once. Service Bus messages? At least once. Event Hubs? Same.

Why? Because in distributed systems, you have to choose between potentially losing messages or potentially delivering them more than once. Microsoft chose the latter for all three. And that's the right call for most scenarios.

But this has an important consequence for your design: **usually your consumers must be idempotent**. If a message arrives twice, processing it twice should produce the same outcome. This is a fundamental pattern in distributed systems. At-least-once delivery + idempotent consumers = effectively exactly-once processing. For more on this, I wrote about [idempotency in system design](/blog/112-idempotence-in-system-design/).

## Combining Services

You don't have to pick just one. For larger systems, combinations are common and often the right choice.

**Example 1: IoT pipeline**

```
IoT sensors ──► Event Hubs (ingest millions of readings)
                    │
                    ├──► Stream Analytics (real-time anomaly detection)
                    │         │
                    │         └──► Service Bus (alert: "motor overheating, create work order")
                    │
                    └──► Capture ──► Data Lake (batch analytics)
```

Event Hubs handles the firehose. Service Bus handles the critical business messages that come out of it.

**Example 2: Azure resource automation**

```
Blob uploaded ──► Event Grid (lightweight notification)
                      │
                      └──► Azure Function (validate + transform)
                                │
                                └──► Service Bus (queue processing job with retry guarantees)
```

Event Grid reacts to the change. Service Bus ensures the downstream work gets done reliably.

**Example 3: E-commerce**

```
User clicks ──► Event Grid (notify: inventory changed, analytics event)
                    │
Order placed ──► Service Bus (process order, payment, shipping - needs transactions)
                    │
All activity ──► Event Hubs (clickstream, telemetry, monitoring)
```

Each service does what it's best at.

## How to Decide

Just a few useful questions to ask in case you're uncertain:

**Ask yourself: what are you actually doing?**

- **Reacting to something that happened?** → Event Grid. A resource changed, a file was uploaded, a deployment completed. Lightweight, cheap, push-based.

- **Ingesting a continuous stream of data?** → Event Hubs. Telemetry, logs, sensor data, clickstreams. High throughput, replay capability, partition-based ordering.

- **Sending work that must be processed reliably?** → Service Bus. Orders, payments, anything where you need transactions, strict ordering, dead-lettering, or duplicate detection.

Think about what would happen if a message was lost or delivered out of order:

- Nobody would notice → **Event Grid**
- You'd lose analytics data but not break anything → **Event Hubs**
- A customer gets charged twice or an order is lost → **Service Bus**

## Common Mistakes

A few things I want to flag because I see them repeatedly.

**Using Service Bus for everything.** Service Bus is flexible enough that you *can* use it for almost anything. But that doesn't mean you should. If you just need to react to Azure resource changes, Event Grid does it with zero infrastructure thinking and at a fraction of the cost. Using Service Bus for that is like using a truck to deliver a letter.

**Picking Event Hubs "for the future."** Event Hubs is priced by throughput units. If your volume is a few hundred events per hour, you're paying for capacity you don't need. Start with Event Grid or Service Bus and move to Event Hubs when your data actually demands it.

**Ignoring idempotency.** All three services deliver at least once. If your consumer isn't idempotent, you will eventually process the same event twice. This isn't a theoretical concern, it happens in production.

**Not considering the dead-letter question.** What happens when a message can't be processed? With Service Bus, it goes to a dead-letter queue where you can inspect it later. With Event Grid and Event Hubs, you need to build that mechanism yourself if you need it.

## Wrapping Up

The three services cover three different problems:

- **Event Grid**: lightweight event distribution
- **Event Hubs**: high-volume data streaming
- **Service Bus**: reliable business messaging

They share the same delivery guarantee (at least once), but differ in everything else. Understanding the difference between an event ("something happened") and a message ("please handle this") gets you most of the way to the right choice. For the rest, look at your throughput requirements, ordering needs, and how critical each piece of data is.

And when in doubt, start simple. You can always add complexity later. Removing it is much harder.
