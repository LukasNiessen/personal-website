---
title: "TerraShark: How I Fixed LLM Hallucinations in Terraform Without Burning All My Tokens"
summary: "Every LLM I tried kept hallucinating Terraform code. Existing skills fixed that but destroyed my token budget. So I built TerraShark - a failure-mode-first skill that prevents hallucinations while staying lean."
date: "Feb 23 2026"
tags:
  - Terraform
  - AI
  - Developer Tools
  - Infrastructure as Code
  - Claude Code
  - Open Source
---

# TerraShark: How I Fixed LLM Hallucinations in Terraform Without Burning All My Tokens

Agentic coding has been a game changer for me. I use Claude Code daily, I've written about it, I build tools around it. For most things, it's incredible. But Terraform? Terraform has been a nightmare.

Not because the models are bad. They're great. But hand them a Terraform task and things go sideways fast. And I mean _fast_.

## The Hallucination Problem

Here's what kept happening. I'd ask Claude to refactor a module - say, migrate from `count` to `for_each`. Simple task. The model would produce syntactically valid HCL, everything looks fine, you run `terraform plan` and suddenly it wants to destroy and recreate 14 resources in production. Why? Because it forgot the `moved` blocks. Every time.

Or I'd ask it to set up a secrets workflow. It would use the `sensitive` flag on a variable and call it a day. But `sensitive` doesn't keep secrets out of state. The value is still there in plaintext in your state file. The model just doesn't know that.

These aren't edge cases. These are the bread-and-butter mistakes:

- Defaulting to `count` instead of `for_each` for collections
- Omitting `moved` blocks during refactors, causing destroy/create cycles
- Using `sensitive` and assuming state is safe
- Recommending CLI-only `terraform import` instead of declarative import blocks
- Producing CI pipelines that re-run plan during apply instead of using saved artifacts

The code _looks_ correct. It passes syntax checks. It even passes basic review if you're not paying close attention. But it's operationally dangerous. And that's the worst kind of bug - the one that looks fine until it blows up in production.

## Trying Existing Solutions

So I looked for Claude Code skills that could help. Claude Code has a skill system. I tried the two I've found, and to be fair, it works. About 90% of the time, the output quality was noticeably better. It covers module patterns, testing, CI templates. Solid work.

But there was a big problem. **It BURNED through my tokens like nothing else.**

I took a loot and saw why: The skills dump around 4,400 tokens into context just on activation. Before any reference files. Before any of my actual code. Then it loads reference files that can be over 1,000 lines each. A single query about module design could easily cost 10,000+ tokens in skill overhead alone.

I'm on the Claude Pro plan. There's a 5-hour usage limit. With terraform-skill active, I was hitting that limit _way_ too fast. Not because I was doing more work, because the skill was eating context for breakfast.

## Building TerraShark

So I built my own. The goal was: fix the hallucinations **without** the token tax.

The project is called [TerraShark](https://github.com/LukasNiessen/terrashark). It's open source, MIT licensed, and works with both Claude Code and Codex (and any agent, including OpenClaw). But the interesting part isn't _what_ it does - it's _how_ it does it.

### The Core Insight

Most skills work like reference manuals. They dump a wall of information into context and hope the model picks the right parts. This is fundamentally wasteful. The model already knows basic Terraform. It doesn't need the syntax explained again. What it needs is to know _what it gets wrong_.

TerraShark is built around a different idea: **telling an LLM what good Terraform looks like is less effective than telling it how to _think_ about Terraform problems.**

Instead of a static reference, TerraShark is a 7-step diagnostic workflow. The model doesn't just read information and generate code. It follows a structured process:

1. **Capture execution context** - runtime, version, providers, backend, environment criticality
2. **(!) Diagnose likely failure modes** - what could go wrong _before_ writing any code
3. **(!) Load only relevant references** - pull a few targeted files, **related** to the detected failure modes
4. **Propose fix path with risk controls** - why this works, what could still fail
5. **Generate implementation artifacts** - HCL, migration blocks, CI updates
6. **Validate before finalize** - command sequences tailored to the runtime
7. **Output contract** - assumptions, tradeoffs, validation plan, rollback notes

The critical step is number 2 and 3. The model _diagnoses before it generates_. This is what prevents the most common failure: producing syntactically valid but operationally dangerous code.

### Five Failure Modes

Every piece of content in TerraShark maps to one of five failure modes. The references are structured by the failure modes. They represent the five most common ways LLM-generated Terraform causes real damage:

1. **Identity churn** - resource addressing instability, refactor breakage, index-based identity problems
2. **Secret exposure** - secrets leaking through state, logs, defaults, or artifacts
3. **Blast radius** - oversized stacks, weak boundaries, unsafe production applies
4. **CI drift** - version mismatches, unreviewed applies, missing plan artifacts
5. **Compliance gate gaps** - missing policies, approvals, audit controls

Content that doesn't reduce the probability of any of these failure modes doesn't make it into the skill. Period.

### Token Efficiency by Design

Some quick math.

The core SKILL.md, the file that loads on every activation, is 79 lines. About 600 tokens. Compare that to terraform-skill's 4,400 tokens. That's **over 7x leaner** on activation alone.

Then: TerraShark has 18 granular reference files instead of 6 large ones. When the model diagnoses "this is an identity churn problem," it loads `identity-churn.md`. Not the compliance gates. Not the CI delivery patterns. Not the testing matrix. Just the one or two files that are relevant.

A query about secret handling never loads the module architecture docs. A query about CI pipelines never loads the compliance framework mappings. This granularity means the model processes hundreds of tokens of reference material instead of thousands.

The difference in practice: No more token burning, my session time is back to normal. Plus, at least IMO, even the quality of the Terraform code is better.

### LLM-Aware Guardrails

Every reference file includes something we call an **LLM mistake checklist** - a list of specific errors that language models make when generating Terraform. Not generic best practices. Specific hallucination patterns.

For example, the coding standards reference includes a feature guard table that maps Terraform features to their minimum version _and_ the specific LLM error pattern:

- `moved` blocks (1.1+) - models omit them during refactors, causing destroy/create
- `for_each` over `count` (0.12+) - models default to `count` for every collection
- `write_only` arguments (1.11+) - models use `sensitive` and assume state is safe
- Declarative `import` blocks (1.5+) - models recommend CLI-only import

The idea is simple: a reference that only shows the right pattern still allows the model to hallucinate the wrong one. A reference that _explicitly names_ the hallucination pattern reduces it.

## Empirical Process

The content in TerraShark was not designed by intuition, we tested it thoroughly.

We started with much larger reference content - broader coverage, more examples, more explanations. Then we built an automated test suite: a large set of practical Terraform task patterns covering module creation, refactoring, CI pipeline setup, migration, security review, compliance checks.

Then we stripped content iteratively. Remove a section. Re-run the full test suite. Measure quality.

- If quality dropped → content was restored. It carried signal the model needed.
- If quality stayed stable → content was permanently removed. It was redundant with the model's existing knowledge.

We kept going until every remaining section was load-bearing. Removing any further content caused measurable quality degradation.

## How To Use

Installation is a one-liner:

```bash
git clone https://github.com/LukasNiessen/terrashark.git ~/.claude/skills/terrashark
```

Claude Code auto-discovers skills in `~/.claude/skills/`. No restart needed.

After that, whenever you ask Claude about Terraform, TerraShark activates (you can with one line turn off auto activation though, then only `/terrashark ...` will activate it). The model follows the 7-step workflow, diagnoses the failure modes, loads only what's relevant, and produces an output with an explicit contract: what it assumed, what it traded off, how to validate, and how to roll back.

You can also invoke it explicitly:

```
/terrashark Migrate this module from count to for_each
```

The output contract is what makes this auditable. Before applying anything, you can check: did the model assume the right version? Did it identify the right risks? Is the rollback path viable?

## Closing

TerraShark has helped me **a lot** sofar. It is open source, MIT licensed, and works with both Claude Code and Codex. If you're burning tokens on Terraform skills or tired of catching hallucinated `count` loops and missing `moved` blocks, give it a try!

**TerraShark**: [https://github.com/LukasNiessen/terrashark](https://github.com/LukasNiessen/terrashark)
