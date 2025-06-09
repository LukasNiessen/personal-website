---
title: 'SOLID Principles: Making Code That Bends But Never Breaks'
summary: "The five SOLID principles explained with real code examples. How to write maintainable code that's easy to change."
date: 'Mar 12 2024'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Software Design
  - SOLID Principles
  - Object-Oriented Programming
  - Clean Code
  - Code Quality
  - Architecture
---

# SOLID Principles: Making Code That Bends But Never Breaks

Writing code is easy. Writing code that's still maintainable six months later is hard.

That's where SOLID comes in. Five principles that help you write better object-oriented code.

## Single Responsibility Principle (SRP)

**One class, one job.**

Bad:

```typescript
class UserService {
  createUser(user: User) {
    /* ... */
  }
  validateEmail(email: string) {
    /* ... */
  }
  sendWelcomeEmail(user: User) {
    /* ... */
  }
  generateUserReport(user: User) {
    /* ... */
  }
}
```

Good:

```typescript
class UserService {
  createUser(user: User) {
    /* ... */
  }
}

class EmailValidator {
  validate(email: string) {
    /* ... */
  }
}

class EmailService {
  sendWelcomeEmail(user: User) {
    /* ... */
  }
}

class UserReportGenerator {
  generate(user: User) {
    /* ... */
  }
}
```

Each class does one thing. Easy to understand, easy to change.

## Open/Closed Principle (OCP)

**Open for extension, closed for modification.**

Instead of modifying existing code, add new code that extends it.

Bad:

```typescript
class PaymentProcessor {
  processPayment(payment: Payment) {
    if (payment.type === 'credit') {
      // process credit card
    } else if (payment.type === 'debit') {
      // process debit card
    } else if (payment.type === 'crypto') {
      // process crypto
    }
  }
}
```

Good:

```typescript
interface PaymentProcessor {
  processPayment(payment: Payment): void;
}

class CreditCardProcessor implements PaymentProcessor {
  processPayment(payment: Payment) {
    /* ... */
  }
}

class DebitCardProcessor implements PaymentProcessor {
  processPayment(payment: Payment) {
    /* ... */
  }
}

class CryptoProcessor implements PaymentProcessor {
  processPayment(payment: Payment) {
    /* ... */
  }
}
```

Add new payment types without touching existing code.

## Liskov Substitution Principle (LSP)

**If it looks like a duck and quacks like a duck but needs batteries, you probably have the wrong abstraction.**

Subtypes must be substitutable for their base types.

Bad:

```typescript
class Bird {
  fly() {
    /* ... */
  }
}

class Penguin extends Bird {
  fly() {
    throw new Error("Can't fly!"); // Breaks LSP
  }
}
```

Good:

```typescript
interface Bird {
  move(): void;
}

class FlyingBird implements Bird {
  move() {
    this.fly();
  }
  private fly() {
    /* ... */
  }
}

class WalkingBird implements Bird {
  move() {
    this.walk();
  }
  private walk() {
    /* ... */
  }
}
```

Don't force inheritance where it doesn't make sense.

## Interface Segregation Principle (ISP)

**Small, focused interfaces are better than one big interface.**

Bad:

```typescript
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

class Robot implements Worker {
  work() { /* ... */ }
  eat() { throw new Error('Robots don't eat'); }
  sleep() { throw new Error('Robots don't sleep'); }
}
```

Good:

```typescript
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

class Human implements Workable, Eatable, Sleepable {
  work() {
    /* ... */
  }
  eat() {
    /* ... */
  }
  sleep() {
    /* ... */
  }
}

class Robot implements Workable {
  work() {
    /* ... */
  }
}
```

Clients shouldn't depend on interfaces they don't use.

## Dependency Inversion Principle (DIP)

**High-level modules shouldn't depend on low-level modules. Both should depend on abstractions.**

Bad:

```typescript
class OrderService {
  private mysql = new MySQLDatabase(); // Hard dependency

  saveOrder(order: Order) {
    this.mysql.query('INSERT INTO orders...');
  }
}
```

Good:

```typescript
interface Database {
  save(data: any): void;
}

class OrderService {
  constructor(private db: Database) {} // Depends on abstraction

  saveOrder(order: Order) {
    this.db.save(order);
  }
}

class MySQLDatabase implements Database {
  save(data: any) {
    // MySQL implementation
  }
}

class MongoDatabase implements Database {
  save(data: any) {
    // MongoDB implementation
  }
}
```

Easy to swap implementations, easy to test.

## Real-World Benefits

**1. Easier Changes**
When requirements change (they always do), SOLID code is easier to modify.

**2. Better Testing**
Small, focused classes with clear dependencies are easy to test.

**3. Reusable Code**
Well-separated concerns lead to reusable components.

**4. Fewer Bugs**
Clear responsibilities and dependencies mean fewer unexpected interactions.

## Common Questions

**"Isn't this overkill for small projects?"**

- Start simple
- Apply SOLID when complexity grows
- Focus on SRP and DIP first

**"How strict should we be?"**

- Use judgment
- Don't over-engineer
- Apply where it reduces complexity

**"What about performance?"**

- Clean code first
- Profile before optimizing
- Most apps aren't CPU-bound

## Practical Tips

**1. Start with Single Responsibility**
If a class is doing too much, split it.

**2. Use Dependency Injection**

```typescript
// Container setup
container.register('database', MySQLDatabase);
container.register('emailService', EmailService);

// Usage
class UserService {
  constructor(
    private db: Database,
    private emailService: EmailService
  ) {}
}
```

**3. Write Interfaces First**
Design your contracts before implementations.

**4. Look for Warning Signs:**

- Giant classes
- Deep inheritance hierarchies
- Classes that change for multiple reasons
- Tight coupling
- Repeated code patterns

## When to Break the Rules

SOLID principles are guidelines, not laws:

**1. Simple Scripts**
Quick scripts don't need perfect architecture.

**2. Prototypes**
Get it working first, make it SOLID later.

**3. Performance-Critical Code**
Sometimes tight coupling is faster.

**4. Framework Constraints**
Some frameworks force specific patterns.

## Bottom Line

SOLID isn't about following rules perfectly. It's about writing code that's easy to change.

Start with Single Responsibility. Add other principles as needed. Use judgment.

Remember: The goal is maintainable code, not perfect code.
