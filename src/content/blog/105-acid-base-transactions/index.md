---
title: "ELI5: What exactly are ACID and BASE Transactions?"
summary: "ACID and BASE transactions. First I give an easy ELI5 explanation and then a deeper dive. At the end, I show code examples."
date: "May 20 2025"
draft: false
repoUrl: "https://github.com/LukasNiessen/acid-and-base-explained"
xLink: "https://x.com/iamlukasniessen/status/1924248827982139869"
linkedInLink: "https://www.linkedin.com/pulse/eli5-what-exactly-acid-base-transactions-lukas-nie%25C3%259Fen-nqpce/"
tags:
  - ACID
  - BASE
  - Database
  - Microservices
---

# ELI5: What exactly are ACID and BASE Transactions?

In this article, I will cover ACID and BASE transactions. First I give an easy ELI5 explanation and then a deeper dive. At the end, I show code examples.

## What is ACID, what is BASE?

When we say a database supports _ACID_ or _BASE_, we mean it supports _ACID transactions_ or _BASE transactions_.

### ACID

An ACID transaction is simply writing to the DB, but with these guarantees;

1. Write it _all or nothing_; writing A but not B cannot happen.
2. If someone else writes at the same time, make sure it still works properly.
3. Make sure the write stays.

Concretely, ACID stands for:

A = Atomicity = _all or nothing (point 1)_  
C = Consistency  
I = Isolation = _parallel writes work fine (point 2)_  
D = Durability = _write should stay (point 3)_

### BASE

A BASE transaction is again simply writing to the DB, but with weaker guarantees. BASE lacks a clear definition. However, it stands for:

BA = Basically available  
S = Soft state  
E = Eventual consistency.

What these terms usually mean is:

- _Basically available_ just means the system prioritizes availability (see CAP theorem later).

- _Soft state_ means the system's state might not be immediately consistent and may change over time without explicit updates. (Particularly across multiple nodes, that is, when we have partitioning or multiple DBs)

- _Eventual consistency_ means the system becomes consistent over time, that is, at least if we stop writing. Eventual consistency is the only clearly defined part of BASE.

### Notes

You surely noticed I didn't address the C in ACID: consistency. It means that data follows the application's rules (invariants). In other words, if a transaction starts with valid data and preserves these rules, the data stays valid. But this is the not the database's responsibility, it's the application's. Atomicity, isolation, and durability are database properties, but consistency depends on the application. So the C doesn't really belong in ACID. Some argue the C was added to ACID to make the acronym work.

The name ACID was coined in 1983 by Theo Härder and Andreas Reuter. The intent was to establish clear terminology for fault-tolerance in databases. However, how we get ACID, that is ACID transactions, is up to each DB. For example PostgreSQL implements ACID in a different way than MySQL - and surely different than MongoDB (which also supports ACID). Unfortunately when a system claims to support ACID, it's therefore not fully clear which guarantees they actually bring because ACID has become a marketing term to a degree.

And, as you saw, BASE certainly has a very unprecise definition. One can say BASE means _Not-ACID_.

## Simple Examples

Here quickly a few standard examples of why ACID is important.

### Atomicity

Imagine you're transferring $100 from your checking account to your savings account. This involves two operations:

1. Subtract $100 from checking
2. Add $100 to savings

Without transactions, if your bank's system crashes after step 1 but before step 2, you'd lose $100! With transactions, either both steps happen or neither happens. All or nothing - atomicity.

### Isolation

Suppose two people are booking the last available seat on a flight at the same time.

- Alice sees the seat is available and starts booking.
- Bob also sees the seat is available and starts booking at the same time.

Without proper isolation, both transactions might think the seat is available and both might be allowed to book it—resulting in overbooking. With isolation, only one transaction can proceed at a time, ensuring data consistency and avoiding conflicts.

### Durability

Imagine you've just completed a large online purchase and the system confirms your order.

Right after confirmation, the server crashes.

Without durability, the system might "forget" your order when it restarts. With durability, once a transaction is committed (your order is confirmed), the result is permanent—even in the event of a crash or power loss.

## Code Snippet

A transaction might look like the following. Everything between `BEGIN TRANSACTION` and `COMMIT` is considered part of the transaction.

```sql
BEGIN TRANSACTION;

-- Subtract $100 from checking account
UPDATE accounts
SET balance = balance - 100
WHERE account_type = 'checking' AND account_id = 1;

-- Add $100 to savings account
UPDATE accounts
SET balance = balance + 100
WHERE account_type = 'savings' AND account_id = 1;

-- Ensure the account balances remain valid (Consistency)
-- Check if checking account balance is non-negative
DO $$
BEGIN
    IF (SELECT balance FROM accounts WHERE account_type = 'checking' AND account_id = 1) < 0 THEN
        RAISE EXCEPTION 'Insufficient funds in checking account';
    END IF;
END $$;

COMMIT;
```

## COMMIT and ROLLBACK

Two essential commands that make ACID transactions possible are COMMIT and ROLLBACK:

### COMMIT

When you issue a COMMIT command, it tells the database that all operations in the current transaction should be made permanent. Once committed:

- Changes become visible to other transactions
- The transaction cannot be undone
- The database guarantees durability of these changes

A COMMIT represents the successful completion of a transaction.

### ROLLBACK

When you issue a ROLLBACK command, it tells the database to discard all operations performed in the current transaction. This is useful when:

- An error occurs during the transaction
- Application logic determines the transaction should not complete
- You want to test operations without making permanent changes

ROLLBACK ensures atomicity by preventing partial changes from being applied when something goes wrong.

Example with ROLLBACK:

```sql
BEGIN TRANSACTION;

UPDATE accounts
SET balance = balance - 100
WHERE account_type = 'checking' AND account_id = 1;

-- Check if balance is now negative
IF (SELECT balance FROM accounts WHERE account_type = 'checking' AND account_id = 1) < 0 THEN
    -- Insufficient funds, cancel the transaction
    ROLLBACK;
    -- Transaction is aborted, no changes are made
ELSE
    -- Add the amount to savings
    UPDATE accounts
    SET balance = balance + 100
    WHERE account_type = 'savings' AND account_id = 1;

    -- Complete the transaction
    COMMIT;
END IF;
```

## Why BASE?

BASE used to be important because many DBs, for example document-oriented DBs, did not support ACID. They had other advantages. Nowadays however, most document-oriented DBs support ACID.

So why even have BASE?

ACID can get really difficult when having distributed DBs. For example when you have partitioning or you have a microservice architecture where each service has its own DB. If your transaction only writes to one partition (or DB), then there's no problem. But what if you have a transaction that spans accross multiple partitions or DBs, a so called _distributed transaction_?

The short answer is: we either work around it or we loosen our guarantees from ACID to ... BASE.

## ACID in Distributed Databases

Let's address ACID one by one. Let's only consider partitioned DBs for now.

### Atomicity

Difficult. If we do a write on partition `A` and it works but one on `B` fails, we're in trouble.

### Isolation

Difficult. If we have multiple transactions concurrently access data across different partitions, it's hard to ensure isolation.

### Durability

No problem since each node has durable storage.

### What about Microservice Architectures?

Pretty much the same issues as with partitioned DBs. However, it gets even more difficult because microservices are independently developed and deployed.

### Solutions

There are two primary approaches to handling transactions in distributed systems:

#### Two-Phase Commit (2PC)

Two-Phase Commit is a protocol designed to achieve atomicity in distributed transactions. It works as follows:

1. **Prepare Phase**: A coordinator node asks all participant nodes if they're ready to commit

   - Each node prepares the transaction but doesn't commit
   - Nodes respond with "ready" or "abort"

2. **Commit Phase**: If all nodes are ready, the coordinator tells them to commit
   - If any node responded with "abort," all nodes are told to rollback
   - If all nodes responded with "ready," all nodes are told to commit

2PC guarantees atomicity but has significant drawbacks:

- It's blocking (participants must wait for coordinator decisions)
- Performance overhead due to multiple round trips
- Vulnerable to coordinator failures
- Can lead to extended resource locking

Example of 2PC in pseudo-code:

```
// Coordinator
function twoPhaseCommit(transaction, participants) {
    // Phase 1: Prepare
    for each participant in participants {
        response = participant.prepare(transaction)
        if response != "ready" {
            for each participant in participants {
                participant.abort(transaction)
            }
            return "Transaction aborted"
        }
    }

    // Phase 2: Commit
    for each participant in participants {
        participant.commit(transaction)
    }
    return "Transaction committed"
}
```

#### Saga Pattern

The Saga pattern is a sequence of local transactions where each transaction updates a single node. After each local transaction, it publishes an event that triggers the next transaction. If a transaction fails, compensating transactions are executed to undo previous changes.

1. **Forward transactions**: T1, T2, ..., Tn
2. **Compensating transactions**: C1, C2, ..., Cn-1 (executed if something fails)

For example, an order processing flow might have these steps:

- Create order
- Reserve inventory
- Process payment
- Ship order

If the payment fails, compensating transactions would:

- Cancel shipping
- Release inventory reservation
- Cancel order

Sagas can be implemented in two ways:

- **Choreography**: Services communicate through events
- **Orchestration**: A central coordinator manages the workflow

Example of a Saga in pseudo-code:

```
// Orchestration approach
function orderSaga(orderData) {
    try {
        orderId = orderService.createOrder(orderData)
        inventoryId = inventoryService.reserveItems(orderData.items)
        paymentId = paymentService.processPayment(orderData.payment)
        shippingId = shippingService.scheduleDelivery(orderId)
        return "Order completed successfully"
    } catch (error) {
        if (shippingId) shippingService.cancelDelivery(shippingId)
        if (paymentId) paymentService.refundPayment(paymentId)
        if (inventoryId) inventoryService.releaseItems(inventoryId)
        if (orderId) orderService.cancelOrder(orderId)
        return "Order failed: " + error.message
    }
}
```

## What about Replication?

There are mainly three way of replicating your DB. Single-leader, multi-leader and leaderless. I will not address multi-leader.

### Single-leader

ACID is not a concern here. If the DB supports ACID, replicating it won't change anything. You write to the leader via an ACID transaction and the DB will make sure the followers are updated. Of course, when we have asynchronous replication, we don't have consistency. But this is not an ACID problem, it's a asynchronous replication problem.

### Leaderless Replication

In leaderless replication systems (like Amazon's Dynamo or Apache Cassandra), ACID properties become more challenging to implement:

- **Atomicity**: Usually limited to single-key operations
- **Consistency**: Often relaxed to eventual consistency (BASE)
- **Isolation**: Typically provides limited isolation guarantees
- **Durability**: Achieved through replication to multiple nodes

This approach prioritizes availability and partition tolerance over consistency, aligning with the BASE model rather than strict ACID.

## Conclusion

- ACID provides strong guarantees but can be challenging to implement across distributed systems

- BASE offers more flexibility but requires careful application design to handle eventual consistency

It's important to understand ACID vs BASE and the whys.

The right choice depends on your specific requirements:

- Financial applications may need ACID guarantees
- Social media applications might work fine with BASE semantics (at least most parts of it).
