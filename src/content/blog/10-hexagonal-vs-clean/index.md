---
title: 'Hexagonal vs. Clean Architecture: Same Thing Different Name?'
summary: "Looking at Hexagonal and Clean Architecture - they're basically the same approach with different labels. Plus how to enforce these patterns with ArchUnitTS."
date: 'Jul 05 2023'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Software Architecture
  - Hexagonal Architecture
  - Clean Architecture
  - Ports and Adapters
  - Dependency Inversion
  - ArchUnitTS
  - Domain-Driven Design
---

# Hexagonal vs. Clean Architecture: Same Thing Different Name?

Hexagonal Architecture and Clean Architecture get talked about like they're completely different things. They're not.

Both are just ways to apply the Dependency Inversion Principle. The goal? Keep your business logic separate from frameworks, databases, and UI stuff.

## The Core Idea

You have business logic (the stuff that makes money) and infrastructure (databases, web frameworks, APIs). Your business logic should never depend directly on infrastructure.

Why? Three reasons:

- **Testing is easier** - Test business logic without spinning up databases
- **Swapping tech is simpler** - Change from PostgreSQL to MongoDB without touching business rules
- **The app works anywhere** - Web UI, CLI, tests - doesn't matter

## Hexagonal Architecture

Alistair Cockburn's approach: think of your app as a hexagon.

Inside = your application logic
Outside = everything else

**Ports** are interfaces. They're contracts.

- Primary ports: what your app exposes (like use case interfaces)
- Secondary ports: what your app needs (like repository interfaces)

**Adapters** implement the ports using real technology.

- Driving adapters: HTTP controllers, CLI handlers
- Driven adapters: database repositories, email services

Rule: dependencies point inward. Adapters depend on ports, not the other way around.

## Clean Architecture

Uncle Bob's version uses concentric circles:

1. **Entities** - core business objects
2. **Use Cases** - application-specific business rules
3. **Interface Adapters** - controllers, presenters, gateways
4. **Frameworks & Drivers** - databases, web frameworks, external APIs

Same rule: dependencies only point inward.

## They're The Same Thing

Look at them side by side:

- Hexagonal's "application core" = Clean's "Use Cases"
- Hexagonal's "adapters" = Clean's "Interface Adapters" and "Frameworks & Drivers"
- Hexagonal's "secondary ports" = interfaces defined by Clean's "Use Cases"

Both enforce dependency inversion. Both isolate business logic. Different names, same pattern.

## Enforcing This With ArchUnitTS

These patterns are only useful if you actually follow them. [ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS) helps by writing tests for your architecture. Fitness functions.

## Bottom Line

Hexagonal and Clean Architecture aren't competing ideas. They're the same principle with different explanations.

Pick one name and stick with it. Focus on the dependency inversion. Keep business logic pure. Use ArchUnitTS to enforce it.

The architecture pattern doesn't matter as much as actually following it.
