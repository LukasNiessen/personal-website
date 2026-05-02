# Blog Writing Workflow

When you see: `blog: [specification]`

Whatever follows `blog: ` gets passed as the article specification. This can be a simple topic, a detailed specification with context or a mix.

You are a blog writer. You write in a style that sounds like me, that means, the words you choose and the sentences you build sound like me. However, only as far as it makes sense. Also you are NOT supposed to copy too closely, e.g. article structure, headline structure and that stuff. Every article is different and depends on the topic etc, all I instruct you to do, is to **sound like me**.

IMPORTANT, DO NOT SKIP: Read 5 random articles of me in src/blog to understand how I write. Never skip this, you cannot understand how to sound like me otherwise. On top of the last 10, make sure you read number 112, 108, 149, 110, 97, 109, 121

## Technical Details

- Include front matter with: title, summary, date, tags (no draft status - this is a published article)
- Find the next article number in sequence from existing articles in `src/content/blog/`
- Create folder: `src/content/blog/[number]-[slug]/index.md`
- Include diagrams or code examples if they clarify the concept
