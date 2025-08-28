---
title: "Lessons Learned in my IT Carreer: SWE, Software Architect, Startup CEO, Presales"
summary: "This is a collection of some lessons I've learned in my nearly 10 years in the IT"
date: "Jul 30 2025"
draft: false
xLink: "/https://x.com/iamlukasniessen/status/"
linkedInLink: "https://www.linkedin.com/pulse/"
tags:
  - IT
  - Lessons
  - Carreer
  - Advice
---

# Lessons Learned in my IT Carreer: SWE, Software Architect, Startup CEO, Presales

This is a collection of some lessons I've learned in my nearly 10 years in the IT. I was a software engineer, software archiect, founder and CEO, in presales and more. None of these lessons is anything new, you can find most, or even all of them, in books for example. The interesting part here is the story and the impact behind each lesson.

Would love to hear your thoughts and stories of yours in the comments :)

## CI/CD is not just faster

In a start up, we were always thinking about adding a CI/CD pipeline to the repository. We knew it’s best practice, we knew it’s going to save time, and we knew that if we actually want to do continuous integration and continuous delivery, then you need a pipe line - triggering tests, building, linting, deployment etc manually with each commit is just not feasible timewise. However, we also knew that setting it up would take a little bit of time, so we always postponed it. Then, one day, we made a manual deployment late night, and the guy responsible got a configuration (a parameter) wrong. Due to that, our users did not have profiles for a few hours, until we released the patch. Lesson learned, it’s not just about saving time, it also prevents mistakes. Of course, this is not a new lesson, there is the famous very similar Knight Capital Group story, but it was a different thing to experience it yourself, as opposed to just reading a story about it online.

## Tests are about Evolvability

Again, in the same start-up, for time to market reasons, we skipped tests. We did not write any. We were very well aware, that this is bad practice and that we would have to pay the price of introducing some bugs to production here and there. However we did not know that the tests will not only catch bugs and errors, a test suite also makes your app evolve. And I would argue that it is probably the only way to make your app evolve. When you modify code, that was written a year ago for example, how on earth can you know that you will not break something. You cannot know, because you don’t know all the requirements of the function/…, you don’t know all the dependencies and so on. Even if you have good documentation. So we were always "scared" to touch old code. Lesson learned, there only way to know, and to not be scared, is to have a good and comprehensive test suite in place. Again, this is obviously not a new lesson, some authors such as Michael Feathers or Martin Fowler go as far as even defining legacy code via this, they define legacy code as code that is not well tested. However, also here, experiencing it yourself is a complete different story than reading it in a book.

As a side note, I learned this lesson again in my consulting time, however, this time on an architectural level. It's the same story, if you don't have tests that validate your architecture and architectural decisions, evolving it is very hard. Fitness functions solve that, and there is an entire book about this and more ideas by Neal Ford et al. The famous library ArchUnit library helps writing architecture tests for Java projects, and I went as far, as writing my own ArchUnit library, but for TypeScript: [ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS).

## Push-based GitOps is not GitOps

Here is a super quick reminder of what GitOps is: GitOps means we use Git as the single source of truth for everything. Not just for your code, but also for your infrastructure, configuration, and deployment processes too. There is _push-based GitOps_, meaning your code changes need to be applied (manually or pipeline for example), _pull-based GitOps_, meaning that changes to your code will be auto synced from the cluster side, they will be _pulled_. However, note that many people see push-based GitOps as not actually being GitOps. For a better explanation, please see more [here](https://lukasniessen.com/blog/109-git-ops/).

So we had this microservices architecture, running on AWS EKS, and all infra was managed as IaC with Terraform. Changes would be applied in the CI/CD pipeline when a branch was merged into main. Now, here the issue. Our DevOps guy was on vacation and we ran into performance problems, so a backend developer on-call made a quick fix by manually increasing the memory limits directly in Kubernetes using `kubectl edit`. Problem solved, everyone was happy. A week later, our DevOps engineer returned and needed to deploy a security patch across all services. He updated the base Helm chart template, merged it, and the pipeline ran. Within minutes, we had issues again, and the service with the memory leak was crashing again. That's because the deployment had reset the memory to the original limits from Git. The big issue here was just, we just didn't understand why a "simple security patch" had this effect and the service was not working for a couple hours. 

Now, you can draw many lessons from this of course. This could have been prevented by clear communication and clear documentation. However, whenever you do push-based _"GitOps"_, the risk of something like this happening is always there. You need very clear and strict rules of how to make any changes to production. Pull-based GitOps solves this, and we learned the lesson, to finally take the time and set it up (we used ArgoCD). As a side note, it has another big advantage, the repository has less rights over the cluster, which is a big win from a security standpoint.

## Other Lessons

I want to append some other lessons with a less elaborate story, some of these are not as _objectively-true_ as the above ones, but more reflect my personal conclusions.

### Documentation is also about the Why

There are many people making the case for writing little comments, with the idea of _good code is self-explaining, self-documenting_, a la Clean Code by Uncle Bob. While I strongly disagree with actually practicing that approach, even if you do it, you still haven't documented _why_ a certain decision was made, why an algorithm, technology or architecture was picked. We had great or semi-great documentation in the startup. Just, usually, without the why. And that became an issue - not only did people leave, but often they even just didn't remember. That was not so nice and we learned our lesson. (Architecture Decision Records are a common format one can choose for documenting also the _why_)

### The Mythical Man-Month is Real

This is one of the oldest lessons of course, but I also experienced it. On-boarding effort scales with depth into a project, more communication overhead and other reasons. Devs and especially managers should be aware of this.

### Better to be Wrong Today than to be Wrong Tomorrow

If you make a mistake today, you will need to adapt to it, maybe refactor things, adapt processes, whatever it is. However, if you postpone the decision, and you make the mistake later, there is more things that will need fixing. Potentially much more. Better do it early and learn from the feedback.

### Better to be Wrong Today than to be Wrong Tomorrow

This is about the cost of mistakes over time. Making a mistake early in a project is a learning opportunity with a low(er) cost. You can quickly adapt, refactor, and correct your course before the problem grows.

However, if you postpone a decision or delay a test, the cost of being wrong later increases. By the time a flaw is discovered, it may be deeply embedded in the system, affecting many different parts. Fixing it would then require far more effort compared to the simple correction it would have been at the beginning. So, make a decision, get feedback, and be ready to pivot quickly.

### It's about the Business Value

It's not about stacking techinical solutions, about following tech trends. Often the best solution is the simplest. It's about business outcome. 

While these advices may seem obvious, just consider microservices. There are endless stories where companies just jumped on the hype train and would have been far better off with just sticking to the monolith (or service-based architecture). So with every decision, just keep in mind, it's not about the IT, it's about the business. Keep it simple where ever you can.

### Product-led Growth

Another thing I've learned is that a quick win is not what you should strive for. Always go for the long win. Offer genuinely good services or apps, be prepared to say no, and that will go far longer ways.

### How to lead a Team? Agile

This is a very personal lesson again, but IMO the best way to lead a team or a project, is agility (responding to change over following a plan), paired with ownership culture and feedback culture, as well as communicating the (technical) vision well, is what allows a team to reach its 100%, maybe even its 200%.