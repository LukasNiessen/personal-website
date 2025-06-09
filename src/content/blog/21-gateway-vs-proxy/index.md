---
title: 'Gateway vs Proxy vs Reverse Proxy: What Each Actually Does'
summary: 'Three network components that get confused all the time. Here is what each one actually does and when to use them.'
date: 'Sep 12 2023'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Networking
  - Software Architecture
  - Proxy Server
  - Reverse Proxy
  - API Gateway
  - Security
  - Performance
---

# Gateway vs Proxy vs Reverse Proxy: What Each Actually Does

These three terms get thrown around and confused constantly. They're all network intermediaries, but they work in different directions and solve different problems.

Let's clear this up.

## Proxy Server (Forward Proxy)

Sits between clients and the internet. Clients send requests to the proxy, which forwards them to servers.

**Flow:** Client → Proxy → Server → Proxy → Client

**What it does:**

- Hides client identity from servers
- Caches content for faster repeat requests
- Filters what clients can access
- Logs client activity

**Use cases:**

- Corporate internet filtering
- Bypass geo-restrictions
- Anonymous browsing
- Bandwidth savings through caching

Think of it as a middleman working for the clients.

## Reverse Proxy Server

Opposite of a forward proxy. Sits in front of servers, intercepts client requests, and distributes them to backend servers.

**Flow:** Client → Reverse Proxy → Backend Server → Reverse Proxy → Client

The client thinks it's talking to the server directly. It has no idea the reverse proxy exists.

**What it does:**

- Load balancing across multiple servers
- SSL termination (handles HTTPS encryption/decryption)
- Caches server responses
- Hides server details from clients
- Web Application Firewall protection

**Use cases:**

- CDNs (Content Delivery Networks)
- Load balancers
- API security and rate limiting
- Static content serving

Think of it as a middleman working for the servers.

## Gateway

Broader term. Connects different networks or systems, often translating between different protocols.

**Types:**

**Network Gateway (Router)**

- Connects your home network to the internet
- Handles different network protocols

**API Gateway**

- Single entry point for microservices
- Handles authentication, rate limiting, request routing
- Manages API versioning and documentation

**Payment Gateway**

- Connects e-commerce sites to payment processors
- Handles different payment protocols

**What it does:**

- Protocol translation
- Network routing
- Security enforcement
- Request orchestration (API Gateway)

## Quick Comparison

| Type              | Works For      | Client Knows? | Server Knows? |
| ----------------- | -------------- | ------------- | ------------- |
| **Forward Proxy** | Clients        | Yes           | No            |
| **Reverse Proxy** | Servers        | No            | Yes           |
| **Gateway**       | Network/System | Usually Yes   | Usually Yes   |

## When to Use What

**Forward Proxy:**

- Company wants to filter employee internet access
- Need to bypass geo-restrictions
- Want anonymous browsing

**Reverse Proxy:**

- Have multiple backend servers that need load balancing
- Want to terminate SSL at the edge
- Need to cache content for better performance

**API Gateway:**

- Building microservices architecture
- Need centralized API management
- Want to handle cross-cutting concerns (auth, logging, rate limiting)

**Network Gateway:**

- Connecting different networks
- Need protocol translation
- Want centralized security enforcement

They often work together. A typical setup might have:

- Forward proxy for outbound employee traffic
- API Gateway for external API access
- Reverse proxy for load balancing internal services
