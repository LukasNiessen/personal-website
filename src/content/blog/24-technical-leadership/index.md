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

### Intent vs Impact

Finally, I belive it's important to always seek to understand a person's intent before judging their behavior. Often intent and impact are very different.