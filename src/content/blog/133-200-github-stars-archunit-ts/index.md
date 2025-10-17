---
title: 'My side project ArchUnitTS reached 200 stars on GitHub'
summary: 'My open source library just hit 200 stars on GitHub, making it the #1 architecture testing framework in the TypeScript world! 🌍 🥇'
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

# ArchUnitTS Hits 200 Stars on GitHub: #1 TypeScript Architecture Testing Framework! 🌍 🥇

This is a big moment for me and the ArchUnitTS community! My open-source library just hit **200 stars on GitHub**, making it the **#1 architecture testing framework in the TypeScript world**. 

## The Backstory
About a year ago, while working as a consultant, I needed an architecture testing framework similar to ArchUnit but for TypeScript. Nothing on the market fully met our needs, so I started building **ArchUnitTS** in my spare time. Since then, more developers have joined me in actively maintaining it. Today, it not only has more GitHub stars than other libraries but also offers **more functionality and greater reliability** (see detailed comparison in the [README](https://github.com/LukasNiessen/ArchUnitTS)). It’s already being used in multiple enterprises!

A special **thank you** to **Jan Heimann**, **Tristan Kruse**, and **Sina Rezaei** for their active contributions, and to everyone who has reported bugs, suggested features, or helped improve the project in any way.

**ArchUnitTS**: [https://github.com/LukasNiessen/ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS)  
**More Info**: [LinkedIn Post](https://www.linkedin.com/feed/update/urn:li:activity:7379093943030013953/)

## 🕒 5-Min Quickstart
1. **Install**  
   ```bash
   npm install archunit --save-dev
   ```

2. **Write your first architecture tests**  
   Here are some simple examples of tests you can write:

   ```javascript
   import { projectFiles, metrics } from 'archunit';

   it('should not have circular dependencies', async () => {
     const rule = projectFiles()
       .inFolder('src/**')
       .should()
       .haveNoCycles();
     await expect(rule).toPassAsync();
   });

   it('presentation layer should not depend on database layer', async () => {
     const rule = projectFiles()
       .inFolder('src/presentation/**')
       .shouldNot()
       .dependOnFiles()
       .inFolder('src/database/**');
     await expect(rule).toPassAsync();
   });

   it('should not contain too large files', async () => {
     const rule = metrics()
       .count()
       .linesOfCode()
       .shouldBeBelow(1000);
     await expect(rule).toPassAsync();
   });

   it('only classes with high cohesion', async () => {
     const rule = metrics()
       .lcom()
       .lcom96b()
       .shouldBeBelow(0.3);
     await expect(rule).toPassAsync();
   });
   ```

   That’s it! These tests live alongside your regular tests and will fail if your architecture drifts or new violations appear.

3. **CI / Pipeline Integration**  
   Since these are just tests, they run like any other test suite. You can also generate HTML reports (still in beta):

   ```javascript
   await metrics().count().exportAsHTML('reports/count.html');
   await metrics().lcom().exportAsHTML('reports/lcom.html');
   ```

   Treat `reports/` as CI artifacts (e.g., GitLab, GitHub Actions).

## Why Architecture Tests Matter
Unit and integration tests catch regressions, but they don’t guard architectural boundaries. Over time, code can creep across layers, violate module structure, or create hidden coupling—especially in large teams or microservices. 

Architecture tests (also called **fitness functions**) encode your architectural invariants in code. When a pull request breaks a boundary, the tests catch it—just like a failing unit test. In the age of LLMs and AI-driven code generation, these boundaries are more critical than ever to prevent inadvertent architectural violations.

## Comparisons & Unique Strengths
ArchUnitTS stands out compared to other TypeScript architecture testing libraries (see [README](https://github.com/LukasNiessen/ArchUnitTS) for details). Key differentiators:

- **Empty-test protection**: Rules matching no files are treated as failures, preventing silent false passes.
- **Rich metrics support**: Cohesion (LCOM), coupling, distance metrics, and custom metrics.
- **UML / diagram validation + slicing**: Validate architecture against PlantUML diagrams or Nx project graphs.
- **Custom rules & metrics**: Author your own rule or metric logic.
- **Universal framework support**: Works with Jest, Vitest, Jasmine, Mocha, and others, with syntax sugar (`toPassAsync`) for common frameworks.
- **Detailed error messages and logging**: Clickable file paths, debug logs, and more.

These features make ArchUnitTS the most robust tooling for real-world TypeScript architecture testing.

## What’s Next?
- **Core engine extraction**: Decouple the core AST/analysis engine for use with Python, Go, Rust, and others.
- **Stronger cross-language support**: Enable hybrid projects (e.g., TS + Python backend) to share architecture rules.
- **Better reporting / dashboards**: Make HTML reports more interactive and support trend analysis over time.

## Thank You!
Thanks again to everyone who has starred, contributed, reported, or evangelized ArchUnitTS. I’m incredibly grateful for this milestone and excited for what’s to come!