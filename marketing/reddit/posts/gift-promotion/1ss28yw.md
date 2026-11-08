```json
{
  "id": "1ss28yw",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "aws",
  "created_utc": 1776808835.0,
  "created_at": "2026-04-22T00:00:35+02:00",
  "permalink": "https://www.reddit.com/r/aws/comments/1ss28yw/special_aws_support_added_to_claude_code_skill/",
  "link_url": "https://github.com/LukasNiessen/terrashark",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "automod_filtered",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "a7c9e4a89814328788e4bbb185c24fa086c467c05284ca04cb8a0ba474894eea",
  "body_sha256": "28ec1f46d7e2a22cfdf9d56994cd4f9e51af4f9fe916acf358b4a3afe516ff7b",
  "body_characters": 2533
}
```

# Original title

Special AWS support added to Claude Code Skill for Terraform (TerraShark)

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

Why not Alibaba, DigitalOcean etc? I Looked into them and their module programs are still small or early-stage, and recommending them as defaults would trade one failure mode (hallucinated attributes) for another (unmaintained wrappers). Happy to add them once the ecosystems mature.

PRs and feedback is highly welcome!