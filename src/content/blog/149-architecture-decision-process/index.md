---
title: 'How to Make Architecture Decisions: RFCs, ADRs, and Getting Everyone Aligned'
summary: 'A practical guide to making software architecture decisions - from writing RFCs to running effective decision meetings to documenting with ADRs'
date: 'Jan 14 2026'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Architecture
  - Decision-Making
  - Team Collaboration
  - Process
---

# How to Make Architecture Decisions: RFCs, ADRs, and Getting Everyone Aligned

Making architecture decisions is one of those things that can go really well or really badly. I've been in both situations. I've seen decisions made in hallway conversations that caused months of rework. I've also seen beautifully documented decisions that nobody read, leading to the same outcome.

The thing is, architecture decisions are different from regular code decisions. They're harder to reverse, they affect more people, and they often involve trade-offs that aren't purely technical. You need buy-in. You need the right people in the room. And you need a process that doesn't turn into endless meetings or bikeshedding.

Here's the approach I've found works well, both in my consulting work and in teams I've led.

## The Core Process

The flow is straightforward:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │     │                 │
│   Write RFC     │────►│  Async Review   │────►│ Decision Meeting│────►│   Write ADR     │
│                 │     │  (Comments)     │     │                 │     │                 │
│                 │     │                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
      1-2 days              2-3 days               30-60 min              Same day
```

**RFC (Request for Comments):** A document that explains the problem, perhaps proposes solutions, and invites feedback. This is the async preparation phase.

**Decision Meeting:** A focused synchronous discussion where you make the actual decision. Everyone has already read the RFC and comments.

**ADR (Architecture Decision Record):** The final documentation of what was decided and why. This becomes part of your permanent record.

Let's break down each step.

## Step 1: Write the RFC

The RFC is where you do the heavy lifting. It forces you to think through the problem properly before bringing others in. Don't skip this step - jumping straight to a meeting is how you get 2-hour discussions that go in circles.

### Where to Put It

Confluence works well. So does Notion, Google Docs, or even a Markdown file in a dedicated repo. The key is that it's somewhere everyone can access, comment on, and reference later. Pick a consistent location - you want people to know where to find RFCs without hunting.

I recommend creating a dedicated space or folder like `/Architecture/RFCs/` with a naming convention:

```
RFC-2026-001-Event-Driven-Architecture
RFC-2026-002-Database-Sharding-Strategy
RFC-2026-003-Authentication-Provider-Migration
```

### RFC Structure

Here's an example template:

```markdown
# RFC: [Title]

**Author:** [Your name]
**Date:** [Date]
**Status:** Draft | Under Review | Decided | Superseded
**Decision Deadline:** [Date - usually 3-5 days from creation]

## Summary
One paragraph. What is this about and why are we discussing it?

## Context
What's the current situation? What problem are we solving?
Why now? Include relevant constraints, requirements, and background.

## Priorities and Requirements (Ranked)

This is the most important part. List what actually matters for this decision, in order of importance. Be specific and quantifiable where possible.

1. **[Priority name]** - [Why this matters. What's the business or technical reason?]
2. **[Priority name]** - [Why this matters?]
3. **[Priority name]** - [Why this matters?]

Example:
1. **Cost** - We're operating at thin margins; any infrastructure cost increase directly impacts profitability
2. **Development velocity** - Our roadmap depends on shipping three features this quarter
3. **Operational complexity** - We have a small ops team; anything complex will create bottlenecks

Note: People often disagree on decisions because they're weighing priorities differently. Making priorities explicit is where the real decision-making happens.

## Proposed Solutions

### Option A: [Name]

Description of the approach.

**How this performs against priorities:**
- **Cost:** [How does this affect cost? High/Medium/Low impact and direction]
- **Development velocity:** [How does this affect velocity?]
- **Operational complexity:** [How does this affect ops complexity?]

**Estimated effort:** X weeks/months
**Risk level:** Low/Medium/High
**Other trade-offs:** [Anything else worth noting]

### Option B: [Name]
...

### Option C: Do Nothing
Often you should include this option. Sometimes the answer is "not now".

## Recommendation
Which option do you recommend and why? Focus on how it aligns with the priorities you outlined above.

## Stakeholders
Who needs to be involved in this decision? Tag them.
- @backend-team (affected by implementation)
- @security-team (compliance implications)
- @product-owner (timeline impact)
- @infrastructure (operational concerns)

## Open Questions
What do you still need input on?

## Timeline
When does this decision need to be made? What's driving that deadline?
```

### Why Priorities Trump Pros/Cons Lists

You might notice this template doesn't use "pros" and "cons" lists. That's intentional.

A pros/cons list tells you *what* varies between options, but not *whether it matters*:

```
Option A
Pros: Fast, Scalable
Cons: No access management
```

This is almost useless unless everyone agrees on priority. Does speed matter more than access management? You don't know. Different people will read this and come to different conclusions. The loud voices in the meeting will win, not the best decision.

The better approach: **Make your priorities explicit first, then evaluate options against them.** Now the same information tells a clear story:

```
Priorities:
1. Must support access management (business requirement)
2. Performance under 500ms (SLA requirement)

Option A: Fast, Scalable, but no access management
→ Fails priority #1. Ruled out.

Option B: Slower but supports access management
→ Meets priority #1, still hits the 500ms target
→ Recommended
```

When priorities are ranked and clear, the decision often becomes obvious. And when people disagree, you're debating what *actually matters*, not arguing over vague trade-offs. This is where real consensus-building happens.

### Tagging the Right People

This is important. Tag everyone who:

1. **Will be affected** by the decision (they need to know)
2. **Has relevant expertise** (they can improve the decision)
3. **Has authority** over the affected area (they need to approve)
4. **Will implement it** (they'll spot practical issues)

Don't tag the entire company. Be specific. In the notification or message, tell them explicitly: "Please read this RFC and leave your comments by [date]. We'll have a decision meeting on [date]."

Be clear about what you need from them. Not everyone needs to deeply analyze every option - some people just need to flag if there's a blocker from their perspective.

## Step 2: Async Review Period

Give people 2-3 days to read and comment. This is where the magic happens. Async comments let people think before responding. They can do research. They can sleep on it. This produces much better feedback than putting people on the spot in a meeting.

### What Good Comments Look Like

Encourage people to:

- **Ask clarifying questions** - "How would this handle X scenario?"
- **Raise concerns** - "This might conflict with Y initiative"
- **Provide additional context** - "We tried something similar before and hit Z issue"
- **Express preferences** - "I lean toward Option B because..."
- **Suggest alternatives** - "Have we considered W approach?"

### Reply to Comments

As the RFC author, actively engage with comments. Answer questions, acknowledge concerns, update the RFC if someone raises a valid point you missed. This builds consensus before the meeting.

### What If Nobody Comments?

This happens. A few things could be going on:

1. **The decision isn't important enough** - Maybe this doesn't need a formal process. Just decide.
2. **People are too busy** - Ping individuals directly. "Hey, I really need your input on Section 3."
3. **It's too long/complex** - Simplify. Add a TL;DR at the top.
4. **People agree but are silent** - Explicitly ask for "+1 if you're okay with the recommendation"

## Step 3: The Decision Meeting

Now comes the synchronous part. But here's the key: **this is NOT a presentation meeting**. Everyone should have already read the RFC and the comments. If they haven't, that's on them.

### Meeting Format

I recommend a **Working Session** format rather than a presentation:

**Duration:** 30-60 minutes (not more)

**Agenda:**
1. **Quick context** (2 min) - "We're here to decide X. Everyone's read the RFC".
2. **Address open questions** (10-15 min) - Go through unresolved comments and open questions from the RFC
3. **Discussion** (15-30 min) - Debate the options, raise new concerns
4. **Decision** (5-10 min) - Make the call

**Who should be there:**
- The RFC author (runs the meeting)
- Key stakeholders who commented
- The decision maker (if that's not you)

Keep the group small. 5-8 people max. Large meetings turn into status updates, not decision forums.

### Decision-Making Methods

How do you actually make the decision? A few approaches:

**Consensus:** Everyone agrees. Ideal but not always realistic.

**Consent:** Nobody has strong objections. Different from consensus - you're asking "can you live with this?" not "is this your favorite?"

**RAPID/DRI:** One person (the Directly Responsible Individual) makes the final call after hearing input. This is often best for architecture decisions where someone needs to own the outcome.

**Voting:** Can work for minor decisions but tends to create winners and losers. Use sparingly.

### What If You Can't Agree?

This happens. Some options:

**Escalate:** If there's a clear owner or manager above the group, they can break the tie. This isn't a failure - it's what leadership is for.

**Time-box:** "Let's try Option A for 3 months and revisit." Not everything needs to be decided forever.

**Do more research:** If the disagreement is factual ("will this scale?"), maybe you need a spike or proof of concept before deciding.

**Smaller scope:** Sometimes you can agree on a subset. "We disagree on the long-term approach, but we agree on the first step."

**Acknowledge trade-offs:** Sometimes people disagree because they're weighing trade-offs differently. Make those explicit. "You're prioritizing speed, I'm prioritizing maintainability. Let's figure out which matters more for this specific situation."

Don't let disagreement fester. Unresolved architecture decisions turn into technical debt as people implement different approaches in parallel.

## Step 4: Write the ADR

Once you've decided, document it. The Architecture Decision Record (ADR) is your permanent record. It's different from the RFC - the RFC was about exploring options, the ADR is about recording what was decided.

### ADR Template

```markdown
# ADR-[number]: [Title]

**Date:** [Date]
**Status:** Accepted | Deprecated | Superseded by ADR-XXX

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?

## Alternatives Considered
Brief summary of options that were rejected and why.
```

IMO, you should keep ADRs short. They're reference documents, not essays. Link back to the RFC if people want the full context. However, that's up to you and your organization, every team writes ADRs a little different.

## Step 5: Rollout and Checkpoints

Making the decision is only half the battle. Ideally an RFC should include a concrete rollout plan - not just "we'll implement this" but a clear path from current state to the desired outcome.

### Why Rollout Plans Matter

Many architecture decisions fail not because the decision was wrong, but because the implementation path was unclear or too ambitious. People push back on "massive paradigm shifts" not because they disagree with the direction, but because they can't see how to get there incrementally.

A rollout plan lets you:
- **Break large changes into manageable steps** - "Week 1-2 we set up the new infrastructure, week 3-4 we migrate 10% of traffic..."
- **Identify blockers early** - "Oh, we can't do phase 2 without fixing that legacy API first"
- **Reduce risk** - By rolling out in stages, you catch problems before they affect everything
- **Maintain momentum** - Teams can start making progress even on large decisions

### What a Good Rollout Plan Includes

**Phases:** Break the work into clear, time-bound phases. Each phase should be completable and somewhat independent.

```
Phase 1 (Weeks 1-2): Setup and experimentation
- Set up new database infrastructure
- Run performance benchmarks
- Checkpoint: Confirm performance meets requirements before proceeding

Phase 2 (Weeks 3-5): Pilot with internal services
- Migrate auth service to new system
- Run in production with monitoring
- Checkpoint: No incidents, performance stable before expanding

Phase 3 (Weeks 6-8): Gradual customer rollout
- Route 5% of traffic to new system
- Monitor error rates and latency
- Checkpoint: All metrics nominal before increasing traffic

Phase 4 (Weeks 9-10): Full migration
- Route 100% of traffic to new system
- Monitor for one week
- Deprecate old system

Phase 5 (Week 11): Cleanup
- Remove old system code
- Document learnings
```

**Checkpoints:** Explicit decision points where you evaluate how things are going. At each checkpoint, you should have clear success criteria:

- "Error rate stays below 0.1%"
- "P99 latency under 200ms"
- "No critical security issues found"
- "Team velocity doesn't drop below 60% of baseline"

If a checkpoint fails, you decide: Do we fix it and continue? Do we roll back? Do we adjust the plan?

**Fallback plan:** If something goes wrong during rollout, what's the exit strategy? Can you quickly roll back? How long would a rollback take? This builds confidence in the plan.

**Resource needs:** Be specific about what you need for each phase - people, infrastructure, time from other teams.

### Who Writes the Rollout Plan?

The RFC author should draft it, but the people who'll actually implement it (the team leads, architects, tech leads) should refine it. They'll spot what's realistic and what's not.

Include the rollout plan in the RFC. It's part of the decision - not a separate implementation detail. This is often where the most important feedback comes from.

## When Stakeholders Need to Be Involved

Not every architecture decision needs this full process. Here's a rough guide:

**Just decide (no RFC needed):**
- Affects only your team
- Easily reversible
- Low cost to change later

**Lightweight RFC (async only, maybe no meeting):**
- Affects 2-3 teams
- Medium impact
- Someone might have concerns

**Full process (RFC + meeting + stakeholders):**
- Cross-cutting concerns (security, performance, cost)
- Hard to reverse (database choices, API contracts)
- Significant investment
- Requires budget or headcount

**Executive involvement:**
- Affects company strategy
- Large budget implications
- External vendor commitments
- Compliance or legal implications

For the big decisions, you might need to present a summary to leadership. That's different from the technical decision meeting - it's about getting approval and resources, not debating technical trade-offs.

### AI-Assistance

LLMs are actually useful for RFC preparation. You can use them to:
- Research trade-offs between technologies
- Generate initial drafts of pros/cons lists
- Summarize documentation for technologies you're evaluating
- Identify edge cases you might have missed

The point being though is NOT to let an LLM write the entire RFC for you and you just publish it, but rather to use an LLM as an immediate thought partner.

## Common Pitfalls

A few things I've seen go wrong:

**Analysis paralysis:** The RFC process becomes an excuse to never decide. Set deadlines and stick to them. "We'll decide on Friday with the information we have".

**Too many stakeholders:** Everyone has an opinion, nothing gets decided. Be explicit about who has input vs. who has decision authority.

**No follow-through:** You make the decision but don't write the ADR. Six months later, nobody remembers why. Write the ADR the same day as the decision meeting.

**Ignoring the quiet people:** In meetings, loud voices dominate. The async comment period is where quieter team members can contribute. Value those comments.

## Wrapping Up

This is the process that I've found to work best while not taking up a lot of time. And it really isn't complicated:

1. Write an RFC with clear options and trade-offs
2. Give people time to read and comment async
3. Have a focused meeting to make the decision
4. Document it in an ADR

How detailed you make the RFC, the meeting, the ADR, and also how long the deadlines are, is really something that depends on your team. The good thing is, it works with both, a lot of detail and formalities, and quick low bureaucracy startup style.
