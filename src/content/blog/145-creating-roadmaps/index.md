---
title: 'How to create Roadmaps?'
summary: 'A guide on how to create roadmaps in the IT, why it matters, and a brief overview of my personal experiences'
date: 'Nov 20 2025'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - roadmap
  - management
---

# How to create Roadmaps?

Roadmaps are a very important part of the Software Development Lifecycle (SDLC). This is supposed to be a short guide of how to write roadmaps and what, over the years, I have personally found to be useful and what to avoid.

## Northstar

Your team needs to know what the direction is. Where are we all headed? And why?

Having your team know what's coming, and why, and ideally having them be excited about it, is absolute key for delivering good software or a good product. And you will only ever get them to 100% if you do that well.

One of the classical tools for achieving that is a roadmap. It's NOT a detailed execution plan, it's a northstar. Where do we go, why, and why is it amazing?

Ideally you want a short term roadmap, which is just for the next sprint, a mid term one for up to a year, and a long term one for ~ 3 years.

## Now/Next/Later

I recommend a very common agile type of roadmaps: Now/Next/Later.

This format divides your roadmap into three time-based buckets:

- **NOW**: What you're actively working on (current sprint or next 4-6 weeks). These are committed items with clear scope and owners.
- **NEXT**: What's coming up (1-3 months). These items are prioritized and roughly scoped, but details may still evolve.
- **LATER**: The backlog and future vision (3+ months). These are ideas, experiments, and strategic bets that may or may not happen.

The beauty of this approach is that it acknowledges uncertainty. The further out you look, the less specific you can be, and that's okay. It prevents teams from over-committing to features that might not make sense by the time you get to them.

## Why Now/Next/Later

The reason this format works so well is rooted in the **pyramid of knowledge**:

1. **What you know**: Your current sprint, active work, and immediate priorities
2. **What you know you don't know**: Upcoming features that need research, design, or technical spikes
3. **What you don't know you don't know**: Future unknowns, market changes, and evolving customer needs

The traditional waterfall model forced teams to pretend they could predict everything months or years in advance. Creating roadmaps with specific dates for specific features is an outdated way of planning and should not be practiced. Decades of empirical evidence in the IT industry have shown that these estimates are barely ever correct. If you planned linearly on them, you will have to trash your entire plan and create a new one whenever reality diverges from your predictions.

This is why "agile" is so common. The Now/Next/Later format embraces that.

## Alternatives 

While Now/Next/Later is my preferred approach, there are other common roadmap formats:

- **Theme-Based Roadmaps**: Organize work around strategic themes (e.g., "Performance," "Security," "User Experience") rather than time buckets
- **Release-Based Roadmaps**: Tied to specific version releases (v2.0, v2.1, etc.)
- **Outcome-Based Roadmaps**: Focus on desired outcomes and metrics rather than features
- **Gantt Charts**: Traditional timeline-based visualization with dependencies (useful for infrastructure projects with hard dependencies)

## Format for Different Time Horizons

Which format you use can vary based on your audience and timeframe:

- **Short and mid-term**: Now/Next/Later or Theme-Based roadmaps work well for quarterly planning
- **Long-term**: Often outcome-Based or Theme-Based roadmaps are best, as specifics will change

## The Process Behind the Roadmap

A roadmap isn't created in a vacuum. It's the output of several processes:

1. **Requirements Engineering**: Gathering and prioritizing stakeholder needs
2. **Stakeholder Involvement**: Regular sync-ups with product, engineering, sales, and customer success
3. **Prioritization Frameworks**: Using methods like RICE (Reach, Impact, Confidence, Effort) or MoSCoW (Must, Should, Could, Won't)
4. **Presentation Format**: PowerPoints or slides for executive reviews, living documents (Confluence, Notion) for teams, visual tools (Jira Roadmaps, ProductBoard) for day-to-day tracking

The key is keeping the roadmap a **living document**. Review it regularly (monthly or quarterly), adjust based on learnings, and communicate changes transparently to all stakeholders.

## Example: Employee Onboarding Portal

Here's a real-world example of a Now/Next/Later roadmap:

### Product Roadmap: Employee Onboarding Portal (Internal)

**Last Updated**: November 20, 2025  
**Product Owner**: Sarah Jenkins (HR Systems)  
**Tech Lead**: David Chen  
**Theme**: Stability, IT Automation, and New Hire Experience

#### NOW (Current Focus)

**Timeline**: Sprint 12–13 (Next 4 Weeks)  
**Strategic Goal**: System stability and resolving critical IT provisioning bottlenecks.

| Feature / Initiative | Type | Description | Success Metric | Stakeholders |
|---------------------|------|-------------|----------------|--------------|
| Jira Integration V1 | Backend | Automate ticket creation for IT hardware provisioning when a candidate is moved to "Hired." | Reduce manual IT ticket creation time by 100%. | IT Support |
| SSO Implementation | Security | Enforce Google Workspace SSO. Remove legacy username/password login. | 100% of logins via SSO; Security compliance met. | InfoSec |
| Fix: "Start Date" Crash | Bug Fix | Resolve server error when start dates are selected in the past/retroactive hires. | Zero crashes related to date selection. | HR Ops |
| Bulk Candidate Upload | Feature | Allow HR to upload CSV for intern cohorts (10+ hires) instead of single entry. | Reduce data entry time for intern season by 80%. | Recruiting |

#### NEXT (Up Next)

**Timeline**: Sprint 14–16 (Months 2–3)  
**Strategic Goal**: Improving the "Day 1" experience for the new employee.

| Feature / Initiative | Type | Description | Success Metric | Stakeholders |
|---------------------|------|-------------|----------------|--------------|
| New Hire "Welcome" Dashboard | UI/UX | A dedicated view for the new employee showing schedule, team info, and tasks. | 90% of new hires log in before Day 1. | HR / L&D |
| Hardware Selection Form | Feature | Self-service form for new hires to select Mac/PC and peripherals. | Reduce hardware swap requests by 50%. | IT / Procurement |
| Manager Check-in Automation | Notification | Automated Slack/Email nudges for managers to schedule welcome lunches and 1:1s. | 100% of managers receive reminders 3 days prior. | People Ops |
| Slack/Directory Sync | Integration | Auto-push new hire profile photo and bio to Slack and Company Org Chart. | Profile availability on Day 1 (currently Day 3). | Internal Comms |

#### LATER (Backlog / Discovery)

**Timeline**: Q2 2026+  
**Strategic Goal**: Full automation and scaling for other departments.

| Feature / Initiative | Type | Description | Dependency |
|---------------------|------|-------------|------------|
| DocuSign Integration | Integration | Auto-trigger offer letters and tax forms; track signature status in portal. | Needs Legal API Access |
| "Offboarding" Workflow | Feature | Reverse workflow to revoke access and generate return shipping labels. | Jira Integration V2 |
| Dept. Specific Templates | Config | Custom checklists for Sales (Salesforce setup) vs Eng (GitHub setup). | None |
| AI Onboarding Bot | AI | Chatbot to answer FAQ ("What is the wifi?", "Holiday policy?"). | Confluence API |