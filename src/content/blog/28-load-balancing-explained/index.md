---
title: 'Load Balancing Explained: Distributing Traffic Like a Pro'
summary: 'How load balancers work, why you need them, and the main algorithms they use to keep your apps running smoothly.'
date: 'Jan 17 2024'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Software Architecture
  - Scalability
  - High Availability
  - Load Balancing
  - Performance
  - Networking
  - Cloud Computing
---

# Load Balancing Explained: Distributing Traffic Like a Pro

Your app gets popular. Traffic increases. One server can't handle it all. What do you do?

Add more servers and a load balancer.

The load balancer sits in front of your servers and spreads incoming requests across all of them. No single server gets overwhelmed.

## Basic Setup

**Client → Load Balancer → Server Pool**

1. Client makes request
2. Load balancer picks a server (using an algorithm)
3. Server processes request and responds
4. Load balancer passes response back to client

The client has no idea multiple servers exist.

## Why You Need Load Balancing

**Performance** - Requests get processed faster when spread across multiple servers

**Scalability** - Add more servers to handle more traffic. Load balancer automatically uses them.

**Reliability** - If one server crashes, others keep working. Load balancer stops sending traffic to dead servers.

## Health Checks

Load balancers constantly monitor server health. They send small requests (like ping or HTTP GET to `/health`) to check if servers are responding.

If a server doesn't respond or returns errors, it gets marked as unhealthy. Traffic stops going to it until it passes health checks again.

## Common Load Balancing Algorithms

**Round Robin** - Requests go to servers in order: Server 1, Server 2, Server 3, Server 1...

- Simple but ignores server load

**Least Connections** - Send to server with fewest active connections

- Better for long-running requests

**Least Response Time** - Send to fastest-responding server

- Considers both load and network latency

**IP Hash** - Hash client IP to pick server

- Same client always gets same server (useful for sessions)

**Weighted** - Assign weights based on server capacity

- Powerful servers get more traffic

## Types of Load Balancers

**Layer 4 (Transport)** - Routes based on IP and port

- Fast, doesn't look at content
- Can't make decisions based on URL or headers

**Layer 7 (Application)** - Understands HTTP/HTTPS

- Can route based on URL, headers, cookies
- More flexible but slower

## Session Persistence

Some apps need users to stick to the same server (shopping carts, login sessions).

**Sticky Sessions** - Same user always goes to same server

- Simple but problematic if that server dies

**Session Store** - Store session data externally (Redis, database)

- Any server can handle any user
- Better approach for scalability

## Where Load Balancing Happens

**DNS Load Balancing** - Different DNS responses for same domain

- Geographic distribution
- Slow to update

**Hardware Load Balancer** - Dedicated device

- Very fast, expensive

**Software Load Balancer** - Nginx, HAProxy, cloud services

- Flexible, cost-effective

**Service Mesh** - Istio, Linkerd for microservices

- Advanced traffic management

## Bottom Line

Load balancing is essential for any app that needs to handle real traffic. Start with a simple round-robin approach and evolve as you learn your traffic patterns.

Don't wait until you need it. Set it up early, even with one server behind it. Makes scaling much easier later.
