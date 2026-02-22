---
title: "Teams in IT: How to Structure, Scale and Not Lose Your Mind"
summary: "How team structures shape the software you build, why Conway's Law still matters, and what strong ownership, platform teams and autonomy actually look like in practice"
date: "Feb 21 2026"
tags:
  - IT
  - Teams
  - Architecture
  - Organization
---

# Building My Own AI Research Assistant

I'm building my own AI chatbot to search for research papers. Two reasons: Hands-on learning and Vertical utility.

I'm starting a new "toy project" that I fully intend to use in my daily life. The goal is to build an automated, AI-powered arXiv research assistant that tracks, summarizes, and chats with me about the latest AI research papers.

Here's a look at what I'm building, how it works, and the tech stack I'm using.

## How It Works: The Architecture

At its core, the application is designed to automatically ingest new knowledge and make it highly searchable.

### The Data Pipeline (Cron Jobs):

A scheduled job will monitor arXiv (and potentially other sources) for newly published AI papers.
Metadata & Summarization: When a new paper drops, the system grabs the metadata (title, authors, ID, PDF link). I will then use an LLM to generate a concise summary of the paper's abstract and findings.

### Vector Search:

That summary isn't just saved as text. It will be passed through an embedding model and stored in a vector database.
The Chat Interface: The user (me) can ask the chatbot something like, "What are the latest techniques in prompt engineering?"
The RAG Magic: The system will convert my prompt into a vector, do a semantic search against the database to find the most relevant papers, and an LLM will synthesize an answer, providing me with a summary and direct links to the source papers.

### The Tech Stack

I'll be hosting this on my personal homepage, with the infrastructure running on AWS.

For the backend, I've chosen Python and FastAPI. Why Python? If we were talking about pure enterprise CRUD applications, a Java/Spring Boot stack might have an edge in maturity and static typing. However, Python is the undisputed king of the AI ecosystem. It has the best framework support, and because it is so widely used in AI, LLMs are incredibly good at writing and debugging Python code. Plus, FastAPI (with Pydantic) provides excellent type safety and validation, making it more than robust enough for this use case.

For the database, I'll be using PostgreSQL with the pgvector extension, keeping my relational metadata and vector embeddings in one unified place.

## Advanced Features on the Roadmap

Getting a basic RAG system up and running is step one. But I want to push this further with advanced Information Retrieval (IR) techniques:

**Temporal RAG:** AI moves fast. A paper from 2024 is usually more relevant than a paper from 2021. I plan to implement temporal weighting so newer papers get a higher relevance score.

**Citation Weighting:** Down the line, I'd like to integrate citation tracking to surface highly influential papers.
C-RAG (Corrective RAG): I want to introduce an agentic evaluation step. If the retrieved papers don't properly answer my prompt, the system should realize this and rewrite the query or fall back to a live web search.

**Prompt/LLM Caching:** To save on token inference costs, I'll be implementing a caching layer for frequent queries.

## Why This Matters

Even though generic LLMs can do similar things, building a highly specialized, vertical RAG system ensures fewer hallucinations and grounds the AI entirely in actual scientific literature.

---

I will try to ship this ASAP - speed trumps super-high-quality and any form of "compliance" in this project. I will make this accessible for anyone, but for obvious reasons, I will put heavy rate limits on the use. Finally, there will be updates, ADRs, diagrams and similar things coming soon.
