```json
{
  "id": "1swzclo",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "djangolearning",
  "created_utc": 1777284562.0,
  "created_at": "2026-04-27T12:09:22+02:00",
  "permalink": "https://www.reddit.com/r/djangolearning/comments/1swzclo/ive_added_special_django_support_to/",
  "link_url": "https://github.com/LukasNiessen/ArchUnitPython",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "reddit",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "fd18b59d6bbe148803b1b330f529a2d5069a58d7d8efbb9f96a4c61c66b14050",
  "body_sha256": "a83f55c2a39ba8344acdd8bf21c32c12a7cdc482115767aae17e8476054f37c1",
  "body_characters": 3287
}
```

# Original title

I've added special Django support to ArchUnitPython. Visualize & enforce dependencies/architecture

## Original body

A week ago I posted about ArchUnitPython, my library for enforcing architecture rules in Python projects as unit tests.

A few of you specifically asked whether this could be used to enforce **clean Django boundaries** in real projects:
keeping `django.*` / `rest_framework.*` imports out of the wrong layers, and not getting noisy false positives from type-only imports between models, services, and serializers.

**So to your request I’ve added both.**

------

First a mini recap of what ArchUnitPython does:

* Most tools catch style issues, formatting issues, or generic smells.
* ArchUnitPython focuses on structural rules: wrong dependency directions, circular dependencies, naming convention drift, architecture/diagram mismatch, and so on.
* You define those rules as tests, run them in pytest/unittest, and they automatically become part of CI/CD

In other words: **ArchUnitPython allows you to enforce your architectural decisions by writing them as simple unit tests.**

That matters more than ever in Claude Code / Codex times, because LLMs are great at generating code but they love to violate architectural boundaries, especially when they get stuck.

Repo: https://github.com/LukasNiessen/ArchUnitPython

------

Now what’s new

**1. External Dependency Rules for Django-style boundaries**

Before, ArchUnitPython could already enforce internal dependency rules like:

*“views must not depend on repositories”* or *“services must not import api”*

Now it can also enforce rules about imports to modules outside your project, which is especially useful for Django projects where framework imports tend to slowly leak everywhere.

For example, you can now enforce things like:

* service/domain code must not import `django.*`
* core logic must not import `rest_framework.*`
* only boundary layers may touch Django HTTP / serializer / ORM APIs directly

Example:

```python
rule = (
    project_files("src/")
    .in_folder("**/services/**")
    .should_not()
    .depend_on_external_modules()
    .matching("django*")
    .matching("rest_framework*")
)
assert_passes(rule)
```

This is especially useful in Django projects where business logic often starts clean, but over time `HttpRequest`, serializers, ORM models, or framework exceptions begin leaking into places they really shouldn’t.

**2. TYPE_CHECKING-aware dependency analysis for Django projects**

A few of you also mentioned a very common Django pain point: type-only imports between models, services, serializers, and query helpers.

For example:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myapp.orders.models import Order
```

Those imports are used for static typing, but they are not real runtime coupling in the same way normal imports are.

Previously, architecture analysis would still count them as ordinary dependencies.  
Now you can choose to ignore them when checking architecture rules.

Example:

```python
assert_passes(
    rule,
    CheckOptions(ignore_type_checking_imports=True),
)
```

This matters because modern Django codebases use type hints much more heavily now, and otherwise architecture checks can become noisy or overly strict for relationships that only exist for typing.

------

Very curious for any type of feedback! PRs are also highly welcome.
