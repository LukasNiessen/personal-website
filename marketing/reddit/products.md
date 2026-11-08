# Product registry

Local inventory checked on **2026-11-08**. This is a lookup map, not a frozen feature specification. Before writing, read the selected repository's current README and only the relevant example, implementation, or test. A feature in a checkout is not necessarily in the published release. Check release availability before claiming users can install it today.

## Identity and shared links

- Author: Lukas Niessen; Reddit: [u/trolleid](https://www.reddit.com/user/trolleid/); GitHub: [LukasNiessen](https://github.com/LukasNiessen).
- Architecture library website: [archunit.net](https://archunit.net). Local source: `/Users/78079/Repos/Private/archunit.net`; [GitHub](https://github.com/LukasNiessen/archunit.net).
- Personal website/blog: [lukasniessen.com](https://lukasniessen.com). Local source: `/Users/78079/Repos/Private/personal-website`; [GitHub](https://github.com/LukasNiessen/personal-website).
- Resolve spoken spellings such as “ArcUnit TS”, “Arkinet.ts”, or “Arduino TS” to **ArchUnitTS** when the architecture-testing context is clear; “ArcUnit Python” to **ArchUnitPython**; “arkin(et).net” to **archunit.net**. Preserve canonical spelling in posts.
- “CubeShark” in this portfolio means **KubeShark**, the Kubernetes agent skill below. Do not substitute another product with a similar name.
- The libraries describe themselves as inspired by the established Java ArchUnit project, without affiliation. Do not imply ownership of that separate project.

## Main products

Source pointers below are relative to the absolute checkout path in the same row. README content and Git remotes establish the names and URLs; the pointers identify where to verify a specific claim.

| Product | Audience tags and useful angles | Public links | Local checkout and feature pointers |
| --- | --- | --- | --- |
| **ArchUnitTS**; npm `archunit` | `typescript`, `javascript`, `react`, `angular`, `nodejs`; dependency boundaries, cycles, architecture metrics, graph reports. Framework-specific examples are possible; runtime compatibility still needs checking. | [Repo](https://github.com/LukasNiessen/ArchUnitTS) · [Docs](https://lukasniessen.github.io/ArchUnitTS/) · [npm](https://www.npmjs.com/package/archunit) | `/Users/78079/Repos/Private/ArchUnitTS`; `README.md`, `examples/angular-example/`, `examples/micro-frontends/`, `examples/layered-architecture/`, `src/files/`, `src/metrics/`, `src/graph/`, `test/` |
| **ArchUnitPython**; local alias ArchUnitPy; PyPI `archunitpython` | `python`, `fastapi`, `django`, `flask`, `pytest`; import boundaries, cycles, layers, metrics, graph reports. Choose Python examples for Python communities. | [Repo](https://github.com/LukasNiessen/ArchUnitPython) · [Docs](https://lukasniessen.github.io/ArchUnitPython/) · [PyPI](https://pypi.org/project/archunitpython/) | `/Users/78079/Repos/Private/ArchUnitPy`; `README.md`, `src/archunitpython/`, `tests/` |
| **TerraShark** | `terraform`, `opentofu`, `iac`, `devops`, `ai-agents`; reusable agent guidance for state, modules, migrations, security, and CI. | [Repo](https://github.com/LukasNiessen/terrashark) | `/Users/78079/Repos/Private/terrashark`; `README.md`, `SKILL.md`, `references/identity-churn.md`, `references/structure-and-state.md`, `references/secret-exposure.md` |
| **KubeShark**; repo `kubernetes-skill` | `kubernetes`, `k8s`, `devops`, `ai-agents`; agent guidance for workload defaults, RBAC, probes, rollouts, resources, and manifests. | [Repo](https://github.com/LukasNiessen/kubernetes-skill) | `/Users/78079/Repos/Private/kubernetes-skill`; `README.md`, `SKILL.md`, `references/insecure-workload-defaults.md`, `references/privilege-sprawl.md`, `references/fragile-rollouts.md` |
| **DockerShark**; repo `docker-skill` | `docker`, `containers`, `buildkit`, `devops`, `ai-agents`; Dockerfile and build guidance, secret handling, runtime defaults, supply-chain checks. | [Repo](https://github.com/LukasNiessen/docker-skill) | `/Users/78079/Repos/Private/docker-skill`; `README.md`, `SKILL.md`, `references/secret-layer-leakage.md`, `references/multi-stage-patterns.md`, `references/runtime-hardening.md` |
| **PulumiShark**; repo `pulumi-skill` | `pulumi`, `iac`, `typescript`, `python`, `go`, `ai-agents`; agent guidance for outputs, identity-preserving refactors, secrets, and CI. | [Repo](https://github.com/LukasNiessen/pulumi-skill) | `/Users/78079/Repos/Private/pulumi-skill`; `README.md`, `SKILL.md`, `references/output-misuse.md`, `references/resource-identity-loss.md`, `references/secret-exposure.md` |

The Shark products are guidance skills, not deterministic guarantees that an agent will never hallucinate. Avoid copying absolute claims or popularity rankings from READMEs without evidence appropriate to the post. Their `SKILL.md` files are product source material when researching marketing; reading them does not mean executing their infrastructure workflows.

## Other architecture libraries

| Product | Audience tags and local status at inventory time | Public links | Local checkout and feature pointers |
| --- | --- | --- | --- |
| **ArchUnitGo** | `go`, `golang`; Go-test architecture rules, files/layers/slices, metrics and graph reports; pre-1.0 API. | [Repo](https://github.com/LukasNiessen/ArchUnitGo) · [Docs](https://lukasniessen.github.io/ArchUnitGo/) | `/Users/78079/Repos/Private/ArchUnitGo`; `README.md`, `files/`, `layers/`, `slices/`, `graph/`, `metrics/`, `readme_test.go` |
| **ArchUnitRuby**; gem `archunit` | `ruby`, `rails`; executable prototype with file, layer, slice, metrics, and graph-reporting APIs. | [Repo](https://github.com/LukasNiessen/ArchUnitRuby) · [Docs](https://lukasniessen.github.io/ArchUnitRuby/) · [RubyGems](https://rubygems.org/gems/archunit) | `/Users/78079/Repos/Private/ArchUnitRuby`; `README.md`, `lib/archunit/`, `spec/` |
| **ArchUnitRust**; crate `archunit` | `rust`, `cargo`; architecture tests, boundaries, layers, slices, metrics, reports. Syntax-based extraction has limitations around macros and generated code. | [Repo](https://github.com/LukasNiessen/ArchUnitRust) · [Docs](https://lukasniessen.github.io/ArchUnitRust/) · [crates.io](https://crates.io/crates/archunit) | `/Users/78079/Repos/Private/ArchUnitRust`; `README.md`, `src/`, `tests/` |
| **ArchUnitZig** | `zig`; preview API for architecture rules and reports. Check exact supported Zig version before writing code. | [Repo](https://github.com/LukasNiessen/ArchUnitZig) | `/Users/78079/Repos/Private/ArchUnitZig`; `README.md`, `release/`, `src/`, `test/` |
| **ArchUnitNET** | `csharp`, `dotnet`; this checkout's README says early development with nothing to install. Recheck implementation and release state before promotion. | [Repo](https://github.com/LukasNiessen/ArchUnitNET) | `/Users/78079/Repos/Private/ArchUnitNET`; `README.md` |
| **ArchUnitJava** | `java`, `spring`, `junit`; this checkout is a planned delivery skeleton. README snippets describe a design target, not a released API. | [Repo](https://github.com/LukasNiessen/ArchUnitJava) | `/Users/78079/Repos/Private/ArchUnitJava`; `README.md` |
| **ArchUnitPHP** | `php`, `laravel`, `symfony`; this checkout is a planned delivery skeleton. Do not advertise planned APIs as shipped. | [Repo](https://github.com/LukasNiessen/ArchUnitPHP) | `/Users/78079/Repos/Private/ArchUnitPHP`; `README.md` |

Use these canonical checkouts first. Issue, release, audit, and confidence worktrees beside them are not separate products. If a canonical checkout appears stale, inspect its branch/revision and compare the relevant published source before concluding a feature is missing.

## Additional local project, only when explicitly relevant

**DragonSec** (`dragonsec`, repository directory still `dragonfire`): staged source/application security review for local development and CI. [GitHub](https://github.com/LukasNiessen/dragonfire); checkout `/Users/78079/Repos/Private/dragonfire`; start with `README.md`, `package.json`, `packages/`, and `examples/`. The README documents building a package from source and explicitly does not assume npm publication. The adjacent `proofstrike` checkout has older Dragonbreath naming and the same remote; do not treat it as a separate current product. The website checkout `/Users/78079/Repos/Private/dragonsec-minus-website` describes a fictional startup and placeholder data, so it is not evidence for customer, pricing, or availability claims.

## Choosing evidence efficiently

1. Resolve the requested product and audience using this map. Java/Spring and Python/FastAPI are not valid ArchUnitTS targets merely because another family member serves those languages.
2. Read the current README section for one real feature, then one matching example or test. Inspect implementation only when needed to settle a claim. Do not scan every sibling repository.
3. Confirm any framework/runtime-specific claim. A general dependency rule can solve a React or FastAPI problem without the feature having been built specifically for that framework. Deno support, integrations, release dates, community requests, benchmarks, rankings, and download totals need their own evidence.
4. Link the canonical public repo/docs, never a local path. Keep unpublished local code and private project material out of posts unless the user specifically intends to disclose it.
