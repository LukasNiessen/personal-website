---
title: 'The 8 Fallacies of Distributed Computing: Still Relevant in 2026'
summary: 'A deep dive into the classic fallacies of distributed computing and why they matter more than ever in the age of microservices, cloud-native, and AI'
date: 'Jan 01 2026'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Distributed Systems
  - System Design
  - Microservices
  - Cloud
---

# The 8 Fallacies of Distributed Computing: All You Need To Know + Why It's Still Relevant In 2026

Back in 1994, Peter Deutsch at Sun Microsystems wrote down something that every distributed systems engineer eventually learns the hard way: a list of assumptions that developers new to distributed computing make. All of them are wrong. All of them will bite you.

These are the **8 Fallacies of Distributed Computing**. And here's the thing - despite three decades of progress, cloud-native architectures, and managed services that abstract away complexity, these fallacies are arguably *more* relevant today than ever.

Why? Because we're building more distributed systems than ever before. Microservices, serverless, edge computing, multi-region deployments, AI inference at scale - all of this means more network calls, more points of failure, and more developers who haven't internalized these lessons yet.

Let's go through each one.

## The 8 Fallacies

Here they are, as originally stated:

1. The network is reliable
2. Latency is zero
3. Bandwidth is infinite
4. The network is secure
5. Topology doesn't change
6. There is one administrator
7. Transport cost is zero
8. The network is homogeneous

Let's break them down one by one with a modern lens.

## Fallacy 1: The Network is Reliable

This is the big one. The mother of all fallacies.

**The assumption:** When you make a network call, it will succeed.

**The reality:** Network calls fail. All the time. Packets get dropped, connections time out, DNS fails, load balancers hiccup, cloud provider networks have issues, your Kubernetes pod gets evicted mid-request. The question isn't *if* your network calls will fail, it's *when* and *how often*.

**What this looks like in 2026:**

```
Your service → API Gateway → Service Mesh → Another Pod → Database
                  ↓              ↓              ↓           ↓
              Can fail       Can fail       Can fail    Can fail
```

Every arrow is a potential failure point. And in a microservices architecture, a single user request might traverse dozens of these arrows.

**What to do about it:**

- **Retry with backoff:** Don't retry immediately - you'll just make things worse. Use exponential backoff with jitter.
- **Circuit breakers:** Stop hammering a failing service. Let it recover.
- **Timeouts everywhere:** Never make a network call without a timeout. Ever.
- **Graceful degradation:** What can your service do if its dependencies are down?
- **Idempotency:** If a request might be retried, make sure handling it twice doesn't cause problems. I wrote about [idempotence in system design](https://lukasniessen.com/blog/112-idempotence-in-system-design/) if you want to dig deeper.

**My take:** I've seen production outages caused by a single missing timeout. One service started hanging, which caused the calling service to exhaust its connection pool, which caused *its* callers to timeout, and suddenly the entire system was down. All because of one missing timeout configuration. Always assume the network will fail.

## Fallacy 2: Latency is Zero

**The assumption:** Network calls are instant, just like local function calls.

**The reality:** Network calls take time. A lot more time than you think.

Here's a rough order of magnitude:

| Operation | Latency |
|-----------|---------|
| L1 cache reference | 1 ns |
| Main memory reference | 100 ns |
| SSD read | 100 μs |
| Network roundtrip (same datacenter) | 500 μs |
| Network roundtrip (cross-region) | 50-150 ms |
| Network roundtrip (cross-continent) | 100-300 ms |

That's a difference of 5-6 orders of magnitude between a memory access and a cross-region network call.

**What this looks like in 2026:**

With microservices, a single user request might trigger 10, 20, or even 50 internal service calls. If each takes 5ms on average, you're looking at 50-250ms just in internal latency. And that's assuming nothing goes wrong.

The rise of AI also makes this worse. If you're calling an LLM for inference, that's typically 500ms-5s per request. Chain a few of those together for an agentic workflow and you're looking at serious latency.

**What to do about it:**

- **Batch requests:** Instead of 100 individual calls, make one call with 100 items.
- **Parallel calls:** If you need data from three services, fetch in parallel, not sequentially.
- **Caching:** Cache aggressively at every level. But be aware of cache invalidation challenges.
- **Async where possible:** Not everything needs a synchronous response. Use message queues for background work.
- **Colocate what talks together:** Services that communicate frequently should be in the same region, ideally the same availability zone.

**The math that matters:**

```
Sequential: Service A (5ms) → Service B (5ms) → Service C (5ms) = 15ms
Parallel:   Service A (5ms) ─┐
            Service B (5ms) ─┼─→ max(5, 5, 5) = 5ms
            Service C (5ms) ─┘
```

That's a 3x improvement just by parallelizing. Always think about your call graph.

## Fallacy 3: Bandwidth is Infinite

**The assumption:** You can send as much data as you want over the network.

**The reality:** Bandwidth costs money, has limits, and can become a bottleneck faster than you think.

**What this looks like in 2026:**

This fallacy manifests in a few ways:

1. **Chatty APIs:** Making hundreds of small requests instead of fewer larger ones
2. **Over-fetching:** Returning entire objects when the client only needs two fields (looking at you, REST without field selection)
3. **Log/metrics explosion:** Modern observability is great until you're shipping terabytes of logs per day
4. **AI model serving:** Moving large models or embeddings around is expensive

Cloud egress costs are real. Moving data out of AWS, GCP, or Azure isn't free, and at scale, it can become a significant line item on your bill.

**What to do about it:**

- **Right-size your payloads:** Only send what's needed. GraphQL helps here. So does designing better REST endpoints.
- **Compression:** Use gzip, brotli, or zstd for API responses and log shipping.
- **Pagination:** Never return unbounded lists. Always paginate.
- **Data locality:** Keep compute close to data. Don't ship terabytes across the internet if you can run the computation where the data lives.
- **Smart sampling:** Do you really need 100% of your traces and logs? Often 1-10% gives you enough visibility at a fraction of the cost.

## Fallacy 4: The Network is Secure

**The assumption:** Data sent over the network is safe from interception or tampering.

**The reality:** Networks are hostile environments. Assume everything can be intercepted, modified, or spoofed.

**What this looks like in 2026:**

The good news: TLS everywhere is basically standard now. The bad news: security threats have evolved.

- **Service-to-service communication:** Are your internal microservices using mTLS? Or can any compromised pod talk to your database service?
- **Zero trust:** The old model of "inside the firewall = trusted" is dead. Every service needs to authenticate and authorize every request.
- **Supply chain attacks:** Your dependencies, container images, and CI/CD pipelines are all attack vectors.
- **AI-specific threats:** Prompt injection, model poisoning, and data exfiltration through AI systems are new attack surfaces.

**What to do about it:**

- **mTLS everywhere:** Service mesh solutions like Istio, Linkerd, or Cilium make this easier.
- **Zero trust architecture:** Authenticate every request, even internal ones.
- **Secrets management:** Use Vault or cloud-native solutions. Never hardcode credentials. I covered this in [my Vault basics article](https://lukasniessen.com/blog/131-vault-basics/).
- **Network policies:** In Kubernetes, restrict which pods can talk to which.
- **Regular security audits:** Penetration testing, dependency scanning, and security reviews should be routine.

## Fallacy 5: Topology Doesn't Change

**The assumption:** The network stays the same. IP addresses are stable, servers stay where they are.

**The reality:** In modern cloud environments, *everything* is ephemeral and constantly changing.

**What this looks like in 2026:**

```
Traditional:  Server A (10.0.0.5) ←→ Server B (10.0.0.6)
              (IP addresses stable for years)

Cloud-native: Pod A (10.0.47.193) ←→ Pod B (10.0.52.17)
              (IP addresses change every deployment, every scale event, every node failure)
```

Kubernetes pods come and go. Auto-scaling adds and removes instances. Multi-region deployments shift traffic between datacenters. Edge computing pushes workloads to wherever users are. The network topology is in constant flux.

**What to do about it:**

- **Service discovery:** Don't hardcode IPs. Use DNS, service registries, or Kubernetes services.
- **Load balancers:** Abstract away individual instances.
- **Health checks:** Know when endpoints become unavailable and route around them.
- **Graceful shutdown:** Handle SIGTERM properly. Drain connections before dying.
- **Design for chaos:** Assume pods will be killed randomly. Because in Kubernetes, they will be. I talked about this in my [ephemeral infrastructure article](https://lukasniessen.com/blog/146-ephemeral-infrastructure/).

## Fallacy 6: There is One Administrator

**The assumption:** One person or team controls the entire network.

**The reality:** Modern systems span multiple teams, cloud providers, third-party services, and organizational boundaries.

**What this looks like in 2026:**

A typical request path might involve:

```
User → CDN (Cloudflare) → API Gateway (AWS) → Your Service (GCP) 
     → Payment Provider (Stripe) → Database (AWS RDS)
```

That's at least four different administrative domains. When something goes wrong, who do you call?

And even within your organization, different teams own different services. Platform team manages Kubernetes, security team manages policies, product teams manage their microservices. Nobody has the full picture.

**What to do about it:**

- **Observability:** Distributed tracing is essential. You need to see the entire request path across service boundaries.
- **Clear ownership:** Every service should have an owner. Every on-call rotation should be defined.
- **SLAs and contracts:** When depending on third-party services, understand their guarantees.
- **Multi-cloud awareness:** Know the failure modes of each cloud provider you depend on.
- **Documentation:** Runbooks for common failure scenarios. Who to contact. Escalation paths.

## Fallacy 7: Transport Cost is Zero

**The assumption:** Moving data over the network is free.

**The reality:** Network operations have real costs - compute, money, and environmental impact.

**What this looks like in 2026:**

Every network call has costs:

- **CPU cycles:** Serialization, deserialization, encryption, compression all take compute.
- **Cloud bills:** Egress costs, load balancer costs, NAT gateway costs, API gateway costs.
- **Energy:** Data centers consume enormous amounts of power. Network I/O is part of that.

At scale, inefficient network patterns become very expensive. A poorly designed API that makes 10x more calls than necessary doesn't just hurt latency - it directly impacts your infrastructure costs.

**What to do about it:**

- **Measure everything:** Track request counts, payload sizes, and costs per service.
- **Optimize hot paths:** The 1% of requests that generate 50% of your traffic are worth optimizing.
- **Connection pooling:** Reuse connections instead of establishing new ones for each request.
- **Regional deployments:** Keep data transfer within regions where possible.
- **Right-size protocols:** gRPC is more efficient than REST for high-volume internal communication. But REST might be fine for low-volume external APIs. Choose appropriately.

## Fallacy 8: The Network is Homogeneous

**The assumption:** All parts of the network have the same characteristics and use the same protocols.

**The reality:** Networks are heterogeneous. Different segments have different properties, protocols, and constraints.

**What this looks like in 2026:**

Your system might communicate over:

- **HTTP/REST** to external partners
- **gRPC** for internal service-to-service calls
- **GraphQL** for frontend-to-backend
- **WebSockets** for real-time features
- **MQTT** for IoT devices
- **Kafka protocol** for event streaming
- **Proprietary protocols** for legacy systems

Each has different characteristics. Some are synchronous, some async. Some support streaming, some don't. Some work well with high latency, some don't.

And the physical network varies too:

```
Datacenter network:    10+ Gbps, <1ms latency
Inter-region:          High bandwidth, 50-150ms latency
Mobile network:        Variable bandwidth, high latency, packet loss
Edge/IoT:              Low bandwidth, unreliable, intermittent
```

**What to do about it:**

- **Protocol translation:** Use API gateways and adapters to bridge different protocols.
- **Design for the weakest link:** If mobile clients are important, design for their constraints.
- **Graceful degradation:** Handle partial failures and reduced functionality.
- **Testing across conditions:** Don't just test on your fast office network. Simulate poor network conditions.

## The Modern Twist: Distributed AI Systems

In 2025/2026, there's a new dimension to these fallacies: AI systems are inherently distributed and make everything more complex.

**LLM inference:** When your application calls an AI model, that's a network call with unpredictable latency (500ms to 10s+), potentially high bandwidth (large prompts/responses), and reliability concerns (rate limits, outages).

**Agentic AI:** AI agents that make decisions and take actions often need to call multiple services, potentially in chains. Each call compounds the fallacies.

**RAG systems:** Retrieval-augmented generation means your AI calls need to hit vector databases, potentially with large embeddings, adding latency and bandwidth concerns.

**Edge AI:** Running inference at the edge (on devices or edge servers) introduces all the heterogeneity and reliability challenges of edge computing.

If you're building AI-powered systems, you need to internalize these fallacies even more deeply.

## Practical Checklist

Here's a quick checklist for system design interviews or when reviewing your architecture:

### For Each Network Call, Ask:

- [ ] What happens if this call fails?
- [ ] What's the timeout? (There should always be one!)
- [ ] Is there retry logic? With backoff?
- [ ] Is the operation idempotent?
- [ ] What's the expected latency? P50? P99?
- [ ] How much data is being transferred?
- [ ] Is it encrypted in transit?
- [ ] How do we discover the endpoint?
- [ ] Who owns the other side?
- [ ] What does it cost?

### For Your System Overall:

- [ ] Can you trace a request across all services?
- [ ] Do you have circuit breakers between services?
- [ ] What's your graceful degradation strategy?
- [ ] Are your services tolerant of topology changes?
- [ ] Do you have capacity for retries? (They increase load!)

## Wrapping Up

The 8 Fallacies of Distributed Computing are over 30 years old, but they're not going away. If anything, they're more relevant than ever. We're building more distributed systems, with more network hops, more cloud dependencies, and more complexity than ever before.

The fundamentals don't change:
- Networks fail
- Latency matters
- Bandwidth isn't free
- Security requires effort
- Everything changes
- Nobody owns everything
- There are real costs
- Heterogeneity is the norm

Understanding these fallacies won't prevent problems - but it will help you design systems that handle them gracefully. And in distributed systems, graceful failure handling is often the difference between a minor blip and a major outage.
