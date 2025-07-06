---
title: 'Data related Non-Functional Requirements'
summary: 'Walk through of the most important Non-Functional Requirements that are data related.'
date: 'May 16 2025'
draft: false
repoUrl: 'https://github.com/LukasNiessen/tdd-bdd-explained'
xLink: 'https://x.com/iamlukasniessen/status/1923444639769432570'
linkedInLink: 'https://www.linkedin.com/pulse/data-related-non-functional-requirements-lukas-nie%25C3%259Fen-hvkae/'
tags:
  - Reliability
  - Scalibility
  - Maintainibility
  - Requirements
---

# Data related Non-Functional Requirements

Brief reminder:

- Functional requirements = what the system should do
- Non-functional requirements = how the system should behave

Usually applications handle complex datasets and need to:

- Store data efficiently in databases
- Cache expensive operation results
- Provide search and filtering capabilities
- Process messages asynchronously
- and more.

Suppose you have a banking website. Would you rather show wrong numbers to your customers or show no data at all? Rather show no data. However, if you're Facebook, you would of course rather show wrong data (not-updated likes count for example) than no data.

So non-functional requirements matter. Here I want to walk through the most important ones. However, I will only discuss on data related ones.

## Reliability

Reliability simply means "continuing to work correctly, even when things go wrong."

A reliable system:

- Performs its function as expected,
- Tolerates user mistakes or other mistakes.

Important distinction here: faults vs failures. A **fault** is when one component doesn't work or works incorrectly, while a **failure** is when the entire system stops working. We clearly want to focus on dealing with faults and prevent faults from causing failures.

### Hardware Faults

Hardware faults will always occur. A disk will die after about 10-50 years (this is the Mean Time To Failure, or MTTF), someone can trips over a cable, power outages, and so on. In fact, in large data centers, disk failures happen daily.

So we use redundancy. For example, instead of one disk, we use 4 disks for example (you can use RAID to combine them). Or instead of one computer at one location, we have 5 computers at 5 locations. When one is down, a different one takes over.

This, by the way, has another advantage: rolling updates. With only one machine your website is down when you make updates, like a security patch at 4 am. With multiple machines, you update them one after another, and your website stays online the entire time.

While it used to be enough to have redundancy on one machine, for example by combining disks using RAID, that is no longer the case for most applications. Cloud computing like AWS, Azure or GCP also play into this trend: it's common for machines you're code is running on to become unavailable, this is because AWS and the like are e designed to prioritize flexibility and elasticity. You will get a different machine instead.

### Software Errors

Also impossible to prevent. Developers make mistakes (ChatGPT & co even more). So we need good Quality Assurance (QA), including unit tests, integration tests, perhaps E2E tests, we need good monitoring, and more. But these errors will happen anyway.

### Human Errors

Humans do mistakes. There are studies showing that human error causes more outages than hardware failures actually. While this again is impossible to prevent, we generally want to:

- Design interfaces that make the right action obvious and wrong actions hard
- Detailed monitoring
- Enabling quick recovery (rollbacks, gradual deployment, data recomputation tools).

So we really want our system to be reliable.

## Scalability

Scalability is how well your system handles increased load. To understand it, you need to:

1. Define your load parameters (requests per second, read/write ratio, etc.)
2. Measure performance under different loads
3. Implement solutions that maintain performance as load increases

### Performance

This is another obvious one. Let's look at some metrics.

**Throughput:** The number of operations your system can handle per unit of time.

**Latency and Response Time:** Note, they are not the same:

- **Latency:** The time it takes a request to reach its destination
- **Response Time:** The total time for a request to be processed and returned (includes latency plus processing time)

Response times are important. But when measuring them, it's important to mote are never constant. They vary for each request. We could take the average response time but that's not enough. We need to look the higher percentiles (that is the very high or very low response times).

An example from Amazon makes very clear why. They found that a 100ms increase in response time reduces sales by 1%. Now they obviously don't want that, there is another reason why high percentiles are very important to them. The users with the worst response times were usually their best customers. That's because they have a long purchase history, slowing things down internally for actions related their account. But these users are the ones that bring the most money, so they really want to keep them happy.

## Maintainability

In many projects, it's more costly to keep things running than to initially develop them. Think of big legacy code systems for example. These systems are difficult to maintain.

Maintainability has many aspects, here are a three important ones.

**Operable:** Good operability means it's easy to keep the system running. Making the ops teams life easy. Some of their tasks are the following:

- Managing deployments and configurations,
- Monitoring system health and fixing issues,
- Debugging problems,
- Keeping software and platforms patched and up-to-date,
- Capacity planning,
- Complex maintenance tasks (like platform migrations),
- and more.

**Simple:** Complex systems harder to understand, modify, and maintain.

**Evolvable:** Systems should be easy to modify as requirements change. This requires good abstractions, clean interfaces, and proper separation of concerns.

## Others

### ACID

Often you want ACID (Availability, Consistency, Isolation and Durability). This usually comes at a tradeoff though and is a topic for a separate article.

## Elasticity

The ability to handle to handle bursts of requests. For example, during the Jake Paul vs Mike Tyson fight, the Netflix servers couldn't handle the traffic. While Netflix is very scalable, they couldn't handle this particular bursts of requests. They had _'bad elasticity'_ in this case.

### Speed to Market

In technology, speed to market often determines success. Some data teams deliberate on technology choices for months without making decisions, which can be fatal for success.

Best practices include:

- Delivering value early and often
- Using tools your team already knows when possible
- Avoiding undifferentiated heavy lifting that adds little value
- Selecting tools that enable quick, reliable, safe, and secure development

### Interoperability

It's rare to use only one technology or system. Interoperability describes how various technologies connect, exchange information, and interact. When evaluating technologies, consider:

How easily does technology A integrate with technology B?
Is seamless integration already built into each product?
How much manual configuration is needed?

### And many more...

## Balancing Trade-offs

You will always have tradeoffs. For example:

- Higher reliability typically means higher costs
- Faster time to market might compromise long-term maintainability
- Better interoperability might require more standardized (but less optimized) approaches
- Lower initial costs might lead to higher long-term costs

Remember the first law of software architecture:

> Everything in software architecture is a trade-off.
