```json
{
  "id": "1ss20ex",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "ClaudeAI",
  "created_utc": 1776808294.0,
  "created_at": "2026-04-21T23:51:34+02:00",
  "permalink": "https://www.reddit.com/r/ClaudeAI/comments/1ss20ex/claude_code_skill_for_terraform_now_supports_for/",
  "link_url": "https://github.com/LukasNiessen/terrashark",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "moderator",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "f7bb201f3abe93e0c258c7a94447bc0c5b96119925aa66cb273145a70d308aa7",
  "body_sha256": "5e13b6ca3ebab27e12c5ca7c6a35bba8e4b7cf742ca174b455f823277b78c8ae",
  "body_characters": 2601
}
```

# Original title

Claude Code Skill for Terraform: now supports for trusted modules (AWS, Azure, GCP)

## Original body

A week ago I posted about TerraShark, my Claude Code / Codex skill for Terraform and OpenTofu. In the comments you requested support for trusted modules, so I've added it! 

First a mini recap:

* Most Terraform skills dump thousands of tokens into every conversation, burning through your tokens with no benefit
* That's why I've built TerraShark, a Claude Code/Codex Skill for Terraform
* TerraShark takes a different approach: the agent first diagnoses the likely failure mode (identity churn, secret exposure, blast radius, CI drift, compliance gaps), then loads only the targeted reference files it needs
* Result: it uses about 7x less tokens than for example Anton Babenko's skill
* It's Based primarily on HashiCorp's official recommended practices

Repo: [https://github.com/LukasNiessen/terrashark](https://github.com/LukasNiessen/terrashark)

I also posted a little demo on YT: [https://www.youtube.com/watch?v=2N1TuxndgpY](https://www.youtube.com/watch?v=2N1TuxndgpY)

\---

Now what's new: **Trusted Module Awareness**

A bunch of you in the comments asked about terraform-aws-modules, Azure support, etc. Which is a great point. Hand-rolled resource blocks are one of the biggest hallucination surfaces for LLMs (attribute names, defaults, for\_each shapes etc). 

A pinned registry module replaces that with a version-locked interface already tested across thousands of production stacks.

So TerraShark now ships a [trusted-modules.md](http://trusted-modules.md) reference that tells the agent to default to the canonical community/vendor module whenever one exists. We support AWS, Azure, GCP, IBM and Oracle Cloud.

Note: to stay token-lean this reference only loads into context when the detected provider is one of the supported clouds.

The reference also enforces a few rules the agent now applies automatically:

* Exact version = pins in production
* Only install from the official namespace (typosquatted forks exist on the Registry)
* Don't wrap a registry module in a local thin wrapper unless you're adding real org-specific defaults or composing multiple modules
* Skip the module when it's trivial (single SSM parameter, lone DNS record) or when no mature module covers the service

Why not Alibaba, DigitalOcean etc? I Looked into them and their module programs are still small or early-stage, and recommending them as defaults would trade one failure mode (hallucinated attributes) for another (unmaintained wrappers). Happy to add them once the ecosystems mature... PRs are very welcome if you think I'm wrong about a specific one.

PRs and feedback is highly welcome!