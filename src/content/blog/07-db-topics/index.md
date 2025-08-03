---
title: "ELI5: OLAP vs OLTP, Batch vs Streaming, and SQL to MongoDB Migration"
summary: "A super simple explanation of data processing patterns with real MongoDB examples from a Solution Architect perspective"
date: "August 03 2023"
draft: false
tags:
  - OLAP
  - OLTP
  - Batch Processing
  - Streaming
  - MongoDB Migration
---

# ELI5: OLAP vs OLTP, Batch vs Streaming, and SQL to MongoDB Migration

This is a super simple ELI5 explanation of data processing patterns. I'll explain OLAP vs OLTP, batch vs streaming processing, and then dive into SQL to MongoDB migration strategies from a MongoDB Solution Architect perspective.

## Super Simple Explanation

- **OLTP** = Online Transaction Processing = Your daily app operations

- **OLAP** = Online Analytical Processing = Your business intelligence and reports

- **Batch Processing** = Process data in chunks, like doing laundry once a week

- **Streaming Processing** = Process data as it comes, like washing dishes right after eating

## OLTP vs OLAP: The Restaurant Analogy

Think of a restaurant:

### OLTP (Taking Orders)
```
Customer: "I want a burger"
Waiter: Updates order system immediately
Kitchen: Gets order right away
Payment: Processed instantly
```

**Characteristics:**
- Fast, simple operations
- Many small transactions
- Current data matters
- High concurrency (many customers at once)

### OLAP (Restaurant Analytics)
```
Manager: "How many burgers did we sell last month?"
System: Analyzes thousands of historical orders
Result: "2,847 burgers, peak on Fridays"
```

**Characteristics:**
- Complex queries across lots of data
- Historical analysis
- Fewer users, but heavy computations
- Response time in minutes/hours is okay

## MongoDB Examples: OLTP vs OLAP

### OLTP with MongoDB
```javascript
// E-commerce order processing (OLTP)
db.orders.insertOne({
  customerId: "user123",
  items: [
    { productId: "laptop001", quantity: 1, price: 999 }
  ],
  status: "pending",
  timestamp: new Date()
});

// Update inventory immediately (OLTP)
db.inventory.updateOne(
  { productId: "laptop001" },
  { $inc: { quantity: -1 } }
);
```

**Why MongoDB is great for OLTP:**
- Document model matches application objects
- Built-in sharding for horizontal scaling
- Replica sets for high availability
- Flexible schema for evolving requirements

### OLAP with MongoDB
```javascript
// Monthly sales analysis (OLAP)
db.orders.aggregate([
  {
    $match: {
      timestamp: {
        $gte: new Date("2025-07-01"),
        $lt: new Date("2025-08-01")
      }
    }
  },
  {
    $group: {
      _id: "$customerId",
      totalSpent: { $sum: "$total" },
      orderCount: { $sum: 1 }
    }
  },
  {
    $sort: { totalSpent: -1 }
  }
]);
```

**MongoDB OLAP Tools:**
- **MongoDB Atlas Data Lake**: Query data across MongoDB and cloud storage
- **Aggregation Pipeline**: Complex analytics within MongoDB
- **Atlas Charts**: Built-in visualization
- **Connector for BI**: Connect to Tableau, Power BI

## Batch vs Streaming Processing

### Batch Processing: The Laundry Approach
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Collect    │───►│   Process    │───►│   Output    │
│  All Day    │    │  Every Hour  │    │   Results   │
└─────────────┘    └──────────────┘    └─────────────┘
```

**Example:** Processing daily sales reports at midnight

### Streaming Processing: The Real-Time Approach
```
Data ───► Process ───► Output ───► Process ───► Output ───►
 ▲           ▲          ▲           ▲          ▲
 │           │          │           │          │
Now        Now        Now         Now        Now
```

**Example:** Fraud detection on credit card transactions

## MongoDB Streaming Examples

### MongoDB Change Streams (Real-time)
```javascript
// Watch for new orders in real-time
const changeStream = db.orders.watch([
  { $match: { "fullDocument.status": "completed" } }
]);

changeStream.on('change', (change) => {
  console.log('New completed order:', change.fullDocument);
  
  // Trigger real-time actions:
  // - Send confirmation email
  // - Update real-time dashboard
  // - Trigger inventory reorder if needed
});
```

### Batch Processing with MongoDB
```javascript
// Daily batch job: Calculate customer lifetime value
db.orders.aggregate([
  {
    $match: {
      timestamp: {
        $gte: new Date(Date.now() - 24 * 60 * 60 * 1000) // Last 24 hours
      }
    }
  },
  {
    $group: {
      _id: "$customerId",
      dailyTotal: { $sum: "$total" }
    }
  },
  {
    $merge: {
      into: "customer_daily_stats",
      whenMatched: "merge",
      whenNotMatched: "insert"
    }
  }
]);
```

## SQL to MongoDB Migration: Solution Architect Perspective

As a MongoDB Solution Architect, I've seen this pattern many times. Here's the realistic approach:

### Common Migration Scenarios

**Scenario 1: E-commerce Platform**
```sql
-- Old SQL schema
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT,
  order_date DATE
);

CREATE TABLE order_items (
  id INT PRIMARY KEY,
  order_id INT,
  product_id INT,
  quantity INT
);
```

```javascript
// New MongoDB schema
{
  _id: ObjectId("..."),
  customerId: "user123",
  orderDate: ISODate("2025-08-03"),
  items: [
    {
      productId: "laptop001",
      name: "Gaming Laptop",
      quantity: 1,
      price: 999
    }
  ],
  shipping: {
    address: "123 Main St",
    city: "New York",
    zipCode: "10001"
  },
  status: "shipped"
}
```

### Migration Strategy: The Strangler Fig Pattern

Don't do a big-bang migration. Use the strangler fig approach:

```
Phase 1: Dual Write
┌─────────────┐    ┌─────────────┐
│     App     │───►│  SQL (Read) │
│             │    └─────────────┘
│             │    ┌─────────────┐
│             │───►│MongoDB(Write│
└─────────────┘    └─────────────┘

Phase 2: Dual Read/Write
┌─────────────┐    ┌─────────────┐
│     App     │◄──►│     SQL     │
│             │    └─────────────┘
│             │    ┌─────────────┐
│             │◄──►│  MongoDB    │
└─────────────┘    └─────────────┘

Phase 3: MongoDB Only
┌─────────────┐    ┌─────────────┐
│     App     │◄──►│  MongoDB    │
└─────────────┘    └─────────────┘
```

### Real Migration Example: User Management System

**Step 1: Schema Design**
```javascript
// Instead of multiple SQL tables, use embedded documents
{
  _id: ObjectId("..."),
  username: "john_doe",
  email: "john@example.com",
  profile: {
    firstName: "John",
    lastName: "Doe",
    preferences: {
      language: "en",
      notifications: {
        email: true,
        sms: false
      }
    }
  },
  addresses: [
    {
      type: "home",
      street: "123 Main St",
      city: "New York",
      zipCode: "10001",
      isDefault: true
    }
  ],
  loginHistory: [
    {
      timestamp: ISODate("2025-08-03T10:30:00Z"),
      ip: "192.168.1.1",
      device: "iPhone"
    }
  ]
}
```

**Step 2: Migration Code**
```javascript
// MongoDB migration script
async function migrateUsers() {
  const sqlUsers = await mysql.query('SELECT * FROM users');
  
  for (const user of sqlUsers) {
    // Get related data
    const profile = await mysql.query('SELECT * FROM user_profiles WHERE user_id = ?', [user.id]);
    const addresses = await mysql.query('SELECT * FROM user_addresses WHERE user_id = ?', [user.id]);
    
    // Transform to MongoDB document
    const mongoDoc = {
      username: user.username,
      email: user.email,
      profile: {
        firstName: profile[0]?.first_name,
        lastName: profile[0]?.last_name,
        // ... other fields
      },
      addresses: addresses.map(addr => ({
        type: addr.address_type,
        street: addr.street,
        city: addr.city,
        zipCode: addr.zip_code,
        isDefault: addr.is_default
      })),
      createdAt: user.created_at,
      lastLogin: user.last_login
    };
    
    await db.users.insertOne(mongoDoc);
  }
}
```

### Key Migration Considerations

**1. Data Modeling Mindset Shift**
- SQL: Normalize everything, join at query time
- MongoDB: Embed related data, optimize for read patterns

**2. Transaction Handling**
```javascript
// MongoDB multi-document transactions (when needed)
const session = client.startSession();

try {
  await session.withTransaction(async () => {
    await db.orders.insertOne(orderDoc, { session });
    await db.inventory.updateOne(
      { productId: "laptop001" },
      { $inc: { quantity: -1 } },
      { session }
    );
  });
} finally {
  await session.endSession();
}
```

**3. Indexing Strategy**
```javascript
// Create indexes for common query patterns
db.orders.createIndex({ customerId: 1, orderDate: -1 });
db.products.createIndex({ category: 1, price: 1 });
db.users.createIndex({ "profile.email": 1 }, { unique: true });

// Text search index
db.products.createIndex({ 
  name: "text", 
  description: "text" 
});
```

## When to Choose What?

### Use OLTP + MongoDB when:
- Building modern applications (web, mobile)
- Need flexible schema evolution
- Handling semi-structured data (JSON, logs)
- Require horizontal scaling

### Use OLAP + MongoDB when:
- Need real-time analytics on operational data
- Want to avoid ETL complexity
- MongoDB Atlas Data Lake for cross-platform analytics

### Use Batch Processing when:
- Large data volumes
- Complex computations
- Cost optimization (run during off-peak hours)
- Historical reporting

### Use Streaming when:
- Real-time fraud detection
- Live dashboards
- Immediate alerts
- User experience optimization