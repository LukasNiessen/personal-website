---
title: 'Presales: How to Handle Questions During Demos - A Framework'
summary: 'A practical framework for answering questions during technical demos without losing momentum or credibility'
date: 'May 24 2025'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Presales
  - Demo
  - Technical Validation
  - Framework
---

# Presales: How to Handle Questions During Demos - A Framework

Handling questions during technical demos is critical in presales. A well-answered question builds credibility and moves deals forward. A poorly handled question can derail your entire presentation. Over years of running demos, I've developed a framework that maintains control while building trust with technical audiences.

## The STAR Framework for Demo Questions

I use a modified STAR framework specifically for demo environments:

**S - Stop and Acknowledge**  
**T - Test for Understanding**  
**A - Answer Appropriately**  
**R - Return to Flow**

### Stop and Acknowledge

Stop what you're doing completely. Make eye contact with the questioner. Use their name if you know it.

"Good question, Marcus" or "That's exactly the kind of implementation detail we should discuss, Sarah."

This shows respect for the question and gives you time to process what they're really asking.

### Test for Understanding

Make sure you understand both the question and the context behind it. Often the surface question isn't the real concern.

**First, repeat or rephrase the question** so everyone in the room hears it clearly and you buy yourself thinking time:

"So you're asking about how this handles failover in a multi-region setup - is that right?"

**Then ask clarifying questions** to understand the real concern:

"When you mention multi-region, are you specifically thinking about your AWS and GCP deployment scenario?"

"What's driving that concern - is it about data consistency, performance, or compliance requirements?"

This clarifies the question, shows you're listening carefully, and often reveals the real concern underneath. The person asking usually appreciates that you're taking their question seriously.

### Answer Appropriately

Match your answer depth to both the questioner and the audience. I use four answer types:

**Quick Clarification** - For simple factual questions.  
"Yes, Vault PKI supports custom TTL policies down to 30-second certificates if needed."

**Contextual Demo** - When you can show something in your current demo.  
"Let me show you exactly how that works. If I navigate to the Vault UI here..."

**Detailed Technical** - For complex questions requiring thorough explanation.  
"That's a great question about certificate chain validation. There are three key components..."

**Parking Lot** - For questions that would derail current flow.  
"That's an important integration question. Can we come back to that after I show you the core workflow?"

### Return to Flow

After answering, smoothly transition back to your demo narrative. Connect your answer to what you're about to show:

"So as Marcus pointed out, failover handling is crucial. What I'm about to demonstrate next ties directly into that - you'll see how the GitOps workflow maintains consistency even during infrastructure failures."

## Handling Difficult Questions

### The Knowledge Test
Be honest about what you know. If you don't know something, say so and explain how you'd find out.

"I don't have those exact benchmarks memorized, but I can connect you with our solutions engineering team who ran similar tests. Would that be helpful?"

### The Comparison Question
Acknowledge the alternative's strengths first, then differentiate based on their specific requirements.

"CDK is solid for AWS-native deployments. The key difference for your multi-cloud setup is that Terraform gives you consistent patterns across both AWS and GCP."

### The Hostile Question
Stay calm, acknowledge their perspective, then redirect to business value.

"I understand that perspective. The question is whether maintaining bash scripts across 35 services is worth the initial simplicity. Let me show you what maintenance looks like with our approach..."

## Common Mistakes to Avoid

Don't guess if you don't know - your credibility matters more than appearing omniscient. Don't get defensive with hostile questions. Don't let one question derail your entire demo flow. Don't rush your answers - taking a moment to think is better than giving a poor response quickly.

## Conclusion

The STAR framework gives you systematic control while building credibility. Questions are opportunities to address concerns directly and strengthen your position. Practice this framework in your next demo, and questions will become less stressful and more valuable for moving deals forward.

## Even Better

4Ps for question management - Pause, Paraphrase, Probe, and THEN Provide the answer to a customers question. Probe here is asking follow up questions if needed, uncovering the why. The question behind the question.