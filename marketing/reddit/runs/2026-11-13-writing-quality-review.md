# Promotion writing quality review · 2026-11-13

Workflow review only. No posts submitted or browser drafts changed. The frozen corpus and the original November 8 campaign records remain unchanged.

## What needed improvement

The [Angular and Vue video drafts](2026-11-08-archunit-video-drafts.json) offered generic folder dependency checks with framework names attached. They met the old “one real feature + one community pain point” instruction, but did not demonstrate enough value for those audiences. These drafts were recorded as project showcases, so the revised quality threshold applies across categories, with stronger community tailoring for gift promotions.

The workflow now compares a few evidence-backed angles before drafting and checks community relevance, substantive payoff, and demonstrable behavior before returning a draft or using the composer. It preserves simple explanations and rejects added complexity or hype as substitutes for usefulness.

## Prompt review cases

| Candidate | Expected verdict under the revised guidance |
| --- | --- |
| Angular: shared files must not import feature files | Rewrite: the framework name does most of the tailoring, and the payoff stops at an introductory folder rule. |
| Angular: permit a feature's root public API and internal collaboration, reject outside deep imports and nested internal barrels | Viable: explains selective access, a subtle exception, and what the diagnostic identifies. Scope remains static imports. |
| Vue: a generic recording plus plain TypeScript domain-to-adapter rules | Rewrite or choose a better destination: the recording and a compatibility caveat do not establish meaningful Vue relevance. |
| Python: allow `TYPE_CHECKING` imports while still rejecting runtime dependencies | Keep: a small example can demonstrate a meaningful language-specific distinction. The original [campaign evidence](2026-11-08-archunitpython-gift-drafts.json) records both behaviors. |

Independent review agreed with these verdicts and identified an ambiguity in draft-only handling. The final instructions scope browser preparation without submission to draft-only requests and preserve the standing publish default for promotion requests. Account verification now honors a campaign account already selected in the chat.

## Angular calibration, verified against a public release

A stronger angle is: “An import from `orders/internal` can compile perfectly while tying another feature to details you wanted to keep private. Allow the feature's root API, keep its own internal imports working, and fail outside imports that reach past that API.” The practical benefit is making the intended boundary explicit before reorganizing those internals.

This is a candidate application for an Angular feature layout, not an Angular-exclusive capability, a new integration claim, or a template to repeat for every post.

Verified on 2026-11-13 using [published archunit 2.5.4](https://registry.npmjs.org/archunit/2.5.4), Node 24.22.0, and an isolated TypeScript fixture with an `@app/*` path alias. The rule exercised inside the async check was:

```typescript
const rule = projectFiles('tsconfig.json')
  .inPath('src/app/**/*.ts', {
    except: { inPath: 'src/app/orders/**' },
  })
  .shouldNot()
  .dependOnFiles()
  .inFolder('src/app/orders/**', {
    except: {
      inPath: ['src/app/orders/index.ts', 'src/app/orders/public-api.ts'],
    },
  });

const violations = await rule.check();
```

Exact root paths matter here: filename-wide exceptions could also admit an unintended nested `internal/index.ts`.

| Executed fixture | TypeScript compilation | Architecture result |
| --- | --- | --- |
| Consumers import root public entry points; the feature imports its own service | Pass | No violations |
| Dashboard imports `@app/orders/internal/order.service` | Pass | One violation, dashboard component → internal service |
| Dashboard imports `@app/orders/internal` through its nested barrel | Pass | One violation, dashboard component → internal `index.ts` |
| Public API intentionally re-exports the service and dashboard uses that API | Pass | No violations |

The check identifies import entry points; it does not audit which symbols the public API exports. The fixture verifies static TypeScript imports in an Angular-shaped layout, not a running Angular application, dependency injection, templates, lazy loading, or bundle size. All four compile checks and exact violation assertions passed. Temporary fixture and execution evidence: `/private/tmp/archunit-angular-quality-2026-11-13/`.
