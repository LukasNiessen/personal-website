---
title: "ELI5: What exactly is Domain Driven Design?"
summary: "Domain Driven Design explained for beginners"
date: "Oct 7 2023"
draft: false
xLink: ""
tags:
  - Domain Driven Design
  - DDD
---

# ELI5: What exactly is Domain Driven Design?

Domain Driven Design (DDD) is a particular way to _structure_ your app. It's more a philosophy than strict rules that can be checked in a yes-no fashion.

The core idea is to put the business domain at the center. We don't want to structure our app in _"technology layers"_ like database, business, user interface but rather around _"business layers"_. Let's get concrete.

I will inverse the order. Typically authors introduce DDD and all its aspects first and then introduce techniques of practicing it. I will, however, introduce such a technique and while doing so define the parts of DDD. It's much easier to grasp the idea of DDD like this.

## Event Storming

The technique is called _Event Storming_. Let's say we build a banking app. Users can see their balance, their transactions, send and receive money and more. No code has been written, we start from scratch (this is called a _greenfield project_). 

### Step 1: Identify Domain Events

Let's start by identifying events. And by events, I mean things that can happen in our system. So we have stuff such as:

- Money Sent
- Money Received  
- Account Opened
- Payment Failed
- Balance Updated

These are **domain events** - facts that business people care about. They're written in past tense because they already happened.

### Step 2: Find the Commands

Next, we ask: what **commands** cause these events? Commands are decisions made by users:

- Send Money → Money Sent
- Open Account → Account Opened
- Process Payment → Payment Failed (sometimes)

### Step 3: Discover Aggregates

Alright, now the first _"DDD-definition"_: Aggregates. 

And aggregate is like a cohesive bundle of _related_ events and commands. So we look at the stuff we've collected so far and identify things that _"belong together"_.

So let's look at "Money Sent" and "Money Received". The noun "Money" could be an aggregate. But that doesn't feel right for banking. Let's think more...

Actually, "Account" makes more sense. An Account can:
- Send money
- Receive money  
- Have its balance updated
- Be opened or closed

**This is an aggregate** - a collection of related objects managed as a single unit with its own lifecycle.

Note that this is of course not a clear cut definition. You will not find a clear cut definition of this anywhere. In fact, you will find a 100 different definitions and they're all not clear cut.

Then do this with all the events and commands. We end up with many different aggregates. For example a transaction aggregate, a payment method aggregate or a regulatory report aggregate.

### Step 4: Group into Bounded Contexts

Next DDD-definition: Bounded Contexts

A bounded context is simply a boundary in our big business picture. Everything in that context is somewhat related, in terms of business. So for example, the transaction aggregate and payment method aggregate would fit in the same bounded context. However, not so much with the regulatory report aggregate.

So we group our related aggregates into **bounded contexts**. In our banking app:

**Account Management Context:**
- Account aggregate
- Customer aggregate

**Payment Processing Context:**
- Transaction aggregate
- Payment Method aggregate

**Compliance Context:**
- Audit Log aggregate
- Regulatory Report aggregate

Notice how the same concept can mean different things in different contexts. A "Customer" in Account Management cares about personal details and account ownership. A "Customer" in Compliance cares about risk scores and regulatory requirements. It's the same word but it has a different meaning depending on the bounded context.

Very important: A bounded context is made up of aggregates as you see. It can be just one or it can be multiple aggregates. However, an aggregate should **never ever** be split across different contexts. It should be in exactly one context, fully contained.

## The Power of Ubiquitous Language

Here is the last part of DDD's most commonly used definitions: Ubiquitous Language.

This means that we use one language that both teams understand, the dev people and the business people. We will not introduce _"special-dev terms"_ when there are names for that already. Instead of generic terms, we use the **exact same words** that business people use.

For example:

**Bad (Generic):**
```java
class Arrangement {
    String type; // Could be loan, deposit, whatever
    BigDecimal amount;
}
```

**Good (Domain Language):**
```java
class SavingsAccount {
    AccountNumber accountNumber;
    Money balance;
    
    void withdraw(Money amount) {
        if (balance.isLessThan(amount)) {
            throw new InsufficientFundsException();
        }
        // ... rest of withdrawal logic
    }
}
```

When a business analyst says "We need to prevent withdrawals when there are insufficient funds," developers immediately understand. No translation needed.

## Where Is It Used?

As you can see in the example above, it's used at code level. For naming classes, structuring packages, slicing etc. But it's also used at system design. It's used very commonly in microservices architectures.

The idea is simple. In microservices we want every service to be totally independent. So the question arises, how to we split our app? What boundaries do we want? One way to answer this is DDD: every bounded context becomes a microservice. By doing this we get that every service has a dedicated business purpose and is _"business-wise cohesive"_. And every aggregate belongs to exactly one service. This gives us a very nice and focused way of splitting our app. And time has shown that this approach works very well, it's the most popular approach for splitting a monolith into microservices.

Note: But of course other approaches exist.

You can read more about DDD in the context of microservices in _Building Microservices_ by Sam Newman. Generally, if you want to dive deeper, I highly recommend reading the original book Domain Driven Design by Eric Evans.