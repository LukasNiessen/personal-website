---
title: "Event Sourcing, CQRS and Micro Services: Real FinTech Example from my Consulting Career"
summary: "This is a detailed breakdown of a FinTech project from my consulting career"
date: "Jul 1 2025"
draft: false
tags:
  - Consulting
  - FinTech
  - Microservices
  - Event Sourcing
  - CQRS
---

# Event Sourcing, CQRS and Micro Services: Real FinTech Example from my Consulting Career

This is a detailed breakdown of a FinTech project from my consulting career. I'm writing this because I'm convinced that this was a great architecture choice and there aren't many examples of event sourcing and CQRS in the internet where it actually makes sense. You are very welcome to share your thoughts and whether you agree about this design choice or not :)

## Project Description

The client was a medium sized fintech company that has in-house developed a real time trading platform that was launched as a beta test version. The functionality included:

- Real time stock info
- Portfolio management
- Real time transaction tracking
- Report generation
- Account with a little social media functionality (making posts, liking and commenting)
- Mobile device notifications
- and more

Their app was an MVP. It had a monolithic Spring boot backend and a simple React based web UI, everything hosted on Azure.

They hired us because of two main reasons: their MVP was not auditable and thus not compliant with financial regulations and also not scalable (high usage and fault tolerance).

## Our Team

We worked with the customer, not alone. Our team were about 10 people, experienced back end or full stack developers and me as a software architect. The client had about 20 developers, ranging from front end, back end to database experts and more. My role was to lead the architecture.

## Our Design Decision

As said, the main issues to solve were auditability (compliance) and scalability (including performance and fault tolerance). I will start with an overview of the design including a super short repetition of what each technology is and later dive into detail in the next session, including discussing the trade offs and alternative solutions.

### Auditability

Our customer must by law always know past states. For example, customer A had exactly $901 on their account 2 months ago at 1:30 pm. This was not possible with the existing system so we needed to tackle it. I proposed to use event sourcing. Here is a very brief explanation of event sourcing.

> Event sourcing = Save events, not state

So instead of having a state we update, we save events. We use these events to create the state when we need it. Consider this simple example:

---

**Old Approach**

```
+--------------------------------------+
| Table: Account_Balance               |
+--------------------------------------+
| Account_ID | Balance | Last_Updated  |
+--------------------------------------+
| Customer_A | $0      | 2025-04-29    | <- Initial state
+--------------------------------------+
| Customer_A | $5      | 2025-04-29    | <- After receiving $5 (overwrites $0)
+--------------------------------------+
| Customer_A | $12     | 2025-04-29    | <- After receiving $7 (overwrites $5)
+--------------------------------------+
```

Problem: Past states (e.g., $5 at 1:30 PM) are lost unless separately logged.

---

**Event Sourcing**

```
+-------------------------------------------------------------------+
| Table: Account_Events                                             |
+-------------------------------------------------------------------+
| Event_ID | Account_ID | Event_Type | Amount | Timestamp           |
+-------------------------------------------------------------------+
| 1        | Customer_A | Deposit    | $5     | 2025-04-29 13:30:00 | <- Event: Received $5
+-------------------------------------------------------------------+
| 2        | Customer_A | Deposit    | $7     | 2025-04-29 13:31:00 | <- Event: Received $7
+-------------------------------------------------------------------+
```

Reconstructing Balance at 2025-04-29 13:30:00:

- Sum events up to timestamp: $5 = $5

Reconstructing Balance at 2025-04-29 13:31:00:

- Sum events up to timestamp: $5 + $7 = $12

Reconstructing Balance 2 months ago:

- Sum all relevant events <= timestamp

---

This is event sourcing in a nutshell. For a more comprehensive explanation, please have a look [here](https://martinfowler.com/eaaDev/EventSourcing.html) for example.

This is the right choice here because this gives us total control and transparency. When we want to know how much money a particular user had 2 months ago at 1:42 pm, we can just query the needed transactions and sum them up. We know everything with this approach. And this is required to be compliant. As a side note, accounting does the same thing but, of course, they don't call it event sourcing :)

But event sourcing comes with more advantages, including:

- Rebuild state: you can always just discard the app state completely and rebuild it. You have all info you need, all events that ever took place.
- Event replay: if we want to adjust a past event, for example because it was incorrect, we can just do that and rebuild the app state.
- Event replay again: if we have received events in the wrong sequence, which is a common problem with systems that communicate with asynchronous messaging, we can just replay them and get the correct state.

#### Alternatives to Event Sourcing

Event sourcing definitely solves the auditability/compliance problem. But there are alternatives:

**1. Audit Log Pattern**: Keep the current state tables but add comprehensive audit logs that track all changes. This is simpler to implement but doesn't provide the same level of detail as event sourcing. You track what changed, but not necessarily the business intent behind the change.

**2. Change Data Capture (CDC)**: Use database-level tools to capture all changes automatically. Tools like Debezium can stream database changes, but this is more technical and less business-focused than event sourcing.

**3. Temporal Tables**: Use database features (like SQL Server's temporal tables) to automatically version data. This provides history but lacks the rich business context that events provide.

**4. Transaction Log Mining**: Extract historical data from database transaction logs. This is complex and database-specific, making it harder to maintain.

### CQRS (Command Query Responsibility Segregation)

The second major architectural decision was implementing CQRS, though we didn't start with it immediately due to complexity. We kept it in mind during the initial design and tested it later through a proof of concept, then implemented it in production.

Here's what CQRS means:

> CQRS = Separate your reads from your writes

This is all. Often CQRS is presented as (among other things) having two separate DBs, one for writing and one for reading. But this is not true, you are doing CQRS already when you just separate read and write code, for example by putting them into separate classes.

However, the benefits we needed do indeed require separate DBs.

```
Traditional Approach:
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│   Client    │────│   Service    │────│   Database   │
│             │    │              │    │              │
│ Read/Write  │    │ Read/Write   │    │ Read/Write   │
└─────────────┘    └──────────────┘    └──────────────┘

CQRS Approach:
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│   Client    │────│ Command Side │────│ Write Store  │
│             │    │   (Writes)   │    │ (Event Store)│
│             │    └──────────────┘    └──────────────┘
│             │           │                    │
│             │           │ Events             │ Events
│             │           ▼                    ▼
│             │    ┌──────────────┐    ┌──────────────┐
│             │────│  Query Side  │────│  Read Store  │
│             │    │   (Reads)    │    │ (Projections)│
└─────────────┘    └──────────────┘    └──────────────┘
```

More about CQRS [here](https://martinfowler.com/bliki/CQRS.html).

The benefits of doing this are the following:

- Scale read and write resources differently
  - By having two separate DBs, you can choose different technologies and scale them independently
  - If performance is critical in your app, this can definitely help, especially when reads and writes are not of a similar amount
    - In our case, we have a read heavy app
- You can have different models for reading and writing

As hinted already, this was crucial for our trading platform because:

- Complex reports and dashboards need denormalized, optimized read models,
- Read and write loads are completely different in trading systems, so we need independent scalability,
- We can use different databases optimized for each purpose.

However, CQRS with separate DBs comes at great cost again, for example, you need to deal with eventual consistency.

**Important note**: We do NOT use CQRS on every service but only where it justifies the complexity.

#### Alternatives to CQRS

You can try to get the benefits of CQRS in other ways, for example by using caching strategies and read replicas. I'll dive into the tradeoffs of these approaches in the detailed discussion section.

### Microservices

We also decided to break the monolith into microservices. The main reason for this decision was again independent scalability and higher fault tolerance. The existing monolith was often running on very high CPU usage due to report generation and real-time market data processing consuming most resources.

By separating these concerns into different services, even if our report generation service crashes due to heavy usage, other critical services like transaction processing are not impacted at all. This improves our overall system availability (MTBF - Mean Time Between Failures) and reduces recovery time (MTTR - Mean Time To Recovery).

An interesting part here was the migration from monolith to microservices using the strangler fig pattern, gradually replacing parts of the monolith.

### Asynchronous Messaging

Another decision was to use asynchronous messaging for inter-service communication instead of request-response communication.

```
Synchronous (Traditional):
Service A ──HTTP Request──► Service B
          ◄──Response─────
```

```
Asynchronous (Our Approach):
Service A ──Event──► Message Queue ──Event──► Service B
```

This event-driven approach has many benefits such as high decoupling. However, we were primarily interested in better fault tolerance:

Suppose Service A informs Service B to save data to its DB. If we use a traditional HTTP request and Service B is down, then the request is lost. Of course there are ways to combat this but if we use asynchronous messaging instead, then Service A just pushed that event to the message queue and if Service B is down, nothing happens. The event just stays on the queue. And as soon as Service B is up again, the event gets processed.

So using this approach gives us better fault tolerance in the case of network partitions.

Now asynchronous messaging has clear downsides too, mainly complexity, particularly when it comes to debugging, testing and things of that kind.

## Detailed Discussion: Tradeoffs and Alternatives

### Microservices Deep Dive

We identified services based on business capabilities as follows:

```
Transaction-Portfolio Service:
├── Owns: Account balances, transaction history, stock holdings
├── Responsibilities: Money transfers, buy/sell orders, balance queries
└── Database: PostgreSQL (ACID compliance critical)

Notification Service:
├── Owns: User preferences, notification history
├── Responsibilities: Email, SMS, push notifications
└── Database: MongoDB (flexible schema for different notification types)
└── Event Sourcing: NOT used (simple CRUD operations)

Social Service:
├── Owns: Posts, likes, comments
├── Responsibilities: Social feed, user interactions
└── Database: MongoDB
└── Event Sourcing: NOT used (not critical for compliance)

Report Service:
├── Owns: Aggregated data, report templates
├── Responsibilities: Generate complex reports
└── Database: ClickHouse (optimized for analytics)
└── CQRS: Read-only projections from other services

User Service:
├── Owns: User profiles, authentication
├── Responsibilities: Registration, login, profile management
└── Database: PostgreSQL
└── Event Sourcing: NOT used (user profiles change infrequently)
```

**Service Boundary Evolution**: Initially, we considered separating Transaction Service and Portfolio Service. However, we discovered early in the design phase that this would be wrong. Due to very frequent boundary crossings and the need for distributed transactions when a trade affects both account balance and portfolio holdings, we decided to keep these as a single service. This eliminated the complexity of distributed transactions while maintaining other benefits.

In my opinion, the need of distributed transactions or sagas is always an indicator to check if your service boundaries are the right choice. Maybe you want to merge services instead. To quote Sam Newman in _Building Microservices (2nd edition)_:

> Distributed Transactions: Just Say No. For all the reasons outlined so far, I strongly suggest you avoid the use of distributed transactions like the two-phase commit to coordinate changes in state across your microservices. So what else can you do? Well, the first option could be to just not split the data apart in the first place. If you have pieces of state that you want to manage in a truly atomic and consistent way, and you cannot work out how to sensibly get these characteristics without an ACID-style transaction, then leave that state in a single database, and leave the functionality that manages that state in a single service (or in your monolith). If you're in the process of working out where to split your monolith and what decompositions might be easy (or hard), then you could well decide that splitting apart data that is currently managed in a transaction is just too difficult to handle right now. Work on some other area of the system, and come back to this later. But what happens if you really do need to break this data apart, but you don't want all the pain of managing distributed transactions? In cases like this, you may consider an alternative approach: sagas.

So he also recommends to either merge the services or, if really needed, to use sagas. In our case we decided that this service boundary would be wrong since the scalibility needs to the transaction service and the portfolio service are not that different actually.

#### Where We Use Event Sourcing

We used event sourcing only in the Transaction-Portfolio Service due to the strict compliance requirements for financial data. The other services used traditional CRUD patterns since they didn't require the same level of auditability.

### Event Sourcing Deep Dive

#### Benefits of Event Sourcing

Event sourcing has better performance when it comes to writing. Consider this example:

Traditional Update Pattern:

```sql
1. SELECT current_balance FROM accounts WHERE id = 123
2. UPDATE accounts SET balance = balance + 100 WHERE id = 123
   (Requires row locking, potential contention)
```

Event Sourcing Pattern:

```sql
INSERT INTO events (account_id, type, amount, timestamp)
   VALUES (123, 'deposit', 100, NOW())
```

And it has even more advantages on the writing part:

- **Write Performance**: Append-only writes are much faster than updates
- **No Lock Contention**: Multiple transactions can write simultaneously
- **Better Concurrency**: No need to lock rows for balance updates
- **Optimized for SSD**: Sequential writes perform excellently on modern storage

Although we talked about this already, here is a sample of how you could implement _summing an event replay_:

```sql
-- Regulatory Question: "What was Account X's balance on Date Y at Time Z?"
-- Event Sourcing Answer:
SELECT SUM(amount) FROM events
WHERE account_id = X AND timestamp <= 'Y Z'
GROUP BY account_id
```

#### Challenges and Solutions

**Performance Issue - Event Replay**

The main challenge we faced was performance degradation when reconstructing current state from thousands of events. For active trading accounts, we had up to 50,000 events per day.

Our solution was a hybrid approach:

- **Event-Based Snapshots**: Create snapshots after every 1,000 events per account
- **Delta Replay**: Only replay events since the last snapshot

This approach ensures that we never need to replay more than 1,000 events for any account, keeping reconstruction time predictable and fast.

```sql
-- Sample code
SELECT snapshot.balance + COALESCE(SUM(events.amount), 0) as current_balance
FROM account_snapshots snapshot
LEFT JOIN events ON events.account_id = snapshot.account_id
    AND events.sequence_number > snapshot.last_event_sequence
WHERE snapshot.account_id = 123
    AND snapshot.last_event_sequence = (
        SELECT MAX(last_event_sequence) FROM account_snapshots
        WHERE account_id = 123
    )
```

This reduced our balance calculation time from 2-5 seconds to 50-200ms for active accounts.

**Storage Growth**

Events accumulate rapidly. We implemented a tiered storage strategy:

- **Hot storage** (Azure Premium SSD): Last 3 months ~ 2TB
- **Warm storage** (Azure Standard SSD): 3-12 months ~ 5TB
- **Cold storage** (Azure Archive): 1+ years ~ 50TB

Total storage costs: $800/month vs $15,000/month if everything was on premium storage.

#### Tradeoffs

Event sourcing adds significant complexity. A part of the team needed training.

**Query Complexity:**
Getting current state requires aggregation:

```sql
-- Current Balance Query:
SELECT account_id, SUM(amount) as current_balance
FROM events
WHERE account_id = 123
GROUP BY account_id

-- vs Traditional:
SELECT balance FROM accounts WHERE id = 123
```

**Storage Growth:**
Events accumulate over time and require storage management strategies.

#### Why We Rejected Alternatives

Yes, we have decided to use event sourcing even though it comes with read performance issues - and performance was a main concern of our customer.

The reason is that event sourcing is simply much superior when it comes to audits. This was much more important to the customer than performance. Plus we managed to solve the performance issue.

### CQRS Deep Dive

**Very important note**: CQRS in the sense of having multiple DBs adds complexity and eventual consistency. This is why we decided **against** using it immediately but just kept it in mind. We later created a proof of concept to compare the performance benefits we would get in the Portfolio Service.

Our POC results showed for a test user account:

- **Report generation time**: 30 seconds → 10 seconds
- **Dashboard load time**: 1 second → 400ms
- **Complex query performance**: about 2x improvement

The result convinced us to implement it. We later added it to the Transaction Service for high-volume trading operations, but **not to all services**. Adding CQRS to all our services would have little benefits (we don't need the performance benefits or different read/write models at most services) but much complexity.

#### Implementation Details

We implemented CQRS for the Transaction-Portfolio Service as follows. We had a Postgres DB for the write side (command side) and a MongoDB for the read side (query side). We chose a document store because we did not want a fixed schema plus we wanted very high read throughput.

So the service received a request and decided to write, it wrote to the Postgres DB and also emitted an event to our message broker (Azure Service Bus). This event was then processed by a different instance of the Transaction-Portfolio Service and we write to the MongoDB. Here we don't write the same data but a denormalized form, so that querying the data we need is faster.

Note we sacrifice ACID by doing this. This gave us eventual consistency between read and write sides, typically within 100-500ms.

**Why This Was Faster**

The performance improvements came from:

1. **Denormalized Read Models**: Instead of complex JOINs across normalized tables, we had pre-computed aggregations
2. **Optimized Indexes**: Each MongoDB collection had indexes tailored for specific query patterns
3. **Separate Scaling**: We could scale read replicas independently of the write database

Consider this example of generating a user's portfolio performance report:

Traditional approach:

```sql
-- Complex query with multiple JOINs and aggregations
SELECT u.name, p.symbol,
       SUM(t.quantity) as total_shares,
       AVG(t.price) as avg_price,
       -- ... more complex calculations
FROM users u
JOIN portfolios p ON u.id = p.user_id
JOIN transactions t ON p.id = t.portfolio_id
WHERE u.id = 123
GROUP BY u.name, p.symbol
-- This took up to 30 seconds for active users
```

CQRS approach:

```javascript
// Simple document lookup from pre-computed projection
db.portfolio_summaries.findOne({ user_id: 123 });
// fast
```

### Major Challenges and How We Solved Them

**1. Debugging Distributed Systems**

This was our biggest pain point initially. When a transaction failed, tracing the issue across multiple services and async message queues was a nightmare.

We solved this by implementing distributed tracing with correlation IDs that flow through every service call and message. Every log entry includes the correlation ID, making it possible to reconstruct the entire flow. We used Jaeger for distributed tracing and structured logging with consistent fields across all services.

**2. Testing Complexity**

Testing event sourcing and CQRS systems is fundamentally different. You can't just mock database calls - you need to verify that events are produced correctly and that projections are updated properly.

We created integration test environments that could replay production events against test instances. This allowed us to validate that code changes wouldn't break existing event processing. We also invested heavily in property-based testing to verify that event sequences always produce valid states.

### What Would I Change?

I'm convinced this was the right architecture for our specific requirements. However, there are definitely things I would approach differently:

- We didn't have a clear strategy for evolving event schemas initially. When we needed to add fields to events or change event structure, it created compatibility issues with existing events.

- Also our monitoring and logging was weak in the beginning and made everything even more complex to start.

- I would consider using EventStore instead of Postgres for the Transaction-Portfolio Service. EventStore is purpose-built for event sourcing and provides features like built-in projections, event versioning, and optimized append-only storage. This would eliminate much of the custom event sourcing infrastructure we had to build on top of Postgres.
