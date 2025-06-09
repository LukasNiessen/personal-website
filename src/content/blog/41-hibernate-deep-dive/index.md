---
title: 'Hibernate Deep Dive: Beyond the Basics'
summary: 'Understanding Hibernate performance, patterns, and pitfalls. Real examples of common issues and how to solve them.'
date: 'November 8, 2022'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Java
  - Hibernate
  - Performance
  - JPA
  - Database
---

# Hibernate Deep Dive: Beyond the Basics

Hibernate makes database access easy—sometimes too easy. Let's look at how it really works and common pitfalls to avoid.

## The N+1 Problem

The most common performance killer:

```java
// The code looks innocent:
@Entity
public class Order {
    @OneToMany(fetch = FetchType.LAZY)
    private List<OrderItem> items;
}

// The usage seems fine:
List<Order> orders = orderRepository.findAll();
for (Order order : orders) {
    // But this triggers N additional queries!
    order.getItems().forEach(item ->
        System.out.println(item.getName()));
}
```

### Solution 1: Join Fetch

```java
@Query("SELECT o FROM Order o " +
       "LEFT JOIN FETCH o.items " +
       "WHERE o.status = :status")
List<Order> findByStatusWithItems(String status);
```

### Solution 2: EntityGraph

```java
@EntityGraph(attributePaths = {"items"})
@Query("SELECT o FROM Order o WHERE o.status = :status")
List<Order> findByStatus(String status);
```

## Lazy vs Eager Loading

```java
// DON'T: Default to EAGER
@Entity
public class Order {
    @ManyToOne(fetch = FetchType.EAGER) // Always loads
    private Customer customer;

    @OneToMany(fetch = FetchType.EAGER) // Always loads
    private List<OrderItem> items;
}

// DO: Use LAZY with specific fetching
@Entity
public class Order {
    @ManyToOne(fetch = FetchType.LAZY)
    private Customer customer;

    @OneToMany(fetch = FetchType.LAZY)
    private List<OrderItem> items;
}
```

## First-Level Cache (Session Cache)

```java
// Same transaction = same object
@Transactional
public void updateOrder(Long id) {
    Order order1 = orderRepo.findById(id).get();
    Order order2 = orderRepo.findById(id).get(); // No DB hit

    assert order1 == order2; // True, same instance
}

// Different transactions = different objects
@Transactional
public void method1(Long id) {
    Order order1 = orderRepo.findById(id).get();
}

@Transactional
public void method2(Long id) {
    Order order2 = orderRepo.findById(id).get(); // DB hit
}
```

## Second-Level Cache

```java
// Entity configuration
@Entity
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class Product {
    @Id
    private Long id;

    private String name;

    @Cache(usage = CacheConcurrencyStrategy.READ_ONLY)
    @OneToMany(mappedBy = "product")
    private List<Review> reviews;
}

// Application properties
spring.jpa.properties.hibernate.cache.use_second_level_cache=true
spring.jpa.properties.hibernate.cache.region.factory_class=org.hibernate.cache.ehcache.EhCacheRegionFactory
```

## Dirty Checking

```java
@Transactional
public void updatePrice(Long productId, BigDecimal newPrice) {
    Product product = productRepo.findById(productId).get();
    product.setPrice(newPrice);
    // No explicit save needed - Hibernate tracks changes
}
```

### Performance Impact

```java
// DON'T: Load unnecessary data
@Entity
public class Product {
    @Column(length = 10000)
    private String description;

    private BigDecimal price;
}

@Transactional
public void updatePrice(Long id, BigDecimal price) {
    // Loads everything, including large description
    Product product = productRepo.findById(id).get();
    product.setPrice(price);
}

// DO: Load only what you need
@Query("SELECT new com.example.ProductPrice(p.id, p.price) " +
       "FROM Product p WHERE p.id = :id")
ProductPrice findPriceById(Long id);
```

## Batch Operations

### Inserts

```java
// Configuration
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true

// Usage
@Transactional
public void saveOrders(List<Order> orders) {
    for (int i = 0; i < orders.size(); i++) {
        entityManager.persist(orders.get(i));

        if (i % 50 == 0) {
            entityManager.flush();
            entityManager.clear();
        }
    }
}
```

### Updates

```java
@Modifying
@Query("UPDATE Product p SET p.price = p.price * :multiplier " +
       "WHERE p.category = :category")
int updatePricesInBulk(BigDecimal multiplier, String category);
```

## Common Pitfalls

### 1. Detached Entities

```java
// DON'T: Use detached entities
public void updateOrder(Order order) {
    // order is detached
    orderRepo.save(order); // Causes full entity update
}

// DO: Load and update
@Transactional
public void updateOrder(Order updates) {
    Order order = orderRepo.findById(updates.getId()).get();
    order.updateFrom(updates); // Updates only changed fields
}
```

### 2. Open Session in View

```yaml
# application.properties

# DON'T: Enable OSIV
spring.jpa.open-in-view=true # Default

# DO: Disable OSIV
spring.jpa.open-in-view=false
```

```java
// Instead, use DTOs or fetch joins
@GetMapping("/orders/{id}")
public OrderDTO getOrder(@PathVariable Long id) {
    return orderRepo.findOrderWithDetails(id);
}

@Query("SELECT new com.example.OrderDTO(o, c, i) " +
       "FROM Order o " +
       "JOIN FETCH o.customer c " +
       "JOIN FETCH o.items i " +
       "WHERE o.id = :id")
OrderDTO findOrderWithDetails(Long id);
```

### 3. Unintended Collection Loading

```java
// DON'T: Access collections in loops
@Transactional(readOnly = true)
public void processOrders(List<Order> orders) {
    for (Order order : orders) {
        // Loads collection for each order!
        order.getItems().size();
    }
}

// DO: Use join fetch or size queries
@Query("SELECT o FROM Order o " +
       "LEFT JOIN FETCH o.items " +
       "WHERE o.status = :status")
List<Order> findWithItems(String status);
```

## Performance Optimization

### 1. Query Plan Caching

```yaml
# application.properties
spring.jpa.properties.hibernate.query.plan_cache_max_size=2048
spring.jpa.properties.hibernate.query.plan_parameter_metadata_max_size=128
```

### 2. Connection Pool Tuning

```yaml
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.idle-timeout=300000
```

### 3. Statement Batching

```yaml
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true
spring.jpa.properties.hibernate.order_updates=true
spring.jpa.properties.hibernate.batch_versioned_data=true
```

## Bottom Line

1. Always use LAZY loading by default
2. Fetch exactly what you need
3. Use batch operations for bulk changes
4. Be aware of session state
5. Monitor and tune based on real usage

Remember:

- DTO projections > Entity projections
- Specific queries > Generic queries
- Batch operations > Individual operations
- Understanding > Magic
