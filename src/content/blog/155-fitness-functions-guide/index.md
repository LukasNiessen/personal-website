---
title: "Fitness Functions: Automating Your Architecture Decisions"
summary: "How fitness functions shift governance left - from code architecture testing with ArchUnit to data product governance in a data mesh"
date: "Feb 3 2026"
tags:
  - Architecture
  - Fitness Functions
  - Evolutionary Architecture
  - Data Mesh
  - ArchUnit
---

# Fitness Functions: Automating Your Architecture Decisions

You've made architectural decisions. You've documented them. Everyone agreed in the meeting. Six months later, someone's importing the database layer directly into the presentation layer, and your beautiful architecture is slowly turning into spaghetti.

This is architectural drift, and it happens everywhere. The solution? Stop relying on code reviews and good intentions. Automate it.

## What Is a Fitness Function?

The term comes from the book *Building Evolutionary Architectures* by Neal Ford, Rebecca Parsons, and Patrick Kua. A fitness function is simply a test that evaluates how close your implementation is to its stated design objectives.

Think of it like this: unit tests verify that your code **behaves** correctly. Fitness functions verify that your code **structure** follows your architectural rules.

The key insight is shifting from "governance by inspection" to "governance by rule." Instead of hoping someone catches the violation in a code review, you write an automated test that fails on every PR that breaks the rule.

This is "shifting left" on governance. You identify problems earlier in the software value stream - at development time rather than during audits or after things have already gone wrong.

## The Three Pillars

Fitness functions embody three principles:

1. **Governance by rule over governance by inspection.** Write the rule as code. Don't rely on humans to remember and enforce it.

2. **Empowering teams to discover problems over independent audits.** Teams get immediate feedback when they break rules, rather than learning about it weeks later from an external review.

3. **Continuous governance over dedicated audit phases.** Every commit is checked. Not quarterly. Not annually. Every single commit.

## Code Architecture Testing

The most common use of fitness functions is enforcing code architecture rules. This is where tools like ArchUnit and ArchUnitTS come in.

### For Java: ArchUnit

[ArchUnit](https://www.archunit.org/) is the go-to library for architecture testing in Java. It lets you write tests that check the structure of your code - package dependencies, class relationships, naming conventions, and more.

```java
@Test
public void services_should_not_access_controllers() {
    noClasses()
        .that().resideInAPackage("..service..")
        .should().accessClassesThat().resideInAPackage("..controller..")
        .check(importedClasses);
}

@Test
public void no_cycles_between_packages() {
    slices().matching("com.myapp.(*)..")
        .should().beFreeOfCycles()
        .check(importedClasses);
}

@Test
public void repositories_should_only_be_accessed_by_services() {
    classes()
        .that().resideInAPackage("..repository..")
        .should().onlyBeAccessed().byAnyPackage("..service..", "..repository..")
        .check(importedClasses);
}
```

### For TypeScript: ArchUnitTS

[ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS) brings the same concept to TypeScript projects. Same idea, different ecosystem.

```typescript
it('presentation layer should not depend on database layer', async () => {
    const rule = projectFiles()
        .inFolder('src/presentation/**')
        .shouldNot()
        .dependOnFiles()
        .inFolder('src/database/**');

    await expect(rule).toPassAsync();
});

it('should have no circular dependencies', async () => {
    const rule = projectFiles()
        .inFolder('src/**')
        .should()
        .haveNoCycles();

    await expect(rule).toPassAsync();
});

it('domain layer should be framework-agnostic', async () => {
    const rule = projectFiles()
        .inFolder('src/domain/**')
        .shouldNot()
        .dependOnFiles()
        .matchingPattern('**/node_modules/@nestjs/**');

    await expect(rule).toPassAsync();
});
```

### What Can You Test?

Common architectural rules you might enforce:

**Layer dependencies:** Presentation shouldn't access the database directly. Services shouldn't call controllers. Domain logic shouldn't depend on frameworks.

**Circular dependencies:** These are architectural cancer. They make refactoring nearly impossible and create unexpected coupling. Catch them automatically.

**Naming conventions:** Services should end in `Service`. Controllers should end in `Controller`. Repositories should end in `Repository`. Makes the codebase predictable and searchable.

**Package boundaries:** In a modular monolith or microservices, modules shouldn't reach into each other's internals. If module A needs something from module B, it should go through B's public API.

**Metrics:** Files shouldn't exceed N lines. Classes shouldn't have more than M dependencies. Methods shouldn't have cyclomatic complexity above X.

**Framework isolation:** Your domain logic shouldn't import from Express, NestJS, Spring, or whatever framework you're using. This keeps your core business logic portable.

The key is putting these in your CI pipeline. They run on every PR and block merges when they fail. The architectural violation never makes it to main.

## Beyond Code: Data Product Governance

Fitness functions aren't limited to code architecture. The same concept applies anywhere you have rules you want to enforce automatically.

A good example is **data mesh governance**. In a data mesh, autonomous teams own their data products. But for those data products to be interoperable and useful across the organization, they need to meet certain standards. How do you enforce that without creating a bottleneck of central data stewards reviewing every data product?

Fitness functions.

Most organizations have a data catalog (Collibra, DataHub, etc.) that stores metadata about data products. You can run assertions against this metadata:

**Discoverability:** Does searching for the data product name actually surface it in the top results?

**Self-descriptiveness:** Does it have a meaningful description? Are fields documented?

**Trustworthiness:** Are SLOs defined and being met?

**Security:** Is access properly restricted?

**Interoperability:** Does it follow standard formats? Are business keys present?

**Addressability:** Is the data product accessible via a unique URI?

```python
def test_existence_of_service_level_objectives():
    response = get_data_product_metadata("marketing_customer360")
    slos = response.get("aspects", {}).get("dataProductSLOs", {}).get("slos")

    assert slos, f"SLOs missing for data product: {response['name']}"

def test_data_product_has_description():
    response = get_data_product_metadata("marketing_customer360")
    description = response.get("aspects", {}).get("dataProductProperties", {}).get("description")

    assert description and len(description) > 50, "Data product needs a meaningful description"
```

You can run these assertions within the catalog itself (tools like Collibra and DataHub provide hooks for custom logic) or externally by pulling metadata via APIs and running your tests in a separate process.

The results get published to a dashboard. Teams see which of their data products pass and which fail. Nobody wants to be the team with the most red marks. Social pressure + automation beats inspection every time.

## LLMs for Fuzzy Fitness Functions

Here's where things get interesting in 2026: some fitness criteria are hard to express as deterministic rules.

How do you automatically check if a data product "represents a cohesive information concept in its domain"? Or if a code comment "meaningfully explains the why, not just the what"? Or if an API endpoint "follows RESTful conventions"?

These are judgment calls. Traditionally, they required human review. But LLMs are surprisingly good at these evaluations.

### Using LLMs for Data Product Fitness

You can use function calling (structured outputs) to get consistent, parseable results from an LLM:

```python
def evaluate_data_product_cohesion(metadata: dict) -> dict:
    prompt = f"""
    Evaluate if this data product represents a cohesive information concept.

    Name: {metadata['name']}
    Description: {metadata['description']}
    Domain: {metadata['domain']}

    A cohesive data product has value on its own and can be used independently.
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        functions=[{
            "name": "evaluate_cohesion",
            "parameters": {
                "type": "object",
                "properties": {
                    "is_cohesive": {"type": "boolean"},
                    "reason": {"type": "string"}
                }
            }
        }]
    )

    return json.loads(response.choices[0].message.function_call.arguments)
```

A data product called "Marketing Customer 360" with a description about comprehensive customer views? The LLM will likely mark it as cohesive. A data product called "Product_Id" that just "represents product ids per customer"? The LLM will correctly flag it as not cohesive - it needs to be joined with other data to be useful.

### Using LLMs for Code Quality

The same approach works for code:

```python
def evaluate_comment_quality(code_snippet: str, comment: str) -> dict:
    prompt = f"""
    Evaluate if this code comment is high quality.

    Code:
    {code_snippet}

    Comment:
    {comment}

    A good comment explains WHY the code exists or WHY it works this way,
    not WHAT the code does (which should be obvious from reading it).
    """

    # ... similar structure with function calling
```

You can use this to flag comments like `// increment i` (useless) vs `// We retry 3 times because the payment provider has transient failures under load` (useful).

### The Trade-offs

LLM-based fitness functions have limitations:

- **Non-deterministic:** The same input might give slightly different results. Use temperature=0 and still expect some variance.
- **Cost:** API calls add up. You probably don't want to run these on every commit - maybe nightly or weekly.
- **Explainability:** Asking for a "reason" in the structured output helps, but it's not the same as a deterministic rule.

Still, for criteria that were previously "too fuzzy to automate," LLMs open up new possibilities. You can now automate governance checks that would have required human review.

## Real-World Patterns

### The Dashboard Pattern

Publish fitness function results to a visible dashboard. Group by team or domain. Show green/red status with the ability to drill down into specific failures.

This creates healthy competition. Teams don't want to be the ones with failing fitness functions. It also helps data product or service consumers make informed decisions - you'd naturally prefer services that pass all fitness checks over ones that don't.

### The Progressive Strictness Pattern

Don't start with 100 rules on day one. Start with one rule that matters. Get it passing across the codebase. Then add another. And another.

If you dump a bunch of failing fitness functions on a team, they'll ignore all of them. If you introduce them gradually and keep the suite green, teams will take them seriously.

### The Exemption Pattern

Sometimes you need to break the rules. A fitness function shouldn't be a blocker without an escape hatch.

```typescript
// @archunit-ignore: Legacy code, scheduled for refactoring in Q2
import { database } from '../infrastructure/database';
```

Track exemptions. Review them periodically. But allow them - otherwise teams will just find ways around your fitness functions entirely.

## Why This Matters

**Continuous governance.** Instead of quarterly architecture reviews, you get feedback on every commit.

**Objective measurements.** No more subjective arguments. The test passes or it fails.

**Living documentation.** Your fitness functions *are* your architectural rules, written in code. They can't get out of sync with reality because they're enforced on every build.

**Faster onboarding.** New team members learn the rules by breaking them and seeing clear error messages.

**Confidence to refactor.** You know that breaking an architectural rule will be caught immediately.

**Scalable governance.** In a decentralized architecture (microservices, data mesh), you can't have a central team reviewing everything. Fitness functions let you enforce standards without creating bottlenecks.

## Getting Started

Start small:

1. Pick **one rule** that keeps getting violated
2. Write a test for it
3. Add it to CI
4. Expand gradually

For code architecture, start with ArchUnit (Java) or ArchUnitTS (TypeScript). For data products or other metadata-driven domains, start with simple assertions against your catalog's API.

Don't try to encode every architectural decision on day one. Build your fitness function suite incrementally as you discover what matters.

The goal isn't perfection. It's making violations visible and automatic, so your architecture has a chance of surviving contact with reality.
