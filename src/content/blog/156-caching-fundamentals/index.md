---
title: "Caching in 2026: Fundamentals, Invalidation, and Why It Matters More Than Ever"
summary: "A deep dive into caching fundamentals - why it's one of the hardest problems in computer science, the difference between invalidation and eviction, and how to think about caching in modern distributed systems"
date: "Feb 8 2026"
tags:
  - Caching
  - System Design
  - Distributed Systems
  - Performance
  - Microservices
---

# Caching in 2026: Fundamentals, Invalidation, and Why It Matters More Than Ever

There's a famous quote in software engineering:

> "There are only two hard things in Computer Science: cache invalidation and naming things."
> — Phil Karlton

This quote has been around since the 90s, and it's still painfully accurate. We've built incredibly sophisticated distributed systems, we've put AI everywhere, we've automated deployments to the point where you can ship code 50 times a day - but cache invalidation? Still hard. Still bites people. Still causes outages.

So why are we talking about caching fundamentals in 2026? Because caching matters more than ever. With microservices architectures, you have dozens of network calls for a single user request. With LLM inference, you're looking at 500ms to 5 seconds per call and high associated costs. With global deployments, every millisecond of latency matters. Caching is often the difference between a snappy application and one that users abandon.

Let's go back to basics and build up from there.

## What Is Caching?

Caching is storing the result of some operation so that subsequent requests can use this stored value rather than spending time and resources recalculating it.

That's it. Simple concept. The complexity comes from everything else.

Consider a recommendation service that needs to check stock levels before recommending items - there's no point in recommending something that's out of stock. But checking stock levels requires calling the Inventory service. If the Recommendation service keeps a local copy of stock levels (a cache), it can avoid that network call most of the time.

When Recommendation looks up a stock level and finds it in the local cache, that's a **cache hit**. If the data isn't there, it's a **cache miss**, and we need to fetch from the origin (the Inventory service).

The problem is obvious: what happens when stock levels change? The cache might be serving outdated data. This is where invalidation comes in.

## Why Cache?

Three main reasons:

### Performance

Network calls are expensive. Not just in latency - each call adds load on downstream services, consumes bandwidth, and introduces failure points. Caching eliminates these calls for frequently accessed data.

Consider generating a list of top-selling items by genre. That might involve an expensive join across several database tables. Without caching, you're running that expensive query for every request. With caching, you run it once and serve the result until it's invalidated.

The difference can be dramatic:

| Operation                      | Typical Latency  |
| ------------------------------ | ---------------- |
| L1 cache hit                   | 1 ns             |
| Memory access                  | 100 ns           |
| SSD read                       | 100 microseconds |
| Network call (same datacenter) | 500 microseconds |
| Network call (cross-region)    | 50-150 ms        |
| LLM inference call             | 500 ms - 5 s     |

That's multiple orders of magnitude difference between a local cache hit and a network call.

### Scale

If you can serve reads from a cache, you reduce load on your origin systems. This is the principle behind database read replicas - read traffic goes to replicas, reducing contention on the primary node.

More broadly, caching is useful whenever the origin is a bottleneck. Put caches between clients and the origin, and you buy yourself headroom.

### Robustness

This one is less obvious. If you have data cached locally, you can potentially keep operating even if the origin is unavailable.

This requires configuring your cache to not automatically remove stale data when it can't be refreshed. You accept that you might serve outdated data during an outage, but at least you serve something. In some cases, stale data is better than no data. Fundamentally, using a cache for robustness means favoring availability over consistency.

## Invalidation vs Eviction

Here's something that gets confused a lot: **invalidation** and **eviction** are not the same thing.

**Invalidation** is the process of marking cached data as no longer valid. The data in your cache is stale - it no longer represents the truth at the origin. You need to either remove it or refresh it.

**Eviction** is the process of removing data from the cache to free up space. This happens when your cache is full and you need to make room for new entries. Eviction policies like LRU (Least Recently Used), LFU (Least Frequently Used), or FIFO (First In First Out) determine which entries get removed.

The distinction matters because:

- Invalidation is about **correctness** - ensuring you're not serving stale data
- Eviction is about **resource management** - making sure your cache doesn't run out of memory

You can invalidate without evicting (mark as stale but keep in cache until confirmed fresh). You can evict without invalidating (remove valid data just because you need space). They're orthogonal concerns.

In most discussions about caching challenges, we're talking about invalidation. That's the hard part. Eviction is relatively straightforward - you pick an algorithm that fits your access patterns and you're done.

## Where to Cache

In a microservices architecture, you have options. Let me walk through them with an example.

Imagine an e-commerce system where the Sales service tracks which items were sold (just IDs and timestamps). When generating a "top 10 best sellers" list, Sales needs to look up the actual product names from the Catalog service.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Sales     │────▶│  Catalog    │
│             │     │  Service    │     │  Service    │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
                                        ┌─────────────┐
                                        │  Database   │
                                        └─────────────┘
```

Where could we cache?

### Client-Side Caching

Sales keeps a local cache of product names. When generating the top 10, it checks the local cache first before calling Catalog.

```
┌─────────────┐     ┌─────────────────────────────┐
│   Client    │────▶│         Sales Service       │
│             │     │  ┌──────────────────────┐   │
└─────────────┘     │  │ Local Cache          │   │
                    │  │ ID → Product Name    │   │
                    │  └──────────────────────┘   │
                    └─────────────────────────────┘
```

**Pros:**

- Eliminates network calls entirely for cache hits
- Great for latency optimization
- Good for robustness (can serve cached data if Catalog is down)

**Cons:**

- Limited invalidation options (the origin doesn't know about your cache)
- Inconsistency between clients (if Sales, Recommendations, and Promotions all cache Catalog data, they might see different versions at the same time)
- Each client uses memory for caching

The inconsistency issue is real. When Catalog updates a product name, whatever invalidation mechanism you use won't update all client caches simultaneously. For a brief window, different services see different data.

### Shared Client-Side Cache

Instead of each client maintaining its own cache, multiple clients share a single cache layer (Redis, Memcached, etc.):

```
                    ┌─────────────────────────────┐
┌─────────────┐     │         Sales Service       │
│   Client    │────▶│                             │
└─────────────┘     └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │     Shared Cache (Redis)    │
                    └─────────────────────────────┘
                                  ▲
                                  │
                    ┌─────────────┴───────────────┐
                    │   Recommendations Service   │
                    └─────────────────────────────┘
```

**Pros:**

- Eliminates inconsistency between clients
- More efficient memory use (one cache instead of many)
- Single place to invalidate

**Cons:**

- Still need a network call to the cache
- Blurs the line between client-side and server-side caching
- Another service to manage

### Server-Side Caching

Catalog itself maintains a cache. When Sales requests product names, Catalog serves them from cache transparently.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────────────────┐
│   Client    │────▶│   Sales     │────▶│       Catalog Service       │
│             │     │  Service    │     │  ┌──────────────────────┐   │
└─────────────┘     └─────────────┘     │  │   Internal Cache     │   │
                                        │  └──────────────────────┘   │
                                        └─────────────────────────────┘
```

**Pros:**

- Transparent to consumers (they don't know or care about the cache)
- Easier to implement sophisticated invalidation (write-through, etc.)
- Benefits all consumers at once

**Cons:**

- Still requires a network round trip
- Less effective for latency optimization
- Doesn't help robustness if the service itself is down

Server-side caching is great when a service is widely used. One optimization benefits everyone.

### Request Caching

Cache the entire result of the top 10 request:

```
┌─────────────┐     ┌────────────────────────────────────┐
│   Client    │────▶│            Sales Service           │
│             │     │  ┌──────────────────────────────┐  │
└─────────────┘     │  │ Cache: "top-10" → [results]  │  │
                    │  └──────────────────────────────┘  │
                    └────────────────────────────────────┘
```

No database queries, no calls to Catalog - just return the cached result.

**Pros:**

- Most efficient (everything is precomputed)
- Minimal latency

**Cons:**

- Highly specific (only benefits this exact request)
- Other operations don't benefit at all
- Need to invalidate when any input changes

## Invalidation Strategies

Here's where Phil Karlton's quote becomes painfully relevant.

### Time to Live (TTL)

The simplest approach. Each cache entry is valid for a fixed duration - say, 5 minutes. After that, it's considered stale and needs to be refreshed.

HTTP supports this via the `Cache-Control` header. The origin tells clients how long to consider data fresh.

**Pros:**

- Dead simple to implement
- Works everywhere

**Cons:**

- Blunt instrument
- If data changes 1 second after caching, you're serving stale data for 4 minutes and 59 seconds

You can get clever with TTLs. Fast-selling items might get shorter TTLs (stock changes rapidly). Slow-moving items get longer TTLs. But it's still fundamentally guessing.

### Conditional GETs (ETags)

HTTP provides entity tags (ETags) for this. When you GET a resource, the response includes an ETag (a hash of the content). Later, you can make a conditional GET with `If-None-Match: <etag>`. If the content hasn't changed, you get a `304 Not Modified` response (saving bandwidth). If it has, you get the new content.

This is useful when the cost of _generating_ the response is high. You still make the network call, but you avoid regenerating unchanged data.

### Notification-Based Invalidation

The origin emits events when data changes. Subscribers use these events to invalidate their caches.

```
┌─────────────────┐                    ┌──────────────────┐
│    Inventory    │──Stock Changed───▶ │  Recommendation  │
│    Service      │      Event         │     Service      │
└─────────────────┘                    │  (invalidates    │
                                       │   local cache)   │
                                       └──────────────────┘
```

**Pros:**

- Minimizes staleness window (cache is invalidated almost immediately)
- Elegant conceptually

**Cons:**

- Complex to implement (need event infrastructure)
- What if the notification mechanism itself fails?
- What does the notification contain? Just "this changed" or the new value?

For the last point: if the notification says "item X changed" but not the new value, the consumer needs to fetch it. If the notification contains the new value, consumers can update directly - but now you're broadcasting potentially sensitive data.

One subtle issue: if you haven't received notifications for a while, how do you know if that's because nothing changed or because notifications are broken? A heartbeat can help - periodic "still alive" messages that let subscribers know the notification channel is healthy.

### Write-Through Caching

The cache is updated at the same time as the origin. When you write to the database, you also write to the cache.

This works best for server-side caches where the write and the cache are in the same service boundary. Coordinating writes across services is hard.

**Pros:**

- Minimal staleness (cache and origin are updated together)

**Cons:**

- Complexity of coordinating updates
- What if the cache update fails?

### Write-Behind Caching

The cache is updated first, then the origin is updated asynchronously.

```
Write → Cache (fast) → Queue → Origin (slower)
```

**Pros:**

- Fast writes (just update the cache)
- Can batch updates to the origin

**Cons:**

- Data loss risk (cache might be lost before origin is updated)
- Confusing source of truth (is the cache the source of truth now?)

I've seen write-behind caches used for in-process optimization, but rarely in microservices architectures. The data loss risk and source-of-truth confusion usually aren't worth it.

## The Golden Rule

**Cache in as few places as possible.**

Every cache you add is another place where data can be stale, another thing to reason about, another potential source of bugs.

Consider a situation where Inventory has a server-side cache with a 1-minute TTL, and Recommendation has a client-side cache, also with a 1-minute TTL. When Recommendation's cache expires and it fetches from Inventory, it might get data that's already 59 seconds old (from Inventory's cache). So Recommendation's cache could be up to 2 minutes stale, even though each individual TTL is 1 minute.

```
Real data changes → 0:00
Inventory cache still fresh → until 1:00
Recommendation fetches at 0:59, gets 59-second-old data
Recommendation cache now valid until 1:59
Total staleness: up to 2 minutes
```

Now perhaps this is not a huge issue but it's a super simple example of how you easily run into unexpected behavior and inconsistencies when caching in too many places. And it gets worse very easily.

Nested caches compound staleness. The more layers, the harder it is to reason about freshness.

This is why premature optimization is dangerous with caching. You add a cache because it seems like a good idea. Then you add another. Soon you can't actually explain how fresh your data is.

**The ideal number of caches is zero.** Everything else is a trade-off you make because you need the performance or scale benefits.

## Caching in the LLM Era

Why is this all more relevant now?

LLM inference is expensive. A single call to a large model might cost $0.01 and take 2 seconds. If you're building an application that uses AI, those costs and latencies add up fast.

Caching LLM responses is attractive but tricky:

- **Exact match caching:** If someone asks the exact same question, return the cached answer. Easy to implement, but cache hit rates are low (slight wording changes mean cache misses).

- **Semantic caching:** Use embeddings to find semantically similar queries and return cached responses. Higher hit rates, but now you're adding complexity and potentially returning subtly wrong answers.

- **Prompt template caching:** If you're calling an LLM with templates (e.g., "Summarize this document: {doc}"), you can cache based on the document hash, not the full prompt.

The stakes are higher too. If your cache serves stale product prices, you might have unhappy customers. If your cache serves stale AI-generated medical advice... you have bigger problems.

## Practical Checklist

When adding caching to a system that might be helpful to keep in mind:

**Before adding a cache:**

- [ ] Do I actually need this? What's the performance/scale problem I'm solving?
- [ ] What's the cost of serving stale data? How stale is acceptable?
- [ ] Where in the system should this cache live?

**When implementing:**

- [ ] What's the TTL? How did I decide that number?
- [ ] What happens on cache miss? Is the origin ready for the load?
- [ ] How will I monitor cache hit rates and staleness?
- [ ] What's my invalidation strategy?
- [ ] Can I easily purge the cache if something goes wrong?

**After deploying:**

- [ ] What's my actual hit rate? Is the cache helping?
- [ ] Am I seeing inconsistencies between cached and fresh data?
- [ ] Is the complexity worth the benefit?

## Wrapping Up

Caching is one of those things that seems simple until you're debugging a production issue at 3am, trying to figure out why some users see outdated data and others don't.

The fundamentals:

- Caching trades freshness for performance
- Invalidation is the hard part, eviction is the easy part
- Cache in as few places as possible
- Understand the full path from origin to consumer
- Measure everything

Phil Karlton was right. Cache invalidation is hard. But understanding why it's hard, and being deliberate about where and how you cache, makes it manageable.
