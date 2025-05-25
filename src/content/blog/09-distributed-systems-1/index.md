---
title: "Single Computers vs Distributed Systems: Why Everything Gets Complicated"
summary: "Pointing out the most important differences of single computer systems and distributed systems"
date: "June 12 2024"
draft: false
repoUrl: "https://github.com/LukasNiessen/distributed-systems-1"
xLink: "https://x.com/iamlukasniessen/status/1926532454401089572"
tags:
  - Scaling
  - Distributed System
---

# Single Computers vs Distributed Systems: Why Everything Gets Complicated

## The Predictable World of Single Computers

One machine is pretty straightforward. For example your laptop. When you run a program, it either works or it doesn't. In the sense if that if something goes wrong, the whole system usually crashes rather than giving you wrong answers. And by _going wrong_ I don't mean software bugs because the OS and the hardware just think this way intentional. I mean 'bugs' at hardware level.

And this is actually by design. Computers are built to fail rather than produce false results.

This deterministic behavior hides all the messy details of physical hardware. Your CPU might have tiny manufacturing defects, your RAM might have occasional bit flips, but the system handles these gracefully by either working correctly or failing completely.

## Distributed Systems

The moment you connect multiple computers over a network, everything changes. Now you're dealing with the messy reality of the physical world, and things get unpredictable fast.

Of course every node itself is still deterministic but there are many other issues. Such as that network cables fail, power goes out in one data center but not another, and that innocent-looking Ethernet switch might just decide to drop packets for no good reason. Suddenly you have **partial failures** - some parts of your system work while others don't, and you might not even know which is which.

This creates nondeterministic behavior. Did your database write succeed? Maybe. Is the user's payment processed? Who knows - the network timeout doesn't tell you if the transaction went through or not.

## Two Different Approaches to Handling This Mess

When you're building large-scale systems, you basically have two philosophical approaches to dealing with these inevitable failures.

### The HPC Approach: If Anything Breaks, Start Over

High-performance computing systems like supercomputers take the single-computer approach and scale it up. They use specialized, expensive, reliable hardware with fancy interconnects like shared memory and RDMA for lightning-fast communication.

When something goes wrong, they don't mess around with partial failures. Instead, they:

- Stop everything
- Roll back to the last checkpoint
- Restart the entire computation

It's like treating a 10,000-node supercomputer as one giant computer that either works or doesn't. This makes sense when you're running a weather simulation that can afford to restart, but it doesn't work so well for systems that need to stay online.

This approach is known as _vertical scaling_.

### The Cloud Approach: Keep Going No Matter What

Cloud computing takes the opposite approach. Instead of expensive, reliable hardware, cloud systems use cheap commodity machines that fail all the time. The assumption is that something is always breaking somewhere.

Rather than stopping everything when a node fails, cloud systems are designed to:

- Keep running even when parts fail
- Route around problems automatically
- Replace broken components without downtime
- Handle rolling updates and gradual replacements

This approach powers every internet service you use. When you're browsing Netflix, some server somewhere is probably crashing, but you never notice because the system just routes around the problem.

This approach is known as _horizontal scaling_.

### Traditional Enterprise: The Middle Ground

Most corporate data centers fall somewhere between these approaches, trying to balance reliability with cost. They're more reliable than cloud commodity hardware but less specialized than supercomputers.

## Why Cloud Systems Are So Much Harder to Build

Here's the thing about building fault-tolerant distributed systems: they're ridiculously complex.

**Scale makes everything worse.** A system with 1,000 nodes has way more failure modes than a system with 10 nodes. Components fail more often, network partitions happen regularly, and debugging becomes a nightmare.

**Cheap hardware fails constantly.** Cloud providers use commodity hardware because it's cost-effective, but that means higher failure rates. The system has to be smart enough to work around constant small failures.

**Network complexity explodes.** Instead of the specialized network topologies supercomputers use (like fancy meshes and toruses), cloud systems rely on IP/Ethernet with Clos network topologies to handle massive bandwidth needs.

But here's the counterintuitive part: you can actually build incredibly reliable systems from unreliable components. Think about it - TCP gives you reliable data transmission over the unreliable internet, and error-correcting codes let you store data reliably on imperfect storage devices.

## The Bottom Line for System Design

If you're building any kind of distributed system, you need to accept that partial failures will happen. There's no avoiding it.

Even small systems need to plan for faults because they will eventually occur. You can't just hope your two-server setup will never have problems - it will, and probably sooner than you think.

The key is building fault tolerance into your software design from the beginning. Test for weird failure scenarios, not just the obvious ones. Plan for network splits, slow nodes, and all the other fun surprises distributed systems throw at you.

Certainly an interesting read here is the Chaos Monkey of Netflix.
