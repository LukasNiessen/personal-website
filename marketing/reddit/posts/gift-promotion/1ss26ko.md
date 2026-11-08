```json
{
  "id": "1ss26ko",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "ChatGPTPro",
  "created_utc": 1776808689.0,
  "created_at": "2026-04-21T23:58:09+02:00",
  "permalink": "https://www.reddit.com/r/ChatGPTPro/comments/1ss26ko/codex_skill_for_terraform_now_supports_for/",
  "link_url": "https://github.com/LukasNiessen/terrashark",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "reddit",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "5b68e64fd25733e4e28c7752a4a8e68fb94930c6d95798a0688b37646056f19c",
  "body_sha256": "bce4d576bb2c3ba370c851134e3564fe85731910c2f9538eebbd52afa1c8e63c",
  "body_characters": 2536
}
```

# Original title

Codex Skill for Terraform: now supports for trusted modules (AWS, Azure, GCP)

## Original body

A week ago I posted about TerraShark, my Codex (or Claude Code) skill for Terraform and OpenTofu. In the comments you requested support for trusted modules, so I've added it! 

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

Why not Alibaba, DigitalOcean etc? I Looked into them and their module programs are still small or early-stage, and recommending them as defaults would trade one failure mode (hallucinated attributes) for another (unmaintained wrappers). Happy to add them once the ecosystems mature.

PRs and feedback is highly welcome!