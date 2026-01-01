---
title: 'Patching: The Boring Security Practice That Could Save You $700 Million'
summary: 'Why patching matters, the Equifax breach, supply chain attacks, and how to stay on top of updates in complex modern systems'
date: 'Jan 01 2026'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Security
  - DevOps
  - Infrastructure
  - Kubernetes
---

# Patching: The Boring Security Practice That Could Save You $700 Million

Patching is one of those things that everyone knows is important but nobody gets excited about. It's not flashy. It doesn't make for great conference talks. But neglecting it can be catastrophic.

Let's start with a story that illustrates this perfectly.

## The Equifax Breach: A $700 Million Lesson

In 2017, Equifax - one of the three major credit bureaus in the US - suffered a massive data breach. The data of more than 160 million people was compromised. Names, Social Security numbers, birth dates, addresses, driver's license numbers. The most sensitive personal information you can imagine.

The result? A $700 million settlement. Massive reputational damage. Years of legal battles. Executives lost their jobs.

And here's the thing: **it was entirely preventable**.

The attackers exploited a known vulnerability in Apache Struts, a Java web framework. The vulnerability had been identified months before the breach. The Struts maintainers had already released a patched version. All Equifax had to do was update their software.

They didn't.

For months, they ran production systems with a known, publicly documented vulnerability. An exploit was available. Attackers found it and used it.

That's the cost of not patching.

## The Growing Complexity Problem

The issue of keeping on top of patching is becoming more complex as we deploy increasingly sophisticated systems. A typical modern infrastructure has many layers, each requiring its own maintenance and patching:

```
┌─────────────────────────────────────────────┐
│           Your Application Code             │
├─────────────────────────────────────────────┤
│        Third-Party Libraries/Packages       │
├─────────────────────────────────────────────┤
│         Application Runtime (Node, JVM)     │
├─────────────────────────────────────────────┤
│              Container Image OS             │
├─────────────────────────────────────────────┤
│          Container Runtime (Docker)         │
├─────────────────────────────────────────────┤
│           Kubernetes / Orchestrator         │
├─────────────────────────────────────────────┤
│              Host Operating System          │
├─────────────────────────────────────────────┤
│               Hypervisor / VMM              │
├─────────────────────────────────────────────┤
│                  Hardware                   │
└─────────────────────────────────────────────┘
```

If you run all of this infrastructure yourself, you're responsible for patching every single layer. How confident are you that you're up to date everywhere? Most organizations honestly can't answer that question.

This is one area where managed cloud services genuinely help. If you use a managed Kubernetes cluster on AWS, GCP, or Azure, you offload responsibility for several of these layers:

```
┌─────────────────────────────────────────────┐
│           Your Application Code             │  ← You manage
├─────────────────────────────────────────────┤
│        Third-Party Libraries/Packages       │  ← You manage
├─────────────────────────────────────────────┤
│         Application Runtime (Node, JVM)     │  ← You manage
├─────────────────────────────────────────────┤
│              Container Image OS             │  ← You manage
├─────────────────────────────────────────────┤
│          Container Runtime (Docker)         │  ← Cloud provider
├─────────────────────────────────────────────┤
│           Kubernetes / Orchestrator         │  ← Cloud provider
├─────────────────────────────────────────────┤
│              Host Operating System          │  ← Cloud provider
├─────────────────────────────────────────────┤
│               Hypervisor / VMM              │  ← Cloud provider
├─────────────────────────────────────────────┤
│                  Hardware                   │  ← Cloud provider
└─────────────────────────────────────────────┘
```

That's a significant reduction in scope. But notice - you're still responsible for four critical layers. And those are often the ones that get neglected.

## The Container Curveball

Containers throw us an interesting curveball here. We treat containers as [immutable](https://lukasniessen.com/blog/129-immutable-infrastructure/) - we don't patch them in place, we replace them entirely. Great for consistency. But there's a catch.

A container isn't just your application code. It includes an entire operating system. And if you haven't rebuilt and redeployed your container in six months, that's six months of operating system patches that haven't been applied. Your "immutable" container might be running with dozens of known vulnerabilities.

Even worse: containers are built from base images, which extend other base images. Do you actually know what's in your base image? Are you confident there are no backdoors? No known CVEs?

This is why container scanning tools like Aqua, Trivy, Snyk Container, or the built-in scanning in container registries exist. They analyze your container images and tell you what vulnerabilities exist. You should be running these scans in your CI/CD pipeline and blocking deployments of vulnerable images.

## The Supply Chain Nightmare

At the top of the stack is your application code and its dependencies. And this is where things have gotten really scary in recent years.

### The npm Package Attacks of 2025

In late 2025, the JavaScript ecosystem experienced one of its worst supply chain attacks. Attackers compromised several widely-used npm packages including `chalk`, `ansi-styles`, and `debug`. These aren't obscure packages - they're foundational utilities with millions of weekly downloads. Countless applications depend on them, often transitively.

The attackers injected malicious code that exfiltrated environment variables, credentials, and other sensitive data from the machines running these packages. Because these libraries are so deeply embedded in the dependency trees of most Node.js applications, the blast radius was enormous.

This attack highlighted something the security community has been warning about for years: **your dependencies are part of your attack surface**. It's not just the code you write; it's the code you import.

### The Growing Pattern

This wasn't an isolated incident. We've seen similar attacks before:

- **event-stream (2018):** A maintainer handed over control to an attacker who added malicious code targeting cryptocurrency wallets
- **ua-parser-js (2021):** A popular package was hijacked to install cryptominers and password stealers
- **node-ipc (2022):** The maintainer intentionally added code that destroyed files on systems with Russian IP addresses
- **Various typosquatting attacks:** Malicious packages with names similar to popular ones (like `lodash` vs `lodahs`)

The pattern is clear: attackers are increasingly targeting the supply chain rather than your code directly. Why spend effort finding vulnerabilities in your application when they can just compromise a library you depend on?

## What To Do About It

### 1. Use Automated Dependency Scanning

This is non-negotiable. You need tools that automatically scan your dependencies and alert you to known vulnerabilities.

**GitHub Dependabot** is probably the most accessible option. It's built into GitHub and free for all repositories. It:
- Scans your dependency files (package.json, requirements.txt, pom.xml, etc.)
- Alerts you when dependencies have known vulnerabilities
- Automatically creates pull requests to update vulnerable dependencies
- Can be configured to auto-merge minor/patch updates

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
    
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Snyk** is another excellent option, especially for enterprise use. It provides deeper analysis, prioritizes vulnerabilities by exploitability, and integrates with more ecosystems.

**GitHub Code Scanning** (powered by CodeQL) can also identify security issues in your own code, not just dependencies.

### 2. Build Security Scanning Into CI/CD

Don't just scan - block. Configure your CI pipeline to fail if it detects vulnerable dependencies above a certain severity threshold.

```yaml
# Example GitHub Actions workflow
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
```

This shifts security left. A developer will know immediately if they've introduced a vulnerable dependency, rather than finding out months later (or worse, after a breach).

### 3. Keep Container Images Fresh

Set up automated processes to rebuild and redeploy containers regularly, even if your application code hasn't changed. This ensures OS-level patches are applied.

Consider using distroless or minimal base images to reduce the attack surface. Fewer packages installed means fewer things to patch.

```dockerfile
# Instead of this
FROM node:20

# Consider this (fewer vulnerabilities to worry about)
FROM node:20-slim

# Or even this (minimal attack surface)
FROM gcr.io/distroless/nodejs20
```

### 4. Monitor Container Registries

Use container registry scanning (available in ECR, GCR, ACR, Docker Hub, and others) to continuously monitor stored images for newly discovered vulnerabilities. A container that was clean when you built it might have known vulnerabilities discovered later.

### 5. Have a Patching Cadence

Don't wait for emergencies. Establish regular cadences for reviewing and applying updates:

- **Critical vulnerabilities:** Same day or next business day
- **High severity:** Within one week
- **Medium severity:** Within one month
- **Routine updates:** Monthly or quarterly batches

The key is having a process, not just reacting to whatever vulnerability makes the news.

### 6. Know Your Dependencies

Maintain a Software Bill of Materials (SBOM). Know exactly what libraries, frameworks, and tools your applications depend on. When a vulnerability is announced, you should be able to quickly answer: "Are we affected?"

Tools like Syft, CycloneDX, and SPDX can generate SBOMs automatically.

### 7. Limit Dependency Sprawl

Every dependency you add is a potential attack vector. Be intentional about what you import:

- Do you really need that 2KB utility library, or can you write those 10 lines yourself?
- Is this package actively maintained?
- Who are the maintainers? Are they known in the community?
- Does it have many dependencies of its own?

The npm ecosystem in particular has a culture of micro-dependencies that creates massive transitive dependency trees. A single `npm install` can pull in hundreds of packages. Each one is potential attack surface.

## The Real Cost of Not Patching

Let's go back to Equifax. $700 million in settlement costs. But that's not even the full picture:

- Stock price dropped 35% after the breach
- Multiple executives resigned or were fired
- Years of regulatory scrutiny
- Ongoing reputational damage
- The personal cost to 160 million people whose data was exposed

All because they didn't apply a patch that had been available for months.

Patching isn't exciting. It doesn't have the glamour of building new features or implementing cutting-edge architectures. But it's fundamental to running secure systems.

The tools exist. Dependabot, Snyk, container scanning, CI/CD integration - all of these are accessible and many are free. The question is whether your organization has the discipline to use them consistently.

## Wrapping Up

Patching feels like basic hygiene, and it is. But "basic" doesn't mean "easy" at scale. Modern systems have many layers, complex dependency trees, and constantly evolving threat landscapes.

The key takeaways:

- **Automate dependency scanning.** Use Dependabot, Snyk, or similar tools. Don't rely on manual tracking.
- **Build security into CI/CD.** Block deployments of vulnerable code.
- **Keep containers fresh.** Rebuild regularly, use minimal base images, scan your registries.
- **Know your dependencies.** Maintain SBOMs. Limit unnecessary dependencies.
- **Have a process.** Define patching cadences and stick to them.

The Equifax breach wasn't caused by a sophisticated zero-day exploit. It was caused by failing to apply a patch that had been publicly available for months. Don't let that be your story.
