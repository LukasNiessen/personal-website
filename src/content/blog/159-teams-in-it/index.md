---
title: "Teams in IT: How to Structure, Scale and Not Lose Your Mind"
summary: "How team structures shape the software you build, why Conway's Law still matters, and what strong ownership, platform teams and autonomy actually look like in practice"
date: "Feb 21 2026"
tags:
  - IT
  - Teams
  - Architecture
  - Organization
---

# Teams in IT: How to Structure, Scale and Not Lose Your Mind

Most technical discussions about software architecture completely ignore the people building it. We talk about microservices, monoliths, event-driven systems - but rarely about the teams behind them. That's a mistake. Because the way you organize your teams has a direct, measurable impact on the software they produce.

This article is about teams in IT. How to structure them, how they relate to your architecture, what ownership models exist, and why getting this wrong can silently undermine everything else you're doing.

## Conway's Law

Let's start with the most important concept. In 1968, Melvin Conway observed:

> Any organization that designs a system will inevitably produce a design whose structure is a copy of the organization's communication structure.

This is known as Conway's Law. And it's one of those things that, once you see it, you can't unsee. If you have four teams working on a backend, you'll end up with four backend services. If your frontend and backend teams barely talk, you'll get an API that feels like it was designed by two groups that barely talk. Because it was.

Eric Raymond put it more bluntly: "If you have four groups working on a compiler, you'll get a 4-pass compiler."

But what does "loosely coupled organization" actually mean? Basically, it's an organization where teams can operate independently without constantly needing approval, coordination, or input from other teams. They can make decisions locally, deploy on their own schedule, and change their systems without creating ripple effects across the company. The opposite - a tightly coupled organization - is one where every change requires meetings, sign-offs, and coordination across multiple groups.

There's solid evidence that this matters. A study called "Exploring the Duality Between Product and Organizational Architectures" looked at software built by loosely coupled organizations (think: distributed open source communities) versus tightly coupled ones (think: colocated commercial teams). The loosely coupled organizations produced more modular, less coupled systems. The tightly coupled ones produced tighter, more intertwined code. Microsoft found something similar when analyzing Windows Vista - organizational metrics like "how many engineers touched this code" were better predictors of bugs than traditional code complexity metrics.

The takeaway is straightforward: a loosely coupled organization tends to produce loosely coupled software. And vice versa. So if you want a modular microservice architecture but your org chart looks like a monolith, good luck.

## Small Teams

Ask any developer about ideal team size and you'll get answers somewhere between 5 and 10. Amazon famously formalized this with its "two-pizza teams" - no team should be so big that it can't be fed by two pizzas. Whether that's lunch or dinner pizzas and how big those pizzas are, nobody really specified. But the general idea holds: somewhere around 8-10 people.

Research backs this up. A study called "Empirical Findings on Team Size and Productivity in Software Development" found that productivity is worst for teams of 9 or more people. Not exactly surprising. With a small group of people focused on the same outcomes, it's easier to stay aligned and easier to coordinate.

But here's the thing. If you can do all your work with a single small team, great. Your world is simple. The problems start when you have more work than one team can handle. The obvious reaction is to add people. And this is where it gets interesting.

## The Mythical Man-Month (Again)

Fred Brooks said it decades ago: "Adding manpower to a late software project makes it later." The reasoning is simple. For you to throw more people at a problem, the work needs to be split into tasks that can be done in parallel. If developer A is waiting on developer B, the work is sequential - more people won't help. Even when work _can_ be parallelized, there's coordination overhead. The more intertwined the work, the less effective it is to add people.

And worse, onboarding new people takes time. The developers who are already overloaded are often the same people who need to help the new ones get up to speed.

The biggest cost to working efficiently at scale is coordination. The more coordination between teams, the slower you go. Amazon understood this early. From "Think Like Amazon" by ex-Amazon executive John Rossman:

> The Two-Pizza Team is autonomous. Interaction with other teams is limited, and when it does occur, it is well documented, and interfaces are clearly defined. One of the primary goals is to lower the communications overhead in organizations.

So the trick is to create large organizations out of smaller, autonomous teams.

## Autonomy

Having lots of small teams doesn't help if they're just smaller silos still dependent on each other for everything. Autonomy is what makes small teams actually work.

The book "Accelerate" by Forsgren, Humble and Kim looked at what characteristics matter most for high-performing teams. Their checklist:

- Can make large-scale changes to their system without permission from outside the team
- Can make changes without depending on other teams to modify their systems
- Can complete work without constantly coordinating with people outside the team
- Can deploy and release on demand, regardless of other services
- Can do most testing on demand, without needing an integrated test environment
- Can deploy during normal business hours with negligible downtime

That's a pretty high bar. But it's a useful checklist for evaluating how autonomous your teams really are.

The key insight: autonomy isn't just about making people feel good. It directly impacts delivery speed. Centralized decision making gets slower as the organization grows. The bigger the company, the worse it gets. So if you want to scale and still move fast, you need to distribute responsibility.

## Ownership Models

There are two main ownership models for services: strong ownership and collective ownership.

### Strong Ownership

One team owns a service. That team decides what changes to make. If another team wants something changed, it either asks the owning team or submits a pull request - and it's entirely up to the owning team whether to accept it. The team controls coding standards, deployment, technology choices, and more.

Strong ownership optimizes for autonomy. The team can move fast because it doesn't need to coordinate with others on most decisions. It also allows for local variation - one team can use a functional style of Java while another uses something completely different, as long as the interfaces between services stay compatible.

Taken further, some organizations adopt **full life-cycle ownership**: a single team designs, builds, deploys, operates and eventually decommissions the service. No tickets to an ops team, no external sign-offs. This is the model Amazon is famous for. It's hard to get there, and it can take years, but each step in that direction increases autonomy.

### Collective Ownership

Any team can change any service. The benefit is flexibility - you can move people where the bottleneck is. If there's a huge backlog of changes in the Payment service, just assign more people. In theory.

The problem is that collective ownership requires a high degree of consistency. You can't have a broad range of technology choices or different deployment models if developers are expected to work on a different service each week. This consistency requirement directly undermines one of the key benefits of microservices: the freedom to choose the right tool for the job.

Collective ownership also requires much more coordination. And as we've discussed, more coordination means more coupling, which leads to more coupled system designs.

**For small teams or a single team, collective ownership is fine.** But as you grow, the coordination overhead becomes a real drag on the benefits of microservices.

### The Balance

Ultimately, the more you lean toward collective ownership, the more global consistency you need. The more you lean toward strong ownership, the more room there is for local optimization. Most organizations that get the most out of microservices are constantly trying to push toward more local optimization - while still maintaining some global standards where it matters, like API protocols or security requirements.

## Platform Teams

If you keep pushing responsibility into stream-aligned teams - own your deployments, manage your infrastructure, handle your monitoring - at some point you're just piling work onto people. This is where the platform comes in.

A platform team builds and maintains the shared tooling that allows other teams to be autonomous. Think: self-service deployment, log aggregation, service meshes, shared authentication. The goal is to make the common things easy so teams can focus on delivering features instead of fighting infrastructure.

A good platform team operates like an internal product team. Its users are the other developers. It should be going out to understand their problems, collecting feedback, iterating. Paul Ingles from RVU put it well - they never mandated the use of their platform. Instead, they set OKRs around adoption: how many teams onboarded, how many apps used autoscaling, what proportion of traffic ran through the platform. By making the platform optional, they forced themselves to make it genuinely useful.

This ties into the concept of the **paved road**. You clearly communicate how things should be done, then make it easy to do them that way. Want mutual TLS between services? Provide a framework that does it automatically. Teams _can_ go off-road and implement it differently - but the paved road should be the path of least resistance.

The alternative - governing via the platform by mandating its use - usually backfires. If the platform isn't easy to use or doesn't fit a use case, people will find ways around it. And then they're operating without any of the guardrails you actually cared about.

## Enabling Teams and Communities of Practice

Not everything is solved by platforms. Sometimes what teams need isn't tooling but knowledge, patterns, or a second pair of eyes.

**Enabling teams** work across multiple stream-aligned teams to help with cross-cutting concerns. Think: a UX enabling team that helps all product teams build consistent user experiences. Or a small architecture group that surveys the landscape, spots trends, connects people, and acts as a sounding board. The modern architect isn't someone who tells people what to do - they're an enabling function, helping teams make better decisions.

**Communities of Practice (CoPs)** are cross-cutting groups focused on learning and sharing between peers. Less formal than enabling teams - members participate a few hours a week at most, membership is fluid. A Kubernetes CoP might share war stories about the dev cluster, which then gives the platform team valuable input on what to fix.

Both structures give you visibility into what's happening across teams - which is essential for knowing when to rebalance global versus local optimization.

## The Internal Open Source Model

What happens when a service owned by one team needs changes from many other teams? One approach is internal open source.

Just like in regular open source: the owning team acts as core committers. Other teams can submit pull requests, but the core team decides what gets merged. The owning team is still in charge, still responsible for quality and consistency.

This works well for mature, stable services. It doesn't work as well for services still under heavy development, where the team doesn't yet know what "good" looks like. Most open source projects don't take outside contributions until the first version is solid. Same logic applies internally.

The cost is real though. Being a good gatekeeper takes time. Reviewing patches, communicating with submitters, maintaining consistency - this is work that the core team can't spend on other things. You have to decide if the overhead is worth it.

## Conway's Law in Reverse

Here's something interesting. Conway's Law usually gets discussed as "org structure shapes architecture." But it works the other way too.

Consider a company that started as a print business with a small website. The website had three parts: an input system, a core processing system, and an output system. As the print business shrank and digital grew, the company's organizational structure grew _around_ that three-part system architecture. Three divisions formed, each aligned with one of the three parts. The system design shaped the organization, not the other way around.

This matters because when you want to change an architecture that has shaped the org around it, you'll likely need to change the org too. The architecture has organizational gravity.

## What Actually Matters

If I had to boil it down:

1. **Your org structure and your architecture will mirror each other** - fight this at your peril
2. **Small, autonomous teams with strong ownership** deliver the best outcomes at scale
3. **Coordination is the enemy** - every dependency between teams slows you down
4. **Platforms should make the right thing easy**, not make the wrong thing impossible
5. **There's no perfect model to copy** - learn from Amazon, Netflix, Spotify, but understand _why_ they do what they do before copying it

The technical decisions are the easy part. Getting the people and team structures right is where the real challenge is.
