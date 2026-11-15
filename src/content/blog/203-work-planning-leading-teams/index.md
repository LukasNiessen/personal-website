---
title: "The Tenin Playbook: How to Lead a Team"
summary: "My practical playbook for leading a team: roadmap, RAID, ownership, and expectations. Keep these four in shape, from planning the work to delivering it."
date: "Nov 15 2026"
tags:
  - Leadership
  - Management
  - Project Management
  - Team Collaboration
  - Planning
---

# The Tenin Playbook: How to Lead a Team

The only thing more important than managing delivery is managing expectations. That's how I think about leading a team.

Suppose someone delivers a good prototype on Friday. The developer expected feedback before building the production version. The stakeholder expected something customers could use on Monday. The work may be good, but you still have a problem. Those expectations should have been aligned much earlier.

The same applies within the team. People need to know what they own, what they're expected to deliver, what they can decide independently, and when they need to involve someone else. Making that clear, and keeping it clear as things change, is a large part of your job.

I call this the **Tenin Playbook** (from Arabic *tinnīn*, ["dragon"](https://www.lisaanmasry.org/online/dictionary.php?coll=1&language=EN&rowid=2945&ui=)), inspired by an Arab friend. It's my take on standard management practices: the better you execute, the more fire you bring as you fly toward your goal.

## Start with discovery

At the start of a project, you often don't yet know what needs to be built. First comes discovery: which topics matter, what the workstreams might be, what each needs to clarify, and who you need to talk to.

Apply the same playbook here. Divide those questions into areas, give each an owner, and define what you want to learn. Put interviews and investigations into a discovery backlog, maintain a RAID log, and agree when to review the findings. For example, "By Friday, find out which teams need deployment support and what currently blocks them" is a clear discovery goal.

As the answers become clearer, use them to plan delivery. You don't need to resolve every unknown first; keep discovery work visible wherever more learning is needed. The playbook helps you organize both figuring out the work and carrying it out.

## First principles, briefly

A team needs a shared destination. Getting there costs time and money. People have different responsibilities and different information. And things change while you're working.

So you need direction, clear responsibility, a way to see what might prevent progress, and communication that keeps everyone aligned. I'd organize this into four things: **roadmap, RAID, ownership, and expectations.**

They're closely connected. A roadmap tells people what to expect next. Ownership tells them what to expect from each other. RAID helps you spot when those expectations need to change.

## 1. Roadmap: where are we going?

Start with the result you want and why it matters. "Build an internal platform" is too vague. "Let product teams deploy their services independently, with the required security controls" gives people something to work toward. Agree how you'll tell whether it helped.

I would keep four horizons visible:

| Horizon | What belongs here |
|---|---|
| **Short term: next 2–3 weeks** | Concrete results, priorities, owners, and upcoming checkpoints. For example, get one team through the deployment process. |
| **Medium term: next few months** | The next capabilities or outcomes, their order, and important dependencies. For example, support more teams and establish operational support. |
| **Long term: this year and perhaps next year** | Broader direction and major investments. Less detail, because more is uncertain. |
| **Vision** | What we're ultimately trying to make possible and why it's worth doing. This doesn't need a fixed time horizon. |

These can be views of the same roadmap. You don't need four separate documents.

Explain the connection between them. Why is this week's work useful for the next few months? How does that move us toward the vision? People should understand the reasoning well enough to make sensible decisions themselves.

Also distinguish a target from something you've actually committed to. If a stakeholder reads a rough idea for next year as a delivery promise, the roadmap has created the wrong expectation.

## 2. RAID: what could interfere with the plan?

A [RAID log](https://www.theirm.org/media/2517814/7-short-guide-raid.pdf) tracks **risks, assumptions, issues, and dependencies**. A shared table is enough to start.

- **Risk:** something that might go wrong. Our only platform specialist might be unavailable during the rollout.
- **Assumption:** something we're planning around but haven't verified. We assume the existing licenses cover the new teams.
- **Issue:** a problem that already exists. The test environment is currently unavailable.
- **Dependency:** something we need before we can proceed. The identity team must provide access before we test the integration.

Risks deserve particular attention because you can still do something before the problem happens. Consider likelihood and impact, and add a **mitigation** column: what will you do to reduce either? For the specialist risk, that might mean pairing with another engineer now.

For every significant entry, record an owner, the effect on delivery, the next action, and when you'll check again. Assumptions need verification. Issues need resolution. Dependencies need an agreement with the people you're relying on, including a date.

Review this regularly and act on it. If access is now expected a week late, update the affected work and communicate the effect on the roadmap. A RAID log that says "access might be delayed" for six weeks isn't helping anyone.

## 3. Ownership: who takes care of what?

Start at the topic level and map it to people. For example:

| Topic | Owner | What they take care of |
|---|---|---|
| Analytics | Ana | Metric definitions, measurement quality, and reporting. |
| Governance | Priya | The process for decisions, reviews, and required approvals. |
| Platform engineering | Ben | Implementation, reliability, and technical maintenance. |

Agree the assignment with each person. Check that they have the time, skills, and authority to take it on. If ownership is shared, explain how decisions are divided and who coordinates.

Ownership should stay flexible. If someone finishes their current work or gets blocked, they can support another workstream, take on additional ownership, or investigate an open question. Align the change with the people affected and update the ownership mapping where needed. Keep it clear who follows up on any unresolved blocker.

Topic ownership continues beyond a ticket. The analytics owner should notice that an important metric is unreliable and take action, even if nobody has created a ticket yet. That is part of owning the topic.

Where useful, assign each stakeholder relationship to someone on your team. That person owns keeping the stakeholder informed, aligning expectations, and following up on questions or decisions. Write down the mapping so everyone knows who takes care of whom.

### Turn topics into smaller pieces of work

"Own analytics" doesn't tell someone what to finish this week. Break the upcoming work into tickets that produce a result you can check. Keep them in an ordered backlog, with priorities that follow the roadmap.

A ticket can be this simple:

```text
Result: Show deployment success rate for the pilot team.
Owner: Ana, working with the platform engineer.
Acceptance: Agreed calculation, verified against sample deployments,
            visible to the pilot team, and documented.
Priority: Before broader reporting and dashboard polish.
Dependency: Access to deployment events.
Estimate: Small, subject to confirming data access.
```

Acceptance criteria say what this particular piece must satisfy. Agree common quality expectations too, such as review, testing, and documentation. Otherwise "done" means different things to different people.

If a ticket is too large to assess or demonstrate, split it. For example, measure one team's deployments before building reporting for every team. If the approach is unclear, create a short investigation with a specific question and a decision at the end.

Agree assignments with the people doing the work. Use T-shirt sizes, story points, or time estimates if they help you judge what fits. Estimates should come from the people who understand the work; they aren't guarantees.

You can organize delivery into sprints using [Scrum](https://scrumguides.org/scrum-guide.html), or work through a continuously ordered backlog. Either way, select work that fits actual capacity and check dependencies. When something urgent comes in, decide what moves out or gets delayed.

## 4. Expectations: make the agreement explicit

This is the most important part. "You own analytics" can mean very different things to two people.

When handing over responsibility, agree:

- **The result:** what should exist, by when, and what counts as good enough?
- **The autonomy:** what can you decide and change yourself?
- **The boundaries:** what requires alignment, and with whom?
- **The communication:** when and where do you update people, and what should the update contain?
- **The escalation:** what should you raise immediately instead of waiting for the next check-in?

For example:

> You own analytics for the pilot. By next Friday, we need the agreed metrics available and verified. Choose the implementation yourself within our existing tools. Align changes to metric definitions with the product lead, and check with me before adding paid tooling. Post progress, next steps, and blockers every Friday. If access problems threaten the review date, tell me as soon as you know.

Now the person can act. They know where they're free to move and where someone else needs to be involved. Ask whether the assignment is feasible and have them explain their intended approach. That often reveals misunderstandings before work starts.

Set expectations upward as well. Does the sponsor expect a demonstration or a production rollout? Which scope is agreed? Who accepts the result? What happens to support afterward? Clarify these before people build their own interpretation.

### Write down the agreements people need to remember

Keep a shared project overview with the roadmap, RAID, topic ownership, stakeholder map, and important working agreements. Link to the backlog instead of copying tickets into it.

Not every conversation needs documentation. But responsibilities, decision boundaries, delivery commitments, and changes to them are worth recording. People should be able to look them up without asking you.

Use a kickoff to walk through the plan and discuss it. Then check understanding with concrete questions: "What would you decide yourself here? When would you involve me?" Silence after a presentation doesn't tell you much.

### Give communication a regular rhythm

Here's a starting point to adapt to your team:

| When | What it should accomplish |
|---|---|
| **Daily, briefly or asynchronously** | Coordinate current work, surface blockers, and agree any immediate priority changes. |
| **Weekly planning and backlog review** | Check capacity, clarify upcoming tickets, and agree the next priorities. |
| **Weekly one-to-ones where useful** | Discuss support needs, unclear expectations, feedback, and concerns someone may not raise in the group. |
| **Every two weeks: review** | Inspect actual results with the relevant stakeholders and decide what follows. |
| **Weekly stakeholder update** | Explain progress, changed expectations, important risks, costs, and decisions needed. |

Make it clear who participates and what they prepare. Combine sessions when that makes sense. Occasionally use part of a team session to discuss how the work itself could improve.

The important thing is that people know when they'll hear from each other and what needs attention sooner. A blocker threatening Friday's delivery shouldn't wait for Friday's update.

## Keeping this in shape is part of the job

Many leads also do individual contributor work. You might design the architecture, write code, or solve difficult technical problems yourself. It's easy to spend the week on that while the backlog becomes unclear and three people wait for decisions.

You need to reserve capacity for leading. Agree that allocation with your own manager too. If your individual delivery commitments assume you're coding full-time, something has to change.

Block time around the team's routine. For example, thirty minutes before weekly planning to inspect the roadmap, backlog, and RAID; a short daily check for decisions people need from you; and time before the stakeholder update to check progress and costs. These are starting points. A complex project needs more.

Use that time to ask:

- Do the current priorities still match the roadmap?
- Is anyone blocked, overloaded, or unclear about their responsibility?
- What changed in the risks, dependencies, capacity, or costs?
- Which decision or expectation needs updating, and who needs to hear it?

Delegate document and backlog maintenance where appropriate. The topic owners should help keep their areas current. You still need enough overview to spot gaps between them and follow up on unresolved actions.

AI can be extremely useful for keeping these views in sync. Connect it to Jira and your planning documents through [MCP](https://developer.atlassian.com/cloud/rovo-mcp/) or authenticated APIs. It can help reflect ticket changes in your short-term swimlane roadmap and suggest corresponding RAID updates. A reusable skill can keep the formatting consistent.

This ongoing work is the baseline of the Tenin Playbook. Setting everything up once doesn't get you very far.

## Where you can really excel

The playbook gives you structure. How well you understand the people and the work determines how well you use it.

### Read people and adjust your support

Some people are ready to own a broad topic independently. Others need a smaller area, more frequent check-ins, or help thinking through an approach. The same person may need different support on an unfamiliar problem.

Notice when someone says "yes" but doesn't sound convinced. Ask what worries them and give them room to answer. Explain the support you're offering, then reduce it as their confidence and judgment grow. This is how you develop ownership without leaving someone to struggle silently.

Your response to bad news matters too. If raising a concern leads to blame, you'll hear concerns later. Address missed agreements directly, but first understand what happened.

### Communicate well across the organization

A strong communicator understands what the other person needs to decide. Engineers need implementation constraints. Executives usually need the consequence, options, cost, and your recommendation.

"We're blocked by another team" gives a sponsor little to act on. "Access is two weeks late. We can reduce the pilot scope or move the launch; I recommend reducing scope, and need your agreement by Wednesday" is useful.

Read the room, too. If two stakeholders disagree, find out whether they're debating facts, priorities, or who has authority. Those require different conversations. Talk to the relevant people before a large meeting when you can resolve concerns more effectively that way.

### Understand the work deeply

You can lead a technical team without deep technical expertise. But if you have it, you can be much better at the job.

You'll recognize hidden dependencies, ask better questions about estimates, and see when a supposedly small change affects access control, operations, or another system. You'll also be better at distinguishing necessary complexity from avoidable work.

Stay close through design discussions, demonstrations, and targeted questions. Use that knowledge to improve decisions and help people. If every implementation choice has to pass through you, you've limited the ownership you were trying to create.

### Build a team that can carry the responsibility

Notice capability gaps early. You may need to hire, borrow a specialist, pair colleagues, or give someone time to learn. Also notice when the same person is required for every difficult decision. Developing another capable owner can improve delivery more than giving that person another task.

As the team becomes stronger, you should be able to delegate larger areas with fewer check-ins. That gives you more time to handle the problems that cross team boundaries.

## Quick recap

Roadmap, RAID, ownership, expectations. Keep these four in view throughout discovery and delivery. You don't need every detail or ceremony from day one. Use this as a starting sequence and revisit it as you learn:

1. **Draft the roadmap:** next 2–3 weeks, next few months, this year and perhaps next year, plus the vision. Explain the goal and why it matters. During discovery, the next milestone might be a question answered or a decision made.
2. **Map ownership:** assign topics, discovery questions, and useful stakeholder relationships to team members. Check capacity and authority. Adjust assignments when people can contribute elsewhere, keeping responsibility clear.
3. **Set up RAID:** risks, assumptions, issues, dependencies. Include owners, mitigation, next actions, and follow-up dates. Give important assumptions a verification step and dependencies an agreed date.
4. **Hold a kickoff:** share the draft beforehand, discuss it together, and agree expectations. Cover deliverables, quality, autonomy, required alignment, updates, and escalation. Ask people to explain their part so you can catch misunderstandings.
5. **Plan the first work:** slice it into tickets with owners and acceptance criteria, including discovery tasks. Order the backlog against the roadmap, check dependencies and capacity, and estimate where useful. Decide what moves when priorities change.
6. **Publish the agreements:** keep the roadmap, RAID, ownership mappings, and expectations somewhere everyone can find them. Link the backlog and record changes as well as the initial plan.
7. **Establish the rhythm:** daily coordination if needed, weekly planning and stakeholder updates, useful one-to-ones, and a review every two weeks. Make the purpose and preparation clear, and adapt the routine to the team.
8. **Block leadership time:** maintain these four ingredients, follow up on actions, resolve blockers, and communicate changes early. Protect that time alongside your IC work, and agree a realistic allocation with your manager.
9. **Keep improving:** adjust support to the person, listen for concerns, and understand the work well enough to ask useful questions. Develop people who can take more ownership, and review what's helping the team deliver.
10. **Delegate early:** good delegation needs work planning. Agree ownership, expectations, and decision boundaries as early as possible, including during discovery, so people can contribute independently from the start.
