---
title: 'CQRS: When Reading and Writing Become Separate Concerns'
summary: "Command Query Responsibility Segregation explained. Why you might want separate models for reading and writing data, and when it's overkill."
date: 'May 03 2024'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Software Architecture
  - CQRS
  - Design Patterns
  - Data Architecture
  - Microservices
  - Event Sourcing
  - Database Design
---

# CQRS: When Reading and Writing Become Separate Concerns

Most applications use the same data model for reading and writing. Users create orders using an Order entity, and reports query the same Order entity.

**CQRS** says: what if we split these completely?

## What Is CQRS?

**Command Query Responsibility Segregation** separates read operations (queries) from write operations (commands) using different models.

Instead of one unified model, you have:

- **Command side** - Handles writes, focused on business rules and validation
- **Query side** - Handles reads, optimized for specific query patterns

Think of it like having separate entrances for deliveries and customers at a store. Different purposes, different optimizations.

## Traditional Approach vs CQRS

**Traditional (CRUD):**

```typescript
class OrderService {
  async createOrder(orderData: CreateOrderRequest): Promise<Order> {
    // Validate and create order
    return this.orderRepository.save(orderData);
  }

  async getOrder(id: string): Promise<Order> {
    return this.orderRepository.findById(id);
  }

  async getOrderSummary(): Promise<OrderSummary[]> {
    // Complex query with joins
    return this.orderRepository.getOrderSummaryWithCustomerAndItems();
  }
}
```

**CQRS:**

```typescript
// Command side - focused on business logic
class OrderCommandHandler {
  async handle(command: CreateOrderCommand): Promise<void> {
    const order = new Order(command.customerId, command.items);
    order.validate();
    order.calculateTotals();

    await this.orderRepository.save(order);
    await this.eventBus.publish(new OrderCreatedEvent(order));
  }
}

// Query side - optimized for reading
class OrderQueryHandler {
  async getOrder(id: string): Promise<OrderView> {
    return this.orderViewRepository.findById(id);
  }

  async getOrderSummary(): Promise<OrderSummaryView[]> {
    // Pre-computed, denormalized data
    return this.orderSummaryViewRepository.findAll();
  }
}
```

## Why Use CQRS?

### 1. **Different Optimization Needs**

Writing requires normalization, validation, and business rules. Reading requires denormalization, aggregation, and speed.

### 2. **Scaling Independently**

Read and write loads are often very different. Scale them separately.

### 3. **Different Data Models**

Commands need rich domain models. Queries need flat, efficient structures.

### 4. **Complex Reporting**

Build specialized read models for complex reports without affecting the write side.

### 5. **Multiple Read Models**

Create different views for different use cases—mobile apps, admin dashboards, analytics.

## CQRS Implementation Patterns

### 1. **Simple CQRS (Same Database)**

Use different classes but same database:

```typescript
// Shared database, different models
class OrderCommand {
  id: string;
  customerId: string;
  items: OrderItem[];
  // Rich domain model with business logic
}

class OrderView {
  id: string;
  customerName: string;
  itemCount: number;
  totalAmount: number;
  status: string;
  // Flat, query-optimized structure
}
```

### 2. **Separate Databases**

Different databases optimized for different purposes:

```typescript
// Write side - normalized relational database
class OrderCommandRepository {
  // PostgreSQL with proper normalization
  async save(order: Order): Promise<void> {}
}

// Read side - document database or read replicas
class OrderViewRepository {
  // MongoDB with denormalized documents
  async findOrderSummaries(): Promise<OrderSummaryView[]> {}
}
```

### 3. **Event-Driven CQRS**

Commands generate events, which update read models:

```typescript
class OrderCommandHandler {
  async handle(command: CreateOrderCommand): Promise<void> {
    const order = new Order(command);
    await this.repository.save(order);

    // Publish event
    await this.eventBus.publish(
      new OrderCreatedEvent({
        orderId: order.id,
        customerId: order.customerId,
        totalAmount: order.totalAmount,
        items: order.items,
      })
    );
  }
}

class OrderViewProjection {
  async on(event: OrderCreatedEvent): Promise<void> {
    // Update read model
    const view = new OrderView({
      id: event.orderId,
      customerName: await this.getCustomerName(event.customerId),
      itemCount: event.items.length,
      totalAmount: event.totalAmount,
    });

    await this.orderViewRepository.save(view);
  }
}
```

## CQRS with Event Sourcing

Often paired together, but they're separate concepts:

**Event Sourcing** stores events instead of current state:

```typescript
// Instead of storing current order state
const order = { id: 1, status: 'shipped', total: 100 };

// Store sequence of events
const events = [
  { type: 'OrderCreated', orderId: 1, customerId: 123 },
  { type: 'ItemAdded', orderId: 1, item: 'laptop' },
  { type: 'OrderShipped', orderId: 1, trackingNumber: 'ABC123' },
];
```

Commands create events, queries rebuild state from events or use projections.

## Benefits of CQRS

### 1. **Performance**

- Optimize reads and writes separately
- Use different databases for different purposes
- Pre-compute complex queries

### 2. **Scalability**

- Scale read and write sides independently
- Use read replicas without affecting writes
- Cache query results aggressively

### 3. **Flexibility**

- Multiple read models for different use cases
- Change query models without affecting business logic
- Add new views without touching commands

### 4. **Security**

- Fine-grained permissions (read vs write)
- Separate sensitive write operations
- Audit trails through events

## Drawbacks and Complexity

### 1. **Eventual Consistency**

Read models might be slightly behind write models:

```typescript
// User creates order
await orderCommandHandler.handle(createOrderCommand);

// Immediately query might not show the order yet
const orders = await orderQueryHandler.getUserOrders(userId);
// Order might not be in the list yet!
```

### 2. **Increased Complexity**

- More moving parts
- Event handling and projections
- Synchronization between models

### 3. **Data Duplication**

- Same data stored multiple times
- Storage overhead
- Consistency challenges

### 4. **Learning Curve**

- Team needs to understand the pattern
- More infrastructure to manage
- Debugging becomes harder

## When to Use CQRS

**Use CQRS when:**

- Read and write workloads are very different
- Complex reporting requirements
- Need to scale reads and writes independently
- Multiple clients with different data needs
- Event-driven architecture already in place

**Don't use CQRS when:**

- Simple CRUD operations are sufficient
- Team lacks experience with distributed systems
- Data consistency is critical
- Small application with simple requirements

## Implementation Tips

### 1. **Start Simple**

Begin with simple CQRS (same database) before moving to separate stores.

### 2. **Handle Eventual Consistency**

```typescript
// Show loading states
const orders = await orderQueryHandler.getUserOrders(userId);
if (orders.isStale) {
  showLoadingIndicator();
}

// Or use push notifications
eventBus.on('OrderCreated', () => {
  refreshOrderList();
});
```

### 3. **Monitor Lag**

Track how far behind read models are from write models.

### 4. **Design for Idempotency**

Events might be processed multiple times:

```typescript
class OrderViewProjection {
  async on(event: OrderCreatedEvent): Promise<void> {
    // Check if already processed
    const existing = await this.orderViewRepository.findById(event.orderId);
    if (existing) return;

    // Process event
    await this.createOrderView(event);
  }
}
```

## CQRS in Practice

Many applications use CQRS without realizing it:

- **Social media feeds** - Complex algorithms for timeline generation, simple writes for posts
- **E-commerce analytics** - Real-time sales tracking with pre-computed dashboards
- **Banking systems** - Transaction processing separate from account balance queries

## Bottom Line

CQRS is powerful but complex. It solves real problems around scalability and flexibility, but introduces operational overhead.

Start with simple CRUD. Move to CQRS when you have clear evidence that read and write requirements are pulling in different directions.

When you do implement CQRS, start simple and evolve. Don't jump straight to event sourcing and separate databases. Build complexity gradually as you prove the value.
