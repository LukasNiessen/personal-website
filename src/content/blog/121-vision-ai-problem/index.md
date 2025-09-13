---
title: "NSFW content detection via AI: How we solved it in my startup"
summary: "Here is exactly how we tackled detecting NSFW content using AI in my startup SocialHubs UG"
date: "January 04 2025"
draft: false
tags:
  - AI
---

# NSFW content detection via AI: How we solved it in my startup

This article is about how we tackled detecting NSFW content using AI in my startup SocialHubs UG. Please note, it **was** my startup, I founded it and led it for 4 years, then I exit and sold all my shares. 

I will largely skip implementation details, this article is focused on the architectural and strategical business viewpoint.

## Situation & Task

We ran social media apps (meaning dev. and operating), about 30,000 monthly active users at that point. Content moderation is a big issue in this field and we did have the classical reporting mechanism in place. However, there was a fraction of users posting really malicious stuff daily (nudity and violence) and even though it got taken down, it always took a while because we relied on our moderators reviewieng it and then taking action. This wouldn't be a huge thing for posts that violate rules such as impersonation, but it definitely is for disturbing images. So we needed a way to dramatically speed this up.

Note that our competitors had this problem too.

## First Solution

We looked into AI for this matter - this was around the beginning of 2022, so before the ChatGPT induced AI boom, however AI was a huge thing already obviously. Since we were running on GCP, we looked at Google Vision AI, which is a SaaS product of GCP that allows you to simply "feed" an image to it, and the API returns "adult," "violence," "medical," and "spoof." It also returns a likelihood value for each category (e.g., VERY_UNLIKELY, LIKELY), allowing you to set your own thresholds for content moderation. 

This is exactly what we needed, and on top of that, it was the easiest set up in the world: we just added a Cloud Function (FaaS, Lambda in AWS) that would be triggered on each image upload to Google Cloud Storage (S3 in AWS) and feed the image to the Vision API. If it detected nudity or violence, we would simply delete the image from the Storage Bucket. We didn't even need to implement authentication since it was running in GCP. So we got this up and running in an hour or so.

### Notes

1. You're right, it's not perfect. By just deleting the image from the bucket, we created a non-ideal UX: the image would just not load. No feedback to the user, no feedback to the creator even. We put items for that in our backlog.

2. AWS and Azure have similar services (AWS Rekognition and Azure AI Content Safety).

### The Problem

This worked and was an amazing and very quick fix, however, it was very expensive. We payed 7,000 EUR for just this in the first month after adding it, which made it the largest part of our cloud bill. This needed to be addressed immediately.

## Clean Slate

This was our first response, a simple and not too interesting one, so I will keep it short. It was highly effective though.

We created a _clean slate_ system: users that _"built trust"_ will not need the AI check. We will let them post pass without throwing the Vision API at their uploads. The more posts you had and the longer you have been on the app, **without causing trouble**, the less likely your posts were to be checked. And _causing trouble_ means having made a post that we later took down.

The vast majority of posts came from _clean slate-users_, so this reduced the Vision AI expenses immensely - IIRC it reduced it to about a tenth.

The logic was simple, we just stored `made-posts-count` and `made-bad-posts-count` in Firestore (comparable to AWS Dynamo DB), retrieved that info, plus how long the user was on the app, in the Cloud Function and passed the values into a formular. Depending on the _trust-score_ that was returned, we _escalated_ the image to Vision API or we didn't.

## Escalation Approach

However, we wanted to reduce the costs further, so we took the _escalation-approach_ of the clean slate even further. This is where things got really interesting from a technical standpoint.

### Custom Model Training

We decided to train our own custom models to detect NSFW content and violence. We went with a two-pronged approach: a full-sized model for server-side inference and a lightweight version for on-device inferece.

For the architecture, we chose **MobileNetV2** as our base model instead of ResNet. Why? ResNet is great for accuracy but it's heavy - not ideal for mobile devices. MobileNetV2 was specifically designed for mobile and embedded vision applications, using depthwise separable convolutions that dramatically reduce the number of parameters while maintaining decent accuracy. For the lite version, we used quantization techniques to compress the model even further, reducing it from ~14MB to about 3MB.

The lite version wasn't bundled into the app - we made it downloadable when users first navigated to the posting screen. This kept our app size manageable while still providing the performance benefits.

### The Multi-Layer Detection Pipeline

Here's how our escalated detection system worked:

1. **On-device inference**: When a user posts, we ran the image through the lite MobileNetV2 model directly on their device. If it flagged the content with high confidence (I think we used 0.9 as a treshold, meaning 9% confidence), we immediately showed an error message explaining why the content couldn't be posted, with clear instructions on how to contact us if they believed it was a false positive.

2. **Upload and trust check**: If the on-device check passed, the image uploaded to our GCS bucket, triggering our Cloud Function. This function first performed the "clean slate" trust score calculation.

3. **Custom model escalation**: If the trust score was low, we escalated to our full-sized custom model running on Google Cloud Run. This model was more accurate than the lite version and could catch cases the on-device version missed. If this model was confident (again I think we used 0.9) that the content violated our policies, we deleted the image and updated the post data for proper UI feedback.

4. **Human-in-the-loop (HITL)**: If our custom model detected potential violations but with lower confidence, we escalated further, meaning the system automatically reported the post after, so that it would appear in our reporting center where a human would review it soon.

This approach reduced our AI-related costs by almost 99% compared to the pure Google Vision AI solution, bringing our monthly bill down from €7,000 to about €100 per month. So the cost metric was great, but this approach was equally effective as the overblown initial _everything-check_ approach, so this was a great success.

### Video Content Handling

For videos, we took a sampling approach. We extracted the thumbnail plus 1-2 additional frames (depending on video length) and fed these static images through our detection pipeline. For videos under 30 seconds, we sampled one additional frame at the midpoint. For longer videos, we sampled frames at 25% and 75% positions. This gave us reasonable coverage without the computational overhead of processing entire video streams.

### Training Process and Costs

Why build a custom model instead of sticking with Google Vision AI? Economics and control. 

We used TensorFlow for our training pipeline, leveraging several great Kaggle datasets focused on NSFW detection and violence classification. The training itself was done on Google Cloud AI Platform (now Vertex AI), using their managed training jobs with GPU acceleration.

**The numbers**: Training cost us about €800 for the full dataset (including hyperparameter tuning and multiple model iterations), and the entire development process took us roughly 3 weeks - 1 week for data preparation and model training, and another 2 weeks for integration and testing. Compare that to our monthly €7,000 Google Vision AI bill, and you can see why this was a no-brainer from a financial perspective.

## Issues We Faced

While the technical delivery went relatively smoothly, we encountered significant challenges within our team dynamics and decision-making process. The main technical issues were minor - some initial false positives with artistic nude photography that we resolved by fine-tuning our confidence thresholds, and occasional model download failures on slower mobile connections that we fixed with better retry logic.

The real drama happened in our team discussions.

### The Great "Make vs Buy" Debate

Our small engineering team found itself in an interesting position. We didn't have a dedicated ML engineer - just a few passionate developers who had been diving deep into machine learning (including hands on pet projects) in their spare time, including me, plus one guy who had worked as a fullstack developer but had previous ML experience from a previous role. That made him our go-to person for anything ML-related.

We had our differences when it came to this decision. One of our backend engineers was naturally cautious about taking on something this complex when we had a working solution, even if it was expensive. His main concern was simple, along the lines of: "We're a small team, we have a hundred other priorities, and this Google thing actually works."

The developer with ML background was more optimistic about building something custom. He'd point out during our weekly engineering meetings that the problem wasn't that technically complex, and he'd been looking at some of the available datasets. His argument was basically: "I think we can do this, and the cost savings would be massive".

At some point, every time I got myself a coffee and saw these two there, they would debate this issue, and let's just say, both didn't look happy. As the _"boss"_, I had to make sure we resolve this in a way that all parties are happy and agree on the solution. No one should feel left out, and it should happen soon. So I asked the ML guy to take a couple hours and prepare a little presentation including a small PoC, similarly, I told the other camp to prepare their arguments, so we can have a decision workshop. I told both sides, the business viewpoint is the only thing that matters here. When the debate took place we let both sides speak, we gathered pros and cons on a white board and made this meeting as interactive as possible (when you participate in something and invest effort, you automatically have some attachment and interest in the outcome of it), I wanted **everyone** to participate. I made sure to strongly acknowledge the arguments of both sides, this is cruicial so they all feel heard.

**Pros and Cons from our whiteboard session:**

**Build Custom Model - Pros:**
- Massive cost savings (€6,900/month potential savings)
- We'd gain ML expertise that's already on our roadmap anyway (recommendation algorithms, user behavior analysis)
- Full control over detection logic and thresholds
- Could be done relatively quickly in startup fashion - MVP in 2-3 weeks
- Strong PoC already showing promising results

**Build Custom Model - Cons:**
- Technical risk - what if it doesn't work as well?
- Takes engineering time away from other features
- We become responsible for maintaining it

**Stick with Google Vision AI - Pros:**
- Zero technical risk - it works today
- No engineering time investment
- Google's model is probably more sophisticated than anything we could build quickly

**Stick with Google Vision AI - Cons:**
- Unsustainable cost trajectory (€7k/month)
- Zero learning for our team
- No control over detection logic
- Missing opportunity to build ML capabilities we need anyway

The key insight was that ML capabilities were already on our roadmap for other features like recommendation algorithms and user engagement optimization. Building this content moderation system would give us the foundation and team experience we'd need for those future projects anyway.

We ran both options through a lightweight decision framework, and the numbers plus strategic fit made the "build" option pretty compelling. The 2-week MVP timeline plus solid PoC results sealed the deal.

Note that change management was not an issue here, we didn't have to _"force"_ anyone into building this solution, it was all done by the ML guy and another developer that was more than happy to do it.

### KPIs

We approached this project systematically, establishing clear success metrics upfront:

**Primary KPIs:**
- **Cost reduction**: Target 90% reduction in AI-related expenses
- **Response time**: Maintain < 1 second average detection time for the on-device lite model (on-server inference can take a little longer, user will not notice)
- **Accuracy**: Achieve >95% precision (minimize false positives) and >90% recall (catch actual violations)

## Key Takeaways

Looking back at this project, here are the main lessons I'd share with others facing similar challenges:

1. **Don't optimize prematurely, but act fast when costs become unsustainable**. Google Vision AI was the right choice initially - it got us to market quickly. But when it started eating 40% of our cloud budget, we had to move fast.

2. **Hybrid approaches often work better than extremes**. Pure SaaS vs pure custom build is a false dichotomy. Our combination of trust scoring, on-device inference, custom models, and HITL gave us the best of all worlds.

3. **Team dynamics matter as much as technical decisions**. The "make vs buy" debate revealed deeper tensions about technical ownership and risk tolerance. Address these early and transparently.

4. **Measure everything, but focus on business impact**. Technical metrics like accuracy are important, but the real success was maintaining user experience while dramatically reducing costs.

For any startup dealing with content moderation at scale, this escalated approach might be worth considering. The initial investment pays for itself quickly, and you gain valuable control over your moderation pipeline - something that becomes increasingly important as you scale.