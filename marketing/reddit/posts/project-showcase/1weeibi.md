```json
{
  "id": "1weeibi",
  "author": "trolleid",
  "category": "project-showcase",
  "subreddit": "FastAPI",
  "created_utc": 1789224387.0,
  "created_at": "2026-09-12T16:46:27+02:00",
  "permalink": "https://www.reddit.com/r/FastAPI/comments/1weeibi/python_architecture_tests_archunit_but_for_python/",
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
  "title_sha256": "f5045325beebe1a31c7a1abc5fb4e1d90f95497e8c4ac55e1662b4392382b8dc",
  "body_sha256": "c73190307d6942139fa3f12958f15d112cd8e7e1a343ce939122c9080e852429",
  "body_characters": 2197
}
```

# Original title

Python architecture tests: ArchUnit but for Python

## Original body

I shipped ArchUnitPython, a library that lets you enforce architectural rules in Python projects through automated tests.

The problem it solves: as codebases grow, architecture erodes. Someone imports the database layer from the presentation layer, circular dependencies creep in, naming conventions drift. Code review catches some of it, but not all, and definitely not consistently.

This problem has always existed but is more important than ever in Claude Code, Codex times. LLMs break architectural rules all the time.

So I built a library where you define your architecture rules as tests. Here two quick examples:

    # No circular dependencies in services
    rule = project_files("src/").in_folder("**/services/**").should().have_no_cycles()
    assert_passes(rule)

    # Presentation layer must not depend on database layer
    rule = project_files("src/")
              .in_folder("**/presentation/**")
              .should_not()
              .depend_on_files()
              .in_folder("**/database/**")
    assert_passes(rule)

This will run in pytest, unittest, or whatever you use, and therefore be automatically in your CI/CD. If a commit violates the architecture rules your team has decided, the CI will fail.

Hint: this is exactly what the famous ArchUnit Java library does, just for Python - I took inspiration for the name is of course.

Let me quickly address why this over linters or generic code analysis?

Linters catch style issues. This catches structural violations — wrong dependency directions, layering breaches, naming convention drift. It's the difference between "this line looks wrong" and "this module shouldn't talk to that module."

Some key features:

* Dependency direction enforcement & circular dependency detection
* Naming convention checks (glob + regex)
* Code metrics: LCOM cohesion, abstractness, instability, distance from main sequence
* PlantUML diagram validation — ensure code matches your architecture diagrams
* Custom rules & metrics
* Zero runtime dependencies, uses only Python's ast module
* Python 3.10+

Very curious what you think! [https://github.com/LukasNiessen/ArchUnitPython](https://github.com/LukasNiessen/ArchUnitPython)