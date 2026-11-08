# Marketing

The [Reddit workflow](reddit/AGENTS.md) is ready to use from this workspace. Its resources load only when relevant. Root `AGENTS.override.md` provides discovery without restoring the previously deleted root `AGENTS.md`; uppercase `AGENTS.md` is the conventional instruction filename. See the [official instruction discovery documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Existing chats that loaded instructions before this setup can start with “Read marketing/reddit/AGENTS.md, then ...”; new chats discover the root router.

Example requests:

- “Do a Reddit promotion activity for ArchUnitTS.”
- “Post three gift promotions for ArchUnitPython.”
- “Write two project showcases for TerraShark, drafts only.”
- “Promote this article on Reddit, using the educational story category.”

A promotion request includes writing and publishing unless you ask for drafts only. Unspecified quantity defaults to three suitable destinations, or fewer if eligibility or limits prevent it. The setup itself publishes nothing. Browser login and JavaScript permission must be working before the first live run; see [browser setup](reddit/browser.md).

Use [products](reddit/products.md) to find local source and public links, [subreddits](reddit/subreddits.md) to select an audience, and [posts](reddit/posts/README.md) for the frozen examples. New activity belongs in `reddit/runs/`, never in the example corpus. See [QA](reddit/qa.md) for what has actually been tested.
