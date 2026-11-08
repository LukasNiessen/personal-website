```json
{
  "id": "1swejc2",
  "author": "trolleid",
  "category": "project-showcase",
  "subreddit": "Python",
  "created_utc": 1777226178.0,
  "created_at": "2026-04-26T19:56:18+02:00",
  "permalink": "https://www.reddit.com/r/Python/comments/1swejc2/archunit_for_python_visualize_enforce/",
  "link_url": "https://www.reddit.com/r/Python/comments/1swejc2/archunit_for_python_visualize_enforce/",
  "is_self": true,
  "crosspost_parent": null,
  "removed_by_category": "moderator",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "720bcd8a3a354626b4dc3e6c8d620b1f3e453e4740aed1048f78622f50c41d80",
  "body_sha256": "97487f0e1ef48c854702976617652057203b850161ab3476a912a2b1f2f603f9",
  "body_characters": 2922
}
```

# Original title

ArchUnit for Python: visualize + enforce dependencies, using modular architecture

## Original body

A week ago I posted about ArchUnitPython, my library for enforcing architecture rules in Python projects as unit tests.

A few of you pointed out two very practical gaps for real Python codebases:  
external dependencies, and type-only imports. **So to your request I’ve added both.**

\------

First a mini recap of what ArchUnitPython does.

## What My Project Does

* Most tools catch style issues, formatting issues, or generic smells.
* ArchUnitPython focuses on structural rules: wrong dependency directions, circular dependencies, naming convention drift, architecture/diagram mismatch, and so on.
* You define those rules as tests, run them in pytest/unittest, and they automatically become part of CI/CD

In other words: **ArchUnitPython allows you to enforce your architectural decisions by writing them as simple unit tests.**

That matters more than ever in Claude Code / Codex times, because LLMs are great at generating code but they love to violate architectural boundaries, especially when they get stuck.

Repo: [https://github.com/LukasNiessen/ArchUnitPython](https://github.com/LukasNiessen/ArchUnitPython)

\------

Now what’s new

**1. External Dependency Rules**

Before, ArchUnitPython could already enforce internal dependency rules like:

*“presentation must not depend on database”* or *“services must not import api”*

Now it can also enforce rules about imports to modules outside your project, for example:

* domain code must not import requests
* core logic must not import sqlalchemy
* only certain layers may use pandas, boto3, etc.

So you can now guard not just folder-to-folder boundaries, but also framework / SDK usage boundaries.

Example:

    rule = (
        project_files("src/")
        .in_folder("**/domain/**")
        .should_not()
        .depend_on_external_modules()
        .matching("requests")
    )
    assert_passes(rule)

This is especially useful in layered or hexagonal architectures where the real problem is often not “wrong local file import”, but “core code now directly depends on infrastructure/framework code”.

**2. TYPE\_CHECKING-aware dependency analysis**

Python has a common pattern for type-only imports:

    from typing import TYPE_CHECKING
    
    if TYPE_CHECKING:
        from my_app.models import User

Those imports are used for static typing, but they are not real runtime coupling in the same way normal imports are.

Previously, architecture analysis would still count them as ordinary dependencies.  
Now you can choose to ignore them when checking architecture rules.

Example:

    assert_passes(
        rule,
        CheckOptions(ignore_type_checking_imports=True),
    )

This matters because modern Python codebases use type hints heavily, and otherwise architecture checks can become noisy or overly strict for relationships that only exist for typing.

\------

Very curious for any type of feedback! PRs are also highly welcome.