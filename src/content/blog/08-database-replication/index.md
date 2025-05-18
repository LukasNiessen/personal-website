---
title: "ELI5: Database Replication"
summary: "Database Replication in ELI5. Not only though, I also cover each topic with a more thorugh summary."
date: "May 18 2025"
draft: false
repoUrl: "https://github.com/LukasNiessen/database-replication"
xLink: "https://x.com/iamlukasniessen/status/1924098784809648615"
linkedInLink: "https://www.linkedin.com/pulse/eli5-database-replication-lukas-nie%25C3%259Fen-tbeae/"
tags:
  - Replication
  - Master-Slave
  - Leaderless
  - Leader-based
  - ELI5
---

# ELI5: Database Replication

This article is Database Replication in ELI5. Not only though, I also cover each topic with a more thorugh summary. I will cover:

- What is replication?
- Why replication?
- Leader-based, multi-leader, and leaderless
- Synchronous vs. asynchronous replication
- How to handle node failures
- Problems with replication lag
- Setting up new replicas

## What is Replication? ELI5

> Replication = Keeping copies of the same data on multiple machines

## Why Replication? ELI5

Three key reasons:

- **Latency**: Keep data geographically close to users
  - Let's say you're in China. Your app will use a nearby database server, ideally also in China. This is much faster than using one in the US for example.
- **Availability**: Keep the system running even when some parts fail
  - What if a DB server goes down? We will just connect to other, more to this later.
- **Read throughput**: Scale out machines serving read queries
  - If you have many users, it's better to have more than one server. Imagine YouTube serving all content from a single computer - not possible. So they put the content on multiple machines and distribute serving content among them.

## Where's the Challenge?

So this was super easy, but of course real life is not that easy. There are many difficulties in replicating your data. Too many to cover in this article so I will just cover the most important ones, the ones you should know about.

First off, if you have 5,000 Terrabytes of data, replicating all that data is probably too much. So you would also want to split the data between DBs. This is called _partitioning_ and is on purpose _ignored_ here. See my other article for that.

So, the main challenge with replication is handling changes. It's easy to once copy data to 10 different computers. But what do we do when we get new changes? There are 3 main approaches.

## Leader-Based Replication

The most common approach is the _leader-based model_ (also called _master-slave_). Here's how it works:

1. One _node_ (computer with DB) is the _leader_ (or _master_)
1. The other nodes are called _followers_ (or _slaves_)
1. Clients send write requests only to the leader
   - Followers are read only!
1. The leader writes to its local storage and sends changes to the followers
1. Followers apply these changes.

This is a high level overview skipping over details. There are still some key questions left, even on this high level.

### Synchronous vs. Asynchronous Replication

A critical decision in replication design is: should changes be applied synchronously or asynchronously?

With **synchronous replication**, the leader waits for the follower to confirm it received the write before confirming success to the client. This guarantees the follower's data is up-to-date with the leader.

With **asynchronous replication**, the leader doesn't wait for acknowledgment from followers. It processes the write locally and moves on, followers catch up when they can.

#### The Trade-offs:

- **Synchronous**:
  - Guarantees up-to-date copies
  - Guarantees durability (that is, we know writes are acutally _'successful'_, that is persisted)
  - But it also means we are slower
    - For example, just one slow follower means the whole system needs to wait. Other writes are blocked.
    - As communication over the network is unreliable, this is a big tradeoff.
- **Asynchronous**:
  - Better performance
    - Writes are not blocked, despite any network conditions or other factors
  - However, followers might lag behind (can be up to minutes)
    - So we do not have _consistency_ anymore, that is, you get result A from one DB but result B from another.
  - Furthermore, what if a write totally fails because a follower is down for example? Then the write is not persisted.
    - So we don't have ensured _durability_

So both have big tradeoffs. Some systems use _semi-synchronous_ replication: one follower is synchronous, the rest are asynchronous. This guarantees at least two nodes have the latest data without sacrificing too much performance.

However, most distributed systems use fully asynchronous replication. This is a conscious trade-off of durability for availability and performance.

## Setting Up New Followers

Sometimes you need new followers - maybe to increase read capacity or replace failed nodes. How do you set this up without downtime?

The conceptual process works like this:

1. Take a consistent snapshot of the leader's database
2. Copy the snapshot to the new follower
3. The follower connects to the leader and requests all changes since the snapshot
4. When the follower processes the backlog, it has "caught up" and can continue applying changes in real-time

This process varies significantly between database systems. Some automate it fully, while others require manual administrator intervention.

## Handling Node Outages

Nodes fail. It's inevitable. Good replication systems should handle these failures. Fault tolerance is one of the main reasons for replications.

### When a Follower Fails: Catch-up Recovery

This one is straightforward. When a follower recovers from a crash, it:

1. Checks its local _log_ to find the last _transaction_ it processed
2. Connects to the leader and requests all changes since that point
3. Applies these changes to catch up
4. Resumes normal operation

### When a Leader Fails: Failover

This is a bit trickier. When a leader fails, we need to:

1. Detect the failure (usually via timeout)
2. Choose a new leader (usually the follower with the most up-to-date data)
3. Reconfigure the system to use the new leader
4. Handle client redirects to the new leader

This process is called _failover_ and can be automatic or manual. But failover has issues:

- With asynchronous replication, the new leader might be missing writes the old leader confirmed
- Split-brain scenario: two nodes both think they're the leader
- Setting the right timeout is hard - too short causes unnecessary failovers during temporary slowdowns

These aren't just theoretical concerns. A prominent example was GitHub: they had an incident where an out-of-date MySQL follower was promoted to leader. The database used auto-incrementing IDs, and the new leader reused primary keys that were previously assigned, causing inconsistency with their Redis store and exposing private data to the wrong users. Read their blog for more: [here](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/)

For these reasons, some teams prefer to manually trigger failovers, accepting a brief outage instead of risking data corruption.

## Replication Lag

> Replication Lag = replications (for example followers) are lagging behind the most recent data

In normal operation, this lag might be milliseconds, but during heavy load or network issues, it can grow to seconds or even minutes. This introduces inconsistencies - the leader has newer data than followers.

This isn't just theoretical. Some real-world issues caused by replication lag include:

- Read-after-write inconsistency: A user writes something, then immediately tries to read it but gets directed to a follower that hasn't received the update yet
- Monotonic reads violations: A user sees newer data, then older data in subsequent reads
- Consistent prefix issues: Related updates appear in a confusing order

### Solutions for Replication Lag

There are several approaches to address these issues:

- **Read-your-writes consistency**: After writing, ensure subsequent reads go to the leader or only to up-to-date followers
- **Monotonic reads**: Make sure each user always reads from the same replica
- **Consistent prefix reads**: Make sure causally related writes are seen in the correct order

Implementing these in application code is complex and error-prone. Ideally, developers shouldn't have to worry about these issues - that's why transactions exist. Transactions are not covered in this article though.

## Multi-Leader Replication

The single-leader model has a critical weakness: if you can't reach the leader, you can't write to the database.

Multi-leader replication addresses this by allowing multiple nodes to accept writes. Each write is still forwarded to all nodes. This approach is especially useful in scenarios like:

- Multi-datacenter operation (a leader in each datacenter)
- Clients with offline operation (like calendar apps)
- Collaborative editing systems

The main challenge is handling write conflicts when different leaders accept conflicting changes to the same data.

This is less common than single-leader replication and I will not go into detail here.

## Leaderless Replication

This is a totally different approach. In leaderless systems (sometimes called Dynamo-style after Amazon's system), any replica can directly accept writes from clients. There are no leaders.

The typical approach works like this:

1. The client sends writes to multiple replicas
2. If enough replicas acknowledge the write, it's considered successful
3. During reads, the client queries multiple replicas in parallel
4. Version numbers identify the most recent value
5. "Read repair" or anti-entropy processes fix stale data

This design eliminates the need for failover, making the system more resilient to node failures. Cassandra, Riak, and Amazon's DynamoDB use variations of this approach.

I will also not go into detail here.

## Choosing the Right Replication Model

Each replication approach has its place:

- **Single-leader**: Simple, well-understood, works for most applications
- **Multi-leader**: Good for multi-datacenter operation and offline clients
- **Leaderless**: Highly available for write-intensive workloads with weaker consistency needs
