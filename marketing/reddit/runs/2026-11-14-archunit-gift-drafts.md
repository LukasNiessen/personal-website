# ArchUnit gift-promotion drafts · 2026-11-14

**30 drafts; 16 submitted.** Statuses and permalinks below reflect this campaign. Unsubmitted entries are not queued. Use cached rules unless missing or expired, and honor visible composer guidance. Reuse this campaign history when checking duplicates.

## 1. ArchUnitTS · Let other Angular features use the public API without exposing every internal file

Audience: Angular feature owners. Candidate: r/angular. Status: submitted.

[Submitted post](https://www.reddit.com/r/angular/comments/1xvn9xi/let_other_angular_features_use_the_public_api/)

An Angular feature can expose a public API and still have other features importing its private services directly. Everything compiles. Then you reorganize that feature and discover how many consumers knew its folder structure.

I maintain ArchUnitTS. Here's a useful boundary you can put in a test: allow imports through the feature's root entry points, reject deep imports from outside, and leave the feature's own internal imports alone.

    const rule = projectFiles('tsconfig.json')
      .inPath('src/app/**/*.ts', {
        except: { inPath: 'src/app/orders/**' },
      })
      .shouldNot().dependOnFiles()
      .inFolder('src/app/orders/**', {
        except: { inPath: [
          'src/app/orders/index.ts',
          'src/app/orders/public-api.ts',
        ] },
      });

Here `projectFiles` is imported from `archunit`; run `await rule.check()` inside an async test and assert that the returned list is empty.

So `@app/orders/public-api` passes, while `@app/orders/internal/order.service` fails. Those aliases need to resolve in your tsconfig. A nested `orders/internal/index.ts` stays private too, because the exceptions are exact paths.

You still decide what the public API exports. This checks the import entry point, not Angular's dependency injection or runtime behavior.

Source: https://github.com/LukasNiessen/ArchUnitTS

## 2. ArchUnitTS · A dependency view for one Express route, instead of the entire backend

Audience: Express maintainers. Candidate: r/expressjs. Status: submitted.

[Submitted post](https://www.reddit.com/r/expressjs/comments/1xvn05c/a_dependency_view_for_one_express_route_instead/)

When an Express route starts doing too much, looking at the route file only gets you so far. Some of the interesting coupling is another import or two away, inside the service it calls.

I maintain ArchUnitTS, and its dependency reports can start from one route module and follow the imports the analysis resolves.

    import { projectGraph } from 'archunit';

    const report = projectGraph()
      .reachableFrom('src/routes/checkout.ts');
    await report.exportAsHTML('reports/checkout-dependencies.html');

Run this in an async function from the project root. In a route → service → store fixture, the report included the store even though the route did not import it directly. An unrelated module stayed out.

That gives you a smaller starting point for splitting a route handler or moving persistence behind an interface. You can inspect that dependency view before deciding which architecture rule to enforce.

It's a static import graph. It won't tell you which middleware ran for a particular request or reconstruct dependencies the extraction cannot resolve.

Source: https://github.com/LukasNiessen/ArchUnitTS

## 3. ArchUnitTS · Check the dependency behind a TypeScript path alias

Audience: TypeScript teams using tsconfig paths. Candidate: unassigned. Status: unsubmitted-draft.

A path alias makes an import look clean. It doesn't tell you whether that import respects your module boundary.

`@app/orders/internal/order.service` is still a deep import into a feature, even though there isn't a long relative path in sight.

I maintain ArchUnitTS. Its file rules can work against the files those aliases resolve to, using your tsconfig. That lets you allow a feature's public entry point and reject its internal service without maintaining a separate policy for every spelling of the import.

I checked this with a small fixture using `@app/*`: the public import passed, the internal service import failed, and the diagnostic identified the source and target files. The TypeScript compiler accepted both imports.

This is useful when aliases make a large app easier to navigate but also make it easier to reach across a boundary. Correct path resolution matters; configure the analysis against the tsconfig that describes your project.

Source: https://github.com/LukasNiessen/ArchUnitTS

## 4. ArchUnitTS · Test the architecture rule with an import that should fail

Audience: Developers maintaining automated architecture tests. Candidate: r/AutomatedTesting. Status: submitted.

[Submitted post](https://www.reddit.com/r/AutomatedTesting/comments/1xvn1zs/test_the_architecture_rule_with_an_import_that/)

An architecture test passing is only useful if the rule would catch the mistake you care about.

I maintain ArchUnitTS. One practical way to check a boundary is to keep a tiny fixture with both a legitimate import and an intentionally forbidden one. This is especially helpful once your rule has exceptions for public entry points or files inside the feature itself.

For example, I checked a feature boundary with four cases: an outside consumer using the public API, an outside consumer reaching into a private service, a nested internal barrel, and the feature using its own internals.

The public API and internal collaboration passed. The two outside deep imports failed, with the actual dependency pair in the result. All four cases were valid TypeScript.

The useful bit is testing the exception as well as the restriction. Otherwise you can end up with a rule that is either too broad to live with or too permissive to catch anything interesting.

ArchUnitTS gives you the violation list through `rule.check()`, so a small verification fixture can use ordinary assertions.

Source: https://github.com/LukasNiessen/ArchUnitTS

## 5. ArchUnitTS · Keep a migration exception from becoming permission for the whole feature

Audience: TypeScript maintainers migrating module boundaries. Candidate: unassigned. Status: unsubmitted-draft.

During a migration, there's usually one awkward import you cannot remove yet. Excluding a whole directory gets the architecture check green, but also gives future code a convenient place to bypass the boundary.

I maintain ArchUnitTS. Its selectors support exclusions on both sides of a dependency rule, so the scope of an exception can be explicit.

You can exclude a named legacy consumer while checking the remaining consumers. Separately, you can allow exact public entry-point paths inside a target feature while keeping the rest of that feature private. Those are different decisions; they don't need one broad folder exclusion.

For a feature boundary I verified that the feature could still import its own service, an outside public-API import passed, and an outside deep import failed. A nested internal barrel did not inherit the root barrel's exception.

The useful part is making the temporary permission visible in a test. Keep the migration exception narrow, and remove it when that consumer has been moved.

Source: https://github.com/LukasNiessen/ArchUnitTS

## 6. ArchUnitTS · Before changing a TypeScript module, look at its indirect consumers

Audience: Developers planning dependency refactors. Candidate: r/devtools. Status: submitted.

[Submitted post](https://www.reddit.com/r/devtools/comments/1xvnf68/before_changing_a_typescript_module_look_at_its/)

Searching for imports of a module finds its direct consumers. A change can matter further up the dependency chain too.

I maintain ArchUnitTS. The graph API has a reverse view for that:

    const report = projectGraph()
      .dependentsOf('src/server/store.ts');
    await report.exportAsHTML('reports/store-consumers.html');

Import `projectGraph` from `archunit` and run this from an async function at the project root.

In a route → service → store fixture, the report included the route as well as the service. An unrelated file was left out. That gives you a focused list to inspect before changing a storage abstraction or moving a shared module.

This isn't a prediction that every listed file will break. It's the transitive dependency view of the imports the tool resolves. I find that distinction useful: use it to decide where to look, then use tests and review to judge the actual change.

Source: https://github.com/LukasNiessen/ArchUnitTS

## 7. ArchUnitTS · Put a readable dependency map next to a small TypeScript project

Audience: Developers sharing programming utilities. Candidate: r/programmingprojects. Status: submitted.

[Submitted post](https://www.reddit.com/r/programmingprojects/comments/1xvnnv6/put_a_readable_dependency_map_next_to_a_small/)

A repo's folder tree tells someone where the code lives. It doesn't show which parts depend on which others.

I maintain ArchUnitTS, and one feature you can use without first designing a set of architecture rules is its dependency report. It can collapse files into folders and export HTML or Mermaid.

For a small tool with parsing, storage and a CLI, a folder-level view is often more useful to a new contributor than a diagram with every file on it. It gives them a way to see that parsing has started depending on CLI code, for example, before they decide where a new option belongs.

The report is generated locally from the dependencies the analysis resolves. You can keep a Mermaid export with the documentation or share the HTML alongside the project.

The graph isn't a runtime trace, and a clean-looking picture isn't proof of good architecture. It is a concrete view you can discuss while the project is still small enough to change.

Source: https://github.com/LukasNiessen/ArchUnitTS

## 8. ArchUnitTS · A public barrel is a policy choice, including what you re-export

Audience: TypeScript library authors. Candidate: unassigned. Status: unsubmitted-draft.

There's a useful distinction between preventing deep imports and deciding what your public API should contain.

I maintain ArchUnitTS. You can allow consumers to import through a library's root entry point while rejecting imports from its internal files. That makes the entry-point policy executable in your test suite.

But if you deliberately re-export an internal service from that allowed entry point, the boundary rule lets consumers use it. I verified that behavior alongside the forbidden deep-import case.

That's the intended division of work: the rule checks where consumers enter the feature. You still review which symbols the entry point exposes.

This is handy when maintaining a library inside a larger TypeScript app. Consumers can stop depending on the internal directory layout, and a test can catch new deep imports. It doesn't pretend that a barrel automatically creates a well-designed API.

Source: https://github.com/LukasNiessen/ArchUnitTS

## 9. ArchUnitPython · A literal plugin import can still be part of your architecture check

Audience: Python developers using dynamic imports. Candidate: r/PythonProgramming. Status: submitted.

[Submitted post](https://www.reddit.com/r/PythonProgramming/comments/1xvnda3/a_literal_plugin_import_can_still_be_part_of_your/)

Replacing a normal import with `importlib.import_module()` doesn't necessarily make the dependency disappear. Sometimes the target is still sitting there as a string literal.

I maintain ArchUnitPython. It can include a call such as `importlib.import_module("app.adapters.store")` in a dependency rule, so moving that import into a plugin factory doesn't automatically avoid the boundary check.

I verified a domain-to-adapter rule against both forms. The ordinary import failed, and the literal dynamic import failed too.

There's a limit worth knowing: when the module name comes from an environment variable or another computed value, the analysis cannot infer it from that literal. An omitted edge isn't evidence that no runtime dependency exists.

This is useful for projects with a mix of regular imports and simple plugin loading. You can enforce the relationships that are statically visible while keeping the genuinely dynamic part explicit in your review and tests.

Source: https://github.com/LukasNiessen/ArchUnitPython

## 10. ArchUnitPython · Keep SDK imports at the integration boundary, not just your own adapters

Audience: Python library maintainers. Candidate: r/PythonLibraries. Status: submitted.

[Submitted post](https://www.reddit.com/r/pythonlibraries/comments/1xvn7x2/keep_sdk_imports_at_the_integration_boundary_not/)

A rule against importing your database adapter won't catch someone importing the database SDK directly.

I maintain ArchUnitPython. Its dependency rules can target external modules as well as files inside your project, which is useful when a library's core should remain independent of a particular HTTP client or persistence package.

    from archunitpython import project_files, assert_passes

    def test_core_does_not_use_requests_directly():
        rule = (
            project_files("src/")
            .in_path("**/domain/**")
            .should_not()
            .depend_on_external_modules()
            .matching("requests")
        )
        assert_passes(rule)

In the verification fixture, importing `requests` failed; importing an unrelated standard-library module passed. The rule applies to the selected source files, so your integration layer can still use the client.

That is the useful distinction: you are expressing which part of the codebase may know about a dependency, rather than treating an installed package as permission to use it everywhere.

Source: https://github.com/LukasNiessen/ArchUnitPython

## 11. ArchUnitPython · Make the type-only dependency decision explicit in Python architecture tests

Audience: Python developers discussing static analysis. Candidate: r/pythoncoding. Status: skipped.

Automatic approval review rejected submission, interpreting the community prohibition on items being sold as a possible conflict with promotional content. No Submit action executed.

A dependency under `if TYPE_CHECKING:` is still a relationship in your source, but it isn't the same thing as executing that import at runtime. An architecture rule needs to be clear about which relationship it is protecting.

I maintain ArchUnitPython. The default analysis counts those imports. If a particular check is about runtime coupling, you can opt out:

    assert_passes(
        rule,
        CheckOptions(ignore_type_checking_imports=True),
    )

Both names are imported from `archunitpython`; `rule` is your file dependency rule.

I checked a domain-to-adapter example both ways. A guarded import failed under the default policy and passed with the option. Moving the same import outside the guard still failed with the option enabled.

So the option doesn't mean “ignore dependencies from typed code.” It makes one specific exclusion. Leave it off if the boundary should forbid type-level coupling too.

The library is open source, and the source includes the import extraction and rule implementation. This is static source analysis, not a measurement of imports observed during execution.

Source: https://github.com/LukasNiessen/ArchUnitPython

## 12. ArchUnitPython · Keep an architecture migration exception on the import that needs it

Audience: Python developers migrating dependencies. Candidate: r/pythontips. Status: submitted.

[Submitted post](https://www.reddit.com/r/pythontips/comments/1xvnm2x/keep_an_architecture_migration_exception_on_the/)

A migration exception is easier to review when it sits next to the import that needs it.

I maintain ArchUnitPython. For a known compatibility shim, it supports an inline directive:

    from app.adapters.store import Store  # archunit: ignore

That import edge is omitted from the architecture analysis. You don't have to exclude the entire module from every rule just to keep that one temporary dependency working.

I checked the same import with and without the directive against a domain-to-adapter boundary. The ordinary import failed. The annotated import was excluded.

Treat this as a visible exception, not a way to declare the design fixed. Add a reason in a nearby comment and remove the directive with the migration. The rest of the module should still be checked.

It's useful when a rule is worth enforcing now but one old call site cannot be moved in the same change.

Source: https://github.com/LukasNiessen/ArchUnitPython

## 13. ArchUnitPython · A renamed Python folder should not silently retire its architecture test

Audience: Python teams maintaining pytest architecture checks. Candidate: r/madeinpython. Status: submitted.

[Submitted post](https://www.reddit.com/r/madeinpython/comments/1xw1rrj/a_renamed_python_folder_should_not_silently/)

You rename a package, update its imports, and the tests are green. An architecture test that still points at the old directory can look green for a less useful reason: it isn't checking any files.

I maintain ArchUnitPython. Its file rules report an empty selection as a violation by default. I verified that with a cycle rule pointing at a missing directory, alongside a real dependency rule with both passing and failing imports.

This is useful for long-lived pytest suites where the architecture checks might be edited less often than the code they protect. A stale selector becomes something to fix instead of a rule that quietly disappears.

There is an option for intentionally empty selections, but keep that permission deliberate. A generated directory that is absent in one build is a different situation from a package path that nobody updated after a refactor.

The library gives you normal assertions through `assert_passes`, so this fits into the same test run as your behavioral checks.

Source: https://github.com/LukasNiessen/ArchUnitPython

## 14. ArchUnitPython · Start an architecture review with the dependency graph, before writing the rules

Audience: Python teams reviewing package boundaries. Candidate: unassigned. Status: unsubmitted-draft.

Sometimes the hard part isn't writing a dependency rule. It's agreeing on which boundary the current code actually has.

I maintain ArchUnitPython. You can generate a dependency map before enforcing anything, and collapse the files to folders so it stays readable:

    from archunitpython import project_graph

    graph = project_graph("src/").collapse_to_folder_depth(2)
    graph.export_as_mermaid("reports/dependencies.mmd")

That gives a review something concrete to point at. If domain code and adapters have gradually become tangled, you can discuss the relationship itself rather than arguing from the directory names.

I checked the export with a small two-group fixture; both groups and their dependency appeared in the collapsed diagram. Mermaid is useful when you want to keep the output next to documentation; HTML is available too.

The map follows imports the analysis resolves. It doesn't reconstruct arbitrary runtime loading, so use it as evidence for the discussion rather than a complete description of execution.

Source: https://github.com/LukasNiessen/ArchUnitPython

## 15. ArchUnitPython · Keep FastAPI exceptions at the HTTP edge of an application

Audience: FastAPI developers with reusable application services. Candidate: unassigned. Status: unsubmitted-draft.

A service that raises `HTTPException` is convenient inside a FastAPI endpoint. Reuse the service from a job or CLI and that HTTP decision has followed it into a different interface.

I maintain ArchUnitPython. External-module dependency rules give you a way to express that decision in the test suite: your application code can return its own result or error, while the HTTP layer owns imports from `fastapi`.

The mechanism is a rule selecting the application files, then `should_not().depend_on_external_modules().matching("fastapi")`. Adapt the selected path to your layout. I verified the same external-module rule mechanism with a forbidden third-party import and an allowed unrelated import.

This doesn't decide whether your service design is good, and it doesn't inspect FastAPI's runtime dependency injection. It checks a concrete coupling that is otherwise easy to add during endpoint work.

If sharing type definitions across that boundary is intentional, decide separately whether type-only imports should count. The library has an opt-in `TYPE_CHECKING` exclusion; it isn't necessary to discard runtime checks to keep annotations.

Source: https://github.com/LukasNiessen/ArchUnitPython

## 16. ArchUnitPython · A plugin boundary needs a passing case and a visibility limit

Audience: Python teams with configurable plugin systems. Candidate: unassigned. Status: unsubmitted-draft.

A plugin system can contain two very different kinds of dynamic imports: a fixed module name in a factory, and a name selected from configuration at runtime.

I maintain ArchUnitPython. Its static dependency analysis can see a literal call such as `importlib.import_module("app.adapters.store")`. It cannot turn every computed string into a reliable import target.

I put both forms through the same boundary check. The literal import into the forbidden adapter produced a violation. A target read from an environment variable wasn't inferred.

That distinction is useful when deciding what an architecture test covers. You can enforce the fixed relationships, keep the dynamic extension point visible in the design, and test that runtime selection separately.

A missing graph edge should not be sold as proof that the dependency cannot happen. The tool gives you a useful check for the statically known part of the plugin system without running the plugin just to discover its imports.

Source: https://github.com/LukasNiessen/ArchUnitPython

## 17. ArchUnitRust · Check Rust import cycles without treating every module declaration as one

Audience: Rust library authors. Candidate: r/madeinrust. Status: submitted.

[Submitted post](https://www.reddit.com/r/madeinrust/comments/1xvn60j/check_rust_import_cycles_without_treating_every/)

A Rust parent declares a child module, and the child uses a type exposed by its parent. If you put every relationship into one cycle graph, module organization can get mixed up with the import policy you actually wanted to check.

I maintain ArchUnitRust. You can choose which dependency kinds belong in a cycle rule:

    use archunit::{ImportKind, assert_passes, project_files};

    #[test]
    fn implementation_imports_stay_cycle_free() {
        let rule = project_files()
            .in_path("src/parent**")
            .should()
            .have_no_cycles()
            .excluding_dependency_kinds([
                ImportKind::Mod,
                ImportKind::PubUse,
            ]);
        assert_passes!(rule);
    }

Use a selector matching your actual module. In my fixture, excluding those structural kinds removed the parent/child-only cycle. Adding an ordinary import in the other direction still produced a cycle violation.

That last part matters: this doesn't simply delete every edge between those files. Retained import evidence can keep the edge in the check.

It runs as an ordinary Cargo test. The extraction is syntax-based; this is an import policy, not proof about runtime call cycles.

Source: https://github.com/dragonsec-ai/ArchUnitRust

## 18. ArchUnitRust · Keep a Rust simulation module independent of the engine crate

Audience: Rust game developers separating simulation and presentation. Candidate: r/rust_gamedev. Status: skipped.

Game-specific benefit not sufficiently demonstrated by the verified fixture.

If you want to run simulation logic without the renderer or engine, keeping it in a separate folder is only the first step. A convenient engine import can quietly make that separation much less useful.

I maintain ArchUnitRust. Its architecture rules can check external crate usage in selected source files, so you can express which modules are allowed to depend on the engine.

The rule shape is `project_files().in_path("src/simulation/**").should_not().depend_on_external_modules().matching("your_engine_crate")`. Use the actual crate name and execute the rule in a Cargo test.

I verified that mechanism with an external import that passed an allowlist and failed a denylist. The point is the source-level policy: code outside the selected simulation scope can keep using the dependency.

This won't prove the simulation is deterministic or safe to run headless. It checks one concrete reason that separation can erode. Macro-generated dependencies and build-script-generated source are outside the documented extraction scope.

Source: https://github.com/dragonsec-ai/ArchUnitRust

## 19. ArchUnitRust · A local dependency report for a Rust project, with no hosted dashboard

Audience: Maintainers who want local open-source tooling. Candidate: r/foss. Status: submitted.

[Submitted post](https://www.reddit.com/r/foss/comments/1xvnikl/a_local_dependency_report_for_a_rust_project_with/)

If you want to inspect a Rust project's dependencies between source files, you shouldn't need a hosted dashboard just to get a diagram out.

I maintain ArchUnitRust, an MIT-licensed architecture-testing library. Its graph builder can export JSON, Mermaid and self-contained HTML from the same source graph.

You can narrow the view to the consumers of one file or collapse it to folders before sharing it. I verified a reverse dependency view and HTML output against the published crate, rather than just taking a screenshot of the README.

That makes it useful for a small open-source project: keep a text diagram with the docs, attach an HTML report to a review, or inspect it locally before deciding which boundary to enforce.

The graph is static source evidence, not a runtime trace. Rust macros and build-script-generated source have documented limits, so the report should help you ask better questions about the architecture rather than claim to describe everything the program does.

Source: https://github.com/dragonsec-ai/ArchUnitRust

## 20. ArchUnitRust · Use the dependency graph as data when reviewing a Rust refactor

Audience: Rust maintainers building review tooling. Candidate: unassigned. Status: unsubmitted-draft.

A diagram is useful for looking at dependencies. Sometimes you also want the graph as data, so a review script can focus on the part that changed.

I maintain ArchUnitRust. Its graph builder can return JSON and narrow the source graph with `dependents_of` or `reachable_from` before rendering it.

For example, a reverse view starting at an internal module can show which source files depend on it. That gives you a bounded set to inspect when moving a module or changing the facade it sits behind.

I verified the reverse query against a small Cargo fixture and checked that the dependent parent was present in the output. The same graph builder produced an HTML report too.

Use the JSON to support a review, not to label every consumer as broken. A dependency path tells you where coupling exists in the analysis; it doesn't tell you whether a particular API change is compatible.

The crate is available as `archunit`, and the reports can be generated locally.

Source: https://github.com/dragonsec-ai/ArchUnitRust

## 21. ArchUnitRust · An architecture test should complain when its Rust module no longer exists

Audience: Rust teams maintaining Cargo test suites. Candidate: unassigned. Status: unsubmitted-draft.

A module gets renamed, its imports get fixed, and an architecture test still selects the old path. That's a surprisingly easy way for a useful check to stop doing work.

I maintain ArchUnitRust. A file rule that selects no files reports an `EmptyTestViolation` by default. I checked it with a cycle rule pointing at a missing source directory.

That is useful when the rule lives in `tests/architecture.rs` while the implementation keeps moving around. The stale selector shows up in the same Cargo test run as your other failures.

There is an explicit option for allowing empty selections. Use it when the scope is intentionally optional, rather than as a blanket way to silence the check.

This is a small feature, but it protects the meaning of the test: a passing rule should mean the selected code satisfied the policy, not that the selected code disappeared months ago.

Source: https://github.com/dragonsec-ai/ArchUnitRust

## 22. ArchUnitRust · A cfg-gated import is still visible to a source-level dependency policy

Audience: Rust maintainers with feature-gated modules. Candidate: unassigned. Status: unsubmitted-draft.

A dependency can be absent from your current Cargo build and still be present in a `cfg` branch in the source.

I maintain ArchUnitRust. Its syntax-based extraction treats those branches conservatively rather than claiming to describe only the active feature combination.

I verified that an external import behind a feature guard still appeared in an external-dependency rule. That makes the rule useful when your policy is “this module should not depend on that crate in any source branch,” rather than “this particular build did not use it.”

The distinction matters when reading a failure. It may be pointing at an optional implementation that wasn't compiled in the test run, not inventing a dependency out of nowhere.

This does not replace testing your supported Cargo feature combinations, and the tool doesn't expand macro-generated or build-script-generated source. It gives you a source-level boundary check with an explicit scope.

Source: https://github.com/dragonsec-ai/ArchUnitRust

## 23. ArchUnitRust · Cargo declares dependencies for a package; architecture rules can narrow who uses them

Audience: Rust library maintainers. Candidate: unassigned. Status: unsubmitted-draft.

Adding a crate to `Cargo.toml` makes it available to the package. It doesn't express which part of your implementation should know about it.

I maintain ArchUnitRust. External-dependency rules let you put that narrower policy into a Cargo test. A core module can have an allowlist while an adapter module is free to use a larger set of dependencies.

For example, `.should().depend_on_external_modules().matching("std")` expresses an allowlist for the selected source files. A negative rule can forbid a particular crate instead. Choose the policy that matches the module, rather than applying a standard-library-only rule to the whole project.

I verified the same external import against both policies: it passed when allowed and failed when forbidden. That is useful when a convenient dependency starts spreading beyond the integration code that originally needed it.

The rule operates on extracted source dependencies. It isn't a replacement for Cargo's dependency resolution or a claim about every dependency generated by macros.

Source: https://github.com/dragonsec-ai/ArchUnitRust

## 24. ArchUnitRuby · Catch a presentation mixin leaking into a Rails model without a require line

Audience: Rails developers using autoloaded constants. Candidate: r/rails. Status: submitted.

[Submitted post](https://www.reddit.com/r/rails/comments/1xvnblq/catch_a_presentation_mixin_leaking_into_a_rails/)

A Rails model can pick up a presentation dependency through `include Presentation::FormattedOrder` without adding a `require_relative` anywhere. An import-only check can miss the relationship you actually care about.

I maintain ArchUnitRuby. There is an opt-in mode that adds known project constant references to the dependency graph:

    options = ArchUnit::CheckOptions.new(
      dependency_analysis: :imports_and_constants
    )
    rule = ArchUnit.project_files
      .in_path('app/models/**')
      .should_not.depend_on_files
      .in_path('app/presentation/**')

    ArchUnit.assert_passes(rule, options)

Require `archunit` in the test setup and adapt the two paths to your app.

I verified this with a model including a root-qualified presentation mixin. Import-only mode found no edge; the expanded mode reported the dependency. Removing the mixin made the rule pass.

That gives you a check for a real autoloading case without booting Rails to collect runtime references. It is still static analysis: dynamic constant definitions and ambiguous ownership have documented limits.

Disclosure: this post was drafted with AI assistance; the example was checked against the published gem.

Source: https://github.com/dragonsec-ai/ArchUnitRuby

## 25. ArchUnitRuby · Ruby constant lookup needs more than matching the last name

Audience: Ruby developers with nested namespaces. Candidate: r/ruby. Status: submitted.

[Submitted post](https://www.reddit.com/r/ruby/comments/1xvngx0/ruby_constant_lookup_needs_more_than_matching_the/)

`Store` and `::Billing::Store` aren't interchangeable names just because they end the same way. Once a Ruby project has nested namespaces, a dependency tool needs to account for where a reference lives.

I maintain ArchUnitRuby. Its opt-in constant analysis resolves known project definitions and records the dependency on the defining file, rather than treating every occurrence of the word `Store` as the same thing.

The supported lookup model includes lexical nesting and explicit root-qualified references. It also has limits: reopened definitions can be ambiguous, and dynamic constant operations aren't a license to guess which file owns a name.

I verified a qualified project-constant reference against a file boundary: it produced a violation, while unrelated code in the same selected file passed. The constant didn't need a matching `require_relative` to appear in the graph.

This is useful when import-only rules are too quiet for your Ruby codebase. Enable `dependency_analysis: :imports_and_constants` deliberately and review the documented lookup limits before treating the graph as complete.

Source: https://github.com/dragonsec-ai/ArchUnitRuby

## 26. ArchUnitRuby · Make architecture checks understand a nonstandard component source directory

Audience: Rails teams with internal components. Candidate: r/rubyonrails. Status: submitted.

[Submitted post](https://www.reddit.com/r/rubyonrails/comments/1xvn4b1/make_architecture_checks_understand_a_nonstandard/)

An internal component doesn't always put its Ruby files under the application's usual source layout. If its `require` paths resolve through a custom source directory, an architecture check needs to know that directory too.

I maintain ArchUnitRuby. You can provide project-contained load paths for the check:

    options = ArchUnit::CheckOptions.new(
      load_paths: ['components/billing/source']
    )
    violations = rule.check(options)

Here `rule` is the file boundary you want to enforce. The paths are relative to the project root.

I tested a consumer requiring `billing/store` from that component directory. With the source root configured, a rule forbidding that component dependency caught it. An unrelated standard-library import passed.

This is useful when extracting parts of an application into internal components: you can keep checking the relationship after the physical layout changes.

It doesn't reproduce every Rails loader customization or evaluate your application to discover its paths. You provide the nonstandard roots that the static analysis should use.

Source: https://github.com/dragonsec-ai/ArchUnitRuby

## 27. ArchUnitRuby · A Ruby dependency map that can show constant references as well as imports

Audience: Developers building tools for Ruby codebases. Candidate: r/IMadeThis. Status: submitted.

[Submitted post](https://www.reddit.com/r/IMadeThis/comments/1xw1omc/a_ruby_dependency_map_that_can_show_constant/)

I maintain ArchUnitRuby. One part that is useful outside the actual test assertions is the dependency report, particularly for Ruby code that relies on autoloaded constants.

With constant analysis enabled, a known project-constant reference can appear in the same graph as imports. That makes relationships visible in autoloaded Ruby code even when there are few `require_relative` calls to analyze.

I checked a model referencing a presentation module without an import. The expanded graph included the relationship and marked it as constant-reference evidence. The corresponding architecture rule could fail on that same relationship.

The useful workflow is to inspect a suspicious edge in a report, then turn the boundary you actually want into a test. You're not maintaining a diagram and a separate, unrelated set of assumptions about the code.

This is a free, open-source Ruby gem. The graph is static and intentionally leaves unresolved or ambiguous constant ownership out rather than assigning an arbitrary file.

Source: https://github.com/dragonsec-ai/ArchUnitRuby

## 28. ArchUnitRuby · Keep a directory rename from making a Ruby architecture test meaningless

Audience: Ruby maintainers using RSpec or Minitest. Candidate: unassigned. Status: unsubmitted-draft.

An architecture check can outlive the directory layout it was written for. If a folder moves and the selector isn't updated, a passing test may mean it checked nothing.

I maintain ArchUnitRuby. File rules report an empty subject selection as an `EmptyTestViolation` by default. I verified that with a cycle rule selecting a missing directory.

That matters in RSpec or Minitest because architecture rules are often small pieces of test code that don't change alongside every refactor. A stale path becomes a failure you can act on.

The gem has an explicit `allow_empty_tests` option for a genuinely optional scope. Keep that exception local to the case that needs it instead of disabling the protection for every rule.

It's a modest feature with a practical payoff: the test keeps asking about real files as the application changes, rather than quietly turning into documentation that no longer runs.

Source: https://github.com/dragonsec-ai/ArchUnitRuby

## 29. ArchUnitRuby · Check imports between internal gems without evaluating their gemspecs

Audience: Ruby maintainers with multiple gems in one repository. Candidate: unassigned. Status: unsubmitted-draft.

A repository with several internal gems can have several `lib` directories. A `require 'accounts/store'` may belong to one of those sibling gems, even though it isn't under the root library directory.

I maintain ArchUnitRuby. Its source discovery uses nested gemspec locations to find adjacent existing `lib` directories, without evaluating the gemspecs.

I verified that with a tiny repository containing an accounts gem. A boundary rule caught a consumer importing its store. The fixture's gemspec would raise if executed; the analysis still resolved the source without running it.

This is useful when you want to inspect coupling between internal gems while keeping analysis separate from build-time Ruby execution. For a nonstandard source directory, there is also an explicit `load_paths` option.

It is static resolution, not a complete simulation of Bundler or arbitrary `$LOAD_PATH` changes at runtime. The benefit is making the common repository layout visible to the check without booting every component.

Source: https://github.com/dragonsec-ai/ArchUnitRuby

## 30. ArchUnitRuby · Why constant-aware dependency checks are opt-in in my Ruby library

Audience: Builders evolving developer tools. Candidate: r/buildinpublic. Status: submitted.

[Submitted post](https://www.reddit.com/r/buildinpublic/comments/1xw1q8h/why_constantaware_dependency_checks_are_optin_in/)

Ruby code can gain a dependency through a constant reference without adding an import. That makes import-only analysis quiet in some autoloaded applications, but changing the default also changes what existing architecture tests mean.

I maintain ArchUnitRuby, a free MIT-licensed gem. The constant-aware mode is explicit: `dependency_analysis: :imports_and_constants`.

That means an existing rule can keep its import-only interpretation until you choose to expand it. When you do, the graph and the rule check use the additional known project-constant relationships.

I verified a concrete case: a model including a presentation mixin passed in import-only mode and failed with constant analysis enabled. Removing the dependency made it pass again. The graph output retained the constant-reference evidence too.

For anyone building analysis tools, this is a useful API decision to make visible. “The analyzer sees more” can mean “your existing test now fails,” even when the application itself hasn't changed.

The static lookup has documented limits; the mode doesn't promise to reconstruct arbitrary metaprogramming.

Source: https://github.com/dragonsec-ai/ArchUnitRuby
