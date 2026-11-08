```json
{
  "id": "1uibqgc",
  "author": "trolleid",
  "category": "project-showcase",
  "subreddit": "django",
  "created_utc": 1782688227.0,
  "created_at": "2026-06-29T01:10:27+02:00",
  "permalink": "https://www.reddit.com/r/django/comments/1uibqgc/archunit_but_for_python_enforce_your_architecture/",
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
  "title_sha256": "3f7ec3b0bae883bf265001da10e8a75057d688ad1e363e68918662487ea7c80c",
  "body_sha256": "2722058806a2e4e4ccf6ec2b1998419e66af7beac7dd8d3881b016808892129e",
  "body_characters": 2190
}
```

# Original title

ArchUnit but for Python: enforce your architecture via unit tests

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