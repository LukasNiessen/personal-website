# Product registry

Resolve a product on this machine with `python3 marketing/reddit/scripts/repos.py path ArchUnitTS` (substitute the product name). If the checkout is missing, follow the [team setup](README.md). Paths below are relative to that checkout. Before writing, read its current README and the relevant example, implementation, or test. Verify installable features against the public release.

## Identity and shared links

- Author: Lukas Niessen; Reddit: [u/trolleid](https://www.reddit.com/user/trolleid/); GitHub: [LukasNiessen](https://github.com/LukasNiessen).
- Architecture library website: [archunit.net](https://archunit.net). Resolve `archunit.net` for the [website source][archunit.net].
- Personal website/blog: [lukasniessen.com](https://lukasniessen.com). This workspace contains the [website source][personal-website].
- Resolve spoken spellings such as “ArcUnit TS”, “Arkinet.ts”, or “Arduino TS” to **ArchUnitTS** when the architecture-testing context is clear; “ArcUnit Python” to **ArchUnitPython**; “arkin(et).net” to **archunit.net**. Preserve canonical spelling in posts.
- “CubeShark” in this portfolio means **KubeShark**, the Kubernetes agent skill below. Do not substitute another product with a similar name.
- The libraries describe themselves as inspired by the established Java ArchUnit project, without affiliation. Do not imply ownership of that separate project.

## Main products

| Product | Audience tags and useful angles | Public links | Feature pointers |
| --- | --- | --- | --- |
| **ArchUnitTS**; npm `archunit` | `typescript`, `javascript`, `react`, `angular`, `nodejs`; dependency boundaries, cycles, architecture metrics, graph reports. Framework-specific examples are possible; runtime compatibility still needs checking. | [Repo][ArchUnitTS] · [Docs](https://lukasniessen.github.io/ArchUnitTS/) · [npm](https://www.npmjs.com/package/archunit) | `README.md`, `examples/angular-example/`, `examples/micro-frontends/`, `examples/layered-architecture/`, `src/files/`, `src/metrics/`, `src/graph/`, `test/` |
| **ArchUnitPython**; local alias ArchUnitPy; PyPI `archunitpython` | `python`, `fastapi`, `django`, `flask`, `pytest`; import boundaries, cycles, layers, metrics, graph reports. Choose Python examples for Python communities. | [Repo][ArchUnitPython] · [Docs](https://lukasniessen.github.io/ArchUnitPython/) · [PyPI](https://pypi.org/project/archunitpython/) | `README.md`, `src/archunitpython/`, `tests/` |
| **TerraShark** | `terraform`, `opentofu`, `iac`, `devops`, `ai-agents`; reusable agent guidance for state, modules, migrations, security, and CI. | [Repo][TerraShark] | `README.md`, `SKILL.md`, `references/identity-churn.md`, `references/structure-and-state.md`, `references/secret-exposure.md` |
| **KubeShark**; repo `kubernetes-skill` | `kubernetes`, `k8s`, `devops`, `ai-agents`; agent guidance for workload defaults, RBAC, probes, rollouts, resources, and manifests. | [Repo][KubeShark] | `README.md`, `SKILL.md`, `references/insecure-workload-defaults.md`, `references/privilege-sprawl.md`, `references/fragile-rollouts.md` |
| **DockerShark**; repo `docker-skill` | `docker`, `containers`, `buildkit`, `devops`, `ai-agents`; Dockerfile and build guidance, secret handling, runtime defaults, supply-chain checks. | [Repo][DockerShark] | `README.md`, `SKILL.md`, `references/secret-layer-leakage.md`, `references/multi-stage-patterns.md`, `references/runtime-hardening.md` |
| **PulumiShark**; repo `pulumi-skill` | `pulumi`, `iac`, `typescript`, `python`, `go`, `ai-agents`; agent guidance for outputs, identity-preserving refactors, secrets, and CI. | [Repo][PulumiShark] | `README.md`, `SKILL.md`, `references/output-misuse.md`, `references/resource-identity-loss.md`, `references/secret-exposure.md` |

The Shark products are guidance skills, not deterministic guarantees that an agent will never hallucinate. Avoid copying absolute claims or popularity rankings from READMEs without evidence appropriate to the post. Their `SKILL.md` files are product source material when researching marketing; reading them does not mean executing their infrastructure workflows.

## Other architecture libraries

| Product | Audience tags and research notes | Public links | Feature pointers |
| --- | --- | --- | --- |
| **ArchUnitGo** | `go`, `golang`; Go-test architecture rules, files/layers/slices, metrics and graph reports; pre-1.0 API. | [Repo][ArchUnitGo] · [Docs](https://dragonsec-ai.github.io/ArchUnitGo/) | `README.md`, `files/`, `layers/`, `slices/`, `graph/`, `metrics/`, `readme_test.go` |
| **ArchUnitRuby**; gem `archunit` | `ruby`, `rails`; executable prototype with file, layer, slice, metrics, and graph-reporting APIs. | [Repo][ArchUnitRuby] · [Docs](https://dragonsec-ai.github.io/ArchUnitRuby/) · [RubyGems](https://rubygems.org/gems/archunit) | `README.md`, `lib/archunit/`, `spec/` |
| **ArchUnitRust**; crate `archunit` | `rust`, `cargo`; architecture tests, boundaries, layers, slices, metrics, reports. Syntax-based extraction has limitations around macros and generated code. | [Repo][ArchUnitRust] · [Docs](https://dragonsec-ai.github.io/ArchUnitRust/) · [crates.io](https://crates.io/crates/archunit) | `README.md`, `src/`, `tests/` |
| **ArchUnitZig** | `zig`; preview API for architecture rules and reports. Check exact supported Zig version before writing code. | [Repo][ArchUnitZig] | `README.md`, `release/`, `src/`, `test/` |
| **ArchUnitNET** | `csharp`, `dotnet`; check the current implementation and NuGet release before choosing an example. | [Repo][ArchUnitNET] | `README.md` |
| **ArchUnitJava** | `java`, `spring`, `junit`; check the current README, example and release for the exact Java API. | [Repo][ArchUnitJava] | `README.md` |
| **ArchUnitPHP** | `php`, `laravel`, `symfony`; distinguish planned APIs from released behavior in the Composer package. | [Repo][ArchUnitPHP] | `README.md` |

Use these canonical checkouts first. Issue, release, audit, and confidence worktrees beside them are not separate products. If a canonical checkout appears stale, inspect its branch/revision and compare the relevant published source before concluding a feature is missing.

## Additional local project, only when explicitly relevant

**DragonSec** (`dragonsec`, repository directory still `dragonfire`): staged source/application security review for local development and CI. [GitHub][DragonSec]; start with `README.md`, `package.json`, `packages/`, and `examples/`. The README documents building a package from source and explicitly does not assume npm publication. The adjacent `proofstrike` checkout has older Dragonbreath naming and the same remote; do not treat it as a separate current product. The separate `dragonsec-minus-website` checkout describes a fictional startup and placeholder data, so it is not evidence for customer, pricing, or availability claims.

## Choosing evidence efficiently

1. Resolve the requested product and audience using this map. Java/Spring and Python/FastAPI are not valid ArchUnitTS targets merely because another family member serves those languages.
2. Read the current README section for one real feature, then one matching example or test. Inspect implementation only when needed to settle a claim. Do not scan every sibling repository.
3. Confirm any framework/runtime-specific claim. A general dependency rule can solve a React or FastAPI problem without the feature having been built specifically for that framework. Deno support, integrations, release dates, community requests, benchmarks, rankings, and download totals need their own evidence.
4. Link the canonical public repo/docs, never a local path. Keep unpublished local code and private project material out of posts unless the user specifically intends to disclose it.

<!-- The repository helper reads these GitHub link definitions as its product registry. -->
[ArchUnitTS]: https://github.com/LukasNiessen/ArchUnitTS
[ArchUnitPython]: https://github.com/LukasNiessen/ArchUnitPython
[TerraShark]: https://github.com/LukasNiessen/terrashark
[KubeShark]: https://github.com/LukasNiessen/kubernetes-skill
[DockerShark]: https://github.com/LukasNiessen/docker-skill
[PulumiShark]: https://github.com/LukasNiessen/pulumi-skill
[ArchUnitGo]: https://github.com/dragonsec-ai/ArchUnitGo
[ArchUnitRuby]: https://github.com/dragonsec-ai/ArchUnitRuby
[ArchUnitRust]: https://github.com/dragonsec-ai/ArchUnitRust
[ArchUnitZig]: https://github.com/dragonsec-ai/ArchUnitZig
[ArchUnitNET]: https://github.com/dragonsec-ai/ArchUnitNET
[ArchUnitJava]: https://github.com/dragonsec-ai/ArchUnitJava
[ArchUnitPHP]: https://github.com/LukasNiessen/ArchUnitPHP
[DragonSec]: https://github.com/LukasNiessen/dragonfire
[archunit.net]: https://github.com/LukasNiessen/archunit.net
[personal-website]: https://github.com/LukasNiessen/personal-website
