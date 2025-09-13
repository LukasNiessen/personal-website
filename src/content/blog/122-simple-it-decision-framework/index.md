---
title: "The DRAGON Framework, aka TOGAF light: Simple IT Decision Framework"
summary: "A simple framework for IT decisions. 6 buckets to consider: financials, timeline, risks, synergies, change management, and other stuff. Nothing revolutionary, just structured thinking."
date: "July 7 2025"
draft: false
xLink: ""
linkedInLink: ""
tags:
  - decision-making
  - IT strategy
  - frameworks
  - business
---

# The DRAGON Framework (TDF): Simple IT Decision Framework

"Make or buy?" "Should we migrate to microservices?" "Do we need Kubernetes?" "Which database should we pick?"

We make IT decisions all the time. I've been in plenty of situations where we picked the shiny new tech, only to realize 6 months later that we didn't think about the migration costs. Or we chose the "enterprise solution" without considering if our team can actually maintain it.

So here's a simple framework I use. It's a **lightweight framework**, lightweight but highly effective. It's inspired by consulting frameworks (MCK, BCG etc.) but focused on the stuff that actually matters in IT.

## The 6 Buckets

```
    IT Decision Framework (Dragon Framework)
    
    ┌─────────────┐
    │             │
    │             │──── Revenue
    │ FINANCIALS  │
    │             │──── Costs ──── One-time
    │             │           └─── Ongoing
    └─────────────┘
    
    ┌─────────────┐
    │             │
    │  TIMELINE   │
    │             │
    └─────────────┘
    
    ┌─────────────┐
    │             │──── Success Risk
    │             │
    │   RISKS &   │──── Vendor Risk
    │ CONSTRAINTS │
    │             │──── Compliance
    │             │
    │             │──── Security
    └─────────────┘
    
    ┌─────────────┐
    │             │──── Current
    │ SYNERGIES & │
    │ CONFLICTS   │──── Future
    │             │
    └─────────────┘
    
    ┌─────────────┐
    │             │
    │   CHANGE    │
    │ MANAGEMENT  │
    │             │
    └─────────────┘
    
    ┌─────────────┐
    │             │
    │    OTHER    │
    │             │
    └─────────────┘
```

## 1. Financials

**Revenue:**
- Whatever makes up the revenue, `price x volume`, subscriptions, ...

**Cost side:**
- One-time costs: implementation, consulting, licenses, hardware
- Ongoing costs:
  - Fixed: maintenance contracts, base licensing, dedicated team members
  - Variable: usage-based fees, scaling costs, per-user licenses

Always remeber that costs include people time. If your senior dev spends 3 months implementing something, that's not free, even if you don't pay external consultants. So that will also include topics like the Mythical Man-Month.

## 2. Timeline

- How long will this take?
- When do we actually need this?

Keep in mind things like time-to-market here.

## 3. Risks & Constraints

**Success risk:** Will this actually work? Do we have the skills? Is the technology mature enough? I've seen teams pick cutting-edge tech only to discover it's not production-ready.

**Vendor risk:** What happens if the vendor goes out of business? Gets acquired? Changes their pricing model? Starts limiting features? 

**Compliance:** Legal requirements (GDPR, HIPAA), company standards, industry regulations.

**Security:** New attack vectors, data exposure, access control complexity. Don't just think about the happy path.

**More:** There can be a lot of risks and constraints, add here everything that fits.

## 4. Synergies & Conflicts

How does this decision fit with everything else you're doing?

**Current state:** Does this integrate well with existing systems? Do you have the right team skills? Will this conflict with other ongoing projects?

**Future roadmap:** Are you planning to replace this system anyway? Does this align with your architectural direction? Do we have similar things on our roadmap?

I've heard enough stories of teams implement a new authentication system just 6 months before migrating to a platform that included auth. Wasted effort. On the other hand, if you have similar IAM topics on your roadmap that align well, then this is a good synergy.

## 5. Change Management

Don't neglect this one.

- Will users adopt this? (If it makes their life harder, they won't)
- Will things change in the team? If so, how will the team react to it?
- How much training is needed?
- What processes need to change?

## 6. Other

Every decision has unique context.

## Notes

We can calculate RoI, TOC, Break-even Point etc with this info. It covers all other most important deciding points for IT projects or decision. Also note that this doesn't cover documentation, which, of course, does not mean it's irrelevant. It's of course highly relevant to document your outcome, for example in an ADR or on Confluence.

And of course, don't listen to the Junior dev saying he can pop out that one feature in 2 days. Always multiply the initial time estimates by π (3.1415926) ;)

## Conclusion

There are many other frameworks in the IT already, including widely accepted ones like TOGAF. The DRAGON Framework is unique in its compactness but still completeness. It's ideal for making a decision that will not impact the entire 50 Billion enterprise (use TOGAF here) but rather one that is limited to a certain project or team.

Also, it does wonders to use a lightweight framework (NOT TOGAF) for conflict resolution. You have a conflict in your team regarding an IT decision? Put a meeting in their calenders, meet tomorrow, use a whiteboard and go through the alternatives using The DRAGON Framework. Hear everyone out, always focus on business outcomes, and find an agreement :)