---
title: 'The Distributed Monolith: When Microservices Go Wrong'
summary: 'How to identify and avoid the distributed monolith anti-pattern: all the complexity of microservices with none of the benefits.'
date: 'July 22, 2022'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Architecture
  - Microservices
  - Anti-patterns
  - System Design
---

# The Distributed Monolith: When Microservices Go Wrong

You've split your monolith into services, but deployments still require everything to be released together. Congratulations, you've built a distributed monolith!

## What is a Distributed Monolith?

A distributed monolith looks like microservices but behaves like a monolith:

```plaintext
Appears as:          But behaves as:
┌───┐ ┌───┐ ┌───┐    ┌───────────┐
│ A │ │ B │ │ C │    │ A   B   C │
└─┬─┘ └─┬─┘ └─┬─┘    │           │
  │     │     │      │ Must      │
  └─────┴─────┘      │ Deploy    │
  Independent?       │ Together  │
                     └───────────┘
```

## Warning Signs

### 1. Shared Database Tables

```java
// Service A
@Entity
@Table(name = "users")
public class User {
    @Id
    private Long id;
    private String name;
}

// Service B
@Entity
@Table(name = "users") // Same table!
public class User {
    @Id
    private Long id;
    private String email;
}
```

### 2. Tight Runtime Coupling

```java
// Service A
@Service
public class OrderService {
    @Autowired
    private PaymentClient paymentClient;
    @Autowired
    private InventoryClient inventoryClient;

    public void createOrder() {
        // Fails if either service is down
        paymentClient.process();
        inventoryClient.reserve();
    }
}
```

### 3. Shared Libraries with Business Logic

```java
// shared-lib project
public class OrderProcessor {
    // Business logic that should be service-specific
    public static Order validateAndProcess(Order order) {
        // Changes here require all services to redeploy
    }
}

// Multiple services
@Service
public class OrderService {
    public void process(Order order) {
        // Every service uses same business logic
        Order processed = OrderProcessor.validateAndProcess(order);
    }
}
```

### 4. Synchronized Deployments

```yaml
# deployment.yaml
kind: Deployment
metadata:
  name: service-a
spec:
  # Must match versions with other services
  template:
    spec:
      containers:
        - name: app
          image: service-a:1.2.3 # Must match B's version
```

## How Did We Get Here?

### 1. Database-First Design

```java
// DON'T: Share tables across services
@Query("SELECT o FROM Order o JOIN User u WHERE u.status = ?1")
List<Order> findByUserStatus(String status);

// DO: Use service-specific queries
@Query("SELECT o FROM Order o WHERE o.userId IN " +
       "(SELECT id FROM UserStatus WHERE status = ?1)")
List<Order> findByUserStatus(String status);
```

### 2. Excessive Service Communication

```java
// DON'T: Chatty services
@Service
public class OrderProcessor {
    public OrderResult process(Order order) {
        // 5 network calls to complete one operation
        UserDetails user = userService.getUser(order.getUserId());
        Product product = catalogService.getProduct(order.getProductId());
        PaymentResult payment = paymentService.process(order.getPaymentDetails());
        InventoryResult stock = inventoryService.check(order.getProductId());
        return shippingService.schedule(order);
    }
}

// DO: Use event-driven patterns
@Service
public class OrderProcessor {
    public void process(Order order) {
        // Fire event, let other services react
        eventBus.publish(new OrderCreatedEvent(order));
    }
}
```

### 3. Shared Code Instead of Shared Contracts

```java
// DON'T: Share implementation
@Component
public class SharedValidator {
    public static boolean isValid(Order order) {
        // All services must use this exact implementation
        return order.getAmount() > 0 && order.getItems().size() > 0;
    }
}

// DO: Share contracts
public interface OrderValidator {
    boolean isValid(Order order);
}

// Each service implements its own validation
@Component
public class ServiceAValidator implements OrderValidator {
    public boolean isValid(Order order) {
        // Service-specific validation
        return order.getAmount() > 0;
    }
}
```

## Breaking Free

### 1. Identify Service Boundaries

```plaintext
Bad Boundaries:           Good Boundaries:
┌─────┐                  ┌─────────────┐
│Users│◄─────┐          │   Orders    │
└─────┘      │          │ ┌─────────┐ │
┌─────┐      │          │ │Orders DB│ │
│Bills│◄─────┤          │ └─────────┘ │
└─────┘      │          └─────────────┘
┌─────┐      │          ┌─────────────┐
│Items│◄─────┤          │   Users     │
└─────┘      │          │ ┌─────────┐ │
    ▲        │          │ │Users DB │ │
    └────────┘          │ └─────────┘ │
                        └─────────────┘
```

### 2. Replace Shared Tables with APIs

```java
// Before: Direct database access
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    User findByEmail(String email);
}

// After: API calls
@FeignClient("user-service")
public interface UserClient {
    @GetMapping("/api/users/email/{email}")
    UserDTO findByEmail(@PathVariable String email);
}
```

### 3. Implement Eventual Consistency

```java
// Instead of immediate consistency:
@Transactional
public void updateOrder(Order order) {
    orderRepo.save(order);
    userService.updateOrderCount(order.getUserId());
    inventoryService.updateStock(order.getProductId());
}

// Use event-driven updates:
@TransactionalEventListener
public void onOrderCreated(OrderCreatedEvent event) {
    kafkaTemplate.send("order-events", event);
}

@KafkaListener(topics = "order-events")
public void handleOrderEvent(OrderCreatedEvent event) {
    // Each service handles updates independently
}
```

### 4. Independent Deployment Pipeline

```yaml
# Before: One pipeline for all
stages:
  - build-all
  - test-all
  - deploy-all

# After: Service-specific pipelines
# service-a-pipeline.yml
stages:
  - build
  - test
  - deploy

# service-b-pipeline.yml (independent)
stages:
  - build
  - test
  - deploy
```

## Escape Plan

1. **Identify Coupling Points:**

```java
// Look for:
@Autowired
private OtherServiceClient client; // Direct coupling

@Table(name = "shared_table") // Data coupling

implementation 'com:shared-lib:1.2.3' // Library coupling
```

2. **Create Service-Specific Storage:**

```java
// Before migration:
@DataJpaTest
class MigrationTest {
    @Test
    void migrateData() {
        // Copy relevant data to service-specific storage
        List<User> users = legacyRepo.findAll();
        users.forEach(u ->
            newRepo.save(new UserEntity(u.getId(), u.getName())));
    }
}
```

3. **Replace Sync with Async:**

```java
// Instead of:
orderService.create()
           .then(paymentService.process())
           .then(shipmentService.schedule());

// Use:
orderService.create();
// Other services react to OrderCreatedEvent
```

## Bottom Line

1. If you can't deploy services independently, you have a distributed monolith
2. If changing one service requires changing others, you have a distributed monolith
3. If services share databases, you probably have a distributed monolith

Better to have a clean monolith than a distributed monolith. If you're going micro:

- Define clear service boundaries
- Maintain separate databases
- Use contracts, not shared code
- Embrace eventual consistency
- Enable independent deployment
