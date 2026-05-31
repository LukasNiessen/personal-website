---
title: "Modern SaaS, AI, and the Return of Service-Led Deployment"
summary: "How SaaS is moving from low-touch self-service toward AI-assisted enterprise deployment, why this is not entirely new, and how companies can borrow the good parts of consulting without becoming consulting."
date: "May 28 2026"
tags:
  - SaaS
  - AI
  - Forward Deployed Engineer
  - Product Strategy
  - Enterprise Software
  - Palantir
---

# Modern SaaS, AI, and the Return of Service-Led Deployment

There is a shift happening in SaaS right now that I find really interesting. It is not that SaaS is dead, and it is not that every software company should suddenly become a consultancy. That would be the lazy version of the take.

What is happening is more nuanced. For a long time, the ideal SaaS company was built around a very simple economic idea: build the product once, sell it many times, and keep the amount of work per customer as small as possible. This is what made SaaS so powerful. A small team could build software that served thousands or millions of customers, and because the incremental cost of serving one more customer was low, the business could have very high gross margins.

But that was never the entire story, especially in enterprise software. Salesforce, ServiceNow, Workday, Palantir, Databricks and similar companies all show that some of the most important software companies did not avoid implementation complexity. They absorbed it, structured it, productized it, and in many cases turned it into a moat.

The AI boom is making this model relevant for many more companies. Not because AI magically removes implementation work. It does not. But because AI changes the economics of discovery, demos, integration, customization, deployment, and productization. Work that previously required weeks of manual engineering can often be compressed. Work that previously produced one-off code can sometimes become a reusable prompt, agent, tool, connector, evaluation set, workflow template, or implementation playbook.

That is the transition I want to describe.

## The Old SaaS Ideal

The classical SaaS model is easy to explain because the economics are beautiful.

You build one product and sell access to it repeatedly. The customer might configure it a little bit, invite users, connect a few tools, and maybe import some data. But ideally, the vendor does not need to assign engineers to every customer. Ideally, the product sells itself, the onboarding is self-serve, and support does not grow linearly with revenue.

This is the world of **PLG**, or product-led growth. PLG means that the product itself drives acquisition, activation, and expansion. Think of tools where a user can sign up, get value, invite colleagues, and only later trigger a sales conversation. Slack, Notion, Figma, Dropbox, Atlassian in parts of its business, Cursor, and ChatGPT are examples of products with a strong PLG motion.

The business reason this became so attractive is **marginal cost to serve**. Marginal cost means the extra cost of serving one more customer. In a perfect software business, this cost is close to zero. Of course it is never literally zero, because you still pay for infrastructure, support, payment processing, customer success, and so on. But compared to consulting, where every new project needs more people, software can scale extremely well.

This is also why people obsess over **gross margin** in SaaS. Gross margin means: after subtracting the direct cost of delivering the product, how much revenue is left? If a customer pays you 100 EUR and it costs you 20 EUR in hosting, support, and delivery to serve them, your gross margin is 80%. Traditional SaaS businesses often aim for 70-90% gross margin, sometimes even higher depending on the category and accounting.

The startup dream looked like this:

```text
Build product once
    |
    v
Sell to many customers
    |
    v
Small implementation effort per customer
    |
    v
High gross margin
    |
    v
Revenue scales faster than headcount
```

This is what made SaaS so amazing. If the product is good enough and the market is large enough, you can get huge revenue with a relatively small team. That is the magic of software.

But this model also pushes you toward a certain type of product. The workflow should be narrow enough that many customers share the same need. The onboarding should be simple enough that customers can do it themselves or with a small customer success motion. The product should not need a three-month data migration, five legacy integrations, a security architecture workshop, a custom approval workflow, and a steering committee before the first value is delivered.

So the old SaaS ideal was not only a pricing model. It was also a product design philosophy:

- minimize per-customer implementation work
- maximize self-service
- push variation into configuration
- avoid customer-specific code
- keep the product surface narrow enough to scale

This was mostly correct. It produced amazing companies. But it also created a blind spot.

## The Blind Spot

The blind spot is that the largest enterprise problems are often not narrow, clean, and self-serve.

They are messy. They touch existing systems. They involve data quality issues, permissions, compliance, approval processes, politics, process change, and people who have been doing the same thing in Excel for 12 years and do not see why your beautiful product should change that.

This is where pure PLG often breaks down. A lightweight product can be adopted quickly, but it may not reach the deepest workflows. It might sit next to the real system of record rather than replacing or extending it. It might become a useful tool, but not a core operating layer.

And core operating layers are where a lot of the money is.

This is why enterprise software has always had a second model. It is just that Silicon Valley spent a long time pretending this model was less elegant, because it involved services, implementation, and humans.

## The Enterprise Platform Exception Was Always There

Salesforce, ServiceNow, and Workday are important examples of enterprise platform SaaS. They moved a lot of the old on-premise enterprise software complexity into cloud platforms. Customers still needed implementation. Customers still needed migration. Customers still needed workflow design, configuration, integrations, data cleanup, training, permissions, and support. The difference was that this work happened around a shared cloud platform, not around completely separate customer-owned software installations.

[Salesforce](https://www.salesforce.com/platform/) is not just CRM with a few settings. It has custom objects, custom fields, Apex, Flow, AppExchange, MuleSoft, industry clouds, a large admin ecosystem, and a massive implementation partner ecosystem.

[ServiceNow](https://www.servicenow.com/products/now-platform-app-engine.html) is not just IT tickets in the browser. The Now Platform and App Engine are built around custom workflows, low-code applications, orchestration, enterprise integration, and process automation.

[Workday](https://www.workday.com/en-us/products/platform-product-extensions/overview.html) is not just HR in the cloud. Workday Extend exists because large customers want to build custom apps and extensions around Workday's HR and finance core.

These companies did a lot of implementation-heavy work, and that initially creates pressure on the financial model. The a16z article [Trading Margin for Moat](https://a16z.com/services-led-growth/) gives a useful framing here: companies like Salesforce, ServiceNow, and Workday accepted significant implementation, services, and support work, but over time that complexity helped them become deeply embedded enterprise platforms.

This is the important point:

> Enterprise customization is not automatically anti-SaaS. Unbounded bespoke work is anti-SaaS. Governed customization inside a platform can be one of the strongest SaaS moats.

That is a big difference.

If you allow customers to customize anything in any way, you end up with snowflakes. A snowflake customer deployment is unique, fragile, difficult to upgrade, and hard to support. But if you allow customers to customize inside a controlled model, for example through metadata, workflow engines, APIs, extension frameworks, marketplaces, and partner playbooks, you can turn customer-specific needs into platform value.

That is what the best enterprise SaaS companies did.

## The Palantir Model

Palantir is the extreme version of this model and probably the cleanest mental model for the current AI wave.

Palantir did not build a purely self-serve product and wait for users to adopt it. It built platforms like Gotham and Foundry and then sent highly technical people into customer environments to make the software useful for real operational problems. Palantir calls some of these people Forward Deployed Software Engineers, or FDSEs. On its own [careers pages](https://www.palantir.com/careers/students-and-early-talent/), Palantir describes the difference roughly as follows: traditional software engineers sit in product development, while forward deployed engineers work in the business development org and are responsible for technical and operational customer outcomes.

In simpler words:

> The FDE does not only implement what sales already sold. The FDE helps discover what should be built, makes it work in the customer's environment, and feeds the learning back into the platform.

This is not normal consulting, at least not when it works. Consulting usually sells hours or projects. The Palantir-style model uses services to pull the platform into messy reality. The platform is still the center. The customer work is supposed to make the platform better.

The flow looks like this:

```text
Sales-led discovery
    |
    v
Service-led deployment
    |
    v
Custom solution on top of platform
    |
    v
Pattern recognition
    |
    v
Productization
    |
    v
Reusable platform capability
```

This is why I like the phrase **sales-led discovery and service-led deployment**. Sales-led discovery means the GTM motion is not just "here is the product, do you want it?" It is much closer to "show us your painful workflow, let us understand the business process, and let us find the highest-value wedge." Service-led deployment means that the first value often comes through hands-on implementation, integration, and workflow design.

This is very different from pure PLG. But it can still be a software business if the loop ends in productization.

## Why AI Changes the Math

The model is not new. That is important. Salesforce, ServiceNow, Workday, Palantir, SAP, Oracle, and many others already proved that implementation-heavy software can become a huge business.

What is new is that AI changes the cost structure of the messy parts.

It changes demos. Before, showing a customized demo often meant a solutions engineer manually configuring a fake environment, creating sample data, building a custom slide deck, and simulating the customer's workflow. Now, a good technical sales team can often build more specific prototypes much faster. They can generate mock workflows, transform messy sample documents, build lightweight agents, write connectors, and produce a more realistic demo. This does not make selling easy, but it shortens the distance between "I understand your pain" and "here is what solving it could look like."

It changes discovery. A lot of enterprise discovery is listening to how work actually happens, then translating that into systems, data models, permissions, workflows, exceptions, and integrations. AI is useful here because it can summarize calls, compare process descriptions, extract requirements from documents, cluster pain points, and help generate a first version of a target workflow. A human still needs judgment, but the translation layer becomes faster.

It changes implementation. Custom integrations used to involve a lot of boring glue work: reading API docs, mapping fields, writing transformations, generating boilerplate, creating test data, validating edge cases, and documenting everything. AI is surprisingly useful for this type of work. Not perfect, not autonomous in a serious enterprise context, but useful.

It changes productization. This is probably the most important part. When you see the same pattern across several customers, AI can help extract it into a reusable artifact faster. That artifact might be a connector, a workflow template, a prompt, an eval set, an agent skill, a reference architecture, a playbook, or a proper product feature.

It also changes support and customer success. Customer-specific questions can be routed through internal knowledge bases. Implementation documentation can be generated more cheaply. Runbooks can be kept closer to reality. Customer success teams can notice repeated issues earlier.

So no, AI does not remove the hard parts. Context switching still exists. Legacy systems are still legacy systems. Security reviews still happen. Enterprise permissions are still painful. Change management is still change management. But a lot of the non-differentiated work around the hard parts gets cheaper.

The compressed version:

```text
Old SaaS fear:
Customization creates labor, labor destroys margin.

AI-era possibility:
Customization creates learning, AI helps convert learning into reusable product.
```

That is the shift.

## The Economic Trade-Off

To understand why this matters, you need a little bit of startup finance vocabulary.

**ARR** means annual recurring revenue. If a customer pays 10k per month, that is 120k ARR.

**ACV** means annual contract value. This is the yearly value of a particular customer contract. Enterprise deals often have much higher ACV than self-serve deals.

**CAC** means customer acquisition cost. This is what it costs to win a customer, including sales, marketing, sometimes pre-sales, and parts of implementation depending on how the company accounts for it.

**CAC payback** means how long it takes to recover the cost of acquiring the customer from gross profit. If you spend 100k to win a customer and generate 25k gross profit per quarter, your CAC payback is about four quarters.

**COGS** means cost of goods sold. In SaaS, this usually includes hosting, support, customer success, implementation costs that are directly tied to delivery, and sometimes third-party API or inference costs.

**Burn rate** means how much cash the company loses per month. A high-touch implementation model can increase burn if the company hires delivery people faster than revenue and gross profit can support.

**NRR** means net revenue retention. It measures whether existing customers expand or shrink over time. If customers pay you 1m last year and the same cohort pays you 1.3m this year, your NRR is 130%.

These terms matter because the forward-deployed model is basically a trade.

You may accept more COGS and lower gross margin early because you can win larger ACV deals, create stronger customer lock-in, increase NRR, learn faster from the customer, and eventually productize enough of the work to recover software-like margins.

That is why the a16z phrase "trading margin for moat" is a good one. You are accepting some margin pressure now in exchange for a stronger strategic position later.

But this only works if the "later" actually happens.

If the services work never productizes, you just have a services company. Maybe a good services company, but not a SaaS company with SaaS multiples. If the implementation team grows linearly with revenue forever, the company has linear scaling. In normal language: more revenue always requires more people. That is not the SaaS dream.

The good version looks like this:

```text
Year 1:
High implementation effort, lower gross margin, high learning.

Year 2:
Repeatable playbooks, reusable connectors, faster deployments.

Year 3:
Partner ecosystem, productized modules, higher gross margin.

Year 4+:
Platform economics, strong NRR, deep customer moat.
```

The bad version looks like this:

```text
Year 1:
Custom work for every customer.

Year 2:
More custom work for every customer.

Year 3:
More custom work, more support burden, unclear product.

Year 4:
Consulting company with a login page.
```

That is the line you have to watch.

## Why This Is Getting Traction Now

You can see the trend in the market.

a16z has been pushing this framing more explicitly, including the [Trading Margin for Moat](https://a16z.com/services-led-growth/) piece and its broader writing on AI companies looking more like a mix of software and services. Their older article [The New Business of AI](https://a16z.com/the-new-business-of-ai-and-how-its-different-from-traditional-software/) already made the point that many AI companies have lower gross margins than classical SaaS because of compute costs, human support, and edge cases.

OpenAI is also a very strong signal. In May 2026, OpenAI announced the [OpenAI Deployment Company](https://openai.com/index/openai-launches-the-deployment-company/), explicitly built around embedding Forward Deployed Engineers into organizations working on complex problems. OpenAI also has many AI Deployment Engineer and FDE roles listed across its careers pages. That is not a small detail. When a model company creates a deployment company, it tells you that the bottleneck is not only model capability. It is adoption, workflow redesign, integration, and production use.

Anthropic has similar signals. Its [Forward Deployed Engineer](https://www.anthropic.com/careers/jobs/4985877008) role in Applied AI describes people embedding with strategic customers, building production applications with Claude, delivering artifacts like MCP servers and sub-agents, and feeding repeatable deployment patterns back into product and engineering. Again, the pattern is the same: high-touch deployment plus product feedback loop.

Databricks is another example, not because it is the same as Palantir, but because it sits in exactly the enterprise data and AI deployment problem space where platform plus delivery matters. Databricks has a large solutions and partner ecosystem, delivery solution architecture, and a product push around [building, evaluating, deploying, and monitoring enterprise AI agents](https://docs.databricks.com/aws/en/agents). AI on enterprise data is not self-serve in the same way a note-taking app is self-serve.

[Harvey](https://www.harvey.ai/brand/company/careers/24f97125-c406-4ae3-9f94-07dd1310e511) in legal AI, [Decagon](https://openai.com/index/decagon/) and [Maven AGI](https://www.mavenagi.com/resources/forward-deployed-engineers) in customer support, [Striveworks](https://www.striveworks.com/) in operational and defense AI, and many other AI-native companies all point in the same direction. The product is software, but the path to value often requires a serious deployment motion. Sometimes that role is called Forward Deployed Engineer. Sometimes it is solutions architect, implementation engineer, applied AI engineer, deployment strategist, agent PM, customer activation manager, or technical delivery lead. The job title matters less than the function.

The function is:

> Get close enough to the customer workflow that the software can actually do the job.

This is why the trend is getting traction. AI demos are easy. Production AI workflows are hard. The gap between demo and production is where forward-deployed teams live.

## The Benefits

The first benefit is obvious: you can win more deals. If you only sell a narrow self-serve product, you will lose customers whose workflows do not fit the product yet. With a service-led deployment motion, you can listen to the customer's pain points, map their workflow, and shape the solution around the highest-value problem. This increases your available market, especially in enterprise.

The second benefit is bigger ACV. A self-serve tool might start at 20k ARR. A workflow transformation project might start at 300k, 800k, or several million, depending on the customer and the problem. Of course the delivery cost is higher too, but the deal size gives you room to invest.

The third benefit is moat. When your product is wired into the customer's systems, data, permissions, processes, reporting, and employee workflows, it is harder to replace. This is switching cost, and switching cost is a real moat if you keep delivering value. It becomes especially strong when the system becomes the place where work happens, not just where work is reported.

The fourth benefit is expansion. Once you are inside the customer, you see adjacent pain. Maybe you start with support automation and expand into knowledge management. Maybe you start with sales operations and expand into onboarding, forecasting, and account planning. Maybe you start with one department and become the cross-functional operating layer. This is where cross-sell and upsell become natural.

The fifth benefit is product learning. A self-serve product gives you usage data, which is useful. But a forward-deployed motion gives you thick qualitative context. You see why the customer is stuck, where the process breaks, who has political power, what data is missing, and which feature would actually unlock adoption. That is incredibly valuable for product strategy.

The sixth benefit is platform expansion. If you manage the loop well, each customer engagement can add to the platform. You build connectors, templates, evals, tools, reusable agents, reference architectures, migration scripts, and best practices. Over time, what was custom becomes standard.

This is how you can move from a product into a suite, and from a suite into a platform.

## The Downsides

The downside is that this can go wrong in very predictable ways.

The first trap is the consulting trap. You say yes to everything, because every enterprise customer has budget and every sales team wants the deal. Six months later, the product is full of customer-specific promises. Engineering is overloaded. Customer success is confused. Support does not know which customer has which behavior. The roadmap is just a list of escalations. That is not a platform. That is consulting with a subscription invoice.

The second trap is margin collapse. If every new customer needs a large internal team, your COGS grows with revenue. Gross margin stays low, CAC payback becomes unattractive, burn rate increases, and the company becomes harder to finance. It can still grow, but the quality of revenue is worse.

The third trap is product drift. This happens when the company no longer knows what it is building. The customer says "we need X", sales promises X, delivery builds X, and product later tries to explain why X exists. Do this enough times and the core product loses its shape.

The fourth trap is bad lock-in. Good lock-in happens when the customer is deeply embedded because the product delivers value. Bad lock-in happens when the customer cannot leave because the migration is painful, but also does not feel happy staying. That creates resentment, procurement pressure, and eventually replacement projects.

The fifth trap is implementation debt. This is like technical debt, but in the customer environment. A rushed integration, an undocumented workflow, a fragile prompt, a manual runbook, a custom permission exception, a half-productized connector. One or two of these are manageable. Hundreds of them become a tax on the entire company.

The sixth trap is underestimating change management. Enterprise AI is not just "connect model to data". People need to trust it. Processes need to change. Managers need to know how to supervise it. Legal and security need to approve it. The agent needs an escalation path. Metrics need to change. If you ignore this, the product might technically work and still fail.

## The Key Question: Tax or Asset?

This is the most important mental model in the whole topic.

Customization can be a tax or an asset.

It is a tax when it creates one-off work that does not help the next customer. It increases support burden, slows down product development, and makes the company harder to operate.

It is an asset when it teaches you something repeatable. It helps you build a connector, workflow, template, dataset, eval, agent skill, API surface, or product module that makes the next deployment faster.

Same activity, totally different outcome.

The difference is usually not the customer request itself. The difference is how disciplined the company is.

If you have a clear platform vision, you can decide which deviations are allowed. If you do not, every customer can pull you in a different direction. If you have a productization process, custom work feeds the core. If you do not, it stays in the field. If you measure deployment repeatability, you learn. If you only measure bookings, you will accidentally reward chaos.

The practical question for every custom request is:

```text
Does this reveal a repeatable pattern in our ICP,
or is it just paid work for one customer?
```

ICP means ideal customer profile. It is the type of customer you are intentionally building for. A custom request from an ICP customer is much more likely to be signal. A custom request from a random customer outside your market can be very dangerous, even if the contract looks attractive.

This is why customer selection matters so much in service-led deployment. The wrong customer does not only waste delivery time. The wrong customer teaches you the wrong product.

## Anchoring the Company

I think the only way to make this model work is to anchor everything in a strong center.

That center can be a mission, a platform, a workflow thesis, or a very clear product vision. Ideally it is all of them.

You should be able to say:

> This is the kind of work our platform wants to own.

And also:

> This is the kind of work we will not own, even if a customer asks for it.

That second sentence is very important. Without it, service-led deployment becomes unbounded. The company starts optimizing for closed deals instead of compounding product value.

The center gives you a way to judge deviation. Some deviation is good. You need it, otherwise you do not learn from customers. But too much deviation breaks the model.

I would think about it like this:

```text
Low deviation:
Customer uses the standard product with normal configuration.
Great for margin, weak for learning if all customers already look the same.

Medium deviation:
Customer needs custom workflow, integration, or deployment help,
but the pattern clearly fits the platform thesis.
This is often the sweet spot.

High deviation:
Customer needs something far away from the product vision.
Could be worth it for strategic reasons, but dangerous by default.

Extreme deviation:
Basically a custom software project.
This is consulting unless you have a very specific reason.
```

The sweet spot is usually medium deviation. Enough customer specificity to create learning and moat, not so much that you lose the product.

## How To Operate This Model

There are a few practices that make the difference between "this scales" and "this becomes chaos".

First, product and deployment teams need a real feedback loop. The people in the field cannot be treated as a post-sales support function only. They are closest to the workflow. They see the product gaps. They see the repeated patterns. Their learning needs to go back into product quickly.

Second, every deployment should leave artifacts behind. Not just revenue. Artifacts. A connector. A workflow template. A prompt pattern. An evaluation set. A migration script. A runbook. A security checklist. A demo environment. A reference architecture. If nothing reusable remains, ask why.

Third, you need a productization review. After a customer implementation, someone should decide what gets pulled into the platform, what stays customer-specific, and what should never be done again. This can be lightweight, but it must exist.

Fourth, measure deployment efficiency. How long from signed contract to first value? How much engineering time per deployment? How much of the deployment used reusable assets? How many customer-specific exceptions were created? How much work was productized afterward? These are operating metrics, not vanity metrics.

Fifth, automate the services motion. AI should not only be in the customer-facing product. It should also help your own team deploy the product: generating integration code, summarizing discovery, creating test cases, writing docs, comparing workflows, producing migration scripts, and maintaining customer runbooks.

Sixth, build the partner ecosystem when the playbook is mature enough. Salesforce did not scale by doing every implementation forever with only internal people. A partner ecosystem can protect margins and expand capacity, but you need to understand the work yourself before you outsource it.

Seventh, price correctly. If deployment is valuable, charge for it. Free professional services can make early deals easier, but it also hides the true cost of delivery. Sometimes selling services at cost is fine. Sometimes you bundle it. Sometimes you make it a paid implementation package. But do not pretend it is free internally.

## What AI Does Not Change

AI does not change the need for product-market fit. If every customer is different in a deep way, you do not have a software company yet. You have a sequence of projects.

AI does not change the need for architecture. If your platform cannot absorb customer variation, the implementation work will become messy. You need extension points, APIs, permissions, observability, workflow primitives, evals, and a sane data model.

AI does not change the need for trust. Especially in enterprise AI, customers care about accuracy, permissions, audit logs, data leakage, compliance, failure modes, and accountability. A demo can be magical and still not be production-ready.

AI does not change the need for humans. The role of humans changes, but it does not disappear. Humans still do discovery, judgment, architecture, stakeholder management, risk assessment, process redesign, and final accountability.

AI also does not make gross margin irrelevant. This is a common mistake. Yes, in the early stage it may be rational to accept lower gross margin if it helps you win important accounts and build a moat. But eventually the business has to show that revenue can scale faster than delivery headcount. Otherwise the market will value it differently.

## My Current View

My current view is that modern SaaS is becoming less dogmatic.

The last decade over-optimized the idea that the best software company is always self-serve, low-touch, bottoms-up, narrow, and high-margin from day one. That model is still excellent when it fits. I would never argue against it in general.

But AI makes a different model attractive again:

```text
Strong core platform
    |
    v
Sales-led discovery
    |
    v
Service-led deployment
    |
    v
AI-assisted customization and integration
    |
    v
Productization of repeated patterns
    |
    v
Broader platform, stronger moat, better margins over time
```

This model borrows the good parts of consulting: deep customer understanding, workflow ownership, trust, and real business outcomes. But it must not become consulting. The whole point is to turn customer-specific work into product leverage.

If you do it well, you get the upside of both worlds. You can sell larger and more flexible deals. You can handle customers with real complexity. You can build stronger switching costs. You can expand from one workflow into a suite. You can collect better product feedback. And over time, you can keep gross margins relatively high because more and more of the delivery work becomes reusable.

If you do it badly, you get the downside of both worlds. You have SaaS expectations from investors and consulting economics in reality. That is a painful place to be.

## Wrapping Up

The transition in SaaS is not from software to services. It is from one narrow version of SaaS to a broader model where service-led deployment becomes acceptable again, because AI makes the deployment motion more scalable and more productizable.

This model existed before. Salesforce, ServiceNow, Workday, and Palantir already proved different versions of it. What changed is that AI reduces the cost of doing the messy work and increases the speed at which that work can be converted into reusable product.

The winning companies will not be the ones that simply say yes to every customer and call it enterprise AI. They will be the ones with a strong platform center, a clear ICP, disciplined deviation, high-touch deployment where it matters, and a serious productization loop.

In other words:

> Use services to discover the product. Use AI to compress the services. Use productization to recover the margins. Use the resulting workflow ownership as the moat.

That, to me, is the interesting version of modern SaaS.
