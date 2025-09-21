---
title: 'Presales: How to get the technical validation? What tradeoffs are there?'
summary: 'A discussion of getting the technical validation'
date: 'May 22 2025'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Presales
  - Sales
---

# Presales: How to get the technical validation? What tradeoffs are there?

As a solution engineer in presales, we want to get the [technical win](https://lukasniessen.com/blog/126-the-technical-win/). For that, we need to do the technical validation. I will give a short definition of what that is, explain how it fits in the bigger picture, give a list of different ways to achieve it, and conclude with a real example from my past.

## Definition

> The technical validation is the process of verifying that your proposed solution works as intended in the customer’s environment and aligns with their technical and business requirements.

So this happens after the solution design and before you achieve the technical win.

The technical validation can be achieved in different ways, for example via a proof of concept or just a demo. I will present them and many other ways later, including when to go for which.

## Bigger Picture

So the technical win is of course part of the pre-sales, meaning, it's part of everything that happens before the deal is closed.

It typically goes like this:

1. Marketing generated a lead
2. Lead becomes sales qualified (SQL)
3. Marketing hands lead off to Sales, meaning the qualified lead enters the sales pipeline
4. Account Executive (AE) owns the sales relationship and manages the overall deal
5. Discovery Phase: AE identifies business needs, budget, timeline, and decision-making process
6. Technical Discovery: Solution Engineer/Architect (SE/SA) joins to understand technical requirements
7. Solution Design: SE/SA creates technical proposal and demos that address client's specific needs
**8. Technical Validation:** SE/SA does the technical validation, for example via a demo that is later followed by a proof of concept
9. Technical Win: SE/SA achieves buy-in from the technical buyer (our main goal)
10. Commercial Negotiation: AE handles pricing, contracts, and commercial terms with the economic buyer
11. Closing: Legal reviews, final approvals, signatures

So the technical validation sits right in front of the technical win. You must give a technical validation to the prospect somehow, they will not buy blindly. Now whether you need a demo, or a PoC, or a hands-on workshop, entirely depends on the specific opportunity.

## Types of Technical Validation

Here are the most common ways to achieve technical validation, ranked roughly by complexity and time investment. Note that not all of them match exactly what I said above, meaning that they are after the solution design, for example a standard demo is earlier in the presales cycle.

### 1. Standard Demo

**What it is:** A prepared demonstration using sample data or a sandbox environment.

**When to use:** Early-stage opportunities where the prospect needs to see basic functionality. Ideal when the solution is straightforward and the customer's requirements are standard.

**Tradeoffs:** Quick to execute and low-risk, but doesn't address custom integrations or unique use cases. Can feel generic if not tailored properly.

**My take:** Start here almost always. It's your baseline. But be ready to pivot quickly if they start asking "How does this work with our SAP system?"

### 2. Customized Demo

**What it is:** A demo tailored to the prospect's specific use cases, data, and workflows.

**When to use:** When the prospect has identified specific pain points or unique requirements that your standard demo doesn't address.

**Tradeoffs:** More preparation time and requires deeper discovery, but significantly more compelling. Risk of over-engineering the demo for a deal that might not close.

**My take:** This is where most deals get won or lost. The extra effort to customize usually pays off, especially with technical buyers who can spot generic demos from miles away.

### 3. Proof of Value (PoV)

**What it is:** A limited-scope implementation using the prospect's actual data and systems, but with minimal integration depth.

**When to use:** When the prospect needs to see real results with their data, but isn't ready for a full PoC. Often used when there's skepticism about performance or data quality.

**Tradeoffs:** More convincing than demos but requires access to their data. Usually 1-2 weeks of effort. Risk of exposing system limitations early. Note that with increased effort, the risk for your company grows. The more resources you spend, for example on a PoV, the worse it is when the deal is not closed, for whatever reason. I will just say more effort from now on, and always indicate the risk being higher.

**My take:** Great middle ground when a demo isn't enough but a full PoC feels like overkill. I've seen this close deals where the "aha moment" comes from seeing their actual data processed.

### 4. Proof of Concept (PoC)

**What it is:** A full-featured implementation in a controlled environment, often including integrations and custom configurations.

**When to use:** High-value deals where the prospect has complex requirements, multiple stakeholders, or significant technical risk concerns.

**Tradeoffs:** Can take 4-8 weeks and requires significant resources (effort) from both sides. High success rate but also high opportunity cost if it doesn't convert.

**My take:** Only do this if you've already achieved strong business alignment and the deal is forecast to close.

### 5. Technical Deep Dive / Architecture Review

**What it is:** Detailed technical sessions where you walk through system architecture, APIs, security models, and integration patterns with their technical team.

**When to use:** When the prospect has strong in-house technical capabilities and wants to evaluate the solution's technical merit before committing to a larger validation effort.

**Tradeoffs:** Low time investment but requires deep technical knowledge. Can be intimidating for prospects who aren't highly technical.

**My take:** Essential for developer-focused products or highly technical buyers. Don't skip this if your primary contact is a CTO or technical architect.

### 6. Hands-On Workshop / Trial

**What it is:** Giving the prospect direct access to your platform to explore independently, often with guided exercises or use cases.

**When to use:** When you have a self-service platform and the prospect prefers to evaluate solutions hands-on rather than through presentations.

**Tradeoffs:** Lower touch from your side but less control over the evaluation process. Risk of them getting stuck or missing key features.

**My take:** Works great for developer tools or platforms with good UX. Just make sure you have tracking and follow-up processes in place, or they'll disappear into the trial and you'll never hear back.

### 7. Pilot Program

**What it is:** A full production deployment with a limited scope, real users, and measurable business outcomes.

**When to use:** Large enterprise deals where the full rollout would be significant, or when the prospect wants to validate business outcomes, not just technical functionality.

**Tradeoffs:** Longest timeline (often 3-6 months) and highest resource commitment (effort), but also highest conversion rates and deal sizes.

**My take:** This is less "technical validation" and more "business validation," but it's the gold standard for enterprise deals. Just make sure you have clear success criteria and a path to expand.

## Choosing the Right Approach

The key is matching the validation method to the deal characteristics:

- **Deal size matters:** Don't do a 6-week PoC for a $50k deal
- **Technical complexity drives depth:** Simple integrations = demo; complex integrations = PoC
- **Buyer type influences format:** Developers want trials; executives want customized demos
- **Competitive pressure affects timeline:** If they're evaluating 3 vendors, speed wins

Most importantly, always start with the simplest validation that could work and only escalate if needed. Complex validations are riskier and hinder the pipeline velocity, often they are the right tool regardless, but often they are not.

## A Real Example: Getting the Technical Win

Let me walk you through a concrete example from my presales days involving a large German property management company that wanted to modernize their heat billing and energy monitoring infrastructure.

**The Setup:** After initial discovery, I learned they needed real-time monitoring, automated report generation, and predictive analytics. But the real pain point was manual CSV exports between their SAP ERP and heating systems - plus tenant complaints getting lost between their CRM and maintenance systems. Key constraint: all data had to stay in Germany due to compliance requirements, and a part of the system needed to keep running on-premise.

**Discovery Key Findings:**
- Goal: real-time monitoring with predictive analytics
- Pain points: manual ERP sync and disconnected systems
- Constraints: German data residency, hybrid architecture needed

### Technical Validation #1: Customized Demo

Instead of our standard SaaS demo, I worked with our dev team to create a hybrid deployment scenario specifically for their use case. This took about a week of prep work.

**Demo Structure (45 minutes):**
1. **Opening (5 min):** Recap their requirements and how our solution addresses each
2. **Core Platform (15 min):** Real-time monitoring dashboard with their building types and heating patterns
3. **Integration Deep Dive (20 min):** The money shot - showing data flow from sensors → cloud platform → automatic SAP sync → CRM ticket creation
4. **German Compliance (5 min):** Architecture diagram showing data residency and hybrid deployment

**The Challenge:** I used realistic German building data and mocked up their SAP screen layouts. The IT director immediately started asking technical questions about API rate limits, data transformation logic, and failover scenarios. This was a good sign - engagement - but also revealed they needed more convincing about the integration complexity.

**Demo Outcome:** Positive reception but not enough to close the technical validation. They wanted to see it working with their actual systems.

### Technical Validation #2: Proof of Value

I suggested a targeted PoV using one of their smaller buildings (47 units) to prove the full integration pipeline. This escalation was necessary because the integration risk was their biggest concern.

**PoV Scope Definition:**
- Duration: 3 weeks setup + 1 week validation
- Scope: 1 building, full data pipeline, basic analytics
- Resources: 2 of our SEs + their sys admin + their SAP specialist

**Week 1-2: Technical Setup**
I spent significant time understanding their data schemas.

**Week 3: Integration Development**
Doing the development work.

**Week 4: Validation & Results**
The results presentation was where we sealed the deal. We showed:
- Live dashboard with their actual heating data from 47 units
- Automatic billing calculations flowing into SAP (they could see it updating in real-time)
- Tenant comfort complaint automatically converted to maintenance ticket with sensor data attached

**What Made It Work:**
The PoV succeeded because we didn't just prove our platform worked - we proved it solved their specific integration headaches.

**The Technical Win:** The PoV achieved our technical validation and secured buy-in from the technical buyer. The key was understanding that this wasn't just about heat monitoring - it was about solving their integration problem. 

### Challenges I Faced

A few things didn't go smoothly during this validation:

**Week 2 Delay:** Their SAP specialist was unavailable for a full week due to a production issue at another site. This pushed back our integration testing and meant working with incomplete field mappings initially.

**API Rate Limiting:** We hit undocumented rate limits in their CRM system during testing. Had to implement exponential backoff and request batching, which added complexity we hadn't planned for.

**Stakeholder Alignment:** The head of operations kept pushing for additional reporting features during our weekly check-ins, while the IT director wanted to keep the scope minimal. I had to facilitate a few alignment calls to keep everyone focused on the original success criteria without alienating either stakeholder. Specifically, I set up a 30-minute "scope confirmation" call where we revisited the original success criteria and had both stakeholders agree on what constituted a successful PoV versus what could be addressed in a future phase.

---

This example shows how starting with a customized demo helped identify what type of deeper validation was needed, then executing a focused PoV that directly addressed their biggest technical concerns.
