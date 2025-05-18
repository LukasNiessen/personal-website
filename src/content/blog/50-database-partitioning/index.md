---
title: "ELI5: Database Partitioning"
summary: "Database Partitioning in ELI5. Not only though, I also cover each topic with a more thorugh summary."
date: "Jan 02 2024"
draft: false
repoUrl: "https://github.com/LukasNiessen/database-partitioning"
xLink: "https://x.com/iamlukasniessen/status/1924125876771324067"
tags:
  - Partitioning
  - Database
  - ELI5
---

# ELI5: Database Partitioning

This article is Database Partitioning in ELI5. Not only that though, I also cover each topic with a more thorough explanation. I will cover:

- What is partitioning?
- Why partition your database?
- Partitioning vs. Replication
- Key-Value partitioning strategies
- Handling skewed workloads and hot spots
- Secondary indexes with partitioning
- Request routing and service discovery
- Parallel query execution

## What is Partitioning? ELI5

Say we run Facebook. There are way too many posts to store it on one computer. So we split it, some posts here, some posts there. Each split is a _partition_.

> Partitioning = Splitting a database into smaller chunks across multiple machines

The first question is, of course, how do we partition? But there are other questions that need an answer. I will address them later.

Note: There are other names for _partitions_, for example, it's called _shards_ (_sharding_) in MongoDB and Elasticsearch, or a _tablet_ with Bigtable. However, _partitioning_ is the most established term.

## Why Partition? ELI5

As said, the main reason for partitioning is **scalability**. When your data or query load gets too big for a single machine to handle, you need to break it up.

With partitioning:

- You can store more data than fits on one machine
- You can distribute query load across many processors
- Different partitions can be placed on different nodes in a shared-nothing cluster

We call a DB holding a partition a _node_.

This has other advantages as well, for example parallelizing queries. For queries that only need data from a single partition, each node can independently handle its part, so you can scale query throughput by adding more nodes. Complex queries that span partitions are harder but can potentially be parallelized.

## Partitioning vs. Replication

Partitioning is usually **combined** with replication. That means:

1. Partitioning splits the data into smaller subsets
2. Each partition is then replicated on multiple nodes

Even though each record belongs to only one partition, it may be stored on several different nodes for fault tolerance. A node may store more than one partition. In a leader-follower model, a node might be the leader for some partitions and a follower for others.

## Key-Value Partitioning Strategies

Alright, so let's address the first question. How do we decide which records go on which nodes?

The goal is to spread data and query load evenly. If every node takes a fair share, then 5 nodes should theoretically handle 5 times as much data and throughput as one node.

If the partitioning is uneven, so some partitions have more data or queries than others, we call it **skewed**. An extreme case of skew is a **hot spot**, so in other words, a partition with disproportionately high load.

### 1. Partitioning by Key Range

**How it works**: Assign each partition a continuous range of keys (from some minimum to some maximum).

**Example:** With movies, you could use the name's starting letters as the keys. So movies with A are stored on one node, those starting with B on the other, and so on.

Partition boundaries can be chosen:

- Manually by an administrator
- Automatically by the database

This approach is used by:

- Bigtable and HBase
- RethinkDB
- MongoDB (before version 2.4)

Within each partition, keys are kept in sorted order. This makes range scans efficient and enables treating the key as a concatenated index for fetching related records in one query.

**Example**: Sensor network data where the key is a timestamp. You can easily fetch all readings from a particular month.

**Problem**: Certain access patterns create hot spots. If the key is a timestamp, all writes go to the partition for "today" while other partitions sit idle.

**Solution**: Use something other than a timestamp as the first element of the key. For example, prefix each timestamp with the sensor name so partitioning happens first by sensor, then by time. This spreads write load across partitions.

### 2. Partitioning by Hash of Key

**How it works**: Apply a hash function to keys and assign each partition a range of hash values.

A good hash function takes skewed data and makes it uniformly distributed. For example, Cassandra and MongoDB use this (with MD5).

This approach distributes keys fairly among partitions. The partition boundaries can be:

- Evenly spaced
- Chosen pseudorandomly (sometimes called consistent hashing)

**The Big Tradeoff**: By using a hash of the key, we lose the ability to do efficient range queries. Keys that were once adjacent are now scattered across partitions, and their sort order is lost.

- In MongoDB with hash-based sharding, range queries must be sent to all partitions
- Range queries on the primary key are not supported in Riak, Couchbase, or Voldemort

## Handling Skewed Workloads and Hot Spots

Hashing helps reduce hot spots but can't eliminate them entirely. If all reads and writes target the same key, all requests still go to the same partition.

This happens in real life: a celebrity on social media doing something noteworthy can create a storm of activity on a single key (the celebrity's user ID or the ID of the action people are commenting on). Hashing doesn't help because identical IDs hash to the same value.

There are solutions for this too though, with tradeoffs of course.

## Request Routing and Service Discovery

Now that we've partitioned our dataset across multiple nodes. Great.

But there's an issue not addressed yet. When a client wants to make a request, how does it know which node to connect to? For example which IP address should it connect to?

This problem is generally (also outside of DBs) known as _service discovery_. There are the main approaches:

### 1. Routing Tier

- All client requests go through a routing layer first
- This layer determines the right node for each request and forwards accordingly
- The routing tier is essentially a partition-aware load balancer
- It doesn't handle requests itself

### 2. Any-Node Routing

- Clients can contact any node (for example via a round-robin load balancer)
- If that node has the partition for the request, it handles it directly
- Otherwise, it forwards the request to the appropriate node and passes the reply back

### 3. Client-Aware Routing

- Clients know about the partitioning scheme and partition-to-node mapping
- They connect directly to the appropriate node without intermediaries

Many systems rely on a separate coordination service like ZooKeeper to track cluster metadata:

1. Each node registers in ZooKeeper
2. ZooKeeper maintains the authoritative partition-to-node mapping
3. Routing tiers or clients subscribe to this information
4. When partitions change ownership, ZooKeeper notifies subscribers

Examples:

- LinkedIn's Espresso uses Helix (built on ZooKeeper)
- HBase, SolrCloud, and Kafka use ZooKeeper directly
- MongoDB uses its own config server implementation with mongos daemons as the routing tier

## How Request Routing Works with ZooKeeper

So, you've partitioned your dataset across multiple nodes, and you're using a coordination service like ZooKeeper to manage cluster metadata. But how does a client actually get its request to the right node? Let's break down the flow, focusing on a system with a **routing tier** and ZooKeeper.

## The Request Routing Flow

Here's how it typically works when a client makes a request in a distributed system with a routing tier and ZooKeeper:

1. **Client Sends Request to Routing Tier**  
   The client doesn't know which node holds the data it needs, so it sends its request (e.g., a database query) to a **routing tier**. This is a partition-aware load balancer, like MongoDB's `mongos` daemon or a custom proxy. The routing tier's job is to figure out where to send the request.

2. **Routing Tier Consults ZooKeeper**  
   The routing tier needs to know which node owns the partition for the requested data. It queries **ZooKeeper**, which maintains the authoritative **partition-to-node mapping**. ZooKeeper stores this metadata in a hierarchical structure (like a file system), updated whenever nodes join, leave, or partitions are reassigned. The routing tier either:

   - Caches this mapping and subscribes to ZooKeeper for updates (to stay current), or
   - Queries ZooKeeper on-demand for each request (less common due to latency).

3. **ZooKeeper Provides Metadata**  
   ZooKeeper responds with the current partition-to-node mapping. For example, it might say, "Partition P1 is on Node A (IP: 192.168.1.10), Partition P2 is on Node B (IP: 192.168.1.11)." This tells the routing tier exactly where to send the request.

4. **Routing Tier Forwards the Request**  
   Armed with the mapping, the routing tier forwards the client's request to the correct node (e.g., Node A). The node processes the request, interacts with the database, and returns the response to the routing tier.

5. **Routing Tier Returns Response to Client**  
   The routing tier passes the response back to the client, completing the request. From the client's perspective, it just sent a request and got a response, unaware of the coordination happening behind the scenes.
