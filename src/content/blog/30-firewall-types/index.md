---
title: 'Firewall Types: Packet Filter vs Circuit Gateway vs Application Proxy'
summary: 'Three types of firewalls explained: where they sit in the OSI model and what they actually do to protect your network.'
date: 'Apr 02 2024'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Network Security
  - Firewall
  - OSI Model
  - Cybersecurity
  - Packet Filtering
  - Stateful Inspection
  - Application Gateway
  - Proxy Firewall
---

# Firewall Types: Packet Filter vs Circuit Gateway vs Application Proxy

Firewalls sit between your network and the internet. They decide what traffic gets through.

But they're not all the same. Some just check basic packet info. Others understand application protocols. Each works at different OSI layers and offers different protection levels.

## OSI Layers Quick Reference

Firewalls work at different OSI layers:

- **Layer 3 (Network)** - IP addresses, routing
- **Layer 4 (Transport)** - TCP/UDP ports
- **Layer 5 (Session)** - Connection management
- **Layer 7 (Application)** - HTTP, FTP, email protocols

Higher layers = more inspection = better security = slower performance.

## 1. Packet-Filtering Firewalls (Layers 3-4)

The basic bouncer. Looks at packet headers and decides: allow or block.

What they check:

- Source/destination IP addresses
- Source/destination ports
- Protocol type (TCP, UDP, ICMP)

**Stateless vs Stateful:**

_Stateless_ - Each packet judged alone. Fast but dumb.
_Stateful_ - Remembers connection states. Knows if a packet belongs to an existing conversation.

**Pros:**

- Fast and cheap
- Works for most basic needs

**Cons:**

- Can't see what's inside packets
- Stateless versions are easy to fool
- Rule management gets messy

## 2. Circuit-Level Gateways (Layer 5)

These watch TCP handshakes. If two systems properly agree to talk (complete the handshake), traffic flows freely.

Think of it as checking that two people agreed to meet, then letting them talk privately without listening in.

How it works:

1. Client wants to connect to server
2. Gateway checks if handshake is legit
3. If yes, data flows without further inspection
4. If no, connection blocked

Often used with SOCKS proxies.

**Pros:**

- Faster than application-level inspection
- Validates connection legitimacy
- Hides internal network details

**Cons:**

- No content inspection
- Malware can still pass through established connections

## 3. Application-Level Gateways (Layer 7)

The smart bouncer. Understands application protocols like HTTP, FTP, email.

Instead of direct client-server connection, you get two connections:

- Client ↔ Proxy Firewall
- Proxy Firewall ↔ Server

The proxy reads everything and decides what's safe.

Example: HTTP proxy can block malicious JavaScript or filter URLs. Email proxy can scan for viruses.

**Deep Packet Inspection** - They look inside packets, not just headers.

**Pros:**

- Best security - can catch application-layer attacks
- Content filtering and virus scanning
- Detailed logging
- User authentication support

**Cons:**

- Slower due to content inspection
- More complex to set up
- Need different proxies for different protocols
- Can break some applications

## Next-Generation Firewalls (NGFW)

Modern firewalls combine all three approaches plus extras:

- Packet inspection (stateful)
- Application awareness
- Intrusion prevention
- Threat intelligence feeds
- SSL/TLS inspection
- Identity-based rules

Basically, they try to do everything.

## Which One to Pick?

**Packet Filter** - Fast and simple. Good for basic needs and high-traffic environments.

**Circuit Gateway** - Middle ground. Validates connections without content inspection overhead.

**Application Proxy** - Maximum security. Use when you need to inspect application content.

**NGFW** - Best of all worlds but complex and expensive.

Most organizations use layered security - multiple types working together.
