---
title: "Harness Engineering Deep Dive: Where The Term Came From, And How To Actually Build One"
summary: "Agent = Model + Harness. Where the term came from, what a harness actually is, and where the line sits between a thin wrapper and a real one. Then the technical part: sensors, ledgers, verification gates, budgets and stall detection, tool tiers, and trajectories, plus why the harness is the part of your AI system you actually own."
date: "Jul 28 2026"
tags:
  - AI
  - Agents
  - Architecture
  - LLM
  - Software Engineering
---

# Harness Engineering Deep Dive: Where The Term Came From, And How To Actually Build One

Let's talk about harness engineering.

The one-line version that has become the standard framing:

```text
Agent = Model + Harness
```

The model is the language model. The harness is everything else: the loop, the tools, the sandbox, the context assembly, the permissions, the tests it has to pass, the state that survives a crash, the traces, the budget caps, the approval gates.

That is a clean formula and it hides the interesting part, which is this: for a real production agent, the harness is *almost all of it*. When the Claude Code source leaked in March, people counted roughly 512,000 lines of TypeScript across about 1,900 files. The part that actually talks to the model is a small fraction of that. Everything else is harness.

So harness engineering is the discipline of treating that surrounding environment as the primary object of design, rather than as plumbing you write once and forget.

## Why This Is An Interesting Lens

Here is the thing that makes it more than a new word.

You do not control the model. You rent it. It gets swapped out from under you every few months, and when it does, its weights, its tool-calling quirks, and its failure modes all change without your permission.

You *do* control the harness. Completely. It is your code, in your repo, under your tests.

```text
The model is the part you rent.
The harness is the part you own.
```

Which means: every time an agent fails in production, you have two possible responses. You can wait for a better model, or you can change the environment so that failure becomes structurally impossible. The second one is engineering. The first one is hoping.

That reframing is the whole value of the term. It moves the question from "is the model smart enough?" to "is the environment I built around it good enough?", and the second question is one you can actually work on.

## How The Term Got Established

Worth being precise here, because this happened fast and the attribution is genuinely contested.

The nouns came first. *Agent harness* and *LLM harness* were practitioner slang well before anyone named a discipline. And the word "harness" was already doing this exact job in three older places:

```text
Test harness (software testing)
  The code around a unit under test that makes it runnable in
  isolation. Sets up fixtures, injects fakes and stubs, feeds inputs,
  captures outputs, asserts, tears down. The unit itself contains no
  test logic. The harness supplies everything the unit needs in order
  to be exercised at all.

Evaluation harness (LLM benchmarking)
  The runner around a model that turns a benchmark into a number.
  Loads the dataset, formats each item into a prompt, calls the model,
  parses the output, scores it against the reference, aggregates.
  lm-evaluation-harness is the well known one. Same model plus a
  different eval harness gives a different score, which is why
  benchmark numbers are hard to compare across papers.

Environment / wrapper (reinforcement learning)
  The code around a learning agent that defines the world. Observation
  space, action space, reward function, episode termination, resets.
  The Gym/Gymnasium wrapper pattern. The agent only emits actions;
  the environment decides what an action even means.
```

All three share one shape: the interesting component is small and useless on its own, and the surrounding scaffold is what makes it do work. The RL one is the closest ancestor conceptually, because it also wraps something non-deterministic and defines the action space rather than just the plumbing. The evaluation harness is the closest one linguistically, and it is where a lot of the vocabulary came from.

The mechanics are older too. The reason-then-act loop is [ReAct](https://arxiv.org/abs/2210.03629) (Yao et al., ICLR 2023), and tool calling is [Toolformer](https://arxiv.org/abs/2302.04761) (Schick et al., NeurIPS 2023).

The *discipline* got named in early 2026:

```text
Feb 2026   Mitchell Hashimoto writes about engineering a permanent fix
           into the agent's environment every time it makes a mistake.

Apr 2026   Birgitta Böckeler (Thoughtworks) publishes "Harness engineering
           for coding agent users" on martinfowler.com. This is where the
           Agent = Model + Harness formula and the inner/outer taxonomy
           come from.

           Vivek Trivedy (LangChain) writes "Anatomy of an Agent Harness",
           deriving the component list from the same formula.

           An OpenAI engineering report describes three engineers producing
           a million-line codebase at ~3.5 PRs per engineer per day, and
           calls the practice harness engineering. This is the one that
           made the term travel.

May 2026   Harness-Bench and friends. It becomes an object of study rather
           than a blog topic.
```

By mid-2026 it has a Wikipedia article, a curated awesome-list, and academic papers using "Agentic Harness Engineering" as a term of art. That is roughly the standard lifecycle of a term that describes something real.

I would put the honest assessment like this: the practice is real and predates the name by a couple of years. The name is useful because it gives a shared word to work that was previously invisible. You could not put "I made the sandbox better" on a roadmap before, and now you can.

## The Evolution, Honestly

Every article about this shows you the same ladder:

```text
2022-2023   Prompt engineering    -> language
2024-2025   Context engineering   -> information
2026        Harness engineering   -> environment
```

That is true but shallow. The more useful way to read the progression is: **what is the unit of work?**

```text
Prompt engineering
  Unit of work: one message.
  You are optimizing a string.
  Ceiling: the model does the right thing but doesn't know your facts.

Context engineering
  Unit of work: one context window.
  You are optimizing what the model can see at inference time.
  RAG, retrieval, chunking, memory summaries, tool schemas in context.
  Ceiling: the model knows the right things but cannot reliably *act*
  over many steps without drifting, looping, or lying about progress.

Harness engineering
  Unit of work: one run.
  You are optimizing a multi-step, stateful, side-effecting execution
  that has to survive crashes, partial failure, and a non-deterministic
  component in the middle of it.
  Ceiling: not reached yet. Probably the org, not the tech.
```

Each layer appeared when the previous one hit a wall, and none of them replaced anything. Prompt engineering did not go away; it became a component of context engineering, which became a component of the harness. This is nesting, not succession.

Two more things to be honest about.

First, some people have already extended the ladder with *intent engineering* and *loop engineering* (self-improving agents). Maybe. I would treat the third rung as the one that has earned its keep so far, and watch the rest.

Second, and more important: harness engineering is largely rediscovered software engineering. Sandboxing, idempotency, circuit breakers, budget caps, audit logs, bounded retries, tests as a feedback signal, durable state. I have written about most of these in a normal distributed systems context and none of it is new.

What *is* new is the thing sitting in the middle of the harness. It is non-deterministic, it will confidently report that it finished work it never did, and it can be talked into doing something else entirely by text it reads from a file. That changes which of the old patterns matter most, and it adds a few that have no real precedent.

## The Anatomy

Böckeler's taxonomy is the most useful map I have found, so let me use it.

The first split is by who builds it:

```text
Inner harness
  Shipped by the model or tool vendor.
  The agent SDK, Claude Code, Codex, Cursor.
  You configure it. You do not write it.

Outer harness
  What you assemble on top.
  Instruction files, MCP servers, skills, hooks, sensors,
  CI wiring, sandbox policy, eval sets.
  This is where your engineering effort pays back.
```

The second split is by *when* the harness acts:

```text
Guides   act before the agent does something.  (feedforward)
Sensors  act after the agent did something.    (feedback)
```

And the third split is by *what runs it*:

```text
Computational  deterministic, runs on a CPU.  linters, tests, type checkers, schemas
Inferential    probabilistic, runs on a model. review agents, LLM-as-judge
```

Which gives you a 2x2 that is genuinely useful when you are staring at an agent that keeps getting something wrong:

```text
                 COMPUTATIONAL              INFERENTIAL
              +--------------------------+--------------------------+
              | schemas that reject bad  | AGENTS.md / CLAUDE.md    |
     GUIDE    | args, narrowed tool      | skills, specs, arch docs |
  (before)    | surfaces, scaffolds,     | worked examples          |
              | generators, templates    |                          |
              +--------------------------+--------------------------+
              | tests, type checks,      | code review agent        |
    SENSOR    | linters, contract        | LLM-as-judge on output   |
   (after)    | validation, diff scope   | semantic diff review     |
              | checks, smoke runs       | tone/policy checks       |
              +--------------------------+--------------------------+
```

Most teams start in the top-right box, because writing a longer instruction file feels like progress. It is the weakest quadrant. Instruction files are advisory; the model may or may not follow them, and they cost context on every single turn.

The bottom-left box is the strongest and the most neglected. A test suite is a sensor that cannot be argued with.

A related point from Böckeler that I think is underrated: the effectiveness of your harness depends on the **ambient affordances of your stack**. A Java/Spring codebase comes with a compiler, a type system, ArchUnit, and strong structural conventions, so half your computational quadrant exists before you write a line of harness. A dynamically typed service with a 40-minute flaky test suite and no schema validation gives you almost nothing to sense with. Same model, same prompts, wildly different agent reliability.

I will come back to that, because it is the most important business consequence in the whole article.

## So Is Everything Around An LLM A Harness?

This is the right objection to make, because "the harness is everything except the model" is the kind of definition that quietly includes everything and therefore means nothing.

The trivial answer is yes. If you call the API from a Flask route, that Flask route is technically the harness. Which is true in the same way that a two line shell script is technically a build system. Not wrong, just not a useful thing to say.

So let me answer the question underneath it, which is not "does my code qualify for the label" but "at what point do harness concerns actually become live for me". The answer is not sophistication, not lines of code, not runtime, and not purpose. **The line is the closed loop.**

```text
Wrapper
  The model's output IS the deliverable.
  You take it and render it, store it, or return it to a caller.
  Any loop is over the model's own output format, not over the world.

Harness
  The model's output is a DECISION the system executes.
  Executing it changes something.
  The model then observes what changed and decides again.
```

That is the phase transition. Not size, not ambition. The question is whether there is a loop that runs *through the world* and back into the model's context.

Before the loop closes, the model is a function you called. Its output is either good or bad, you can look at it, and if it is bad you try again. After the loop closes, the model is a process running inside a system, and it accumulates consequences that neither of you can fully see.

A concrete pair, because this is easy to get abstract about:

```text
Not a harness:
  RAG chatbot. Retrieve, stuff the context, one model call, stream the
  answer to the user. Retrieval is upstream of the call. There is no
  loop. This is context engineering, and doing it well is real work,
  but none of the harness concerns apply.

A harness:
  Same chatbot, except the model can now call search itself, read what
  came back, decide the results were bad, and search again. Nothing got
  more sophisticated. One arrow got added, pointing backwards. Every
  concern in the next section just went live.
```

## Now The Technical Part

Let me build up from the naive loop, because the naive loop is what everyone writes first and every problem in harness engineering is visible as something missing from it.

```python
def run(task: str) -> str:
    messages = [{"role": "user", "content": task}]
    while True:
        response = model.call(messages, tools=TOOLS)
        messages.append(response)
        if not response.tool_calls:
            return response.text
        for call in response.tool_calls:
            result = dispatch(call)
            messages.append({"role": "tool", "id": call.id, "content": result})
```

That is a working agent. It is also a production incident waiting to happen. Everything below is a thing this loop does not have.

### 1. Sensors Are Transformers, Not Pipes

The single highest-leverage thing in a harness, and the one people get wrong most often.

Here is the wrong version, which is what almost everyone ships:

```python
def run_tests(workspace):
    proc = subprocess.run(["pytest"], cwd=workspace, capture_output=True, text=True)
    return proc.stdout + proc.stderr   # <- 6,000 tokens of noise
```

You just handed the model a wall of text where maybe forty tokens matter. It has to find the signal, it will sometimes find the wrong signal, and you will pay for those 6,000 tokens on this turn and every subsequent turn until compaction drops them.

A sensor is not a pipe from a tool to the context window. It is a **transformer that produces a signal optimized for the reader**, and the reader is a model.

```python
from dataclasses import dataclass

@dataclass
class Signal:
    ok: bool
    headline: str            # one line. always present.
    detail: str = ""         # bounded. only when it changes the next action.
    next_action: str = ""    # what to do about it.

def test_sensor(workspace: Path) -> Signal:
    proc = subprocess.run(
        ["pytest", "-q", "-x", "--tb=line", "--no-header"],
        cwd=workspace, capture_output=True, text=True, timeout=300,
    )
    if proc.returncode == 0:
        return Signal(ok=True, headline="All tests pass.")

    failures = parse_pytest_lines(proc.stdout)      # [(file, line, msg), ...]
    if not failures:                                 # collection error, not a test failure
        return Signal(
            ok=False,
            headline="pytest could not collect tests. Likely an import or syntax error.",
            detail=tail(proc.stderr, 600),
            next_action="Fix the import/syntax error before touching test logic.",
        )

    first = failures[0]
    return Signal(
        ok=False,
        headline=f"{len(failures)} failing. First: {first.file}:{first.line} {first.msg}",
        detail=source_window(first.file, first.line, radius=8),
        next_action=f"Read {first.file} around line {first.line} before editing anything else.",
    )
```

Look at the harness decisions hiding in that function.

`-x` stops at the first failure, because an agent handed twelve failures will try to fix twelve things at once and produce an unreviewable diff. `--tb=line` collapses tracebacks. The collection-error branch exists because "pytest exited non-zero" and "your code does not import" are completely different situations that demand different next actions, and the raw output makes them look similar. `source_window` attaches the code instead of making the agent spend a turn reading the file.

That last one is the pattern worth internalizing: **a good sensor pre-answers the question the agent would otherwise burn a turn asking.**

Same idea applies everywhere. A type checker sensor should group errors by root cause, not list 200 downstream complaints. A diff sensor should report scope violations, not the diff. An HTTP tool should surface `429 with retry-after: 30` as a distinct signal from `500`, because those want different next actions.

### 2. The Transcript Is A Cache. The Ledger Is The Truth.

The naive loop keeps everything in `messages`. That is the bug.

Message history grows without bound, then you compact it, and compaction is lossy by definition. Anything the agent needs to still know after compaction cannot live only in the transcript. Also: the process holding `messages` will die at some point, and pods are ephemeral, so in-memory history is not a state model.

So split it:

```python
def build_context(run_id: str) -> list[Message]:
    ledger = store.load_ledger(run_id)          # authoritative, structured, durable
    recent = store.last_turns(run_id, n=8)      # bounded window, disposable

    return [
        system(HARNESS_PROMPT),
        system(render_ledger(ledger)),           # regenerated fresh every single turn
        *recent,
    ]
```

A ledger is **one mutable document per run holding the state the agent is not allowed to forget**: objective, constraints, task statuses, decisions, facts learned. Durability is not part of the definition (an in-memory dict is a ledger, just a bad one), but since the point is surviving compaction and process death, in practice it is a real record with a real schema in a database or a file, which the agent reads and writes through tools:

```json
{
  "run_id": "run_8fa2",
  "objective": "Add rate limiting to the public API",
  "constraints": ["do not touch src/billing/**", "no new dependencies"],
  "tasks": [
    {"id": 1, "desc": "add middleware",        "status": "done",
     "evidence": "commit a91f2c, 3 tests added"},
    {"id": 2, "desc": "wire config",           "status": "done",
     "evidence": "commit 4c02aa"},
    {"id": 3, "desc": "per-tenant limits",     "status": "in_progress",
     "attempts": 2, "last_error": "TenantResolver returns None for internal callers"},
    {"id": 4, "desc": "update API docs",       "status": "pending"}
  ],
  "decisions": [
    "Chose token bucket over sliding window: existing Redis lease helper fits."
  ],
  "facts_learned": [
    "tests/conftest.py fakes Redis; integration tests need REDIS_URL set."
  ]
}
```

Three properties matter and all three are easy to get wrong.

**It is regenerated, not appended.** Both words are load-bearing, so let me be precise about them.

*Appended* is the version people write by accident. The agent reports progress as messages ("task 2 done", "task 3 failed, tenant was None"), and those messages stay in the transcript forever. Current state is never written down anywhere. It has to be reconstructed by reading every update in order and working out which ones are still true.

*Regenerated* means state lives in exactly one document, updates overwrite fields in place, and every turn the harness removes the previously rendered copy from context and inserts a freshly rendered current one. Context holds one copy, always current, sized by the state rather than by the number of turns. Nothing has to be reconciled, because "task 3 failed" from turn 9 no longer exists next to "task 3 done" from turn 40.

The obvious objection is that history has value. The agent genuinely does need to know that task 3 failed twice before, that the last attempt died on a None tenant, that this approach was already tried. Losing that would be worse than the token cost.

But that is an argument for recording history, not for putting all of it in the context window every turn, and those are separate decisions made by separate parts of the harness. The full append-only history of the run (every turn, every tool call, every signal, in order) is the **trajectory**, it is written durably, and it is what you replay, audit and debug against. It is section 7. What the ledger carries is the distilled version: the fields that change what the agent should do next. That is exactly what `attempts: 2` and `last_error` are doing in the schema above, and why `facts_learned` exists.

So the test for any piece of history is which consumer needs it. If it changes the next decision, it belongs in the ledger as a field and gets rendered every turn. If it only matters when a human is working out what went wrong, it belongs in the trajectory and never needs to enter context at all.

**Compaction may drop turns but never the ledger.** That is the invariant your compaction function has to preserve.

**`facts_learned` is the cheapest thing in the whole harness.** Every time the agent discovers something the environment should have told it (a fixture that fakes Redis, an env var that must be set, a build step that has to run first), that discovery gets written down once instead of being rediscovered every run. And each entry there is a bug report against your guides: if the agent had to learn it, a guide should have told it.

Because the ledger is durable and the transcript is not, a run becomes resumable. Crash on step 3, restart, rebuild context from the ledger, continue. Which only works if steps are idempotent. See [idempotency in system design](/blog/112-idempotence-in-system-design); this is the exact same argument as at-least-once message delivery, for the exact same reason.

### 3. The Agent Does Not Get To Decide It Is Done

This is the failure mode I would put at the top of the list, and it is the one with no real precedent in normal software.

The agent will tell you it finished. Sometimes it did not. Not because it is lying in any human sense. It generates plausible text from context, and "I have completed the task and all tests pass" is extremely plausible text. Its narrative about the world drifts from the world.

You will see all of these:

```text
"I completed the task"        -> the write failed
"All tests pass"              -> tests were never run
"I already checked that file" -> it never read it
"Waiting on approval"         -> no approval request was ever created
```

Harness-Bench calls this class of problem *execution-alignment failure*: reasoning that looks sound but has drifted away from tool feedback, workspace state, and the actual output contract.

So the terminal state of a run cannot be a model output. It has to be a machine-checked verdict:

```python
def attempt_completion(run: Run, claim: str) -> Signal:
    """The agent proposes completion. The harness decides it."""
    for name, sensor in run.exit_criteria:
        signal = sensor(run.workspace)
        if not signal.ok:
            return Signal(
                ok=False,
                headline=f"Not done: '{name}' failed. Your claim was: {claim[:80]!r}",
                detail=signal.detail,
                next_action=signal.next_action,
            )
    return Signal(ok=True, headline="Exit criteria met.")
```

And `attempt_completion` is registered as a *tool*, not as a special text response. The agent calls it. If it returns `ok=False`, that is just another tool result and the loop continues. The model has no way to exit the run.

Exit criteria are per-run and explicit:

```python
run.exit_criteria = [
    ("tests",      test_sensor),
    ("types",      typecheck_sensor),
    ("scope",      partial(diff_scope_sensor, allowed=["src/api/**", "tests/**"])),
    ("no_secrets", secret_scan_sensor),
    ("contract",   partial(schema_sensor, schema=OUTPUT_SCHEMA)),
]
```

The general principle:

```text
"The agent says it is done" is an event.
"The system confirms it is done" is a state.
Never let the first one write the second one.
```

Note that `diff_scope_sensor` is doing something subtler than the others. It is not checking correctness; it is checking that the agent stayed inside the boundary it was given. That is a whole category of sensor, the "did you do only what you were asked" category, and it is the one that catches the runs where the agent decided to helpfully refactor something else.

### 4. Narrow The Action Space Instead Of Prompting Harder

This is the Hashimoto rule, and it is the thing that separates harness engineering from prompt engineering as an actual practice.

The agent keeps forgetting to apply migrations before running tests. Three possible fixes:

```text
Weak    Add "always run migrations before tests" to AGENTS.md.
        Advisory. Costs context every turn. Followed most of the time.

Better  Make run_tests apply pending migrations itself.
        The mistake is now impossible through that path.

Best    Make the app fail at startup with a clear message if migrations
        are pending, and make that message say exactly what to run.
        Now every path is covered, including the human ones.
```

Notice the best fix improved the product for humans too. That happens constantly, and it is a good sign you are fixing the right layer.

Generalized: when the agent misuses a tool, do not describe the correct usage better. Change the tool so the misuse cannot be expressed.

```python
# Before: two ways to be wrong, both discoverable only at runtime.
def query(sql: str) -> list[dict]: ...

# After: the shape of the call constrains the action space.
def get_orders(
    tenant_id: str,
    status: Literal["open", "shipped", "cancelled"],
    since: date,
    limit: Annotated[int, Field(ge=1, le=500)] = 50,
) -> list[Order]: ...
```

The second one cannot produce a cross-tenant query, cannot invent a status value, and cannot pull a million rows. None of that is enforced by a prompt. It is enforced by a schema, which is a guide in the computational quadrant, which is the quadrant that actually works.

### 5. Budgets And Stall Detection

An agent loop that runs away returns `200 OK` while burning ten thousand dollars in tokens. Your latency and error-rate alerts will not fire, because nothing is slow and nothing is erroring. This is why production harnesses now carry cost-based circuit breakers next to the classical ones.

Step counting is the obvious control and it is not enough, because thirty steps of real work and thirty steps of the same failing tool call look identical to a counter. What you actually want to detect is **absence of progress**:

```python
from collections import deque

class Budget:
    def __init__(self, max_steps=60, max_output_tokens=400_000,
                 max_wall_clock_s=1800, max_tool_errors=12, stall_window=4):
        self.limits = dict(steps=max_steps, tokens=max_output_tokens,
                           seconds=max_wall_clock_s, tool_errors=max_tool_errors)
        self.used = dict(steps=0, tokens=0, seconds=0, tool_errors=0)
        self.fingerprints = deque(maxlen=stall_window)

    def charge(self, **kwargs) -> None:
        for k, v in kwargs.items():
            self.used[k] += v

    def exceeded(self) -> str | None:
        for k, limit in self.limits.items():
            if self.used[k] >= limit:
                return f"{k} budget exhausted ({self.used[k]}/{limit})"
        return None

    def stalled(self, workspace_hash: str, ledger_hash: str) -> bool:
        """No observable change to the world for N consecutive steps."""
        self.fingerprints.append((workspace_hash, ledger_hash))
        return (len(self.fingerprints) == self.fingerprints.maxlen
                and len(set(self.fingerprints)) == 1)
```

`stalled()` is the interesting one. If four steps pass and neither the workspace nor the ledger changed, the agent is thinking in circles, and no amount of additional steps will help. Stop, escalate, and (this is the part people skip) **write the trajectory somewhere a human will look at it**, because a stall is almost always a missing sensor. The agent did not know how to make progress because nothing in the environment told it what was wrong.

Wiring it in is one call per method, and each one has a specific place in the step:

```python
budget = Budget()                      # one per run, alongside the ledger

while True:
    if reason := budget.exceeded():                             # 1. top of the step
        return finish(run, status="exhausted", note=reason)

    t0 = time.monotonic()
    response = model.call(build_context(run.id), tools=TOOLS)
    budget.charge(steps=1,                                      # 2. next to the spend
                  tokens=response.usage.output_tokens,
                  seconds=time.monotonic() - t0)

    for call in response.tool_calls:
        signal = dispatch(call, ctx)
        budget.charge(tool_errors=0 if signal.ok else 1)
        store.append_turn(run.id, call, signal)

    if budget.stalled(hash_workspace(run.workspace),            # 3. bottom of the step
                      hash_ledger(store.load_ledger(run.id))):
        return finish(run, status="stalled",
                      note="no observable progress in 4 steps")
```

Three placement rules, all of which people get wrong at least once:

**`exceeded()` goes before the model call, not after.** Check it after and you always overshoot by a full turn, and the turn you overshoot by is the expensive one, because context is largest at the end of a run.

**`charge()` goes immediately next to whatever actually cost something.** Tokens and wall clock come from the model call, `tool_errors` comes from the dispatch result. Note that seconds are measured rather than estimated; a tool that hangs for four minutes needs to show up in the budget as four minutes.

**`stalled()` runs exactly once per step, at the bottom.** It appends to the deque on every call, so calling it twice per step silently halves your window from four steps to two. Put it after the tool loop, once the workspace and the ledger have both had their chance to change.

The two hashes just need to be stable and cheap. `hash_workspace` over the tracked file contents (`git status --porcelain` plus the diff hash is enough), `hash_ledger` over the serialized ledger. What matters is that a step which read three files and concluded nothing produces the same pair as the step before it.

Also note what happens when a budget trips. Not a crash. A run that ends in a reportable state:

```text
status: exhausted
completed: tasks 1, 2
blocked_on: task 3, TenantResolver returns None for internal callers
spent: 47 steps, 312k output tokens, 14m 20s
trajectory: s3://traces/run_8fa2/
```

Partial results with an honest boundary beat a vague failure. Same argument as graceful degradation in any distributed system.

### 6. Tool Gateway: Tiers, Not A Flat List

Not all tools are the same kind of thing, and a flat `TOOLS` array pretends they are.

```python
@dataclass
class Tier:
    approval: str | None      # None | "allowlist" | "human"
    audit: str                # "sample" | "always"
    idempotency: bool = False
    scope: str | None = None

TIERS = {
    "read":   Tier(approval=None,        audit="sample"),
    "write":  Tier(approval=None,        audit="always", scope="workspace"),
    "egress": Tier(approval="allowlist", audit="always"),
    "mutate": Tier(approval="human",     audit="always", idempotency=True),
}

def dispatch(call: ToolCall, ctx: RunContext) -> Signal:
    tool = REGISTRY[call.name]
    tier = TIERS[tool.tier]

    if not authorized(ctx.principal, tool, call.args):
        return Signal(ok=False, headline="Not authorized for this tool.",
                      next_action="Choose a different approach or ask the user.")

    if tier.approval == "human" and not ctx.approvals.granted(call):
        ctx.approvals.request(call)
        return Signal(ok=False, headline="Approval requested. Paused.",
                      next_action="Wait. Do not retry or find a workaround.")

    key = idempotency_key(ctx.run_id, call) if tier.idempotency else None
    if key and (prior := ctx.results.get(key)):
        return prior                                  # replay, do not re-execute

    with ctx.trace.span(tool.name, args=redact(call.args)):
        signal = tool.execute(call.args, ctx)

    if key:
        ctx.results.put(key, signal)
    return signal
```

Two details worth calling out.

The `next_action` on the approval branch says "do not retry or find a workaround." Say it explicitly, because an agent that hits a wall will look for a way around it, and that is exactly the behaviour you do not want from something that just got told to wait for a human.

Authorization takes `call.args`, not just the tool name. "Can this principal call `get_orders`" is the wrong question. "Can this principal call `get_orders` for *tenant X*" is the right one. Get this wrong and you have built a confused deputy: the agent has the union of every permission any caller ever gave it.

### 7. The Trajectory Is The Unit Of Debugging

The last one is short but it changes how you operate the system.

In normal software you debug with log lines. With agents, the unit that matters is the **trajectory**: the ordered sequence of context assembled, model output, tool called, signal returned, state changed, for the whole run.

You need it stored and replayable, because the interesting questions are all trajectory-shaped:

```text
Which sensor should have caught this and did not?
At which step did the model's story diverge from the workspace?
Was the right context present at step 12, or had compaction dropped it?
Did the agent ignore a guide, or was the guide never in context?
Which tool result was misleading?
```

"The AI did it" is not an audit trail. Who requested it, which agent path led there, which capability executed it, under which scopes: *that* is an audit trail, and you only have it if the harness recorded the trajectory as a first-class artifact.

This is also how the harness improves. Every trajectory that ended badly names the missing guide or sensor. That is your backlog, and it is a much better backlog than intuition.

## The Business And Architecture View

Now the part that matters if you are the one paying for this.

**Your model comparison is probably meaningless.** [Harness-Bench](https://arxiv.org/abs/2605.27922) ran 106 sandboxed tasks across 5,194 trajectories and found that completion rate, efficiency and *failure behaviour* all vary substantially across model-harness pairings, concluding that capability should be reported at the **model-harness configuration level** rather than credited to the model. So "we evaluated A against B and A won" is not a result unless the harness was held constant, and it usually was not, because each vendor's model arrives inside its own inner harness. If you are running a bake-off: fix the harness, swap only the model, use your own tasks, report the pair.

**The moat is the outer harness.** Models converge and get commoditized; any advantage one vendor has this quarter is gone in two. The outer harness encodes your conventions, your failure modes, your sensors, your accumulated `facts_learned`. It is specific to you, it compounds, and it is portable across models.

```text
Inner harness   ->  buy. table stakes, moves fast.
Outer harness   ->  build. it is the asset. keep it in your repo.
```

That last clause is a real architectural constraint. Guides and sensors living in a vendor's web UI are not yours to move, and swapping inner harness becomes a rebuild instead of a migration.

**"AI readiness" is mostly engineering fundamentals.** The harness you can build is bounded by what your codebase lets you sense and constrain. Static types, fast hermetic tests, schema-validated boundaries and [mechanically enforced architecture rules](/blog/169-archunit-python) are cheap computational sensors sitting there for free. No types, a 40-minute flaky suite and manual QA leave you nothing to build on, so you substitute inferential sensors (LLM-as-judge, review agents) that are slower, costlier and less trustworthy than a type checker. Same model, same prompts, radically different reliability. It is rare that the AI-shaped budget line and the correct engineering priority point the same direction.

**Cost lives in the harness.** Everyone negotiates price per token; the harness decides how many tokens you spend. A sensor dumping 6,000 tokens of pytest output thirty times a run is 180,000 tokens of noise. A ledger that accumulates instead of regenerating grows quadratically. A missing stall detector pays for forty steps of nothing.

```text
Model choice     ->  maybe 2-5x on unit price
Harness quality  ->  routinely 10-50x on tokens consumed per task
```

**Ownership splits like any platform capability.** Harness work is horizontal (sensors, tracing, budgets, gateway, sandbox policy) while the knowledge it needs is vertical, because only the payments team knows how payments code fails. Centralize all of it and the platform team becomes a bottleneck that has to understand every domain; push all of it down and you get twelve incompatible harnesses with no shared tracing. Platform owns the loop, tool gateway, permission tiers, budgets, trajectory storage, eval infrastructure and the harness templates. Domain teams own their guides, domain sensors, tool schemas, exit criteria and eval cases. Conway's Law again.

**Three risks the vendor does not solve for you.** An agent reporting success it did not achieve is a **correctness** risk, mitigated by machine-verified exit criteria and not by a better prompt. An agent holding the union of everyone's permissions is a **confused deputy**, mitigated by per-call authorization on arguments rather than per-tool allowlisting. An agent reading a document that contains instructions is a **prompt injection** surface where injection becomes *action*, mitigated by the tier system. Approval gates are not an admission that the AI is not good enough yet; they are frequently the correct architecture.

## Common Mistakes

- **A longer instruction file instead of a sensor.** A fourth revision of AGENTS.md for the same recurring failure means you are solving it at the wrong layer.
- **Piping raw tool output into context.** Sensors are transformers. Unshaped output is expensive, ambiguous and often actively misleading.
- **Letting the model declare the run finished.** Completion is a verified state, never a claim.
- **Keeping run state only in the transcript.** Compaction is lossy and processes die. The ledger is the truth.
- **Counting steps but not detecting stalls.** Thirty productive steps and thirty repetitions of the same failing call look identical to a counter.
- **Comparing models without fixing the harness.** You are measuring a pair and reporting it as a single variable.
- **Building the outer harness inside a vendor's UI.** If it is not in your repo, you cannot migrate it.
- **Exposing every tool you have.** More tokens, worse selection, more attack surface. Narrow and group.
- **Treating a runaway loop as a cost problem only.** It is a signal that a sensor is missing. Fix the sensor, not just the cap.
- **Skipping trajectory storage.** Without replayable trajectories you cannot debug, cannot audit and cannot systematically improve the harness.

## Sources Worth Reading

- [Harness engineering for coding agent users (Birgitta Böckeler, martinfowler.com)](https://martinfowler.com/articles/harness-engineering.html)
- [Harness Engineering: first thoughts (memo)](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html)
- [Harness engineering and agent feedback: exploring AI coding sensors (Thoughtworks)](https://www.thoughtworks.com/insights/blog/generative-ai/harness-engineering-agent-feedback-exploring-ai-coding-sensors)
- [Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows](https://arxiv.org/abs/2605.27922)
- [What is an AI Agent Harness? (Databricks)](https://www.databricks.com/blog/ai-harness)
- [The Agent Harness: Why the LLM Is the Smallest Part of Your Agent System (MongoDB)](https://www.mongodb.com/company/blog/technical/agent-harness-why-llm-is-smallest-part-of-your-agent-system)
- [Agent harness (Wikipedia)](https://en.wikipedia.org/wiki/Agent_harness)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering)
