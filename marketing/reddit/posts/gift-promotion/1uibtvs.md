```json
{
  "id": "1uibtvs",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "angular",
  "created_utc": 1782688474.0,
  "created_at": "2026-06-29T01:14:34+02:00",
  "permalink": "https://www.reddit.com/r/angular/comments/1uibtvs/my_architecture_testing_library_now_has_special/",
  "link_url": "https://github.com/LukasNiessen/ArchUnitTS",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "reddit",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "0de2ee90f0b5d9688e5b2482492b7d9362687254710e6da3904f605911202f48",
  "body_sha256": "19a6c31cd6d6cfc55d4b03b4e83c0cca88de40d8da41ad8aa06d6b34b78a3923",
  "body_characters": 3923
}
```

# Original title

My architecture testing library now has special Angular Support (ArchUnitTS)

## Original body

A week ago I posted about ArchUnitTS, my library for enforcing architecture rules in TypeScript projects as unit tests.

A few of you specifically asked whether this could be used to enforce **clean Angular feature/module boundaries** in real projects:
making sure feature modules don’t import directly from each other’s internal files, and instead communicate through public API barrel files like `index.ts` or `public-api.ts`.

**So to that request I’ve added exactly that.**

------

First a mini recap of what ArchUnitTS does:

* Most tools catch style issues, formatting issues, or generic smells.
* ArchUnitTS focuses on structural rules: wrong dependency directions, circular dependencies, naming convention drift, architecture/diagram mismatch, code metrics, and so on.
* You define those rules as tests, run them in Jest/Vitest/Jasmine/Mocha/etc., and they automatically become part of CI/CD.

In other words: **ArchUnitTS allows you to enforce your architectural decisions by writing them as simple unit tests.**

That matters more than ever in Claude Code / Codex times, because LLMs are great at generating code but they love to violate architectural boundaries, especially when they get stuck.

Repo: https://github.com/LukasNiessen/ArchUnitTS

------

Now what’s new

**Exclusion-aware dependency rules for Angular public API boundaries**

Before, ArchUnitTS could already enforce internal dependency rules like:

* “components must not depend on infrastructure”
* “core must not depend on shared”
* “feature A must not depend on feature B”
* “folders must be cycle-free”

But one common Angular case was still a bit annoying to express cleanly:

A component in one feature should not import directly from another feature’s internal files.

For example, this should usually be forbidden:

```typescript
import { OrderService } from '../orders/internal/order.service';
import { OrderCardComponent } from '../orders/components/order-card.component';
```

But this should be allowed:

```typescript
import { OrderSummary } from '../orders';
import { PUBLIC_ORDERS_TOKEN } from '../orders/public-api';
```

This is not technically always a circular dependency.  
But it is still architectural coupling.

It means another feature now knows the internal folder structure of `orders`. If the `orders` feature reorganizes its components, services, hooks, facades, or models, unrelated features can suddenly break.

So ArchUnitTS now supports `except` in pattern matchers.

Example:

```typescript
import { projectFiles } from 'archunit';

it('should consume orders only through its public API', async () => {
  const rule = projectFiles()
    .inPath('src/app/**/*.ts', {
      except: { inPath: 'src/app/orders/**' },
    })
    .shouldNot()
    .dependOnFiles()
    .inFolder('src/app/orders/**', {
      except: ['index.ts', 'public-api.ts'],
    });

  await expect(rule).toPassAsync();
});
```

This says:

* check all Angular app files
* exclude files inside `orders` itself, because a module may use its own internals
* forbid other features from depending on files inside `orders`
* but allow imports through `orders/index.ts` and `orders/public-api.ts`

So this fails:

```typescript
import { OrderService } from '../orders/internal/order.service';
```

But this passes:

```typescript
import { OrderSummary } from '../orders';
```

You can also make the exceptions explicit by target:

```typescript
.inFolder('src/app/orders/**', {
  except: {
    withName: ['index.ts', 'public-api.ts'],
  },
});
```

This is especially useful in Angular projects because Angular feature modules often create natural architectural boundaries, but violations tend to accumulate silently over time.

And these imports are very hard to catch in code review because they look like normal TypeScript imports.

Now the boundary can be tested directly.

------

Very curious for any type of feedback! PRs are also highly welcome