---
title: "Technical Leadership: a modern approach"
summary: "My view of how to lead tech teams in 2025"
date: "February 02 2024"
draft: false
tags:
  - Leadership
---

# Technical Leadership: a modern approach

In this short article, I want to present what I think is the essence of being a (technical) leader in 2025. This is my personal view of course, however, I see that many colleagues in the industry share a very similar view. My leadership experience includes 4 years as a founder and head of architecture of a startup in the social media industry (quite successful IMO, over 200k monthly active users) where I've led over 15 people, project leadership in consulting, and more. 

The article is short because I believe it's best to have few core principles that you enforce consistently, as opposed to enforcing many smaller ones that dilute your focus.

## The Core: Ownership-Driven Leadership

I know "agility" is an overused word and much of it is just hype, but to me, agile leadership is the absolute core of technical leadership. What does this mean in practice? Give people freedom and responsibility - that is _ownership_ - over what they do, and then let them execute. You hired them for a reason. You hired Leon because he is an ML expert. Let him tackle the ML challenges without micromanagement.

But ownership without direction is chaos. For this model to work, you need the right guardrails.

### Vision as Your North Star

Most importantly, you need to ensure everyone knows where the team is headed. And I don't just mean defining a sprint goal, but something deeper. Why do we do what we do? Why are we developing this product? What makes it so good and unique? Why should they be excited to get up Monday morning and drive to work to keep building this thing?

You need to be a salesman. A compelling communicator. You need to sell the vision - not with corporate buzzwords, but with genuine conviction. If you can convince your team that what they're building together actually makes the world a better place, even if just by a tiny bit, that's gold. This, paired with the ownership and freedom you give each team member, will push the team to achieve not just their 100%, but their 200%.

### The Essential Guardrails

You need to embrace open communication and build a genuine feedback culture. You must implement the ownership culture properly - which means knowing when to step back and when to step in. There are certain times where you might still need to provide more direct guidance on a particular process, but that's not the default.

## Making It Real: Frameworks and Implementation

This sounds great in theory, but how do you actually do it? The combination of Scrum and OKRs is designed to achieve precisely this balance. Scrum provides a framework for iterative work and continuous feedback, while Objectives and Key Results give the team clear direction. But frameworks are just tools - the vision communication and culture building parts are on you as the leader.

Here's a concrete example of how I learned to implement this during my time as Founder and Software Architect at SocialHubs.

### SocialHubs: Learning Through Mistakes

This was my first time being a leader, so I made mistakes and learned from them. In the beginning, I employed pretty much waterfall management. Sure, I knew agile methodologies from my previous job, but calling yourself agile and actually being agile are two different things entirely.

I encountered typical issues: "Definition of Done met, ticket complete, rest not my problem" attitudes, siloed thinking where developers would complete their individual tasks without considering the broader system impact, and team members waiting for explicit permission before making obvious improvements that fell outside their assigned tickets.

Then I introduced the ownership-driven approach with proper guardrails. It took time and there were mistakes along the way. Here are some examples with lessons I learned:

#### Lesson 1: Ownership Without Communication is Dangerous

I gave our backend developer complete ownership over refactoring a critical service. He spent two weeks on it and did truly amazing technical work. However, he didn't consider an interoperability issue with other services, which made large parts of his work unusable. We lost significant time due to this isolated ownership approach.

**What we changed:** We introduced "design docs for major changes," usually in the form of Architecture Decision Records (ADRs). This wasn't bureaucracy - the documentation would need to be created eventually anyway. The doc had to be created **and shared** before starting development. To keep everything lightweight and unbureaucratic, there was no formal approval process, the owner could start working immediately. But team members would read the doc and alert the owner if they spotted issues.

#### Lesson 2: Enthusiasm Needs Direction

I gave one developer total control over our notification system. He was so excited about making it "the best notification system ever" that he spent a month building a complex, AI-powered, personalized notification engine. It was technically impressive but completely over-engineered for our actual needs and introduced bugs we didn't have before. Meanwhile, users were still complaining about basic email notifications not working.

**Solution:** We added informal "solution validation" to our process. For any significant feature or change, the developer would need to sync their concrete approach with me or another senior team member before diving deep into implementation.

#### Lesson 3: Technical Excellence Must Serve Business Value

One of my developers was absolutely convinced that Go was the perfect language for our backend and kept pushing for a major rewrite. He provided solid technical arguments, but it would have required enormous resources, so we didn't do it. However, he kept bringing it up to the point where team members were getting annoyed.

So I told him I thought it was actually a great idea and I was interested. However, I explained that we needed to base our decision on business value, not just technical value. I suggested he take a few days to prepare a presentation showing how this would help our business overall, and if he convinced me, we'd do it.

The outcome? During his preparation, he realized that from a business standpoint, it would indeed not make sense given our priorities, budget and constraints. Topic closed, and he was satisfied because he had been heard and had worked through the logic himself.

### The Results

This shift to ownership-driven leadership was a big success for our team, a day and night difference if you ask me. Communicating the vision was the most important aspect, in my opinion. All my employees were also customers who used our apps themselves because they genuinely loved the product. I know this isn't always possible, especially in B2B contexts, but I'd argue this is the ideal state, and this is how we achieved _"the 200%"_ :)

---------------------------------


## Leadership in Complex Ecosystems

While the above examples focus on internal teams, modern technical leadership often extends beyond your immediate team. Let me share how I've adapted this ownership-driven approach to more complex scenarios.

## Leading Client and Mixed Teams

Often, especially in consulting environments, you lead hybrid teams - a mix of your consultants, client employees, and sometimes third-party vendors. The ownership principle still applies, but with nuanced execution.

When working with client teams, I believe in collaborative ownership - pairing consultants with client employees on key initiatives. This isn't about control or mistrust, but about knowledge transfer and capability building. For example, instead of having our data scientist own the AI component alone, they partner with the client's senior analyst as co-owners. This ensures sustainable solutions - the client team gains expertise through hands-on involvement rather than just receiving a handover document at project end. It also keeps them more in the loop, increasing trust and transparency.

Of course, ownership models need to match the context and readiness. Some team members or areas might benefit from more structured guidance initially. For instance, if someone is new to agile methodologies or dealing with a highly regulated component, we might start with more defined processes and gradually increase autonomy as comfort and capability grow.

Note that this is also a great oppurtunity for a gradual transitions: start with pair programming, move to _"supervised ownership"_, and finally to _"proper ownership"_. The key is making this progression transparent and celebrated, so it feels like growth, not surveillance.

## Cross-Functional Leadership

Another interesting aspect is cross-functional teams. Nothing really changes here but, again, it brings nuance.

Leading across disciplines, e.g. designers, data scientists, business strategists, engineers, requires translating vision into multiple "languages". Each discipline has its own success metrics and ways of thinking. And it also typically requires more and a more careful communication.


# Stakeholder Leadership

Talking to stakeholders and executives is no magic, but here are some tips that I've learned over the years.

## Core Communication Principles

- **Speak their language.** They don't care (or know) about the technical details, they are only interested in business outcome.
- **Avoid jargon.** This is not only about the technical side, the technical side just be (in 99% of the cases) extremely simplified and very high-level without jargons, but so should the business and strategical side. There is always a risk of the other person not understanding what you said when you use jargon. And if that's the case, chances are even higher, they won't ask. So strongly avoid using jargon.
- **Ask open ended questions rather than yes/no questions.** Often you want them to speak more than you, you want information from them. By asking open ended questions, this is what you get. Also people like to talk.
- **Pause.** When you pause, it allows them to ask you a question, to share a thought. This is highly important. You want the communication not to be a speech, you want them to partake, so pause.

## Trust Building & Documentation

- **When you get the chance to give a recommendation that would go against your own interest** (e.g. making money), use that chance. Obviously only if it makes sense! But if that's the case, use that chance. They will notice. And that will build immense trust.
- **Use the Pyramid Principle of Minto**
- **Write things down and repeat them at the end.** When you agree on following up on something for example, write it down. This makes them feel better. Just compare it to ordering at a restaurant, when you order with 5 people, everyone has a main dish, snack and drink, that's 15 things, and the waiter doesn't write anything down, nor repeats it at the end... Will you feel confident getting the right things?

## Executive-Specific Considerations

- **Respect their time constraints.** Executives have limited time - be concise, start with the most important points, and always have a clear ask or recommendation ready.
- **Frame around decisions they need to make.** Structure conversations around specific decisions requiring their input, approval, or direction rather than general updates.
- **Adapt your communication style** based on stakeholder type. A CFO cares about financial impact and ROI, a CTO focuses on technical feasibility and architecture, while business unit heads want operational implications and user impact. But what's true for them all is that, in my experience, they want numbers. Concrete numbers. (Some typical metrics would ve ROI, time-to-market, cost-to-serve, SLAs, adoption, etc.)

## Digital Transformation Context

- **Address change management proactively.** Acknowledge stakeholder resistance to new technologies like AI or blockchain, and present clear change management strategies to ease adoption concerns. This is always a big topic.
- **Translate innovation into measurable business value.** Always connect technical innovations to concrete ROI, efficiency gains, or competitive advantages with specific metrics where possible.

## Meeting Leadership

- **When owning a meeting, be prepared, including an agenda.** At the beginning, present the agenda, read it out and ask if that's okay. If they want to change or add something, do that. But once everyone buys into the agenda, that makes a huge difference.
- **When owning a meeting, don't anyone sidetrack you.** When someone asks you about a topic totally unrelated to the agenda, say _"that's a great thought, let me get back to this in 10 min"_. Don't engage with it, you will waste time, maybe not finish the agenda, or other things. ... and, yes, the client's thoughts are always _"great thoughts"_ ;)

Note that some of these principles apply to general client communication as well, but the executive-level considerations become increasingly critical as you move up the organizational hierarchy.

### Stakeholder Mapping

Whether you really map them or not is up to you. But you must know who plays what role. Sponsor (budget owner, signs SOW, ...), champions (influential day-to-day advocates), detractors, and more.

### Some Metrics

Here are some interesting metrics to consider in consulting and transformation projects:

- Knowledge Transfer Velocity: How quickly are client teams becoming self-sufficient?
- Innovation Adoption Rate: What percentage of explored technologies make it to production?
- Cross-Team Collaboration Index: How often do teams spontaneously collaborate without being asked?
- Client Capability Maturity: Can the client continue evolving the solution without us?

But of course there are many others and it always depends on the project.

## Other Minor Things

While the above is the essence, here are some additional things that I believe help in leadership.

### Creativity

Creativity is what gives your team an edge. Encourage trying new approaches, being original, and thinking outside conventional solutions. Create space for experimentation and be genuinely open to ideas from all team members, regardless of seniority. Also, ideas don't just come from senior people. And the team should know that you have this view.

### Commitment

Encourage a culture of full engagement, no half-things. When someone commits to something, they should be all-in. Your job as a leader is to foster an environment that makes this level of commitment both possible and rewarding.

### Trends

As a technical leader, you need to see what's coming around the corner. What technologies, methodologies, or market shifts will impact your team and product? Think forward, anticipate changes, and be willing to experiment and adapt before you're forced to react.

### Be an Example

As the leader you should set high standards. Lead by example.

### Collective Success

It's always the collective team or company success that matters. Not individual success.

### Challenges and Mistakes

Challenges should be seen as chances and mistakes should be seen as learning oppurtunities.

### Intent vs Impact

Finally, I belive it's important to always seek to understand a person's intent before judging their behavior. Often intent and impact are very different.