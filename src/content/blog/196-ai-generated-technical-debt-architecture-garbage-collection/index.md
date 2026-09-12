---
title: "AI-Generated Technical Debt: Architecture Garbage Collection for Coding Agents"
summary: "Coding agents can ship correct features while quietly degrading a codebase. Architecture tests and recurring cleanup loops keep that debt from compounding."
date: "Sep 12 2026"
tags:
  - AI
  - Coding Agents
  - Software Architecture
  - Technical Debt
  - Python
  - ArchUnitPython
---

# AI-Generated Technical Debt: Architecture Garbage Collection for Coding Agents

The agent implements the feature. The tests pass. The pull request looks clean. You merge it.

But the agent also duplicated an existing helper, imported a database adapter directly from an API route, and added another responsibility to a class that was already doing too much.

The feature works. The codebase got worse.

This is one of the interesting software engineering problems of 2026. Generating working code is becoming cheap. Keeping a system coherent while humans and agents generate changes in parallel is not.

The short version is:

> Coding agents need a gate that prevents new structural debt and a garbage collector that continuously removes debt which still gets through.

You need tests that enforce this deterministically. For Python projects, [ArchUnitPython](/blog/169-archunit-python) is a practical way to build both loops. Instead of only reading "please respect clean architecture" in `AGENTS.md`, the agent receives a failed test naming the dependency it must remove.

## The Research Is Starting to Catch Up

A 2026 preprint called [Debt Behind the AI Boom](https://arxiv.org/abs/2603.28592) analyzed 302,579 explicitly attributed AI-authored commits from 6,299 public GitHub repositories. The authors compared static-analysis results before and after each commit for production Python, JavaScript, and TypeScript code.

They reported:

- 484,366 introduced issues, 89.3% of them code smells
- More than 15% of commits from every analyzed assistant introduced at least one issue
- 22.7% of tracked issues still existed at the repository's latest analyzed revision

Another paper, [More Code, Less Reuse](https://arxiv.org/abs/2601.21276), was accepted at MSR 2026. Its full dataset contained 3,858 Python pull requests. A detailed redundancy analysis of 617 crewAI pull requests found an Average Max Redundancy score of `0.2867` for agent changes and `0.1532` for human changes: almost `1.87x` higher. Yet reviewers expressed more neutral or positive sentiment toward agent pull requests.

That combination is worrying. Ugly code attracts attention. Plausible, well-formatted, redundant code gets approved.

The conclusion is:

> Passing tests and pleasant-looking diffs do not tell us whether generated code is maintainable.

GitHub makes a similar point in [its guide to reviewing agent pull requests](https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/): agents often replicate a nearby pattern without checking whether the repository already contains a reusable solution. Once the duplicate is merged, future agents can copy that too.

## Why Green Tests Miss Architectural Debt

Agents do not have a unique desire to create spaghetti. Humans create the same problems. The difference is the optimization target and the rate.

Suppose the task is:

```text
Add an endpoint that returns the customer's subscription.
All tests must pass.
```

A direct database query in the route handler can satisfy every visible requirement. But the real requirements may also include:

```text
API depends on application services, not database adapters
authorization logic is reused
domain code remains framework-independent
no second subscription lookup is created
```

Unit tests answer a local question: does the feature behave correctly? Architecture is a graph question: is this dependency allowed, did the change create a cycle, and is a module accumulating unrelated responsibilities?

If those constraints exist only in an architect's head, they do not exist for the agent. Instructions help, but they change the probability of compliance. A test changes the definition of success.

## Architecture Garbage Collection

The term comes from an [OpenAI engineering report](https://openai.com/index/harness-engineering/) about building a product with an agent-generated codebase. The team initially spent one day per week cleaning up AI slop. It later encoded mechanical "golden principles" and ran recurring tasks that scanned for deviations and opened small refactoring pull requests.

Thoughtworks describes the same pattern in its [April 2026 Technology Radar](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2026/04/tr_technology_radar_vol_34_en.pdf): deterministic analysis finds structural problems, an LLM can evaluate or fix them, and an independent verification loop checks the result.

The operating model is simple:

```text
architectural invariant
        ↓
deterministic scan
        ↓
one small violation
        ↓
agent proposes a refactoring
        ↓
behavioral + architecture tests
        ↓
human reviews and merges
```

This is not a quarterly rewrite. It is continuous maintenance in small increments.

I would use three loops:

1. **Admission control:** Fast architecture checks run during development and on every pull request.
2. **Scheduled collection:** A daily or weekly agent selects one violation and opens one focused refactoring pull request.
3. **A ratchet:** Existing systems start at their current quality level, then tighten thresholds as debt is removed.

The scheduled collector should not create a 20,000-line "fix the architecture" change. One cycle, one oversized class, or one duplicated abstraction per pull request is much easier to review and revert.

## Making the Rules Executable with ArchUnitPython

Suppose a Python project uses this structure:

```text
src/shop/
├── domain/       # Business rules
├── application/  # Use cases and ports
├── adapters/     # Database and external-system implementations
└── api/          # FastAPI routes
```

The API may call the application layer, the application may depend on the domain, and adapters implement ports owned further inside. The API must not jump directly to a database adapter.

With [ArchUnitPython](https://github.com/LukasNiessen/ArchUnitPython), this becomes a pytest test:

```python
from archunitpython import assert_passes, metrics, project_files, project_layers


def test_layer_dependencies_point_inward():
    rule = (
        project_layers("src/")
        .layer("domain").defined_by_folder("**/domain/**")
        .layer("application").defined_by_folder("**/application/**")
        .layer("adapters").defined_by_folder("**/adapters/**")
        .layer("api").defined_by_folder("**/api/**")
        .where_layer("domain").may_only_depend_on_layers()
        .where_layer("application").may_only_depend_on_layers("domain")
        .where_layer("adapters").may_only_depend_on_layers(
            "application", "domain"
        )
        .where_layer("api").may_only_depend_on_layers("application")
    )
    assert_passes(rule)


def test_project_has_no_dependency_cycles():
    assert_passes(project_files("src/").should().have_no_cycles())


def test_files_do_not_keep_growing():
    rule = metrics("src/").count().lines_of_code().should_be_below(600)
    assert_passes(rule)
```

Now an agent adds this shortcut:

```python
# src/shop/api/subscriptions.py
from shop.adapters.postgres.subscription_repository import SubscriptionRepository
```

The endpoint tests may pass, but the architecture test fails because `api` may depend on `application`, not `adapters`. The agent can introduce the correct application port, rerun pytest, and fix itself before a human reviews the pull request.

Do not copy the `600`-line threshold blindly. Metrics are sensors, not quality scores. Measure comparable files, start near the current maximum, and lower the ceiling as cleanup work lands.

Also, ArchUnitPython cannot detect every kind of debt. Dependency directions, cycles, external imports, naming, and size are good deterministic rules. Semantically equivalent code written with different syntax needs a clone detector or LLM to find candidates, followed by human review and behavioral tests.

## Put the Check in the Agent's Loop

CI integration is boring because these are normal pytest tests:

```yaml
- name: Architecture fitness functions
  run: python -m pytest tests/test_architecture.py -q
```

Tell the coding agent to run that command before declaring success. If it fails, the agent should fix production code, rerun the focused behavioral tests, then rerun the architecture suite.

One rule matters enormously: **the agent must not weaken, delete, or skip the failing guardrail.** Architecture tests, CI workflows, thresholds, and ignore lists should require explicit human approval, for example through `CODEOWNERS`. Otherwise an agent optimizing for green CI may move the verifier instead of improving the implementation.

## Starting in a Brownfield Project

A legacy system may produce hundreds of violations on the first scan. A permanently red suite is useless.

Start with one painful boundary:

```text
Problem: API handlers import repositories directly.
Rule: API may depend on application, never adapters.
Initial scope: one already-clean module.
Next step: fix a neighboring module and expand the rule.
```

For metrics, set the first ceiling near the current maximum and ratchet it downward. Keep exceptions narrow, documented, owned, and time-limited. A broad permanent ignore for `legacy/` is not a migration plan; it is a second architecture with no owner.

Track new violations, removed violations, dependency cycles, post-merge rework, pull request size, and review rounds. Do not optimize for lines of code generated. That metric rewards the exact behavior we are trying to control.

## Wrapping Up

AI-generated technical debt is not a new species of debt. We already had duplicated logic, cycles, giant classes, and layer violations. What changed is the production rate.

The practical model is:

```text
instructions explain the architecture
architecture tests enforce objective boundaries
scheduled agents propose small cleanups
independent tests verify the result
humans retain judgment and control the rules
```

That is architecture garbage collection: prevent known debt at the pull-request boundary and continuously collect what still gets through.

## Sources Worth Reading

- [Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild](https://arxiv.org/abs/2603.28592)
- [More Code, Less Reuse: Investigating Code Quality and Reviewer Sentiment towards AI-generated Pull Requests](https://arxiv.org/abs/2601.21276)
- [Thoughtworks Technology Radar, Volume 34](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2026/04/tr_technology_radar_vol_34_en.pdf)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- [Agent pull requests are everywhere. Here's how to review them](https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/)
- [Our Architectural Guardrails for AI-Generated Code](https://codesai.com/en/posts/2026/04/minimal-architecture-constrainsts-in-agentic-world)

