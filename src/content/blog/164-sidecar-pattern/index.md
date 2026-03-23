---
title: "The Sidecar Pattern: Why Every Major Tech Company Runs Proxies on Every Pod"
summary: "How the sidecar proxy pattern became the industry standard for service-to-service communication, and why the trade-offs are worth it"
date: 'Mar 23 2026'
tags:
  - Architecture
  - Microservices
  - Service Mesh
  - Kubernetes
  - Envoy
---

# The Sidecar Pattern: Why Every Major Tech Company Runs Proxies on Every Pod

"But doesn't that mean every single request goes through an extra hop?"

This is the first question I hear whenever I propose adding a sidecar proxy to a microservices architecture. And the answer is: yes. Every request gets an additional hop through the sidecar. But let's talk about what that actually means in practice, and why Google, Uber, Airbnb, eBay, and practically every company running microservices at scale has decided that this trade-off is absolutely worth it.

## What Is the Sidecar Pattern?

The sidecar pattern is exactly what it sounds like. You deploy a small helper process alongside your main application container, in the same pod (in Kubernetes terms) or on the same host. The sidecar handles cross-cutting concerns - things like mTLS, observability, traffic management, authorization - so your application doesn't have to.

The most common sidecar is a proxy like Envoy. When your service makes or receives a network call, it goes through this local proxy first. The proxy handles the networking concerns, and your application just talks to localhost.

```
┌─────────────────────────────────────┐
│              Pod                     │
│                                     │
│  ┌──────────────┐  ┌─────────────┐  │
│  │              │  │             │  │
│  │  Your App    │──│   Envoy     │──────► Network
│  │  (Container) │  │  (Sidecar)  │  │
│  │              │  │             │  │
│  └──────────────┘  └─────────────┘  │
│                                     │
│      localhost call (~1ms)          │
└─────────────────────────────────────┘
```

Your app thinks it's making a normal network call. The sidecar intercepts it, applies whatever policies or transformations are configured, and forwards it. On the receiving side, the sidecar does the same thing in reverse.

## "But It's an Extra Hop"

Let's address this directly because it's a legitimate concern.

Yes, the sidecar adds a network hop. But it's a **localhost call** - same pod, same network namespace. We're talking about 1-2ms of latency, not 10-50ms. The sidecar and your application share the same network stack. There's no crossing network boundaries, no DNS resolution, no TLS handshake between them (they're in the same pod).

And here's the thing: if you're doing mTLS (and you should be), this hop already exists. The sidecar is already sitting there handling your TLS termination and certificate rotation. Adding an authorization check - say, an ext_authz call to a policy engine - adds one more sub-millisecond gRPC call on top of what's already happening.

The alternative is embedding all of this logic - mutual TLS, authorization, retries, circuit breaking, observability - directly into every service's application code. That's far more expensive in engineering time, error surface, and auditability than the ~1ms network overhead.

So yes, it's an extra hop. But it's a localhost hop on infrastructure that's already there. The marginal cost of adding functionality to an existing sidecar is near zero.

## How Service Meshes Use Sidecars

The sidecar pattern is the foundation of every modern service mesh. To understand why sidecars became the standard, it helps to understand what problem service meshes solve.

In any microservices architecture, there's a lot of common functionality that every service needs: mutual TLS, service discovery, load balancing, retries, timeouts, circuit breaking, distributed tracing, metrics collection. This stuff is the same regardless of whether your service processes payments or sends notifications.

Historically, you'd handle this with shared libraries. Netflix, for example, built an entire ecosystem of Java libraries (Hystrix for circuit breaking, Eureka for service discovery, Ribbon for load balancing) and mandated that all inter-service communication happen JVM-to-JVM. This worked, but it meant every service had to be on the JVM, every service needed the right library version, and updating the library meant redeploying every service.

Service meshes solve this by pushing all that common networking logic into the sidecar proxy. Your service can be written in Go, Python, Java, Rust - it doesn't matter. The sidecar handles the networking, and the control plane manages all the sidecars centrally.

```
                    ┌─────────────────────────────┐
                    │        Control Plane          │
                    │  (Configuration, Certificates,│
                    │   Policies, Telemetry)        │
                    └──────┬───────────┬────────────┘
                           │           │
           ┌───────────────┘           └───────────────┐
           ▼                                           ▼
┌──────────────────────┐                 ┌──────────────────────┐
│        Pod A         │                 │        Pod B         │
│                      │                 │                      │
│  ┌────────┐ ┌─────┐ │    mTLS + authz │ ┌─────┐ ┌────────┐  │
│  │Order   │ │Envoy│ │◄───────────────►│ │Envoy│ │Payment │  │
│  │Service │ │Proxy│ │                 │ │Proxy│ │Service │  │
│  └────────┘ └─────┘ │                 │ └─────┘ └────────┘  │
└──────────────────────┘                 └──────────────────────┘
```

The Order Service sends a request to the Payment Service. That call first goes to the local Envoy proxy (localhost, fast), then across the network to the Payment Service's Envoy proxy, which handles TLS termination, authorization, and finally forwards it to the Payment Container. The Order Service has no idea any of this is happening. It just makes a normal HTTP or gRPC call.

The control plane sits on top, distributing certificates, pushing configuration changes, and collecting telemetry from all the proxies.

## Data Plane vs Control Plane

This is a distinction that trips people up, so let's be explicit about it. A service mesh has two parts:

The **data plane** is the actual proxy sitting in your pod. It's the thing that intercepts network traffic, handles mTLS, enforces policies, and collects metrics. This is usually Envoy.

The **control plane** is the management layer that tells all those proxies what to do. It distributes configuration, manages certificates, defines routing rules, and aggregates telemetry. This is what Istio, Linkerd, Consul, etc. actually are.

So when someone says "we use Istio," what they mean is: we run Envoy sidecars in every pod (data plane), and Istiod manages all of them (control plane). Istio is not Envoy. Istio uses Envoy.

```
Service Mesh = Data Plane + Control Plane

Istio   = Envoy proxies        + Istiod
Consul  = Envoy proxies        + Consul Server
Linkerd = linkerd2-proxy        + Linkerd control plane
Cilium  = eBPF (kernel-level)  + Cilium agent
```

Notice that most service meshes chose Envoy as their data plane because it's battle-tested and extensible. Linkerd is the notable exception - they built their own Rust-based proxy (linkerd2-proxy) optimized for low resource usage. Cilium goes even further and skips the sidecar proxy entirely, implementing data plane functionality directly in the Linux kernel via eBPF.

You can also run Envoy without a control plane. It's a perfectly capable standalone proxy. But then you're configuring each instance manually, which doesn't scale. The control plane is what turns a bunch of individual proxies into a mesh.

## Why Envoy Specifically?

So why did most service meshes converge on [Envoy](https://www.envoyproxy.io/) as their data plane? Envoy is a lightweight, high-performance C++ proxy originally built at Lyft. It's the building block for Istio, the data plane for Consul Connect, and is used directly or indirectly by a huge number of service meshes and API gateways.

Why Envoy and not just nginx or HAProxy?

- **Designed for service mesh.** Envoy was built from the ground up for the sidecar use case. It supports dynamic configuration via xDS APIs, meaning the control plane can update routing, load balancing, and security policies without restarting the proxy. This is the big one - nginx and HAProxy traditionally require a reload for config changes.
- **L4 and L7 aware.** It understands both TCP and HTTP/gRPC, so it can make smart routing decisions based on headers, paths, or gRPC methods.
- **Extensibility.** Envoy supports filters and extensions - this is how features like ext_authz (external authorization) work. You can plug in custom logic without modifying the core proxy.
- **Observability built in.** Envoy emits detailed metrics, access logs, and tracing spans out of the box. Free observability just by deploying the sidecar.

## The Trade-offs

Let's be honest about the downsides. The sidecar pattern isn't free, and pretending otherwise doesn't help anyone make good architecture decisions.

### Resource Overhead

Every pod now runs an additional container. That's additional memory and CPU per pod. Envoy is lightweight, but it's not zero. In a typical setup, you're looking at 50-100MB of memory and a fraction of a CPU core per sidecar. Multiply that by hundreds or thousands of pods and it adds up.

For most organizations at the scale where a service mesh makes sense, this is a rounding error on the infrastructure bill. But if you're running 5 microservices on a small cluster, the overhead is proportionally much larger.

### Debugging Complexity

When something goes wrong, you now have an additional layer to investigate. Is the 504 timeout coming from the application or the sidecar? Is the sidecar misconfigured? Is the control plane pushing bad configuration?

Service meshes add powerful debugging tools (distributed tracing, detailed access logs, traffic visualization), but they also add another layer that can itself be the source of problems. 

### Operational Complexity

Running a service mesh means operating the mesh itself. The control plane needs to be highly available. Sidecar versions need to be kept in sync. Upgrades need to be rolled out carefully. This is real operational overhead that requires expertise.

This is the main reason I don't recommend service meshes for small setups. If you have 5 microservices and a team of 3, the operational cost of running Istio likely outweighs the benefits. But once you're at 20+ services with multiple teams, the calculus shifts dramatically.

### Latency (Yes, Really)

I said the latency is small, and it is. But small multiplied by many hops can matter. If a single user request traverses 10 services, each with two sidecar hops (one on the sending side, one on the receiving side), that's 20 extra localhost hops. At 1ms each, that's 20ms added to every request. For most applications, 20ms is nothing, but it's important to keep it in mind. Know your latency budget and measure the actual impact in your environment.

## "Aren't Service Meshes Smart Pipes?"

If you've read about microservices, you've probably heard the principle "smart endpoints, dumb pipes." The idea is that business logic should live in the services, not in the infrastructure between them. So pushing functionality into a service mesh sounds like it might violate this principle.

It doesn't, and here's why: the functionality in the mesh is entirely generic. No business logic leaks into the sidecar. We're configuring things like retry policies, timeout durations, mTLS certificates, and traffic routing rules. None of this is specific to what any individual service does.

This is fundamentally different from, say, putting request aggregation or protocol transformation into an intermediary - that's where you start creating "smart pipes" that embed business decisions in infrastructure. A service mesh doesn't do that. It handles the plumbing so your services can focus on the business logic.

And importantly, most service meshes allow individual teams to self-service configure their own policies. With Istio, for example, you define your timeout requirements and retry policies in your own service definition. No tickets. No waiting on a platform team. The mesh provides the capability; your team decides how to use it.

## The State of Service Meshes in 2026

The service mesh space has matured significantly. When the idea first gained traction around 2017-2018, there was a lot of churn. Linkerd pioneered the space, then completely rebuilt from v1 to v2. Istio took years to reach 1.0 and then went through significant architectural changes (moving to a more monolithic control plane, which was actually the right call). New entrants appeared constantly.

Today, the landscape has settled. The major options are:

**Istio** remains the most widely deployed service mesh, now part of the CNCF. Its move to an ambient mesh model (ztunnel-based, no sidecar for L4) is the biggest architectural shift in years. This gives you mTLS without a per-pod sidecar, and you only add the full L7 proxy (called a waypoint proxy) for services that need advanced traffic management. This directly addresses the resource overhead concern.

**Linkerd** continues to be the lightweight, opinionated choice. It's simpler to operate than Istio and has excellent performance characteristics. If you want a service mesh that "just works" without a lot of configuration knobs, Linkerd is worth a serious look.

**Consul** (HashiCorp) is the go-to choice if you're not all-in on Kubernetes. Consul was built for service discovery and configuration across heterogeneous environments - VMs, bare metal, containers, multiple clouds. Its service mesh capabilities use Envoy as the data plane, just like Istio, but the control plane is designed to work across platforms, not just Kubernetes. If your infrastructure is a mix of Kubernetes and non-Kubernetes workloads, Consul is probably the most practical option.

**Cilium** takes a different approach entirely, using eBPF to implement networking, security, and observability at the Linux kernel level. This can reduce the overhead of traditional sidecar proxies significantly. Cilium's service mesh capabilities have matured rapidly and it's becoming a popular choice especially for teams already using Cilium for networking.

The trend in 2026 is clear: service meshes are moving toward reducing or eliminating the sidecar overhead for basic functionality (L4, mTLS) while keeping proxies available for advanced L7 features. Istio's ambient mesh, Cilium's eBPF approach, and Consul's platform-agnostic model are all evolving in this direction.

## When to Use Sidecars

Not every deployment needs a service mesh. A few examples:

**You probably don't need one if:**
- You have fewer than ~10 microservices
- Your team is small and doesn't have Kubernetes expertise to spare
- Your latency requirements are extreme (sub-millisecond)

**You should seriously consider one if:**
- You have 20+ microservices, especially across multiple teams
- Services are written in different languages
- You need consistent mTLS, observability, or traffic management across all services
- You're implementing zero-trust security
- You want to enforce authorization policies without embedding them in every service

**You almost certainly need one if:**
- You're operating at significant scale (hundreds of services)
- Regulatory requirements demand consistent security and auditability
- Multiple teams need self-service control over traffic policies
- You're implementing fine-grained authorization (like relationship-based access control with something like SpiceDB or OpenFGA)

## A Real Example: Authorization via Sidecar

Here's a concrete example of why sidecars are powerful. Say you want every inter-service call to be authorized - not just authenticated (mTLS handles that), but authorized. Service A can call Service B's `/orders` endpoint, but not its `/admin` endpoint.

Without a sidecar, you'd need to implement authorization checks in every service. Every language, every framework, every team doing it slightly differently. Some services would have bugs. Some would have gaps. Auditing would be a nightmare.

With a sidecar, you configure Envoy's ext_authz filter to call a centralized policy engine (SpiceDB, Open Policy Agent, whatever you prefer) on every request. The authorization decision happens in the sidecar before the request ever reaches your application code.

```yaml
# Envoy ext_authz configuration
http_filters:
  - name: envoy.filters.http.ext_authz
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
      grpc_service:
        envoy_grpc:
          cluster_name: authz-service
        timeout: 0.050s    # 50ms timeout
      failure_mode_deny: true  # deny if authz service is unavailable
```

Now every service gets authorization for free. No code changes. No library imports. No risk of one team forgetting to add the check. And because it's in the sidecar, you get a complete audit trail of every authorization decision across your entire system.

The total added latency? The existing localhost hop to Envoy (already there for mTLS) plus one sub-millisecond gRPC call to the policy engine. That's it.

## Wrapping Up

The sidecar pattern has become the industry standard for managing cross-cutting concerns in microservices architectures. It's not without trade-offs - resource overhead, operational complexity, and a small latency cost are all real. But for organizations operating at any meaningful scale, these costs are vastly outweighed by the benefits: consistent security, observability, and traffic management across every service, regardless of language or framework.

The pattern is evolving too. Ambient meshes, eBPF-based approaches, and smarter control planes are all reducing the overhead while keeping the benefits. The sidecar might eventually disappear as an explicit container in your pod, but the concept - offloading generic networking concerns from application code to infrastructure - is here to stay.

If someone pushes back on the "extra hop," remind them: it's a localhost hop on infrastructure that's already there. The real question isn't whether you can afford the 1ms. It's whether you can afford to implement, maintain, and audit mTLS, authorization, retries, circuit breaking, and distributed tracing in every service's application code instead.
