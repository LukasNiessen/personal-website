---
title: "Solution Architect: Presales Basics"
summary: "The very basics of presales for a solution architect"
date: "May 01 2025"
draft: false
tags:
  - Presales
  - Sales
  - Solution Architect
---

# Solution Architect: Presales Basics

This article covers the very basics of presales. That is things like what it is, the language and terms used, other people involved and how the process works.

## What is it?

So let's start with laying out what it even is. Your company, often a consulting company, wants to close a deal with some other company. So it goes from _"hello, we want x"_ to _"here is the finished and working product"_. There are many steps in between obviously.

Your role as a solution architect is in the _presales_, that is, all the stuff _before_ the deal is closed, before it's signed. And even that is often lenghty process with many steps in between.

### Summary of the Presales Process

Let's say you have a customer HappyDogs Inc and they want to modernize their entire system since they're having latency issues.

#### 1. Lead Generation / First Contact

The initial contact takes place typically by one of these options:

- HappyDogs is contacting you, this is called Inbound leads. This could be a form on your website, direct contact from referrals or similar things.
- You contact HappyDogs, this is called Outbound outreach. This could be cold emails, LinkedIn messages, conferences or networking events.
- Other things such as channel partners (agencies for examples), webinars, ads, SEO etc.

This first contact is owned by the marketing team or business development. The objective here is to identify and engage potential clients. These potential clients are called _leads_. They may or may not be a fit at this stage.

#### 2. Discovery Call

The next step is to have a discovery call where you want to understand what the client needs, the business goals, the timeline and the budget. You will conclude if there is a mutual fit.

This is done by the sales representative or Account Executive (AE).

#### 3. Opportunity Planning

Now if there is a mutual fit, we move on and internally make plans. Those plans may include diving deep into the client needs and forming solution options - this would be owned by the Solution Architect. You also may identify competitors and influencing factors.

This is owned by many different people, but the important note is that this is usually the first step where you would come into play as a solution architect.

However, note that in some cases the solution architect is involved in the discovery call already, but that's only if that call requires technical knowledge already. If that's the case, you would ask questions, spot risks and complexity and build credibility with the client.

#### 4. Solutioning

This is the step where you craft a tailored solution and proposal. A proposal is formal document or presentation (slide deck, PDF, ...) outlining the concrete solution, timeline, pricing and benefits. This proposal will be used for discussion and negotation before later signing a formal contract (closing the deal).

This step is highly important for you as a solution architect. You design the high-level solution, estimate effort, duration, resources and identify risks. You often write or co-write the proposal.

#### 5. Pitch

Now it's time to convince the client of your proposal. So your team, that is for example the sales lead, walks through the proposal, addresses clearly why it's a good solution and what the benefits are, showcases relevant studies, builds trust and addresses the clients questions and objections.

The solution architect will present technical or complex engagement and answer questions. It's important to demonstrate competence.

One could say: sales owns the _relationship_ while the solution architect owns the _how it's done_.

#### 6. Negotiation & Refinement

Here you address the client feedback and perhaps make adjustments. Legal things are negotiated too.

You as a solution architect are often involved here. If the client pushes back on the solution, the scope, or the timeline, you need to clarify the questions. Or maybe adjust the solution.

#### 7. Closing the Deal

The deal is closed and the contract is signed. This is owned by sales. Solution architects are not involved here anymore.

### Notes

The client may want to see a Proof of Concept (PoC) or you offer it yourself. This is sort of a little demo of your solution. It's used to see the solution _in action_ and validate it works. It's done in the solutioning step usually, so before the pitch takes place. The PoC results may then be used in the pitch.

The length of each step depends on the solution. If it's a small project some of these steps may even fall into one step. While when it's a big project, some steps may consist of many meetings per step. However, typically the longest steps are the solutioning and the negotiation back and forth.

Also note that the name _solution architect_ varies by company, it's also called _sales engineer_ and _technical sales resource_.

## BANT

When dealing with a lead (remember, that's a potential client), we want to determine if there's a real oppurtunity. So for example, can we even implement what the client wants and if so, can we do so in a way that satisfies the client, e.g. timeline, budget and things of that nature. This is often called BANT qualification, BANT = Budget, Authority, Need, and Timeline.

## The Lingo

Here are some additional terms from (pre)sales. This is not comprehensive of course.

**Pipeline**: The collection of all active opportunities, usually measured in total potential revenue. Your contributions directly impact pipeline health and velocity.

**Annual Recurring Revenue (ARR)**: This is sometimes seen as the holy grail metric. A $10K monthly commitment represents $120K ARR.

**Total Contract Value (TCV) vs Annual Contract Value (ACV)**: TCV is the total value over the contract lifetime; ACV is the annual value. Understanding both helps you position multi-year deals effectively.

**Customer Acquisition Cost (CAC)**: How much it costs to acquire a customer. Your efficiency in moving deals through technical qualification directly impacts CAC.

**Land and Expand**: Start with a smaller initial implementation, prove value, then expand usage across the organization. This is particularly relevant for selling SaaS where you might start with one application and grow to enterprise-wide adoption.

**Champion vs Economic Buyer**: Your champion is the technical person who advocates for your solution internally. The economic buyer is the person who can actually approve the budget. These are often different people, and you need strategies for both.

**Compelling Event**: The business or technical driver that creates urgency. Maybe they're launching a new product, facing compliance deadlines, or their current system is at breaking point. No compelling event usually means no urgency to buy.

**MEDDIC**: A qualification framework - Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion. This framework is very common, however some swear one it while others say it's just a fancy term for management.

**Prospect**: A lead that's been qualified and is more likely to buy. For example, a company that's actively looking for a consultant, has a budget, and wants to move quickly.

**Opportunity**: A potential deal that's in progress. It's tracked in CRM systems like Salesforce or HubSpot.

**SOW (Statement of Work)**: A detailed breakdown of the work you'll deliver, often part of the contract. More technical and delivery-focused than a general proposal.

**SME (Subject Matter Expert)**: A specialist who provides deep technical or industry knowledge during presales. For example, a cloud architect, data scientist, or healthcare consultant.

**RFP / RFI**: RFP = Request for Proposal, where the client formally asks vendors to submit detailed bids. RFI = Request for Information, which is an earlier stage where the client asks for general info.

**Deal / Contract**: Deal is slang for a signed agreement for services. Contract is the legal agreement that includes terms, payment schedule, SOW, etc.

**Close / Win**: Close the deal means get the contract signed. Win the deal means beat competitors and land the engagement.

## Technical Discovery

Often, as a solution architect, you will need to do _technical discovery_. That is, during the discovery call(s) (step 2) or the opportunity planning (step 3), you will notice that the lead (potential customer) did not express his wishes in concrete technical language. You then need to get to the root of it and make it concrete and technical.

They'll say they need _"better performance"_, but what they actually need is the ability to handle unpredictable traffic spikes during marketing campaigns - which would be elasticity. Or they'll ask for a _"more flexible schema"_, but they're really trying to accelerate feature development by eliminating database schema change approvals.

### The SPIN Discovery Framework

SPIN Selling (Situation, Problem, Implication, Need-payoff) works well for technical discovery:

**Situation Questions**: Understand their current state
- "Walk me through your current data architecture"
- "How are you handling user session data today?"
- "What's your deployment model - on-premises, cloud, or hybrid?"

**Problem Questions**: Identify pain points
- "What challenges are you facing with schema changes?"
- "How do performance issues impact your user experience?"
- "What happens when you need to scale during peak periods?"

**Implication Questions**: Expand the impact of problems
- "How much developer time is spent waiting for schema changes?"
- "What's the business impact when your application can't handle traffic spikes?"
- "How does database complexity affect your time to market for new features?"

**Need-payoff Questions**: Help them visualize the solution
- "How valuable would it be to deploy schema changes without downtime?"
- "What would faster development cycles mean for your competitive advantage?"
- "How would elastic scaling change your infrastructure planning?"

## Value Engineering

A common mistake is to lead with features instead of outcomes. Customers don't buy databases, they buy solutions to business problems. It's all about business value.

### The Business Value Framework

Let's use a database solution as an example here.

**Developer Productivity Impact**: Calculate the time savings from simplified data modeling, reduced schema change overhead, and faster development cycles. If a team of 10 developers saves 2 hours per week each, that's 1,040 hours annually - worth $104,000 at a loaded rate of $100/hour.

**Operational Efficiency Gains**: A modern database's operational simplicity reduces DBA overhead, eliminates complex tuning procedures, and provides built-in high availability. Document the current operational costs and show the reduction.

**Infrastructure Cost Optimization**: Elastic scaling means paying only for resources you use, rather than provisioning for peak capacity. Calculate the difference between peak provisioning and average utilization.

**Revenue Enablement**: Faster time-to-market for new features, improved application performance leading to better user experience, and the ability to handle traffic spikes without outages all directly impact revenue.

**Risk Mitigation Value**: Quantify the cost of downtime, the risk of scalability bottlenecks, and the business impact of slow feature delivery. Built-in resilience and scaling capabilities reduce these risks.

### Creating Compelling Solution Narratives

Every solution needs a story that connects current pain to future success. Here's how to structure your solution narrative:

**Current State (Pain)**: "Today, your development team spends 30% of their time managing database schema changes, your application performance degrades during marketing campaigns, and you can't quickly adapt your data model for new features."

**Desired Future State (Gain)**: "With our solution, your developers focus on building features instead of managing database constraints, your application automatically scales to handle any traffic load, and you can deploy new data models without downtime."

**Technical Bridge**: "Our document model eliminates complex joins, the cloud platform provides elastic scaling, and flexible schema adapts to changing requirements without migrations."

**Business Impact**: "This means 40% faster feature delivery, 99.99% uptime during peak periods, and $200K annual savings in development and infrastructure costs."

### Solution Design Approaches

Once you understand their needs, you can use different approaches for crafting the solution:

**The Reference Architecture Approach**: Start with proven patterns that match their use case. Most vendors have reference architectures for common scenarios like real-time personalization, product catalogs, content management, and IoT data ingestion.

**The Minimally Viable Solution**: Don't over-architect the initial solution. Start with core requirements and plan for evolution. This reduces initial costs and proves value before expanding scope.

**The Migration Strategy Framework**: For displacement opportunities, you need clear migration paths. Plan for parallel running, data synchronization, and gradual cutover strategies that minimize business risk.

**The Integration-First Design**: Modern applications require extensive integration. Design your solution with APIs, event streaming, and data synchronization as first-class concerns.

### Note on PoCs

PoCs can settle the deal. A great PoC can be very convincing and is a strong tool. However, keep in mind that it can also extend sales cycles and consume resources if not managed properly.

## Convincing Work

You will need to convince not just one party but multiple. For example, developers and architects, as well as business stakeholders of your client. They all have different perspectives and you need to make that your focus when communicating with them.

**Developers** care about productivity, simplicity, and modern tooling. Show them how your solution maps naturally to their code, eliminates complex operations, and provides developer-friendly tooling.

**Architects** focus on scalability, reliability, and integration. Demonstrate horizontal scaling, multi-region deployment options, and how your solution fits into their existing technology stack.

**Operations Teams** worry about management overhead, monitoring, and troubleshooting. Show automated operations, built-in monitoring, and operational simplicity compared to their current systems.

**Business Stakeholders** want to understand ROI (Return of Investment), risk mitigation, and competitive advantage. Focus on faster time-to-market, reduced operational costs, and business agility.

### Example Story Structure

Let's look at an example of such a story. This might fit into the pitch (step 5).

**The Developer Productivity Story**: Start with a traditional approach that involves multiple components, complex configurations, and manual processes. Then show your simplified equivalent. For example, instead of managing 5 different systems with complex integration... you have one unified platform that handles everything.

Then demonstrate the power: "Now when you need to make changes, it's a single operation instead of coordinating across multiple systems. When you need to add new capabilities, just configure them - no complex integration required."

**The Scaling and Performance Story**: Show how your solution handles growth from startup to enterprise scale. Start with simple configuration for basic needs, then show how the same platform scales automatically. Demonstrate monitoring and analytics capabilities that provide insight into performance.

Connect this to business value: "When your traffic spikes during product launches, the platform automatically scales. You don't provision for peak capacity - you pay for what you use and scale elastically."

**The Real-Time Analytics Story**: Demonstrate how your solution provides real-time insights and automated responses. Show real data flowing through the system and immediate actionable results.

Connect this to business value: "Instead of waiting for batch processing overnight, you can respond to customer behavior, update inventory, and optimize performance in real-time."

### What to do when something goes wrong?

Technology demos fail. Internet connections drop, services timeout, and Murphy's Law applies. Preparation and recovery strategies separate professional presenters from amateurs.

**Always Have Backups**: Pre-recorded videos of key demo segments, local demo environments, and alternative presentation materials.

**Practice Failure Scenarios**: Know exactly what to do when things go wrong. Have transition phrases ready: "While that's loading, let me show you the architecture behind this capability."

**Turn Failures Into Teaching Moments**: "This actually gives me a chance to show you the automatic failover. Notice how the application continues running even when there are connectivity issues."

**Keep Moving Forward**: Don't spend demo time troubleshooting. Acknowledge the issue, switch to backup materials, and continue the story.

## Competition

In presales, you're not just selling your solution - you're selling it instead of something else. Every deal is competitive, even if competitors aren't explicitly mentioned. You're competing against status quo, alternative solutions, and budget allocation to other priorities.

**Direct Competitors**: Other solutions in your category that solve the same problem. These require head-to-head technical comparison and differentiation.

**Indirect Competitors**: Adjacent solutions or traditional approaches where customers might choose to optimize existing systems instead of adopting new technology.

**Alternative Solutions**: Cloud-native services, in-house development, or completely different architectural approaches to solving the same business problem.

**Status Quo**: The most common competitor - doing nothing, delaying decisions, or working around existing limitations.

### Competitive Positioning

The key to competitive positioning is understanding what your solution does better, not just what it does differently.

**Positioning Strategy**: "Alternative X requires you to know your requirements upfront and design your solution around them. Our approach gives you flexibility - you can adapt to new requirements without restructuring everything."

**Technical Proof Point**: Show complex operations that would require multiple steps or significant custom development with alternatives, but are simple with your solution.

**Business Impact**: "This type of capability helps you respond quickly to market changes. With Alternative X, you'd need multiple development cycles to achieve the same result."

### Handling Competitive Objections

**"Your solution is not [standard/established/proven]"** - This surfaces when you're dealing with newer technology.

Response: "That's exactly why it provides competitive advantage. Established solutions were designed for yesterday's problems. Let me show you what this means for your specific challenges..."

**"We're concerned about vendor lock-in"** - A common enterprise concern.

Response: "I understand that concern about technology dependencies - it's smart planning. What you'll find is that our solution actually provides more flexibility than traditional approaches because of its open architecture. Let me show you three specific portability features..."

**"Alternative X is cheaper"** - Price objections need to be reframed around value.

Response: "That's exactly why Alternative X might not be the right choice for your use case. The lower cost reflects limited capabilities - you're optimizing for price instead of business results. Let me show you what that limitation would mean for your requirements..."

### Advanced Objection Handling

Beyond basic objection responses, use objection handling as relationship building and value demonstration opportunities.

**The Question-Behind-the-Question Method**:
- Customer: "Can your solution handle our transaction volume?"
- Real Question: "Will this scale without breaking our budget or requiring massive operational overhead?"
- Response: "Your question about transaction volume really gets at scalability planning and cost predictability. Let me show you how our platform handles scaling decisions and cost optimization automatically..."

## CRM Systems and Your Workflow

As a solution architect, you'll be living in CRM systems whether you like it or not. Understanding how to use these tools effectively is important for tracking deals, working with sales teams, and showing your impact.

### The Main CRM Players

**Salesforce** is everywhere in enterprise. You'll work with these main areas:
- **Opportunities**: The deals you're working on
- **Accounts**: The companies you're trying to sell to
- **Contacts**: People at those companies
- **Activities**: Meetings, calls, emails, tasks
- **Cases**: Technical questions or issues

**HubSpot** is popular with smaller companies. Similar setup but usually easier to use.

**Microsoft Dynamics** shows up a lot in enterprise, especially if they're already using Microsoft everything.

### What You Need to Do in CRM

**Keep Opportunities Updated**: After talking to customers, update the opportunity with:
- What technical stuff you learned
- Solutions you discussed
- Problems or risks you found
- What happens next
- What you heard about competitors

**Log Your Activities**: Record customer interactions:
- Discovery calls and technical meetings
- Demos and presentations
- Proof of concept work
- Handling technical objections

**Help with Forecasting**: Give your technical opinion on:
- Can we actually build what they want?
- How well does our solution fit their needs?
- How complex will implementation be?
- What could go wrong with this deal?

### Working with Sales Through CRM

**Share Information**: You and the sales rep need to see the same stuff. Use CRM to:
- Share what you learned technically
- Coordinate follow-ups
- Track proposal versions and feedback
- Plan demos together

**Document Handoffs**: When deals close, delivery teams need your notes. Write down:
- Detailed technical requirements
- Assumptions you made
- Who to talk to on the technical side
- Any promises or constraints

**Keep Data Clean**: Update things regularly. Bad data hurts everyone's ability to plan and forecast.

### How to Measure Your Success

You need to know how you're being measured so you can focus on the right things and show your value.

## The Main Metrics

**Win Rate**: Percentage of deals you work on that close. Usually 25-40% is normal for enterprise software. Track your overall rate and break it down by deal size, industry, or solution type.

**Deal Velocity**: How fast deals move when you're involved. Faster usually means better technical qualification. Measure average days from when you first engage to close.

**Average Deal Size**: Your technical skills should enable bigger deals. Compare deal sizes when you're involved versus pure sales deals.

**Pipeline Contribution**: Total value of opportunities where you're actively working. Shows your capacity and business impact.

### Other Important Metrics

**Proposal Win Rate**: Track deals where you wrote or heavily contributed to proposals. This shows your direct impact.

**Technical Assessment Accuracy**: How often you get it right. If you say a deal is "high technical fit" and it closes, good. If deals you mark "low risk" have implementation problems, not good.

**Demo Effectiveness**: How often demos lead to next steps. Good demos should move deals forward and create follow-up meetings.

**Reference Customer Creation**: Your successful deals should become customers who talk to prospects. Track how many become references.

## Stuff That's Harder to Measure But Still Matters

**Technical Credibility**: Customer feedback, internal recognition, requests for your involvement. Look for:
- Customers asking for you specifically in meetings
- Sales reps bringing you into new deals
- People escalating technical questions to you
- Speaking at customer events

**Solution Innovation**: Creating new solutions or using technology in new ways:
- New solution patterns that others start using
- Winning deals where standard approaches wouldn't work
- Customer results that beat expectations

**Knowledge Transfer**: How well you help the sales team learn:
- Sales reps handling basic technical questions without you
- New sales people getting up to speed faster
- More confidence in technical discussions across the team