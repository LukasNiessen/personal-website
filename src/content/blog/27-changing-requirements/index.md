---
title: "Changing Requirements: The Basics"
summary: "How to handle requirements that evolve during a project"
date: "Jan 1 1970"
draft: true
tags:
  - Project Management
  - Requirements
  - Consulting
---

# Changing Requirements: The Basics

Requirements change. That's normal and often good - it means your client is learning what they actually need.

The problem isn't the changes themselves, it's how you handle them.

## Why Requirements Change

Building software is discovery. You start with assumptions, but once people see something working, they understand their problem better.

Sometimes the business changes while you're building. New regulations, market shifts, or strategic decisions can make your original requirements obsolete.

## Types of Changes

**Clarifications**: You built something different than intended. These are corrections, not changes.

**Enhancements**: Nice-to-have features that aren't essential.

**Fundamental changes**: Changes to core business logic that affect the foundation.

## Managing Changes

Understand what problem they're trying to solve. Often there are multiple ways to address their need.

For clarifications, just fix them. For enhancements, decide if they belong in this phase. For fundamental changes, stop and reassess.

## Communication

Explain impact clearly. Don't say "this will delay the project." Say "adding user roles means rebuilding permissions, which takes two weeks."

Give options: reduce scope elsewhere, wait for phase two, or implement a simpler version now.

Document decisions so everyone remembers what was agreed and why.

## Practical Tips

- Build 15-20% buffer for changes
- Show working software early
- Make sure requester has authority to make trade-offs
- Track changes in a simple log

## Requirements vs Feature Creep

Real changes address business needs or correct misunderstandings. Feature creep is adding things because they seem cool.

Key question: does this help solve the core business problem?

## Conclusion

Changes are part of projects. Manage them so they improve your solution rather than derail it.

Stay focused on the business problem, communicate clearly, and make sure someone with authority decides.

Here's the pattern:
- Client describes what they think they need
- You build exactly that
- They see it and realize it's not right
- "Can we just change this one thing?"

I've seen this on every project. The problem gets worse with multiple stakeholders who all want different things.

## What Doesn't Work

I tried two approaches early on that both failed:

**Saying no to everything**: "That's not in scope, we need a change request."
Technically correct but destroys relationships.

**Saying yes to everything**: "Sure, it's just a small change."
Projects never end, timelines slip, everyone gets frustrated.

Both miss the point. Changes aren't good or bad, they're just information about what the client actually needs.

## What I Do Now

### Understand Why They Want It

When someone requests a change, don't think about scope immediately. Ask: "What problem does this solve for you?"

Often there's a simpler way to address their concern without the change they're asking for.

### Put Changes in Buckets

**Clarifications**: They're explaining what they meant originally. Not scope changes, just corrections.

**Nice-to-haves**: They want to make something better but it's not essential. Push to phase two.

**Actual requirements**: They need this for the solution to work. Real scope changes.

### Be Honest About Impact

For significant changes, explain what it really means:

"Adding this means reworking the authentication system. That's about a week plus testing. We can do it, but it pushes timeline back or we move something else to phase two."

Let them make informed decisions.

## A Real Example

I was building a financial dashboard. Original requirement: show key metrics for executives.

Two weeks in: "Can we add drill-downs? Executives want to see details."

Week later: "Regional managers need access too, but different metrics."

Another week: "Can we add trend analysis? And forecasting?"

Each request made sense, but we were building a completely different system.

I called the sponsor: "We've added three major features. System is more powerful but we're three weeks behind and need another month for testing."

Options:
- Original dashboard on time
- Enhanced version with new timeline  
- Hybrid: core dashboard on time, enhancements in phase two

They picked option three. We delivered basic dashboard on schedule, got user feedback, then built enhancements based on what people actually used.

## Common Problems

**Feature creep**: "Since we're building X, might as well add Y." Dangerous because Y often needs different architecture than X.

**Multiple stakeholders**: Different people want different things. The person requesting change isn't always the person using the system.

**"Simple" changes**: "Just add a field" sounds easy until you need validation, database changes, reporting updates, permissions.

## Practical Stuff

- Add 20% buffer for scope changes. Not because you're bad at estimating, because changes are inevitable.
- Show working software early and often. Earlier feedback = cheaper changes.
- Document what changed and why. Prevents "I thought we agreed" conversations.
- Make sure the person requesting changes understands impact and can make trade-offs.

## The Point

Goal isn't eliminating changing requirements. It's handling them without derailing the project.

When you handle changes well, clients trust you more. They see you understand their business and can adapt while delivering results.

Best projects I've worked on had lots of small course corrections. Worst ones stubbornly stuck to original plan when it was obviously wrong.

## What Actually Works

Here's the approach I use now:

### Acknowledge and Understand

When someone requests a change, don't immediately think about scope or timelines. First, understand why they want it.

Ask: "Help me understand what problem this solves for you."

Often, there's a simpler way to address their underlying concern without the change they're requesting.

### Categorize the Change

Not all changes are equal. I put them in three buckets:

**Clarifications**: They're explaining what they meant originally, you just misunderstood. These aren't scope changes, they're corrections.

**Improvements**: They want to make something better but it's not essential. These can often be pushed to a future phase.

**Requirements**: They need this for the solution to work for their business. These are real scope changes that need proper handling.

### Be Transparent About Impact

When a change is significant, explain the real impact:

"Adding this feature means we need to rework the user authentication system. That's about a week of development plus testing. We can do it, but it will push our timeline back or we'll need to move something else to phase two."

Give them the information to make good decisions.

### Document Everything

This sounds boring, but it's critical. Keep a simple log of what changed and why. Not for blame, but for clarity.

When the project is 80% done and someone says "I thought we agreed on X," you can refer back to when and why it changed to Y.

## A Real Example: The Dashboard That Kept Growing

I was working on a financial reporting dashboard. The original requirement was simple: show key metrics for the executive team.

Two weeks in, the CFO said: "This is great, but can we add drill-down capabilities? The executives will want to see the details behind these numbers."

Fair point. We added drill-downs.

A week later: "The regional managers want access too, but they need different metrics."

Another week: "Can we add trend analysis? And maybe some forecasting?"

Each request made sense individually, but we were building a completely different system than what we started with.

### How I Handled It

I called a meeting with the project sponsor and explained what was happening:

"We've added three major features since we started. The system is much more powerful now, but we're also three weeks behind schedule and probably need another month for all the testing this complexity requires."

Then I gave them options:
- Deliver the original dashboard on time
- Deliver the enhanced version with the new timeline
- Deliver a hybrid: core dashboard on time, enhanced features in phase two

They chose option three. We delivered the basic dashboard on schedule, got feedback from actual users, and then built the enhanced features based on what people actually used.

## Common Patterns I've Seen

### The Feature Creep Pattern

"Since we're already building X, we might as well add Y." This is dangerous because Y often requires different architectural decisions than you made for X.

### The Stakeholder Alignment Problem

Different people want different things. The person who requested the change isn't always the person who has to use the system daily.

### The "Simple" Change That Isn't

"Just add a field to the form" sounds easy until you realize it needs validation, database changes, reporting updates, and permission logic.

## Practical Tips

**Build in buffer time**: I add 20% to all estimates specifically for scope changes. Not because I'm bad at estimating, but because changes are inevitable.

**Show early and often**: The earlier people see working software, the earlier they can give you course corrections when they're still cheap to implement.

**Keep a change log**: Document what changed and why. It helps with future decisions and prevents the "I thought we agreed" conversations.

**Involve the right people**: Make sure the person requesting changes understands the impact and has authority to make the trade-offs.

## The Real Goal

The goal isn't to eliminate changing requirements - it's to handle them professionally without derailing the project.

When you handle changes well, clients trust you more, not less. They see that you understand their business needs and can adapt while still delivering results.

The best projects I've worked on had lots of small course corrections along the way. The worst ones stubbornly stuck to the original plan even when it was obviously wrong.
