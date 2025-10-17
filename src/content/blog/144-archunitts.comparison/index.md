---
title: 'ArchUnitTS vs eslint-plugin-import: My side project reached 200 stars on GitHub'
summary: 'ArchUnitTS vs eslint-plugin-import comparison'
date: 'Oct 15 2025'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Architecture
  - TypeScript
  - ArchUnitTS
  - ArchUnit
---

# ArchUnitTS vs eslint-plugin-import: My side project reached 200 stars on GitHub

A couple days ago I proudly posted that my open-source library ArchUnitTS reached 200 stars on GitHub. While I received amazing feedback from you, many of you also asked me how my library compares to linter plugins - in particular eslint-plugin-import. I will answer this in here!

## Backstory

Just super quickly for those that haven't read the other post. ArchUnitTS is an architecture testing library for TypeScript applications. 

About a year ago, while working as a consultant, I needed an architecture testing framework similar to ArchUnit but for TypeScript. Nothing on the market fully met our needs, so I started building **ArchUnitTS** in my spare time. It is now the #1 architecture testing framework in the TypeScript world - well, at least measured by stars.

**ArchUnitTS**: [https://github.com/LukasNiessen/ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS)

The library lets you write tests such as this one.

  ```javascript
it('presentation layer should not depend on database layer', async () => {
  const rule = projectFiles()
    .inFolder('src/presentation/**')
    .shouldNot()
    .dependOnFiles()
    .inFolder('src/database/**');
  await expect(rule).toPassAsync();
});
```

Now, this is something you can also do with linter plugins like eslint-plugin-import. So, rightfully, people wondered: what advantages does ArchUnitTS even have?

## ArchUnitTS vs eslint-plugin-import

While both tools can validate dependencies between modules, **ArchUnitTS goes far beyond what eslint-plugin-import offers**. Here's a detailed breakdown of what makes ArchUnitTS unique:

### 1. Code Metrics Analysis

ArchUnitTS provides extensive code quality metrics that eslint-plugin-import completely lacks:

- **LCOM (Lack of Cohesion of Methods)** metrics for measuring class cohesion
- **Count metrics**: lines of code, method count, field count, statements per file
- **Distance metrics**: coupling factor, abstractness, instability, distance from main sequence
- **Custom metrics**: ability to define your own metrics with custom calculation logic
- **Complexity metrics**: cyclomatic complexity analysis

### 2. Architecture Slices and Layers

ArchUnitTS offers sophisticated architectural boundary validation:

- Project slices with `projectSlices().definedBy()` for defining architectural boundaries
- Layer dependency validation across multiple architectural layers simultaneously
- Slice-to-slice dependency rules (e.g., "services should not depend on controllers")
- **UML diagram validation** - validate actual code against PlantUML architectural diagrams

### 3. Nx Monorepo Support

ArchUnitTS has built-in support for Nx monorepos:

- Read and validate against Nx project graph
- Enforce boundaries between Nx applications and libraries
- Validate Nx project type boundaries and naming conventions

### 4. HTML Report Generation

ArchUnitTS can generate rich HTML dashboards and reports:

- Visual metrics dashboards with charts
- Comprehensive architecture analysis reports
- Customizable CSS and formatting
- Export individual or combined metric reports

### 5. Empty Test Protection

ArchUnitTS fails tests by default when no files match the specified patterns (preventing false positives from typos), while eslint-plugin-import would silently pass.

### 6. Custom Architecture Rules

ArchUnitTS allows defining completely custom rules with arbitrary logic:

```javascript
const myCustomRule = (file: FileInfo) => {
  // Any custom validation logic
  return file.content.includes('export');
};
```

### 7. Test Framework Integration

ArchUnitTS provides:

- Special async matchers for Jest, Vitest, and Jasmine (`toPassAsync()`)
- Better error messages with clickable file paths
- Works with **ANY testing framework** (not just as a linter)

### 8. Advanced Logging and Debugging

- Multiple log levels (debug, info, warn, error)
- File logging for CI/CD pipeline integration
- Detailed violation tracking and reporting
- Session-based logging with timestamps

### 9. Pattern Matching Flexibility

While both support glob patterns, ArchUnitTS offers:

- Combined filtering methods (`inFolder()`, `withName()`, `inPath()`)
- Class name matching for metrics (`forClassesMatching()`)
- More flexible pattern combination strategies

### 10. Architecture Fitness Functions

ArchUnitTS is specifically designed to implement **architectural fitness functions** as part of evolutionary architecture practices.

### 11. Circular Dependency Detection with Context

While eslint-plugin-import has `no-cycle`, ArchUnitTS provides:

- More granular control over where to check for cycles
- Better reporting of cycle paths
- Integration with other architectural rules

### 12. Class-Level Analysis

ArchUnitTS can analyze class structures, methods, and fields - not just module imports:

- Method-to-field ratios
- Class cohesion analysis
- Field count restrictions per class type

### 13. Performance Optimization

- Built-in caching system for analysis results
- Parallel processing capabilities
- Configurable cache lifetime for long-running processes

### 14. Architecture Documentation Validation

- Validate code against architectural diagrams (PlantUML)
- Support for component, package, class, and custom architecture diagrams
- Enforce documented architectural decisions

## What eslint-plugin-import Does Better

To be fair, eslint-plugin-import does have some advantages:

- **Real-time feedback** - As a linter, it provides immediate feedback while coding
- **Auto-fixing** - Can automatically fix certain issues (with `--fix` flag)
- **Editor integration** - Native IDE/editor support as part of ESLint
- **Import-specific rules** - More granular import/export validation (like `no-deprecated`, `no-anonymous-default-export`, etc.)
- **Module resolution** - More sophisticated resolver system for various module systems
- **Simpler setup** - Just ESLint configuration, no test files needed

## The Bottom Line

**ArchUnitTS** and **eslint-plugin-import** serve different purposes:

- Use **eslint-plugin-import** for day-to-day linting and immediate feedback on import/export issues
- Use **ArchUnitTS** for comprehensive architecture testing, metrics analysis, and enforcing architectural boundaries as part of your CI/CD pipeline

They're not mutually exclusive - in fact, they complement each other perfectly! Many teams use both: eslint-plugin-import for immediate developer feedback, and ArchUnitTS for deeper architectural validation in their test suites.