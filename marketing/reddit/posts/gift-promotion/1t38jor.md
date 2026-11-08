```json
{
  "id": "1t38jor",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "reactjs",
  "created_utc": 1777872466.0,
  "created_at": "2026-05-04T07:27:46+02:00",
  "permalink": "https://www.reddit.com/r/reactjs/comments/1t38jor/i_added_special_react_support_to_archunitts/",
  "link_url": "https://github.com/LukasNiessen/ArchUnitTS?v=5",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "reddit",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "67ddebfbc706e2bac16b8b15b17daf3a183ce0314a6b4bb18e34563ad7cd5c5d",
  "body_sha256": "3e8c6d8fc8bb50b393aca9c994ffff926aac58cbc269bdafeb2fb1b429f30ebc",
  "body_characters": 3691
}
```

# Original title

I added special React support to ArchUnitTS (architecture testing library for TypeScript)

## Original body

A week ago I posted about ArchUnitTS, my library for enforcing architecture rules in TypeScript projects as unit tests.

A few of you specifically asked whether this could be useful for **React feature-folder architectures**:
keeping feature internals private, while allowing other features to import only from public entry points like `index.ts`.

**So to that request I’ve added exclusion-aware dependency rules.**

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

**Exclusion-aware dependency rules for React feature boundaries**

A lot of React codebases use feature folders:

```text
src/
  features/
    orders/
      index.ts
      components/
        OrderCard.tsx
      hooks/
        useOrders.ts
      api/
        orderClient.ts
    customers/
      CustomerPage.tsx
```

Usually the intended dependency is:

```typescript
import { OrderCard, useOrders } from '../orders';
```

But over time, imports like this start appearing:

```typescript
import { useOrders } from '../orders/hooks/useOrders';
import { orderClient } from '../orders/api/orderClient';
```

That works technically, but it bypasses the feature’s public API.

Now `customers` knows that `orders` has a `hooks` folder, an `api` folder, and a specific internal file layout.

If `orders` reorganizes itself later, unrelated features break.

So ArchUnitTS now lets you express this kind of boundary with `except`:

```typescript
import { projectFiles } from 'archunit';

it('should consume orders only through its public API', async () => {
  const rule = projectFiles()
    .inPath('src/features/**/*.ts?(x)', {
      except: { inPath: 'src/features/orders/**' },
    })
    .shouldNot()
    .dependOnFiles()
    .inFolder('src/features/orders/**', {
      except: ['index.ts'],
    });

  await expect(rule).toPassAsync();
});
```

This says:

* check files inside `src/features`
* ignore the `orders` feature itself
* forbid other features from importing into `orders` internals
* allow `orders/index.ts` as the public API

So this fails:

```typescript
import { useOrders } from '../orders/hooks/useOrders';
import { orderClient } from '../orders/api/orderClient';
```

But this passes:

```typescript
import { useOrders, OrderCard } from '../orders';
```

You can also allow multiple public entry points:

```typescript
.inFolder('src/features/orders/**', {
  except: {
    withName: ['index.ts', 'public-api.ts'],
  },
});
```

Or exclude multiple features/folders from the source side:

```typescript
.inPath('src/features/**/*.ts?(x)', {
  except: {
    inPath: [
      'src/features/orders/**',
      'src/features/generated/**',
      'src/features/testing/**',
    ],
  },
});
```

This is the kind of architectural rule that is hard to enforce in code review because the bad import still looks like normal TypeScript.

But once it is a unit test, it becomes part of CI/CD.

------

Very curious for any type of feedback! PRs are also highly welcome.
