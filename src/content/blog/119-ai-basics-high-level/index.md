---
title: "AI, GenAI, RAG, Agentic AI: Some Basics, Business View"
summary: "Some basics of AI, GenAI, RAG, and agents, less from a tech viewpoint, more from a business viewpoint"
date: "January 03 2025"
draft: false
tags:
  - AI
  - GenAI
---

# AI, GenAI, RAG, Agentic AI: Some Basics from a Business View

This article covers some basics of AI, GenAI and agentic AI. It's about the tech viewpoint, more about the strategic business viewpoint.

## What's AI, GenAI, Agents?

Let's give a super basic and very high level overview of what these terms mean.

### AI

AI is a very broad umbrella term of anything non-living that is smart. This really can mean a lot, so let's narrow it down to what people mean in 99% of the time when they say _AI_. Most of the times, when someone mentions AI, it's about Deep Learning. This means that we have a _network_ of things, that receievs and input and gives an output. It's basically a huge math formula, just modeled as a _network_. Importat: these networks have _weights_, and the formula only works if the weights are good. Meaning, you can use any numbers as weights, but you will get nonsense output. It doesn't work. However, when you do a lot of training and adjust the weights always a little bit, then the outputs will get better and better. It's kind of like _"solving an equation for x"_, just that we don't have one x, but we have a couple million or even billion. And we are just trying to get _good x's_. 

This process is called training and is what matters. It's very expensive, you need a lot of data (good data!), a lot of processing power (expensive GPUs), and a lot time. The training of ChatGPT cost over 100 million US Dollars. The outcome of the training is called a _model_.

Once the training is done, we can use the model, for whatever we need. An LLM like ChatGPT, or an image classifier, whatever.

### GenAI

GenAI just means Generative AI. The name is very suggestive, it's really just an AI that generates something. So LLMs are GenAIs for example. Or image generation AIs like Midjourney are too. There are important differences between classifier AIs for example and GenAIs, however, I will not go into any technical depth here, so we will just leave it at that.

### AI Workflow

An AI workflow is really nothing more than defining a certain _workflow_ that involves an AI. 

For example, if you ask ChatGPT "what's in my calender tomorrow?", it of course doesn't know the answer. So what you can do is, write a simple program, that first makes an API call to your calender, get's that information, and then asks that question to ChatGPT, but appends the info onto the prompt. A la: "what's in my calender tomorrow? Here is the API response I received: xyz. Please summarize for me". 

This would be a simple AI workflow. Another example would be to let ChatGPT generate a nice poem and updating your website with it every morning at 6 a.m. using a cron job.

### RAG

RAG = Retrieval Augmented Generation. It's a simple concept. You retrieve some data first, then you use that data for generating the output. So a very typical example would be:

#### Company-internal Chatbot

Company A wants a company-internal chatbot that helps their employees get data about products, processes, regulations etc. specific to the company. So esentially, the want to speed up the process of looking through countless Confluence pages or whatever is used in the company. It's a great idea and RAG is perfect use case for this. A little bit simplified, it could work as follows:

1. John Doe asks "how does our product xyz work again?"
2. The chatbot fetches relevant data for this question from a database
3. The chatbot then asks an LLM, such as ChatGPT: "how does our product xyz work again? Here is some related info that you should use for answering the question: [RETRIEVED_INFORMATION]"
4. The bot then sends the LLM output back to John

This is the idea. Of course it's usually a little bit complicated, for example you would do quite a bit of prompt engineering in the bot, plus how do you know what data is relevant in step 2? For the latter, Vector DBs are often used, they allow you to embed text and fetch embeddings that are similar to the embedded version of John's requested info. However, that's another topic.

#### Other Info

So a RAG is just a specific case of an AI workflow and there is actually no magic involved. However, it's still immensely useful. There are countless other examples of how a RAG system helps solve problems, for example a customer care chatbot or even voice bot. 

Note that augmenting your prompt with the retrieved data not only helps providing info that the LLM might not know, it also helps reducing hallucination risk.

### Agentic AI

An agent is again a particular type of AI workflow, however, with a highly important feature. The decision of _what to do next_ is not static, nor by a human, it's up to the AI itself. The AI determines itself what the next step is going to be.

This contrasts with our previous examples, where we had a static flow of, for example, _retrieve data, then feed into LLM, then return to user_. With an agent, there is no such static flow, it's all up to the AI. So in other words, an agent is an AI workflow with decision-making autonomy.

Let's look at examples.

#### Cursor

Cursor is a great example of an agentic AI tool. It's an AI-powered code editor that can understand your codebase and make decisions about what to code next. When you give it a task like "implement a user authentication system", it doesn't just follow a predefined script. Instead, it analyzes your existing code, figures out what files need to be created or modified, and then goes ahead and implements the solution step by step. The key here is that Cursor decides on its own what the next action should be - whether to create a new file, modify an existing one, or even ask you clarifying questions.

But it goes even further than that. If you tell Cursor to "google the latest best practices for React state management", it can actually do that autonomously. It decides what specific search terms to use, how many web pages to crawl through, when it has enough information, and when to stop searching. This is true agentic behavior - you give it a high-level instruction, and it figures out all the steps needed to complete the task.

GitHub Copilot works on the same principle, just with a different scope. It suggests code completions and can generate entire functions based on your context and comments, and similarly can perform web searches and research tasks when needed.

#### AutoGPT and Similar Autonomous Agents

AutoGPT was one of the early examples that really showcased what agentic AI could do. You give it a high-level goal like "research the top 5 competitors in the electric vehicle market and create a report", and it breaks this down into sub-tasks on its own. It might decide to search the web, gather information, create a document structure, fill it with content, and even refine the report based on its own analysis. Each step is decided by the AI itself, not pre-programmed.

#### Customer Service Agents

Modern customer service bots are becoming increasingly agentic. Instead of following rigid decision trees, they can analyze a customer's issue, decide whether to check order status, initiate a refund, escalate to human support, or gather more information. The bot determines the conversation flow based on the customer's needs and company policies, making real-time decisions about next steps.

#### Trading and Investment Agents

Financial institutions are using agentic AI for trading decisions. These agents analyze market data, news, and various indicators, then decide whether to buy, sell, or hold positions. They can also determine when to gather more data, adjust risk parameters, or even temporarily pause trading during volatile conditions. The decision-making autonomy here is crucial because markets move too fast for human intervention in every decision.

---

## AI Infrastructure and Tooling

### LangChain and LangGraph

When you're building AI workflows and agents, you quickly realize you need some proper tooling. That's where frameworks like LangChain come in. Think of LangChain as a toolkit that makes it easier to build complex AI applications. Instead of writing everything from scratch, you get pre-built components for common tasks like connecting to different LLMs, managing conversation memory, or integrating with various data sources.

LangGraph takes this a step further and is specifically designed for building agentic workflows. It lets you define your agent's decision-making process as a graph, where each node represents a different action or decision point. The cool thing is that the AI can navigate this graph dynamically, choosing different paths based on the situation. It's like giving your agent a map of possible actions, but letting it decide which route to take.

Neither is rocket science from a technical standpoint, but they save you a ton of development time and make your AI applications more robust.

### The Blood-Brain Barrier Problem

Here's something that sounds fancy but is actually a very practical issue: the "blood-brain barrier" problem in AI systems. Just like your brain has a barrier that controls what substances can enter, AI systems need barriers that control what information can flow where.

In practical terms, this means you can't just dump all your company's sensitive data into an external AI service like ChatGPT. You need to carefully control what information your AI agents can access, process, and potentially share. This becomes especially tricky with agentic AI, because agents make autonomous decisions about what data to retrieve and use.

Companies are solving this in different ways - some use private AI deployments, others implement strict data filtering and anonymization, and many use hybrid approaches where sensitive operations stay in-house while less critical tasks can use external services.

### Human-in-the-Loop (HITL)

HITL is exactly what it sounds like - keeping humans involved in AI decision-making processes. While agentic AI is powerful, you usually don't want it making every decision completely autonomously, especially for high-stakes situations.

For example, an AI agent handling customer refunds might be able to process standard cases automatically, but anything over $500 or involving special circumstances gets escalated to a human. Or a content generation agent might create draft articles, but a human editor reviews and approves them before publication.

The key is finding the right balance. Too much human involvement and you lose the efficiency benefits of AI. Too little and you risk the AI making decisions you wouldn't be comfortable with. Most successful AI implementations start with heavy human involvement and gradually increase automation as confidence in the system grows.

## Other Important Considerations

### AI Hallucinations and Reliability

One thing that's crucial to understand from a business perspective is that AI systems, especially LLMs, can and will hallucinate - meaning they'll confidently provide information that's completely made up. This isn't a bug, it's just how these systems work. They're designed to be helpful and provide responses, even when they don't actually know the answer.

This is why RAG systems are so valuable - by grounding the AI's responses in actual retrieved data, you significantly reduce hallucination risk. But you can never eliminate it completely.

### Cost Considerations

AI can be expensive, and costs can spiral quickly if you're not careful. Every API call to a service like ChatGPT costs money, and with agentic systems making autonomous decisions about when to call various services, costs can become unpredictable.

The training costs I mentioned earlier (100+ million for ChatGPT) are just the beginning. Running these models, especially for high-volume applications, requires significant ongoing investment in infrastructure and API costs.

### Data Privacy and Compliance

Especially in Europe with GDPR, but really everywhere, data privacy is a huge concern with AI systems. When you send data to external AI services, you're essentially sharing that data with third parties. For many businesses, this is a non-starter for sensitive information.

This is driving the growth of private AI deployments and edge AI solutions, where the AI processing happens on your own infrastructure rather than external services.

### The Competitive Landscape

The AI space moves incredibly fast. What's cutting-edge today might be outdated in six months. From a business strategy perspective, this creates both opportunities and risks. Companies that move too slowly risk being left behind, but those that move too fast might invest in technologies that quickly become obsolete.

The key players are constantly shifting too. OpenAI dominated early with ChatGPT, but now we have strong competitors like Claude (Anthropic), Gemini (Google), and various open-source alternatives. Each has different strengths, pricing models, and capabilities.

### Implementation Strategy

For businesses considering AI adoption, the biggest mistake is trying to boil the ocean. Start small with well-defined use cases where you can measure clear ROI. A customer service chatbot for FAQ handling or a simple document summarization tool are much better starting points than trying to build a comprehensive AI-powered business transformation.

Also, don't underestimate the change management aspect. Your employees need to understand and trust these systems. Training and gradual rollouts are usually more successful than big-bang implementations.

## Wrapping Up

AI, especially in its current GenAI and agentic forms, is genuinely transformative technology. But like any powerful tool, success depends more on how you use it than on the technology itself. The companies winning with AI aren't necessarily the ones with the fanciest tech stack - they're the ones that understand their business problems clearly and apply AI strategically to solve them.

The key is to stay informed about capabilities without getting caught up in the hype, start with clear business cases, and always keep humans in the loop for decisions that matter.