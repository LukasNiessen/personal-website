```json
{
  "id": "1sn4tm8",
  "author": "trolleid",
  "category": "project-showcase",
  "subreddit": "IndiaTech",
  "created_utc": 1776348957.0,
  "created_at": "2026-04-16T16:15:57+02:00",
  "permalink": "https://www.reddit.com/r/IndiaTech/comments/1sn4tm8/i_built_archunit_for_python_enforce_architecture/",
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
  "title_sha256": "7a0fcf659e5b6dd9c429ff9378ad77e358af9fa3ff129c914f8c580dc3b729a3",
  "body_sha256": "2722058806a2e4e4ccf6ec2b1998419e66af7beac7dd8d3881b016808892129e",
  "body_characters": 2190
}
```

# Original title

I built ArchUnit for Python: enforce architecture rules as unit tests.

## Original body

I just shipped ArchUnitPython, a library that lets you enforce architectural rules in Python projects through automated tests.

The problem it solves: as codebases grow, architecture erodes. Someone imports the database layer from the presentation layer, circular dependencies creep in, naming conventions drift. Code review catches some of it, but not all, and definitely not consistently.

This problem has always existed but is more important than ever in Claude Code, Codex times. LLMs break architectural rules all the time.

So I built a library where you define your architecture rules as tests. Two quick examples:

```python
# No circular dependencies in services
rule = project_files("src/").in_folder("**/services/**").should().have_no_cycles()
assert_passes(rule)
```



```python
# Presentation layer must not depend on database layer
rule = project_files("src/")
          .in_folder("**/presentation/**")
          .should_not()
          .depend_on_files()
          .in_folder("**/database/**")
assert_passes(rule)
```


This will run in pytest, unittest, or whatever you use, and therefore be automatically in your CI/CD. If a commit violates the architecture rules your team has decided, the CI will fail.

Hint: this is exactly what the famous ArchUnit Java library does, just for Python - I took inspiration for the name is of course.


Let me quickly address why this over linters or generic code analysis?


Linters catch style issues. This catches structural violations — wrong dependency directions, layering breaches, naming convention drift. It's the difference between "this line looks wrong" and "this module shouldn't talk to that module."

Some key features:

- Dependency direction enforcement & circular dependency detection
- Naming convention checks (glob + regex)
- Code metrics: LCOM cohesion, abstractness, instability, distance from main sequence
- PlantUML diagram validation — ensure code matches your architecture diagrams
- Custom rules & metrics
- Zero runtime dependencies, uses only Python's ast module
- Python 3.10+

Very curious what you think!
[https://github.com/LukasNiessen/ArchUnitPython](https://github.com/LukasNiessen/ArchUnitPython)