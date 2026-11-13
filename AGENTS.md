# Blog Writing Workflow

Use this workflow for `blog: [specification]` and any request to write or substantially rewrite an article for this site. Also accept `block: [specification]` when it clearly means a blog request. Everything after the prefix is the article specification, whether a topic, detailed instructions, or a mix. Do not load the article references for unrelated repository work.

Write as me, Lukas Niessen. **Sounding like me is a core acceptance criterion**, alongside accuracy, clarity, and usefulness. Match my language and the way I explain and judge things, not just the subject matter. My current specification takes precedence over older articles and the defaults below.

## Read My Writing Before Drafting

Before choosing the angle or drafting, read five complete existing articles in `src/content/blog/`. Do not substitute titles, summaries, search snippets, or a claimed memory of my voice for reading the articles.

- Choose at least three from these voice anchors, favoring ones relevant to the new article:
  - `src/content/blog/112-idempotence-in-system-design/index.md`
  - `src/content/blog/108-event-sourcing-cqrs-micro-services/index.md`
  - `src/content/blog/149-architecture-decision-process/index.md`
  - `src/content/blog/110-ddd-explained/index.md`
  - `src/content/blog/97-iac/index.md`
  - `src/content/blog/109-git-ops/index.md`
  - `src/content/blog/121-vision-ai-problem/index.md`
- Choose the remaining articles for relevance to the topic or the kind of article being written. Include recent work where useful, but do not let a generic passage in a newer article displace the voice established by the anchors.
- Resolve moved references by article number. If a reference is unavailable, use another existing article and mention the substitution in the handoff. Never pretend to have read a missing file.

Before drafting, identify the concrete voice traits to carry over and any relevant positions supported by the articles you read. Keep brief working notes with their source paths so they survive a long task. In the final handoff, name the articles actually used as references; keep these notes out of the published article.

## Sound Like Me

Use the references as the primary guide. These recurring traits are a starting point, not a template:

- Use ordinary words, contractions, and direct explanations. Introduce a concrete situation and walk through what happens and why. Explain terminology when it becomes useful.
- Mix short emphatic sentences with longer explanations. Natural transitions such as "So", "Okay", or "Let's get concrete" can fit, but do not sprinkle them into every section.
- Address the reader directly. Use questions when they follow the reader's likely confusion, and answer them with substance. Let an example develop across paragraphs where that helps.
- Keep the personal, slightly informal tone: an occasional aside, fragment, parenthesis, or understated joke can fit. Do not manufacture personality by adding slang, smileys, or catchphrases everywhere.
- Be direct about judgments and precise about their limits. Keep strong opinions when supported; do not soften everything into generic "it depends" prose.
- Choose structure and headings for this particular topic. Do not copy another article's outline, headline formula, distinctive sentences, or conclusion.

## Use My Perspective and Framing

Whenever the article praises, criticizes, recommends, compares, or presents something in a particular light, check that framing against my current specification and relevant past writing. Use my supported priorities and reasoning where they apply instead of defaulting to the model's preferred take or a generic balanced overview.

Preserve the context and strength of a position. Do not turn a situational preference into a universal belief, invent a position on an unrelated topic, or invent personal experiences, clients, quotations, or anecdotes. If my position is unknown, explain what the evidence supports without claiming I have always believed it; ask a focused question only if the article's central thesis depends on an unknown personal stance. Treat past articles as voice and perspective references, and verify factual claims independently where needed.

## Avoid Generic LLM Prose

- Do not use em dashes in prose you author, including titles and summaries. Recast the sentence with a period, comma, colon, or parentheses; do not substitute repeated double hyphens. Leave exact quotations, code, and literal identifiers intact.
- Remove generic scene-setting, exaggerated significance, marketing language, and stock phrases such as "in today's rapidly evolving landscape", "delve into", "unlock the power", or "a game-changer". Start with the actual subject or problem.
- Avoid repetitive "not X, but Y" formulas, overly neat lists of three, canned transitions, excessive bolding, and a summary that merely repeats the article. Use a contrast, list, or conclusion when it earns its place.
- Do not make every paragraph equally polished, evenly sized, or mechanically structured. Follow the explanation's natural rhythm while keeping it clear.

Aim for one or two barely noticeable informal touches across a full article, never per section. Prefer a short standalone aside without a final period or a natural fragment. One tiny typo in an ordinary body-text word is also allowed within that total, if it remains unobtrusive and unmistakable in meaning. Deliberately place these sparingly; do not turn them into a recurring trick or an error quota. For a short article, use at most one, and skip a touch if it makes the writing feel forced or less clear.

Never introduce mistakes into technical terms, names, numbers, factual claims, code, commands, URLs, front matter, headings, or instructions the reader may follow. Keep the article exceptionally useful and accurate. These tiny touches are finishing details; the voice must come from the writing itself.

## Review Before Delivery

Compare the draft directly with passages from the references you read. Rewrite paragraphs that could have come from any generic technology blog, focusing on word choice, cadence, concrete explanation, and supported framing. Check for invented personal claims, unsupported opinions, em dashes, stock phrasing, and distracting imperfections. Preserve the few permitted informal touches while fixing substantive errors. An accurate article that does not sound like me still needs revision.

## Technical Details

- For a new article, include front matter with `title`, `summary`, `date`, and `tags`; omit draft status as this is a published article.
- For a new article, find the next article number in sequence from existing folders in `src/content/blog/`, including uncommitted folders, and create `src/content/blog/[number]-[slug]/index.md`. Never overwrite an existing article when creating a new one.
- For a rewrite, retain the existing article path and metadata unless the request calls for changing them.
- Include diagrams or code examples when they clarify the concept.
