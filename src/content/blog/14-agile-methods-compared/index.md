---
title: 'Agile Methods: Waterfall vs Kanban vs Scrum vs Scrumban'
summary: 'Understanding the differences between agile methodologies and when to use each one'
date: 'Nov 3 2023'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Agile
  - Scrum
  - Kanban
  - Scrumban
  - Waterfall
  - Project Management
  - Software Development
  - Agile Manifesto
---

# Agile Methods: Waterfall vs Kanban vs Scrum vs Scrumban

"We're doing Agile" doesn't mean much anymore. Everyone claims to be agile, but most teams are just doing Waterfall with shorter phases.

Let me break down the actual differences between these methodologies and help you pick the right one.

## The Agile Revolution (Quick Context)

Before we dive into specifics, here's what changed everything:

### The Agile Manifesto (2001)

- **Individuals and interactions** over processes and tools
- **Working software** over comprehensive documentation
- **Customer collaboration** over contract negotiation
- **Responding to change** over following a plan

This wasn't just about process – it was about **fundamentally changing how we think about software development**.

## Waterfall: The Old Guard

Waterfall isn't agile, but it's worth understanding as the baseline.

### How It Works

```
Requirements → Design → Implementation → Testing → Deployment → Maintenance
     ↓           ↓            ↓            ↓         ↓            ↓
   (3 months)  (2 months)   (6 months)   (2 months) (1 month)   (ongoing)
```

### When It Makes Sense

- **Regulatory environments** with strict documentation requirements
- **Fixed-scope projects** where requirements won't change
- **Hardware integration** where changes are expensive
- **Teams new to software development** (controversial, but sometimes true)

### The Problems

- **Late feedback** (you discover problems after months of work)
- **Change resistance** (any modification breaks the plan)
- **Risk concentration** (all integration happens at the end)

## Kanban: Continuous Flow

Kanban focuses on **visualizing work** and **limiting work in progress**.

### Core Principles

1. **Visualize the workflow** (usually with a board)
2. **Limit WIP** (work in progress)
3. **Manage flow** (optimize the whole system)
4. **Make policies explicit** (everyone knows the rules)
5. **Improve collaboratively** (evolve the process)

### Typical Board

```
To Do    |  In Progress  |  Code Review  |  Testing  |  Done
---------|---------------|---------------|-----------|-------
Task A   |  Task D (2/3) |  Task G (1/2) | Task I    | Task K
Task B   |  Task E       |               |           | Task L
Task C   |  Task F       |               |           |
```

_(Numbers show WIP limits)_

### When Kanban Works

- **Continuous flow** of varied requests (support teams, maintenance)
- **Unpredictable priorities** that change frequently
- **Operational work** where batching doesn't add value
- **Teams that want to improve gradually** without big process changes

## Scrum: Sprint-Based Development

Scrum organizes work into **fixed-length sprints** with defined ceremonies.

### The Framework

```
Product Backlog → Sprint Planning → Sprint (1-4 weeks) → Sprint Review → Retrospective
       ↑                                    ↓
       └─────── Product Backlog Refinement ←─┘
```

### Key Roles

- **Product Owner**: Defines what to build
- **Scrum Master**: Facilitates the process
- **Development Team**: Builds the product

### When Scrum Works

- **Product development** with evolving requirements
- **Teams that benefit from regular reflection** (retrospectives)
- **Stakeholders who want predictable delivery** (every sprint)
- **Complex work** that benefits from regular planning

### Common Scrum Problems

- **Sprint commitment pressure** (cramming work to "meet the sprint goal")
- **Artificial deadlines** (forcing work into sprint boundaries)
- **Ceremony overhead** (too many meetings for simple work)

## Scrumban: The Hybrid

Scrumban combines Scrum's structure with Kanban's flow.

### How It Works

- **Planning meetings** from Scrum (but triggered by WIP, not time)
- **Continuous flow** from Kanban
- **Retrospectives** from Scrum
- **Pull system** from Kanban

### Typical Implementation

```
Backlog | Ready | Development | Testing | Done
--------|-------|-------------|---------|------
        | (5)   |    (3)      |   (2)   |

Planning Trigger: When "Ready" drops below 3 items
```

### When Scrumban Works

- **Mature Scrum teams** that want more flow
- **Support teams** that need some planning structure
- **Mixed work types** (features + bugs + operational tasks)
- **Teams transitioning** from Scrum to Kanban

## Choosing the Right Method

### Team Maturity

- **New teams**: Start with Scrum (structure helps)
- **Experienced teams**: Consider Kanban or Scrumban
- **Distributed teams**: Scrum ceremonies can help coordination

### Work Type

- **Product development**: Scrum or Scrumban
- **Operational work**: Kanban
- **Mixed work**: Scrumban
- **Regulated environments**: Waterfall (unfortunately)

### Organizational Context

- **Need predictability**: Scrum
- **Need flexibility**: Kanban
- **Want both**: Scrumban
- **Traditional organization**: Start with Scrum, evolve

## Common Agile Anti-Patterns

### "Agile-fall"

Using Scrum ceremonies but keeping waterfall thinking. Planning everything upfront, no mid-sprint changes.

### "Process Worship"

Following the framework rigidly without understanding the principles. "The retrospective said we must do X."

### "Fake Agile"

Claiming to be agile while maintaining command-and-control management. "Be agile, but follow this detailed plan."

## The Real Goal

All of these are just **tools**. The real goal is:

1. **Fast feedback** on what you're building
2. **Ability to change direction** when you learn something new
3. **Sustainable pace** for the team
4. **Continuous improvement** of how you work

Pick the method that best supports these goals for your context.

## Getting Started

### If You're Doing Waterfall

1. **Shorten cycles** (6 months → 6 weeks)
2. **Get feedback early** (show working software)
3. **Plan less detail** upfront

### If You're New to Agile

1. **Start with Scrum** (structure helps)
2. **Focus on working software** over documentation
3. **Retrospect and improve** every few weeks

### If Scrum Feels Heavy

1. **Try Scrumban** (keep planning, add flow)
2. **Remove unnecessary ceremonies**
3. **Focus on continuous delivery**

## The Bottom Line

There's no "best" agile method. There's only the method that works for your team, your work, and your organization **right now**.

Start somewhere, measure what matters, and evolve. That's the most agile thing you can do.
