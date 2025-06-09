---
title: 'Why IT Estimates Are Always Wrong (And How to Make Them Less Wrong)'
summary: 'Why we use story points, T-shirt sizes, and Fibonacci numbers instead of absolute time estimates. Plus the knowledge pyramid that explains why everything takes longer than expected.'
date: 'Aug 14 2023'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Project Management
  - Agile
  - Software Estimation
  - Planning
  - Scrum
  - Product Management
---

# Why IT Estimates Are Always Wrong (And How to Make Them Less Wrong)

"How long will this feature take?"

Every developer's least favorite question. And every manager's most asked one.

The answer is always the same: "It depends." Then you give a number anyway, knowing it's probably wrong.

## Why Absolute Time Estimates Fail

Software development isn't like building a house. You're not laying bricks in a predictable pattern. You're solving problems you've never solved before.

**The problems with time estimates:**

- **Optimism bias** - We assume everything will go smoothly
- **Planning fallacy** - We focus on best-case scenarios
- **Unknown complexity** - Simple-looking features hide massive complexity
- **Interruptions** - Meetings, bugs, and "quick questions" derail focus
- **Changing requirements** - Scope creep is the norm, not exception

When you say "3 days," stakeholders hear "exactly 72 hours." When it takes 5 days, you're late.

## The Knowledge Pyramid

Here's why estimates are fundamentally hard:

```
         /\
        /  \
       /????\ Unknown Unknowns
      /______\
     /        \
    / Known   \ Known Unknowns
   / Unknowns  \
  /_____________\
 /               \
/   Known Knowns  \
\                 /
 \_________________/
```

**Known Knowns** - Things we know we know (existing APIs, proven patterns)
**Known Unknowns** - Things we know we don't know (new framework, integration complexity)  
**Unknown Unknowns** - Things we don't know we don't know (hidden dependencies, edge cases)

The pyramid gets bigger as you go up. Unknown unknowns are the real killers.

## Better Approaches: Relative Sizing

Instead of absolute time, use relative sizing. Compare stories to each other.

### Story Points

Rate complexity, not time. Use Fibonacci numbers: 1, 2, 3, 5, 8, 13, 21.

Why Fibonacci? The gaps force decisions. A story can't be "exactly between 5 and 8." It's either 5 or 8.

**Story Point Guidelines:**

- 1 point: Trivial change, copy-paste with small modification
- 2 points: Simple feature, clear requirements, no unknowns
- 3 points: Standard feature, some complexity
- 5 points: Complex feature, multiple components involved
- 8 points: Very complex, lots of unknowns
- 13+ points: Break it down into smaller stories

### T-Shirt Sizing

Even simpler: XS, S, M, L, XL.

Good for high-level planning when you don't have detailed requirements yet.

### Planning Poker

Team estimates together. Everyone shows their cards simultaneously. Discuss outliers. Re-estimate until consensus.

Prevents anchoring bias and gets diverse perspectives.

## Connection to Agile

This is why the [Agile Manifesto](https://agilemanifesto.org/) emphasizes:

- **Responding to change** over following a plan
- **Working software** over comprehensive documentation
- **Individuals and interactions** over processes and tools

Agile accepts that we can't predict everything. Instead of trying to estimate perfectly upfront, we:

- Plan in short iterations (sprints)
- Measure velocity over time
- Adjust based on actual delivery
- Re-prioritize frequently

## Making Estimates Less Wrong

**1. Use Historical Data**
Track your velocity. How many story points does your team complete per sprint? Use that for future planning.

**2. Break Things Down**
Big stories hide complexity. Break everything into small, digestible pieces.

**3. Include Buffer Time**
Add time for testing, code review, deployment, and inevitable issues.

**4. Estimate as a Team**
Multiple perspectives catch blind spots.

**5. Re-estimate Often**
Update estimates as you learn more about the problem.

**6. Track Accuracy**
Compare estimates to actuals. Learn from the differences.

## The Three-Point Method

For critical features, use three estimates:

- **Optimistic** - Best case, everything goes right
- **Most Likely** - Realistic scenario
- **Pessimistic** - Murphy's Law applies

Expected time = (Optimistic + 4×Most Likely + Pessimistic) ÷ 6

Still not perfect, but better than single-point estimates.

## When You Must Give Time Estimates

Sometimes stakeholders demand calendar dates. Here's how to handle it:

1. **Give ranges** - "2-4 weeks" instead of "3 weeks"
2. **Communicate confidence** - "I'm 90% confident it'll be done by X"
3. **Include assumptions** - "Assuming no major blockers"
4. **Update frequently** - Weekly estimate updates
5. **Pad appropriately** - Add 25-50% buffer for unknowns

## Bottom Line

Perfect estimates don't exist in software development. The goal isn't to be exactly right—it's to be approximately useful.

Use relative sizing to plan sprints. Use historical velocity to forecast delivery. Accept that estimates will be wrong and build processes that adapt to that reality.

The teams that deliver consistently aren't the ones with perfect estimates. They're the ones that plan for uncertainty and adjust quickly when reality hits.
