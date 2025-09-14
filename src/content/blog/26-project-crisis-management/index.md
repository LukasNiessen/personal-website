---
title: "When Projects Go Sideways: Managing Crisis Situations"
summary: "How to handle unexpected problems, stakeholder panic, and last-minute changes without derailing your project"
date: "Jan 1 1970"
draft: false
tags:
  - Project Management
  - Crisis Management
  - Consulting
  - Leadership
---

# When Projects Go Sideways: Managing Crisis Situations

Two weeks before go-live, you get the call: "Oh, by the way, we have this security requirement that's mandatory." Or "The compliance team just told us this approach won't work." What do you do then?

This article is about handling crisis situations when projects go sideways. I'll share what I've learned from my own mistakes.

## Projects Often Have Crisis Moments

The difference between a good project and a disaster is how you handle these moments.

The types of problems I've seen:
- New requirements that appear out of nowhere
- Key people leaving at the worst possible time
- Integration failures that nobody saw coming
- Stakeholder panic when executives get involved

You can't prevent all of these, but you can get better at handling them.

## What to Do When Everything Goes Wrong

When things go sideways, your first instinct is probably to dive into the technical problem and try to fix it immediately. I used to do this too. It's the wrong approach.

Here's what I do now:

### Stop and Figure Out What's Actually Happening

Don't react immediately. I know it's hard when people are panicking, but take an hour to understand the real problem. Ask these questions:
- What exactly broke? (Not what people think broke)
- Who needs to be involved?
- What's the real deadline? (Often more flexible than people claim)
- What are our options?

### Tell People About Problems Early

This is counterintuitive, but tell your stakeholders about problems quickly, not after you've solved them. I learned this the hard way. When you surprise people with problems, they lose trust. When you surprise them with solutions, they still lose trust because they wonder what else you're not telling them.

The phrase I use: "We've identified an issue that may impact our timeline. I'm working on solutions and will have an update for you by [specific time]."

### Think About More Options

When you're in crisis mode, you tunnel vision on the obvious solutions. Force yourself to think of alternatives:
- Can we reduce scope?
- Can we deliver in phases?
- Can we work around the problem temporarily?
- Who else has solved this before?

### Communicate More, Not Less

Once you have a plan, update people frequently. If you normally send weekly updates, make them daily. If they're daily, make them twice daily. People can handle problems, they can't handle silence.

## A Story: Security Requirements That Appeared Two Weeks Before Go-Live

Let me tell you about a GitOps transformation I was leading. We were moving a client from manual deployments to automated Infrastructure as Code with ArgoCD. Everything was going well until two weeks before production.

Then the client's security team dropped this on us: "All inter-service communication requires mTLS authentication. It's been mandatory for months, but somehow this didn't get communicated to your team."

Our entire deployment pipeline would fail in production. None of our applications had the necessary certificates.

### What I Did

So this of course caught me off guard and I wasn't very happy. However, I know from my own experience as CEO for example, things like that happen. Even way more unexpected stuff happens. And 2 weeks isn't too bad, fortunately it wasn't 2 days or so. So I focused on choosing the correct next steps.

What I did first is assess the situation. Do we really have to have in the go live? I immediately met with the security contact guy and cleared questions up. What certificates? Which authority? What's the timeline? Can anything be phased?

Since we did have to have it, I escalated this right after, directly notifying key stakeholders (CTO and IT director). "We've discovered a security requirement that will impact our go-live date. I'm working on options and will have a full assessment by tomorrow morning in a stakeholder emergency meeting".

Again, such things are obviously no pleasant news, but quite normal actually. So I knew the most important thing would be to keep everyone confident in the success of the project, avoid any panic, and avoid team conflicts. So for the stakeholder meeting I prepared a list of possible next steps, each with the respective tradeoffs.

What we ended up doing was to delay a certain operational improvement that we were working on and instead funneled all our energy into implementing this. It's possible in 2 weeks, especially since I have experience with service meshes. The tradeoff was just to delay the other thing. Another option would be of course to delay the go live, but that was not wished by the stakeholders. 

### What Would I Change?

- Periodically syncing with key security and compliance personnel, even just for a quick check-in, might have prevented this situation

- I didn't keep the development team in the loop; involving them earlier for collaboration and sparring on ideas might have been more effective. While it wasn't a major issue, it's always better for a team to be involved in the process from the beginning rather than just receiving an order suddenly. They feel better and strongly boosts the team dynamic and efficiency.

