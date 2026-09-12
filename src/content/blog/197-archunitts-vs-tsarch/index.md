---
title: "ArchUnitTS vs. tsarch in 2026: Which Architecture Test Should You Choose?"
summary: "Angular Architects recently recommended tsarch for AI coding agents. The idea is excellent. But for a new TypeScript project in 2026, the maintenance, correctness, feature, and performance evidence points to ArchUnitTS."
date: "Sep 12 2026"
tags: ["TypeScript", "Software Architecture", "Testing", "AI", "Open Source"]
---

Angular Architects recently published an excellent article about turning architecture into an executable contract for AI coding agents. The core idea is exactly right:

```text
architecture document
        ↓
executable architecture rule
        ↓
test or agent Stop hook
        ↓
deterministic feedback
```

An AI agent can ignore prose. It cannot negotiate with a red test.

The article uses [tsarch](https://www.angulararchitects.io/en/blog/architecture-beyond-layers-tsarch-for-ai-agents/) for that last deterministic guardrail. That surprised me, because there is another library in the same family: [ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS).

I maintain ArchUnitTS, so let me put the conflict of interest on the table immediately. This is a maintainer's comparison, not a neutral consumer report. To keep it useful, I reproduced the Angular Architects example, inspected both repositories, ran both tools against the same source tree, and included the uncomfortable results too.

My conclusion is still quite clear:

> For a new TypeScript architecture-testing setup in 2026, ArchUnitTS is the only choice I can responsibly recommend.

tsarch can still execute basic rules, including the four from the Angular Architects article under Vitest, but it has extreme downsides: it is not actively maintained, its latest npm release is nearly two years old, its current CI is broken, it relies on TypeScript 3.9 internally, and a selector that matches nothing can silently produce a green test. ArchUnitTS, by contrast, is actively maintained, supports modern TypeScript project resolution, fails empty tests by default, provides substantially more rules, metrics, reports, and test-runner integrations, and was faster in both benchmark measurements. tsarch's higher GitHub star count reflects its longer history, not the safer choice for a new or long-lived codebase today.

## The short comparison

This snapshot was taken on September 12, 2026.

| Question | ArchUnitTS | tsarch |
| --- | --- | --- |
| Latest release | [2.5.0, September 12, 2026](https://github.com/LukasNiessen/ArchUnitTS/releases/tag/v2.5.0) | [5.4.1, December 23, 2024](https://github.com/ts-arch/ts-arch/releases/tag/v5.4.1) |
| TypeScript used internally | 5.9.x | 3.9.x in a current install |
| `tsconfig` inheritance and project references | Supported | The article requires a duplicated config because `extends` is not resolved |
| Empty selector protection | Fails by default | Silently returns no violations |
| Generic `.check()` | Yes | Yes |
| Dedicated test matchers | Jest, Vitest, and Jasmine | Jest |
| Custom rules | Yes | No equivalent API |
| Code metrics | Counts, cohesion, coupling, instability, abstractness, distance, custom metrics | No equivalent suite |
| Dependency reports | DOT, Mermaid, D2, CSV, JSON, and HTML | No equivalent report suite |
| Current repository CI | Green on a modern toolchain | [Latest `main` run is red](https://github.com/ts-arch/ts-arch/actions/runs/23619864229) |
| Benchmark result | Faster in both measurements | Slower in both measurements |
| GitHub stars | 479 | 661 |
| Recent npm download rate | Currently ahead | Currently behind |

The last two rows are worth reading together. Stars measure accumulated attention over the lifetime of a repository. Recent downloads measure what people are installing now. tsarch has the historical star lead; ArchUnitTS now has the stronger recent npm download trend. Neither number proves technical quality, but the direction of current use matters more to me than an old popularity snapshot.

You can inspect the live [npm trend](https://npmtrends.com/archunit-vs-tsarch) because, unlike stars, this row will keep changing.

## 1. Maintenance is not decoration

An architecture test sits unusually deep in the development loop. It parses the project, resolves imports, runs in CI, and may block every pull request. In the setup proposed by Angular Architects, it even runs after an AI agent finishes a turn.

That makes maintenance the strongest differentiator here.

The latest tsarch release is 5.4.1 from December 23, 2024. At the time of writing, that release is 628 days old. The repository is not archived, so calling it "dead" would be unfair. There is even an open [TypeScript 6 migration pull request](https://github.com/ts-arch/ts-arch/pull/87).

But the merged history tells a different story. The only two commits on `main` after the 5.4.1 release were README changes in March 2026. The most recent source change is still from 2024. The current backlog contains [17 open issues](https://github.com/ts-arch/ts-arch/issues) and [10 open pull requests](https://github.com/ts-arch/ts-arch/pulls), with the oldest issue dating back to 2020.

ArchUnitTS released 2.5.0 on the day of this comparison. Recent releases fixed real compatibility and correctness problems, including Vitest 4 behavior, package-entry metrics, distance-metric filtering and coupling, folder exclusions, TypeScript path aliases, and referenced `tsconfig` projects.

That is what active maintenance looks like: not a green badge in a comparison table, but short feedback cycles between a reported problem and a released fix.

## 2. A guardrail must not pass when it checked nothing

This is the most important correctness difference.

Imagine this rule:

```typescript
projectFiles('tsconfig.json')
  .inFolder('src/payment')
  .shouldNot()
  .dependOnFiles()
  .inFolder('src/web')
  .check();
```

Now somebody renames `src/payment` to `src/payments`. The architectural boundary did not become valid. The rule became empty.

tsarch returns an empty violation array and the test goes green. This is not theoretical; it has been reported in [tsarch issue #73](https://github.com/ts-arch/ts-arch/issues/73) since August 2023. I also reproduced it with a nonexistent selector against the current package.

ArchUnitTS fails empty tests by default with an `EmptyTestViolation`. You can opt out with `allowEmptyTests` when an empty match is intentional, but the safe behavior is the default.

```text
Selector typo or refactor
        │
        ├── tsarch:       0 files → 0 violations → green
        │
        └── ArchUnitTS:   0 files → EmptyTestViolation → red
```

For an ordinary test helper, this may sound like a small ergonomic detail. For an architectural fitness function, it is existential. A false failure is annoying. A false green result tells you that a boundary is protected when it is not.

And AI makes this more important, not less. Agents rename directories, move files, and reshape modules quickly. The guardrail has to detect when its own assumptions disappeared.

## 3. Modern TypeScript projects need modern project resolution

The Angular Architects tutorial has to create a dedicated `tsconfig.arch.json`. It repeats the target, module format, module resolution, decorators, path aliases, includes, and excludes because tsarch does not resolve `extends`.

The article is honest about this and calls the duplication "not pretty." I agree.

Duplicated configuration is not only ugly. It is drift:

```text
tsconfig.json changes
        │
        ├── architecture config updated     → test sees reality
        │
        └── architecture config forgotten   → test sees an old project
```

ArchUnitTS 2.5.0 reads TypeScript configuration through the TypeScript configuration API and resolves imports in referenced project contexts. That includes inherited options, path aliases, and composite/project-reference layouts. In a modern Angular workspace or monorepo, this removes an entire synchronization problem.

The compiler dependency matters too. The Angular demo uses TypeScript 5.9.3, while `tsarch@5.4.1` installs its own nested TypeScript 3.9.10. The [tsarch package manifest](https://github.com/ts-arch/ts-arch/blob/main/package.json) still declares `typescript: ^3.8.3`, Jest 23, Node 10 type definitions, TSLint, and TypeDoc 0.17-era tooling.

Old code can be perfectly good code. Old compiler infrastructure is different: module resolution evolves, syntax evolves, `tsconfig` behavior evolves, and real applications move on.

## What tsarch still gets right

There are good reasons why tsarch became popular.

Its fluent API is readable. It brought the ArchUnit idea into TypeScript early. Its basic dependency, cycle, slice, Nx, and PlantUML concepts are useful. Its generic `.check()` method can be called from any test runner, which is why the Angular Architects Vitest example works even though tsarch only provides special matcher integration for Jest.

The article's four rules are not fake. I ran them unchanged:

- only stores may access clients;
- only smart components may access stores, with locality exceptions;
- stores must not access other stores;
- dumb components must not access smart components.

All four passed with Vitest 4.

tsarch also has 661 GitHub stars versus 479 for ArchUnitTS at the time of writing. It has a longer history and a larger accumulated installed base. If a team already uses it successfully, has simple configuration, and accepts ownership of future compatibility work, a forced migration may not be worth the disruption.

That is the strongest case for tsarch. It is real, but it does not reverse the recommendation for a new project.

## 4. Four rules are the shared starting point, not the feature ceiling

Both libraries can express the four rules in the article. The difference appears when an architecture program grows beyond import boundaries.

ArchUnitTS adds several categories that tsarch does not offer as an equivalent integrated API:

### Safer and richer rule definition

- glob and regular-expression selectors for files, paths, folders, and classes;
- reusable exclusions for generated files, barrels, and public APIs;
- custom file predicates for rules that do not fit the fluent vocabulary;
- configurable empty-test behavior;
- detailed logging and graph caching;
- cycle checks, slice rules, Nx rules, and PlantUML conformance.

### Architecture metrics

- file, class, method, field, and dependency counts;
- several LCOM cohesion algorithms;
- afferent and efferent coupling;
- instability and abstractness;
- distance from the main sequence;
- normalized zones and summaries;
- custom metrics for project-specific health signals.

This is an important distinction. Dependency rules answer "is this edge allowed?" Metrics answer "is this component becoming harder to change?" A serious architecture fitness suite eventually needs both.

### Reports that humans and agents can consume

ArchUnitTS exports dependency information to DOT, Mermaid, D2, CSV, JSON, and standalone HTML. It can focus or collapse graphs and generate metric dashboards.

That gives the same model several consumers:

```text
TypeScript dependency graph
        ├── test assertion
        ├── CI failure
        ├── agent feedback
        ├── reviewable Mermaid/D2 graph
        ├── machine-readable JSON/CSV
        └── human-readable HTML report
```

The Angular Architects article makes a strong case for closing the feedback loop for coding agents. ArchUnitTS closes more of that loop because the architecture model is not limited to one returned violation array.

## 5. Performance: faster, but let us not turn one machine into a law

I used the exact [Angular Architects demo at commit `caaac81`](https://github.com/angular-architects/flights42/tree/caaac81f414188d2ca7410a6e1e236d4a200e5e4). The project runs Angular 21.2, TypeScript 5.9.3, and Vitest 4.0.18.

For each library I started a fresh Node process, extracted the graph without a warm application cache, alternated execution order, and took the median of four runs. I compared internal, non-self import edges so synthetic bookkeeping and different external-module classification did not distort the equivalence check.

Both libraries found exactly 198 internal edges.

| Four-run median | ArchUnitTS | tsarch | Result |
| --- | ---: | ---: | ---: |
| Initial measurement | 3.812 s | 7.434 s | ArchUnitTS 1.95x faster |
| Clean 2.5.0 rerun | 4.274 s | 5.171 s | ArchUnitTS 1.21x faster |

The first result is the attractive headline: almost twice as fast. The second result is why benchmark sections need methodology. File-system cache state, antivirus activity, process startup, and machine load move these numbers considerably.

The defensible conclusion is not "ArchUnitTS is always exactly twice as fast." It is:

> ArchUnitTS produced the same internal dependency graph and was faster in both order-balanced measurements, with the observed advantage ranging from about 21% to 95%.

For a test that runs after every agent turn, even the lower end is useful.

## 6. Security: the honest answer is maintenance risk, not a proven consumer exploit

It would be easy to look at the old toolchain and declare tsarch insecure. The evidence does not justify that sentence.

A clean install of the Angular demo reported zero npm audit vulnerabilities, and a minimal consumer install of `tsarch@5.4.1` also reported zero. I found no evidence of a known vulnerability shipped to consumers through the current package.

My local `npm audit` of ArchUnitTS 2.5.0's full locked development tree also returned zero. GitHub's repository security banner, however, currently lists [21 Dependabot alerts](https://github.com/LukasNiessen/ArchUnitTS/security/dependabot): 11 moderate and 10 high, but no critical alerts. Scanner state and advisory resolution can differ, so "my local audit is clean" should not be turned into "there is no security work left."

The tsarch contributor tree is much less comfortable. A clean `npm ci` of the repository installed 1,489 packages and `npm audit` reported 130 findings, including 22 critical findings. Those results are dominated by old development and release tooling, so they are not proof that an application importing tsarch is exploitable.

They are proof of maintenance work waiting to happen.

The same pattern appears in CI. The [workflow](https://github.com/ts-arch/ts-arch/blob/main/.github/workflows/build.yaml) still targets Node 16, `actions/setup-node@v1`, `actions/cache@v2`, and `actions/checkout@v2`. Node 16 has been [end-of-life since August 2023](https://nodejs.org/en/about/previous-releases), and GitHub warned that workflows remaining on deprecated cache action versions would fail after the old cache service was retired in February 2025. The latest tsarch `main` run is red and failed before recording normal build steps.

So my security conclusion is deliberately narrow:

- there is no demonstrated consumer vulnerability that would justify calling tsarch unsafe;
- the stale contributor dependency tree and broken CI increase supply-chain and maintenance risk;
- ArchUnitTS's current, green, actively updated toolchain is the stronger operational position, while its own Dependabot alerts still deserve attention.

## 7. Neither library sees every JavaScript dependency

There is one shared limitation worth making explicit: both extractors currently center on static TypeScript `ImportDeclaration` nodes.

That means teams should test their own use of:

- dynamic `import()`;
- CommonJS `require()`;
- re-export-only barrel chains;
- framework-generated or runtime-only dependency wiring.

The Angular Architects article already notes that barrels can obscure a rule. That is a good warning for both libraries. Architecture tests are a deterministic line of defense, not a semantic proof of every runtime relationship.

ArchUnitTS also has a narrower known caveat today: it adds synthetic self-edges so isolated project files remain visible in graph projections. A negative dependency rule whose source and target selectors overlap can therefore report `file → same file`. Cycle detection excludes these edges, but overlapping negative dependency rules may need to filter them until [the self-dependency issue](https://github.com/LukasNiessen/ArchUnitTS/issues/6) is resolved.

I do not think this outweighs empty-test protection, active TypeScript support, or the broader feature set. But it belongs in a serious comparison.

## 8. The projects are related, and that should be acknowledged

ArchUnitTS did not appear from nowhere. Its beginnings used code from the MIT-licensed tsarch project, which itself brought the ideas of Java's [ArchUnit](https://www.archunit.org/) to TypeScript. ArchUnitTS has since evolved substantially in maintenance, rules, metrics, reporting, integrations, and project resolution.

That lineage deserves clear attribution. Open source competition is healthier when we can say both things at once:

1. tsarch made an important early contribution to TypeScript architecture testing.
2. ArchUnitTS is now the stronger choice for a new project.

Respect for the origin does not require pretending the two packages are equivalent today.

## My recommendation

The Angular Architects architecture is good. The combination of architecture documentation, deterministic tests, and agent hooks is exactly where AI-assisted development should go.

I would only change the package behind the guardrail:

```bash
npm install --save-dev archunit
```

Choose ArchUnitTS for a new project when you care about:

- active releases and current TypeScript behavior;
- inherited and referenced `tsconfig` projects;
- failing safely when selectors match nothing;
- dedicated Jest, Vitest, and Jasmine ergonomics;
- custom rules and architecture metrics;
- dependency graphs and HTML reports;
- a faster feedback loop in the tested Angular project.

Keep tsarch when its existing installation is stable, its narrower feature set is sufficient, and your team is willing to own compatibility fixes. Its accumulated popularity and readable API are legitimate advantages. They are simply weaker than correctness and maintenance for a dependency whose job is to tell you whether the architecture is still protected.

The point of an architecture test is trust.

In 2026, ArchUnitTS gives me more of it.

## Sources and reproduction links

- [Angular Architects: Architecture Beyond Layers — tsarch for AI Coding Agents](https://www.angulararchitects.io/en/blog/architecture-beyond-layers-tsarch-for-ai-agents/)
- [Angular demo source at the benchmarked commit](https://github.com/angular-architects/flights42/tree/caaac81f414188d2ca7410a6e1e236d4a200e5e4)
- [ArchUnitTS repository](https://github.com/LukasNiessen/ArchUnitTS) and [2.5.0 release](https://github.com/LukasNiessen/ArchUnitTS/releases/tag/v2.5.0)
- [tsarch repository](https://github.com/ts-arch/ts-arch) and [5.4.1 release](https://github.com/ts-arch/ts-arch/releases/tag/v5.4.1)
- [tsarch empty-selector issue](https://github.com/ts-arch/ts-arch/issues/73), [open TypeScript 6 PR](https://github.com/ts-arch/ts-arch/pull/87), and [latest `main` CI run](https://github.com/ts-arch/ts-arch/actions/runs/23619864229)
- [Node.js release status](https://nodejs.org/en/about/previous-releases) and [GitHub cache action retirement notice](https://github.com/actions/cache#whats-new)
