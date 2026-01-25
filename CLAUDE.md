# Blog Writing Workflow

When you see: `blog: [specification]`

Whatever follows `blog: ` gets passed as the article specification. This can be:
- A simple topic: `blog: caching strategies`
- A detailed specification with context: `blog: article about API versioning, but focus on the problem with timestamp-based versioning and explain why it fails in distributed systems. Include the feedback from Sarah about deprecation periods.`
- Quoted text or feedback: `blog: incorporate this feedback: "your explanation of consensus algorithms was too theoretical, make it practical with real examples"`
- A mix: `blog: write about database migrations. Here's what a user said: "I wish you covered how to handle long-running migrations without downtime". Also make sure to mention blue-green deployments.`

## Your Style

Write in a style that sounds like Lukas. This means:
- The words you choose reflect how Lukas writes
- Your sentences are structured the way Lukas structures them
- The tone and rhythm match Lukas's voice
- Only do this where it makes sense - don't force it if the topic calls for a different approach

Importantly: Do NOT copy Lukas's article structure too closely. Every article is different and depends on its topic. The structure, headline organization, and flow should be appropriate for this specific topic, not a template.

## How to Learn the Style

Read the last 10 articles in `src/content/blog/` to understand:
- How Lukas explains concepts (practical vs theoretical balance)
- How he structures arguments
- What level of detail he goes into
- How he uses examples
- His tone (direct, unpretentious, practical)
- How he handles edge cases and nuance
- His use of formatting, lists, code examples

## What to Write

Write a comprehensive article that addresses the specification provided. The article should:
1. Explain the concept(s) clearly with practical examples
2. Address common misconceptions or pitfalls
3. Include real-world scenarios or use cases
4. Provide actionable guidance
5. Acknowledge trade-offs and complexity where relevant
6. Is appropriate length for the topic (not artificially short or long)
7. Incorporate any additional context, feedback, or requirements provided

## Technical Details

- Include front matter with: title, summary, date, tags (no draft status - this is a published article)
- Find the next article number in sequence from existing articles in `src/content/blog/`
- Create folder: `src/content/blog/[number]-[slug]/index.md`
- Include diagrams or code examples if they clarify the concept
- Write in Markdown with clear structure

## Output

Present the finished article ready to be saved to the file system.
