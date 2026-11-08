```json
{
  "id": "1swex79",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "FastAPI",
  "created_utc": 1777227004.0,
  "created_at": "2026-04-26T20:10:04+02:00",
  "permalink": "https://www.reddit.com/r/FastAPI/comments/1swex79/ive_added_special_fastapi_support_to/",
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
  "title_sha256": "37c0e0d52e42a3d4d1f25fb51b5b7b2ea6d5d4590a62847ab48a832efa44c3f8",
  "body_sha256": "37227856b1e0a8493e6eb19ac32d0b4518f69b8ae98e279c4a159b845b646836",
  "body_characters": 3383
}
```

# Original title

I've added special FastAPI support to ArchUnitPython. Visualize & enforce dependencies/architecture.

## Original body

A week ago I posted about ArchUnitPython, my library for enforcing architecture rules in Python projects as unit tests.

A few of you specifically asked whether this could be used to enforce **clean FastAPI boundaries** in real projects:
keeping `fastapi`, `starlette`, `pydantic`, or `sqlalchemy` from leaking into the wrong layers, and not getting noisy false positives from type-only imports between routers, schemas, services, and persistence code.

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

**1. External Dependency Rules for FastAPI-style boundaries**

Before, ArchUnitPython could already enforce internal dependency rules like:

*“routers must not depend on repositories”* or *“services must not import api”*

Now it can also enforce rules about imports to modules outside your project, which is especially useful for FastAPI projects where framework and persistence imports tend to spread fast.

For example, you can now enforce things like:

* domain/core code must not import `fastapi.*`
* core logic must not import `starlette.*`
* service code must not directly depend on `sqlalchemy.*`
* only boundary layers may use `pydantic.*` request/response models

Example:

```python
rule = (
    project_files("src/")
    .in_folder("**/domain/**")
    .should_not()
    .depend_on_external_modules()
    .matching("fastapi*")
    .matching("starlette*")
    .matching("sqlalchemy*")
)
assert_passes(rule)
```

This is especially useful in FastAPI projects where things start clean, but over time route handlers, request models, DB sessions, and framework exceptions begin leaking into the core application logic.

**2. TYPE_CHECKING-aware dependency analysis for FastAPI projects**

A few of you also mentioned a very common FastAPI pain point: type-only imports between routers, schemas, services, and models.

For example:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.user import UserResponse
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

This matters because modern FastAPI codebases often lean heavily on typing, and otherwise architecture checks can become noisy or overly strict for relationships that only exist for annotations.

------

Very curious for any type of feedback! PRs are also highly welcome.
