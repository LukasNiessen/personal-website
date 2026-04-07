---
title: 'ArchUnitTS just hit 400 GitHub Stars and 50k Monthly Downloads'
summary: 'My open source architecture testing library ArchUnitTS reached 400 stars on GitHub and 50,000 monthly downloads on npm'
date: 'Apr 7 2026'
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Architecture
  - TypeScript
  - ArchUnitTS
  - ArchUnit
  - Open Source
---

# How my Library hit 400 GitHub Stars and 50k Monthly Downloads

About six months ago I wrote a post celebrating 200 stars on GitHub. Today, ArchUnitTS has doubled that to **400 stars** and crossed **50,000 monthly downloads on npm**. That second number is what really gets me. Stars are nice, but downloads mean people are actually using this thing in their projects, in their CI pipelines, in their daily work.

## Some Context

ArchUnitTS is an architecture testing library for TypeScript. You write tests that enforce architectural rules - things like "the presentation layer should not depend on the database layer" or "no file should exceed 1000 lines of code." These tests run alongside your unit tests and catch architectural drift before it makes it into production.

I started building it about two years ago while working as a consultant. We needed something like ArchUnit (the Java library) but for TypeScript. Nothing out there fully met our needs, so I built it. Since then, it's grown into the #1 architecture testing framework in the TypeScript ecosystem.

**ArchUnitTS**: [https://github.com/LukasNiessen/ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS)

## What 50k Downloads Actually Means

The GitHub stars are a nice vanity metric, sure. But 50,000 monthly npm downloads tells a different story. That's real adoption. That's teams integrating ArchUnitTS into their build pipelines, developers writing architecture tests as part of their workflow. It means the library is stable enough and useful enough that people rely on it.

What's also interesting is where the growth came from. A significant chunk of downloads are coming from enterprise projects. I've received messages from developers at companies I didn't even know were using it. That's the beauty of open source - you publish something and it finds its way into places you'd never expect.

## Why Architecture Tests Matter Even More Now

In the age of AI-generated code, architecture tests are critical. LLMs are great at writing code that works, but they don't understand your architectural boundaries. They'll happily import a database module from your presentation layer if it gets the job done.

Architecture tests are the safety net. They encode your structural decisions in code and catch violations automatically, regardless of whether a human or an AI wrote the code. If you're using Copilot or Cursor or any other AI coding tool in your team, you really should have architecture tests in place.

## Quick Start

Here's how to get started in 2 minutes:

```bash
npm install archunit --save-dev
```

Then write your first test:

```javascript
import { projectFiles } from 'archunit';

it('controllers should not depend on repositories directly', async () => {
  const rule = projectFiles()
    .inFolder('src/controllers/**')
    .shouldNot()
    .dependOnFiles()
    .inFolder('src/repositories/**');
  await expect(rule).toPassAsync();
});
```

That's it. This runs with Jest, Vitest, Mocha, Jasmine - whatever you're using.

## More Examples

Here are some more things you can do with ArchUnitTS. First, circular dependency detection:

```javascript
import { projectFiles } from 'archunit';

it('should not have circular dependencies', async () => {
  const rule = projectFiles()
    .inFolder('src/**')
    .should()
    .haveNoCycles();
  await expect(rule).toPassAsync();
});
```

Code metrics - enforce limits on file size, class cohesion, and cyclomatic complexity:

```javascript
import { metrics } from 'archunit';

it('no file should be too large', async () => {
  const rule = metrics()
    .count()
    .linesOfCode()
    .shouldBeBelow(1000);
  await expect(rule).toPassAsync();
});

it('classes should have high cohesion', async () => {
  const rule = metrics()
    .lcom()
    .lcom96b()
    .shouldBeBelow(0.3);
  await expect(rule).toPassAsync();
});

it('functions should not be overly complex', async () => {
  const rule = metrics()
    .complexity()
    .cyclomatic()
    .shouldBeBelow(15);
  await expect(rule).toPassAsync();
});
```

Layer architecture enforcement using slices:

```javascript
import { projectSlices } from 'archunit';

it('slices should be free of cycles', async () => {
  const rule = projectSlices()
    .definedBy('src/(**)/')
    .should()
    .beFreeOfCycles();
  await expect(rule).toPassAsync();
});
```

Custom rules when you need something specific:

```javascript
import { projectFiles } from 'archunit';

it('service files should not import from React', async () => {
  const rule = projectFiles()
    .inFolder('src/services/**')
    .should()
    .matchCustomRule((file) => {
      return !file.content.includes("from 'react'");
    });
  await expect(rule).toPassAsync();
});
```

And you can generate HTML reports for your CI pipeline:

```javascript
await metrics().count().exportAsHTML('reports/count.html');
await metrics().lcom().exportAsHTML('reports/lcom.html');
```

Treat these as CI artifacts and you've got architecture dashboards for free.

## How Does It Compare to ESLint?

I wrote a [detailed comparison](/blog/archunitts-comparison), however, the short version: they serve different purposes.

**eslint-plugin-import** (and similar linter plugins) is great for real-time feedback while you code. It can catch import issues immediately in your editor, and it can auto-fix certain problems. If you want quick linter-style enforcement, that's the right tool.

**ArchUnitTS** goes much further than what a linter can do. Here's what you get on top:

- **Code metrics**: LCOM cohesion, cyclomatic complexity, coupling, instability, lines of code - none of this exists in ESLint
- **Architecture slices and layers**: Define architectural boundaries and validate them, including against PlantUML diagrams
- **Nx monorepo support**: Validate against the Nx project graph, enforce boundaries between apps and libraries
- **HTML report generation**: Visual dashboards with charts for your CI pipeline
- **Empty test protection**: If your pattern matches zero files (typo in a path, for example), ArchUnitTS fails the test instead of silently passing - linters would just pass
- **Custom rules with full access**: Write arbitrary validation logic with access to the full file AST, not just import paths

So the answer isn't "one or the other." Use ESLint for immediate feedback on imports and style. Use ArchUnitTS for enforcing your actual architecture as part of your test suite. They complement each other nicely.

## What's Next

We're working on a few things:

- **Cross-language support**: Extracting the core analysis engine so it can work with Python, Go, and Rust projects. The idea is that hybrid projects can share architecture rules across languages.
- **Interactive HTML dashboards**: The current HTML report export is still in beta. We're building proper interactive dashboards with trend analysis so you can track how your architecture metrics evolve over time.
- **VS Code extension**: Real-time feedback on architecture violations while you code, similar to how a linter works but for architectural rules.

## Thank You

A huge thanks to everyone who has contributed, reported bugs, suggested features, or simply used ArchUnitTS in their projects. And to everyone who starred the repo or shared it with their team - thank you. Reaching 400 stars and 50k monthly downloads is something I genuinely did not expect when I started this project. Here's to the next milestone.
