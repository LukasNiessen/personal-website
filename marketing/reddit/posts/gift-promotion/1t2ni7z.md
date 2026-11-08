```json
{
  "id": "1t2ni7z",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "typescript",
  "created_utc": 1777819807.0,
  "created_at": "2026-05-03T16:50:07+02:00",
  "permalink": "https://www.reddit.com/r/typescript/comments/1t2ni7z/i_added_support_for_barrelfile_boundaries_to/",
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
  "title_sha256": "51523275a94b952fe49143ffa0c97b48e84f12923189662aea224d9a793ccc21",
  "body_sha256": "46e118f2a457d60a0d4c34c45de03fc67b1c8cb4121ce7a9b77502214f04485a",
  "body_characters": 3694
}
```

# Original title

I added support for barrel-file boundaries to ArchUnitTS (architecture testing library for TypeScript)

## Original body

A week ago I posted about ArchUnitTS, my library for enforcing architecture rules in TypeScript projects as unit tests.

A few of you specifically asked whether this could be used to enforce **barrel-file boundaries** in real TypeScript projects:
allowing imports through `index.ts` or `public-api.ts`, while preventing other parts of the codebase from reaching into internal files.

**So to that request I’ve added support for exclusion-aware dependency rules.**

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

**Exclusion-aware dependency rules for TypeScript barrel files**

A common TypeScript project structure looks like this:

```text
src/
  orders/
    index.ts
    public-api.ts
    internal/
      order.service.ts
    components/
      order-card.ts
```

The intended contract is often:

```typescript
import { something } from '../orders';
```

or:

```typescript
import { something } from '../orders/public-api';
```

But over time, imports like this creep in:

```typescript
import { OrderService } from '../orders/internal/order.service';
```

That compiles perfectly.  
It may even look harmless in a PR.

But architecturally, another part of the codebase is now coupled to the internal structure of `orders`.

Before, ArchUnitTS could already express this with regular expressions, but the developer experience was not as nice as it should be.

Now you can write the rule directly with `except`:

```typescript
import { projectFiles } from 'archunit';

it('should only import orders through public barrel files', async () => {
  const rule = projectFiles()
    .inPath('src/**/*.ts', {
      except: { inPath: 'src/orders/**' },
    })
    .shouldNot()
    .dependOnFiles()
    .inFolder('src/orders/**', {
      except: ['index.ts', 'public-api.ts'],
    });

  await expect(rule).toPassAsync();
});
```

This says:

* files outside `orders` may not depend on files inside `orders`
* files inside `orders` are allowed to use their own internals
* `index.ts` and `public-api.ts` are allowed entry points

So this fails:

```typescript
import { OrderService } from '../orders/internal/order.service';
```

But this passes:

```typescript
import { OrderService } from '../orders';
```

Arrays are supported too:

```typescript
.inPath('src/**/*.ts', {
  except: {
    inPath: [
      'src/generated/**',
      'src/testing/**',
      'src/orders/**',
    ],
  },
});
```

And exclusions can be targeted:

```typescript
.inFolder('src/orders/**', {
  except: {
    withName: ['index.ts', 'public-api.ts'],
  },
});
```

This is useful for:

* public barrel files
* generated code
* test helpers
* migration folders
* legacy exceptions
* `*.spec.ts` files
* explicitly allowed public entry points

The nice part is that this is still just a normal test.

You can put it next to the rest of your test suite, run it locally, and enforce it in CI/CD.

------

Very curious for any type of feedback! PRs are also highly welcome.
