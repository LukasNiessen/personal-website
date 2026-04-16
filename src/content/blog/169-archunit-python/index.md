---
title: "Architecture Testing in Python with ArchUnitPython"
summary: "ArchUnitPython brings architecture testing to the Python ecosystem. Enforce layer boundaries, detect circular dependencies, and keep your codebase honest, all from pytest."
date: "Apr 16 2026"
tags:
  - Architecture
  - Python
  - ArchUnit
  - Open Source
  - Testing
---

# Architecture Testing in Python with ArchUnitPython

A while back I wrote an [article about Python project architecture](/blog/python-typical-architecture). It covered the two dominant patterns, horizontal and vertical slicing, when to use which, and how to structure a FastAPI project. The response was great. But one question kept coming up: "How do I actually enforce this?"

Because that's the thing with Python. It doesn't care how you organize your code. There's no framework yelling at you when your route handler imports directly from the database layer. No compiler rejecting a circular dependency between your `users` and `orders` modules. Python gives you modules, packages, and an import system. The rest is up to you.

And that's fine. Until your project grows, your team grows, and suddenly someone's importing `sqlalchemy` from inside a Pydantic schema file because it was the quickest way to get the job done.

So I built [**ArchUnitPython**](https://github.com/LukasNiessen/ArchUnitPython).

## What Is It?

ArchUnitPython is an architecture testing library for Python. You write tests that enforce structural rules, things like "the presentation layer should not import from the database layer" or "no file should exceed 500 lines of code." These tests run alongside your regular pytest suite. When someone violates a rule, the test fails. Simple as that.

If you've used [ArchUnit](https://www.archunit.org/) in Java or [ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS) in TypeScript, this is the same idea for Python. It uses Python's `ast` module to analyze imports statically. No runtime dependencies, no magic.

```bash
pip install archunitpython
```

Requires Python 3.10+.

## Enforcing Layer Boundaries

This is the most common use case and probably where you should start. Let's say you have a typical layered Python project:

```
src/
└── myapp/
    ├── routes/          # HTTP layer
    ├── services/        # Business logic
    ├── repositories/    # Data access
    └── models/          # Database models
```

The rule is simple: routes call services, services call repositories, repositories talk to the database. Nothing skips a layer. But without enforcement, someone will eventually add a direct SQLAlchemy query inside a route handler. It works. It ships. And now your architecture diagram is a lie.

Here's how you prevent that:

```python
from archunitpython import project_files, assert_passes

def test_routes_should_not_depend_on_repositories():
    rule = (
        project_files("src/")
        .in_folder("**/routes/**")
        .should_not()
        .depend_on_files()
        .in_folder("**/repositories/**")
    )
    assert_passes(rule)

def test_routes_should_not_depend_on_models():
    rule = (
        project_files("src/")
        .in_folder("**/routes/**")
        .should_not()
        .depend_on_files()
        .in_folder("**/models/**")
    )
    assert_passes(rule)

def test_services_should_not_depend_on_routes():
    rule = (
        project_files("src/")
        .in_folder("**/services/**")
        .should_not()
        .depend_on_files()
        .in_folder("**/routes/**")
    )
    assert_passes(rule)
```

That's it. These are pytest functions. They run with `pytest tests/test_architecture.py -v` and they fail with clear error messages when someone breaks the rules:

```
Found 2 architecture violation(s):

  1. File dependency violation
     'src/routes/orders.py' depends on 'src/repositories/order_repo.py'

  2. File dependency violation
     'src/routes/orders.py' depends on 'src/models/order.py'
```

No ambiguity. The file path, the violating dependency, done.

## Keeping Your Domain Clean

If you're doing anything resembling clean architecture or hexagonal architecture in Python, you probably have a rule like "domain logic should not depend on frameworks." Your business rules shouldn't know about FastAPI, Flask, SQLAlchemy, or any other infrastructure concern.

```python
def test_domain_should_not_depend_on_fastapi():
    rule = (
        project_files("src/")
        .in_folder("**/domain/**")
        .should_not()
        .depend_on_files()
        .in_path("**/fastapi/**")
    )
    assert_passes(rule)

def test_domain_should_not_depend_on_sqlalchemy():
    rule = (
        project_files("src/")
        .in_folder("**/domain/**")
        .should_not()
        .depend_on_files()
        .in_path("**/sqlalchemy/**")
    )
    assert_passes(rule)
```

This one is especially important in the Python AI/ML world. You've got a core pipeline with business logic, and then you've got infrastructure: vector stores, embedding APIs, database connections. Keeping them separate means you can swap out your vector database or your embedding provider without rewriting your domain logic. Architecture tests make sure that separation actually holds.

## Circular Dependencies

Circular dependencies in Python are tricky. They don't always blow up immediately. Python's import system can handle some circular imports at runtime, depending on the order and timing. But they make your codebase brittle. Refactoring becomes dangerous because touching one module can break another through a dependency chain you didn't know existed.

```python
def test_no_circular_dependencies():
    rule = (
        project_files("src/")
        .in_folder("src/**")
        .should()
        .have_no_cycles()
    )
    assert_passes(rule)
```

You can also scope this down to specific areas where cycles tend to sneak in:

```python
def test_services_have_no_cycles():
    rule = (
        project_files("src/")
        .in_folder("**/services/**")
        .should()
        .have_no_cycles()
    )
    assert_passes(rule)
```

## Naming Conventions

Python's flexibility extends to naming. There's no framework forcing your service files to end in `_service.py` or your test files to start with `test_`. But consistency matters, especially on larger teams. When you see `user_service.py`, you know what it is without opening it. When you see `helpers2.py`, you don't.

```python
def test_service_files_should_follow_naming():
    rule = (
        project_files("src/")
        .in_folder("**/services/**")
        .should()
        .have_name("*_service.py")
    )
    assert_passes(rule)

def test_repository_files_should_follow_naming():
    rule = (
        project_files("src/")
        .in_folder("**/repositories/**")
        .should()
        .have_name("*_repo.py")
    )
    assert_passes(rule)
```

## Code Metrics

Beyond structural rules, ArchUnitPython can enforce code quality metrics. This is where things get interesting.

**File size limits.** A file that's grown to 2000 lines is telling you something. It's doing too much and needs to be split.

```python
from archunitpython import metrics, assert_passes

def test_no_large_files():
    rule = metrics("src/").count().lines_of_code().should_be_below(500)
    assert_passes(rule)
```

**Class cohesion.** LCOM (Lack of Cohesion of Methods) measures how well the methods and fields of a class are connected. A value close to 0 means high cohesion (methods use the class's fields). A value close to 1 means your class is really multiple classes pretending to be one.

```python
def test_classes_should_be_cohesive():
    rule = metrics("src/").lcom().lcom96b().should_be_below(0.3)
    assert_passes(rule)
```

**Method count.** A class with 30 methods is almost certainly violating the Single Responsibility Principle.

```python
def test_classes_not_too_many_methods():
    rule = metrics("src/").count().method_count().should_be_below(20)
    assert_passes(rule)
```

**Distance from the main sequence.** This is a metric from Robert C. Martin that combines abstractness and instability. Classes that are far from the "main sequence" are either in the "zone of pain" (too concrete and too stable, hard to change) or the "zone of uselessness" (too abstract and too unstable, basically unused abstractions).

```python
def test_proper_distance():
    rule = (
        metrics("src/")
        .distance()
        .distance_from_main_sequence()
        .should_be_below(0.3)
    )
    assert_passes(rule)

def test_not_in_zone_of_pain():
    rule = metrics("src/").distance().not_in_zone_of_pain()
    assert_passes(rule)
```

You can also define custom metrics if the built-in ones don't cover your needs:

```python
def test_method_field_ratio():
    rule = (
        metrics("src/")
        .custom_metric(
            "methodFieldRatio",
            "Ratio of methods to fields",
            lambda ci: len(ci.methods) / max(len(ci.fields), 1),
        )
        .should_be_below(10)
    )
    assert_passes(rule)
```

## Custom Rules

Sometimes the built-in rules don't cover what you need. Maybe you want to enforce that every Python file has a module docstring, or that no file imports `os.system` directly (for security). You can write arbitrary validation logic:

```python
def test_all_files_have_docstrings():
    rule_desc = "Python files should have module docstrings"

    def has_docstring(file):
        return '"""' in file.content or "'''" in file.content

    violations = (
        project_files("src/")
        .with_name("*.py")
        .should()
        .adhere_to(has_docstring, rule_desc)
        .check()
    )
    assert len(violations) == 0
```

The `adhere_to` method gives you access to the full file object, so you can check anything: content, structure, naming, whatever your project needs.

## Validating Against PlantUML Diagrams

If you have architecture diagrams in PlantUML, you can validate your actual code against them. This is probably the most powerful feature for teams that maintain architecture documentation.

```python
import re
from archunitpython import project_slices, assert_passes

def test_code_matches_architecture_diagram():
    diagram = """
@startuml
  component [routes]
  component [services]
  component [repositories]

  [routes] --> [services]
  [services] --> [repositories]
@enduml"""

    rule = (
        project_slices("src/")
        .defined_by("src/(**)/**")
        .should()
        .adhere_to_diagram(diagram)
    )
    assert_passes(rule)
```

Your diagram says `routes` depends on `services` and `services` depends on `repositories`. If the actual code has a dependency from `routes` to `repositories`, the test fails. Your documentation stays honest.

You can also load the diagram from a file:

```python
def test_matches_diagram_file():
    rule = (
        project_slices("src/")
        .defined_by("src/(**)/**")
        .should()
        .adhere_to_diagram_in_file("docs/architecture.puml")
    )
    assert_passes(rule)
```

## CI Integration

Since these are just pytest tests, CI integration is straightforward:

```yaml
# GitHub Actions
- name: Run Architecture Tests
  run: pytest tests/test_architecture.py -v

- name: Upload Test Logs
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: architecture-test-logs
    path: logs/
```

The tests run on every PR. If someone introduces a layer violation, the pipeline goes red. The violation never makes it to main.

You can also generate HTML reports for your metrics and treat them as CI artifacts:

```python
from archunitpython.metrics.fluentapi.export_utils import MetricsExporter, ExportOptions

MetricsExporter.export_as_html(
    {"MethodCount": 5, "FieldCount": 3, "LinesOfCode": 150},
    ExportOptions(
        output_path="reports/metrics.html",
        title="Architecture Metrics",
    ),
)
```

## Why This Matters for Python Specifically

I've built architecture testing for TypeScript already with [ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS), and the Java world has had [ArchUnit](https://www.archunit.org/) for years. But Python needed this arguably more than either of them.

Python is _the_ language for AI and ML. Every data pipeline, every RAG system, every ML training loop is Python. And these projects are growing fast, often without much architectural discipline because they started as a notebook or a quick script. The transition from "it works" to "it's maintainable" is where architecture testing helps.

On top of that, with LLMs generating code in Python projects at an increasing rate, there's no guarantee that the generated code respects your architectural boundaries. Copilot doesn't know that your `services/` folder shouldn't import from `routes/`. It just writes code that works. Architecture tests are the safety net that catches these violations regardless of whether a human or an AI wrote the code.

## Getting Started

Start small. Don't try to write 20 architecture rules on day one. Pick the one thing that keeps going wrong in your project. Maybe it's circular dependencies, maybe it's layer violations. Write a test for it. Add it to your CI. Get it passing. Then add the next rule.

```bash
pip install archunitpython
```

Write a `tests/test_architecture.py`. Start with one rule. Run it. Expand from there.

**ArchUnitPython**: [https://github.com/LukasNiessen/ArchUnitPython](https://github.com/LukasNiessen/ArchUnitPython)
