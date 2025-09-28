---
title: "Change Management: My Experience"
summary: "What actually works when implementing change in organizations - my experience"
date: "Jan 1 1970"
draft: false
tags:
  - Change Management
  - Consulting
  - Leadership
  - Organizations
---

# Change Management: The Consulting Reality

Change management is a highly important topic. Like Weinberg said, "no matter what they tell you, it’s always a people problem".

Most change management articles focus on ADKAR or Kotter's 8-step process. Those are fine frameworks, but they miss the human reality. Here's what actually matters when you're trying to get an organization to adopt new ways of working.

## The Core Problem: Resistance Isn't About the Change

People don't resist change itself. They resist **losing control**, **looking incompetent**, or **having their expertise become irrelevant**. Undestanding this is the most important step.

This is the real challenge in any transformation project.

## What Actually Works: The Human-First Approach

### 1. Start with the Why (But Make It Personal)

When encountering or anticipating change management issues, think of how you frame things. For example.

Instead of: "This digital transformation will improve operational efficiency by 30%."

Try: "This change means you'll spend less time on manual data entry and more time on analysis that actually influences business decisions."

**Make it about their day-to-day experience**, not abstract business metrics.

### 2. Find Your Champions Early

Every organization has informal influencers. They're not always in leadership positions. Sometimes it's the developer everyone asks for help, or the account manager who knows all the client quirks.

Identify these people early and bring them into the process. Give them early access, ask for their input, make them part of the solution. When they advocate for the change, others listen.

I've seen projects succeed because we convinced the right two people, and fail despite executive support because we ignored the informal network.

### 3. Parallel Running is Your Friend

Don't force big-bang transitions. If it helps, let people run both the old and new systems for a while. Yes, it's more work. Yes, it's "inefficient". But it removes the fear factor.

When people can verify that the new system produces the same results as their trusted old process, they relax. They start experimenting. They begin to trust.

## An Example

Let me share an example from my past. We were implementing a full GitOps transformation for a mid-sized client - moving them away from manual deployments and "ClickOps" infrastructure management to Infrastructure as Code with automated deployments through ArgoCD.

This was a massive change for their two-person DevOps team. Instead of manually deploying to clusters and clicking through AWS consoles, everything would now be automated through Git commits. The business outcomes were clear: faster deployments, reduced errors, better compliance tracking, security benefits from pull-based GitOps, rollback abilities, and more.

One of the two DevOps engineers resisted though. Regularly, he'd come up with new arguments against it, or recycle old ones. "What if ArgoCD goes down?" "How do we handle emergency fixes?" "This adds too much complexity." Initially, I thought these were technical concerns and kept explaining the solutions.

But after a while, I suspected it was something different. Marcus probably doesn't have IaC expertise, probably doesn't know ArgoCD well. He was the guy everyone called when deployments failed. His professional identity was built on being the "deployment expert" who could fix anything manually.

The new system would make much of his specialized knowledge obsolete, or at least shift the needed expertise quite heavily. 

So I had a conversation with the client's project manager. I explained that we most likely had a change management issue, not a technical one. So we brainstormed and decided that he would talk to the guy and frame it as a growth-oppurtunity, as that they actually need someone capable of IaC, when he would learn that, and we will give him time and trainings if needed, he will become even more valuable to the company than he is already - and it's the truth, IaC is cruicial for any modern DevOps. Also, we gave him and the other mate ownership of the monitoring and troubleshooting procedures for the new system, as well as documentation etc.

It worked (but wasn't perfect, he still grumbled here and there).

My lesson was that thinking about change management before needing it is very valuable. I totally understand the DevOps guy and our framing was a good one, true and worked - just I could have thought about that before :)

## Change Management with Stakeholders

So it's still the same. What changes is just that stakeholders and c-level execs care about different things than developers or DevOps people. They worry about:

- Political capital and how the change reflects on them
- Business continuity and risk to their departments
- ROI and being able to justify the investment
- Control over outcomes and timelines
- Credit for success (and blame for failure)

So here it's typically not about them fearing to lose personal relevance but more that they are not fully convinced that the business outcome is good. Maybe you have them on 8 out of 10 points, but these 2 points make them resist. It's key to figure out what the issue is.

## The Bottom Line

Change management isn't rocket science, it's about understanding, empathy, clear and careful communication. About framing. Frameworks help, but empathy and patience matter more.

The goal isn't to eliminate resistance - it's to understand it and work with it. When you treat resistance as valuable feedback rather than an obstacle, you build better solutions and more committed teams.

Most importantly: **change takes time**. Real, sustainable change happens in months and years, not weeks. Plan accordingly, and don't mistake compliance for commitment.
