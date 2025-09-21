---
title: 'Presales: What is the technical win?'
summary: ''
date: 'May 21 2025'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Presales
  - Sales
---

# Presales: What is the technical win?

When working in presales as a solution engineer or solution architect, the main goal is to get the _technical win_. I will shortly give a definition, put it into context in the bigger picture, and give a high-level example from my past.

## Definition

### Technical Buyer

> The technical buyer is the person who can typically say no but can't say yes. 

For example the technical lead of the client's team. They have typically no authroity over the budget, so they're not the ones to make the final _yes_-decision, however, if they say _no_, because of xyz-technical reason, then the deal will not be closed.

The _economic buyer_, on the other hand, is the person with the budget.

### Technical Win

> A technical win means that the technical buyer believes your solution is the right thing to do.

Note that this includes everything, it must match the clients environment and it must solve their critical business issues. They should also believe that it will work and that it's better than any other competing solutions, including the option of doing nothing. Achieving the technical win basically means, we expect the technical buyer to recommend your your solution to the economic buyer.

In simplified words, having the technical win means that the deal is ready to be closed when it comes to the technical stuff. And this is obviously cruicial, especially for SaaS products.

## Bigger Picture

So the technical win is of course part of the pre-sales, meaning, it's part of everything that happens before the deal is closed. When you have the technical win, it doesn't necessarily mean that the deal will be closed, but it's a major factor in that. 

It typically goes like this:

**Marketing & Lead Generation**
- **Marketing Qualified Leads (MQLs)**: Marketing team generates leads through content, events, advertising
- **Business Development Reps (BDRs)**: Qualify inbound leads and do cold outreach to generate **Sales Qualified Leads (SQLs)**
- **Handoff to Sales**: Qualified leads enter the sales pipeline

**Sales Process** 
- **Account Executive (AE)**: Owns the sales relationship and manages the overall deal
- **Discovery Phase**: AE identifies business needs, budget, timeline, and decision-making process
- **Technical Discovery**: Solution Engineer/Architect (SE/SA) joins to understand technical requirements
- **Solution Design**: SE/SA creates technical proposal and demos that address client's specific needs
- **Technical Win**: SE/SA achieves buy-in from the technical buyer (our main goal)
- **Commercial Negotiation**: AE handles pricing, contracts, and commercial terms with the economic buyer
- **Closing**: Legal reviews, final approvals, signatures

**Post-Sales Handoff**
- **Customer Success**: Ensures smooth onboarding and ongoing adoption
- **Implementation/Professional Services**: Deploys and configures the solution

The technical win sits right in the middle of this process. Without it, even if the economic buyer loves the price and the AE has built great rapport, the deal won't close. But having the technical win alone isn't enough either - you still need the commercial and relationship pieces to fall into place.

## A Real Example: Getting the Technical Win

Let me walk you through a concrete example from my presales days. We were targeting a large German property management company that handles thousands of residential buildings across multiple cities. They were looking for a SaaS solution to modernize their heat billing and energy monitoring infrastructure, moving away from their legacy on-premise systems.

I first heard about this opportunity when our AE mentioned it during our weekly pipeline review. It was an existing client that we reached out to and proposed the service. Initial discovery revealed they wanted real-time monitoring, automated report generation, and predictive analytics to optimize heating costs across their portfolio. Additionally, they also needed integration with their existing ERP system for financial reconciliation and their CRM for tenant communication.

The technical discovery phase was where I got involved. Since everything was done remotely, I ran structured MS Teams workshops with their IT director (our technical buyer) and the head of operations. I mapped stakeholders and their pain points in Miro, loosely following MEDDICC to make sure we understood metrics, decision criteria, and the real economic drivers. What became clear quickly was that while they loved the idea of our SaaS platform, they were nervous about data sovereignty - all tenant data had to stay in Germany, and they needed to maintain some on-premise components for compliance reasons. So they needed a hybrid architecture.

During our use case exploration sessions, I uncovered that their biggest pain point wasn't just monitoring - it was the manual process of reconciling heating data with their SAP ERP system for billing. They were literally having employees export CSV files and manually upload them. Meanwhile, their tenant complaints about heating issues were getting lost between their CRM system and the maintenance ticketing system. Everything was disconnected.

So I now knew everything to continue: 
- the goal (real-time monitoring, automated report generation, predictive analytics)
- the pain points (automated sync with ERP and CRM system)
- contraints (all data in Germany, hybrid architecture)

With the discovery complete, I moved on to solution design and drafted an architecture proposal. This included risk mitigation strategies such as canary releases, staged rollbacks, and fallback plans to ensure a smooth deployment.

So I was ready to move on to a demo, this seemed like the right next step. Just a quick note, I almost always do the technical discovery first and then the use case exploration. This reduces risk of getting everyone excited about automation and integrations, only for IT to kill it later with a "No cloud allowed" or "Data must stay in Germany".

I proposed a demo that would specifically address these integration challenges. So instead of just showing our standard SaaS dashboard, I worked with our development team to mock up a hybrid deployment scenario. We demonstrated real-time data flowing from sensors to our cloud platform, then showing how that data could be automatically synchronized with their ERP for billing calculations, and how heating anomalies could automatically create support tickets in their CRM.

That was good and I was hoping this would be enough, keeping the pipeline velocity high, but after the meeting, it became clear that more convincing work needed to be done, specifically regarding the integration complexity. So I suggested a small proof of value, in which we take one of their smaller buildings and set up the full integration pipeline as a pilot. We connected to our cloud platform for analytics, and built the actual API integrations with their SAP and CRM systems. This wasn't just a demo - this was the real thing, working with their real data and real systems. (But of course with a narrow scope and not as well engineered etc as the real implementation later - just a PoV)

The PoV took about three weeks to set up. I worked closely with their technical team across 3–4 touchpoints per phase (discovery, demo prep, PoV execution), making sure we were aligned at each step. We used Jira/Confluence to jointly track tasks and requirements, which kept transparency high. I also spent time understanding their data schemas, API limitations, and security requirements. I partnered with two of our SEs (solution engineers), who executed most of the implementation. When we presented the results, we weren't just showing pretty charts - we were showing their actual heating data automatically flowing into their billing system, with predictive alerts already identifying two potential equipment failures before they happened.

This PoV was indeed what got us the technical win. My part was done and the negotiations about pricing, scope, legal and more were to be done between our sales team and the client.

Getting to that technical win required understanding that this wasn't just about heat monitoring - it was about solving their integration and process automation challenges. Sort of a _question behind the question_. It took multiple iterations plus the use case exploration to figure this out, so my lesson here was that listening is key. Asking a lot of questions (open ended ones!) rather than talking yourself is cruicial in the discovery phase.

