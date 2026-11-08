```json
{
  "id": "1t2hynt",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "Terraform",
  "created_utc": 1777804661.0,
  "created_at": "2026-05-03T12:37:41+02:00",
  "permalink": "https://www.reddit.com/r/Terraform/comments/1t2hynt/terraform_skill_for_claude_code_and_codex/",
  "link_url": "https://github.com/LukasNiessen/terrashark?v=2",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "reddit",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "ae66a2db51d3ced029eaaf1f689e2adcc4be34b9f0e1bd62e22c9111f1536df4",
  "body_sha256": "19993a477e1e4d16a6d4d9207b74d1301eaba6b29b3ddd980816c7d6eff07fb7",
  "body_characters": 4424
}
```

# Original title

Terraform Skill for Claude Code and Codex: TerraShark now has special backend-state safety support

## Original body

I added dedicated backend-state safety support to TerraShark.

**Mini recap:**

TerraShark is my Terraform and OpenTofu skill for Claude Code and Codex.

LLMs hallucinate a lot with Terraform. They often produce HCL that looks correct, but is operationally dangerous: unstable resource identity, missing `moved` blocks, secrets leaking into state, oversized root modules, unsafe production applies, weak CI pipelines, missing policy checks, or rollback plans that do not actually help when something goes wrong.

TerraShark fixes this by making the AI reason in a failure-mode-first way.

It does not just tell the model “write good Terraform”. It forces the model to ask what can go wrong before generating code. Is this an identity-churn risk? A secret-exposure risk? A blast-radius risk? A CI drift risk? A compliance-gate risk?

Then it loads only the references that matter for that task and returns the answer with assumptions, tradeoffs, validation steps, and rollback guidance.

That matters because Terraform mistakes can be accepted by the toolchain and still be dangerous. A plan can look normal while replacing important infrastructure. A refactor can look clean while changing resource addresses. A secret can be marked `sensitive` and still live in state. A pipeline can pass validation and still apply in an unsafe way.

Repo: [https://github.com/LukasNiessen/terrashark](https://github.com/LukasNiessen/terrashark)

---

**Now what’s new:**

TerraShark now has dedicated backend-state safety support.

Terraform keeps a state file. That state file is Terraform’s memory: it maps the code you wrote to the real infrastructure that already exists. The backend is where that state lives, for example in S3, Azure Blob Storage, GCS, Terraform Cloud, PostgreSQL, Consul, or locally on disk.

When the task involves backend configuration, backend migration, state storage, locking, force-unlock, backup, restore, S3, AzureRM, GCS, Terraform Cloud/remote, PostgreSQL, Consul, or local state, TerraShark now switches into backend-aware guidance.

This matters because state is one of the highest-impact parts of Terraform.

If state is lost, corrupted, unlocked, migrated badly, or readable by the wrong people, Terraform can make very dangerous assumptions. It may try to recreate infrastructure that already exists. It may allow two applies to run at the same time. It may leak sensitive values. It may turn a backend migration into a production incident.

So TerraShark now keeps the boring but critical backend details in mind:

S3 needs versioning, encryption, public access blocking, narrow IAM, locking, and clean state keys per environment. AzureRM needs storage encryption, blob recovery/versioning where available, lease-based locking, network restrictions, and narrow RBAC. GCS needs versioning, uniform bucket-level access, encryption, narrow IAM, and clean prefixes. Terraform Cloud needs workspace boundaries, restricted state sharing, sensitive variables, and approved execution mode.

It also knows the common LLM mistakes: suggesting local state for a team setup, forgetting state locking, creating backend storage inside the same root module that uses it, recommending `force-unlock` too casually, mixing backend migration with unrelated refactors, skipping state backups, or assuming encrypted state is safe for anyone to read.

TerraShark applies progressive disclosure strictly everywhere and stays very token lean. The core skill stays small and procedural. Deeper backend-state guidance is only loaded when the task actually touches backend or state risk.

So instead of generic Terraform advice, you get backend-aware Terraform guidance exactly when the risk appears.

---

**Compared to Anton Babenko’s Terraform skill:**

Anton Babenko’s Terraform skill is more like a broad Terraform reference manual. It includes a lot of useful Terraform material up front, but that also means the model carries more general context from the beginning.

TerraShark takes a different approach. It keeps activation much leaner and is built around a diagnostic workflow. First it identifies the likely failure mode, then it loads the specific reference material needed for that risk.

That is the core difference: TerraShark is not trying to be the biggest Terraform knowledge dump. It is trying to be the most focused safety layer for LLM-assisted Terraform work.

---

Feedback and PRs are highly welcome!