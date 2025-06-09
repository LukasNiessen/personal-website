---
title: 'RabbitMQ and Spring Boot: Beyond Hello World'
summary: 'Deep dive into RabbitMQ patterns and Spring Boot integration, with real-world examples and common pitfalls.'
date: 'February 14, 2023'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - RabbitMQ
  - Spring Boot
  - Messaging
  - Integration
  - Architecture
---

# RabbitMQ and Spring Boot: Beyond Hello World

RabbitMQ is more than just queues. Let's explore its patterns and how to implement them in Spring Boot.

## Core Concepts

```plaintext
Exchange Types:
┌─────────────┐
│   Direct    │─► Exact routing key match
├─────────────┤
│   Topic     │─► Pattern matching (#.*.orders)
├─────────────┤
│   Fanout    │─► Broadcast to all queues
├─────────────┤
│   Headers   │─► Header-based routing
└─────────────┘
```

## Basic Setup

```yaml
# application.yml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
```

```java
@Configuration
public class RabbitConfig {
    @Bean
    public Queue ordersQueue() {
        return new Queue("orders", true);
    }

    @Bean
    public TopicExchange orderExchange() {
        return new TopicExchange("order-exchange");
    }

    @Bean
    public Binding orderBinding(Queue ordersQueue,
                              TopicExchange orderExchange) {
        return BindingBuilder.bind(ordersQueue)
                           .to(orderExchange)
                           .with("orders.#");
    }
}
```

## Publishing Messages

```java
@Service
public class OrderService {
    private final RabbitTemplate rabbitTemplate;
    private final ObjectMapper objectMapper;

    public void createOrder(Order order) {
        try {
            // Convert to message
            Message message = MessageBuilder
                .withBody(objectMapper.writeValueAsBytes(order))
                .setContentType(MessageProperties.CONTENT_TYPE_JSON)
                .setHeader("order_id", order.getId())
                .build();

            // Publish with confirmation
            rabbitTemplate.invoke(ops -> {
                ops.send("order-exchange", "orders.created", message);
                // Wait for confirm
                return ops.waitForConfirms(timeout);
            });
        } catch (Exception e) {
            // Handle failure
        }
    }
}
```

## Consuming Messages

### Simple Consumer

```java
@Component
public class OrderConsumer {
    @RabbitListener(queues = "orders")
    public void handleOrder(Order order) {
        // Process order
    }
}
```

### Advanced Consumer

```java
@Component
public class OrderConsumer {
    @RabbitListener(queues = "orders")
    public void handleOrder(Message message,
                          Channel channel,
                          @Header(AmqpHeaders.DELIVERY_TAG) long tag) {
        try {
            // Process message
            Order order = objectMapper.readValue(
                message.getBody(), Order.class);
            processOrder(order);

            // Acknowledge
            channel.basicAck(tag, false);
        } catch (Exception e) {
            // Reject and requeue if temporary failure
            channel.basicNack(tag, false, true);
        }
    }
}
```

## Error Handling

### Dead Letter Exchange

```java
@Configuration
public class RabbitConfig {
    @Bean
    public Queue ordersQueue() {
        return QueueBuilder.durable("orders")
            .withArgument("x-dead-letter-exchange", "dlx")
            .withArgument("x-dead-letter-routing-key", "dead-orders")
            .build();
    }

    @Bean
    public Queue deadLetterQueue() {
        return new Queue("dead-orders");
    }

    @Bean
    public FanoutExchange deadLetterExchange() {
        return new FanoutExchange("dlx");
    }

    @Bean
    public Binding dlqBinding() {
        return BindingBuilder.bind(deadLetterQueue())
                           .to(deadLetterExchange());
    }
}
```

### Retry Policy

```java
@Configuration
public class RabbitConfig {
    @Bean
    public RetryOperationsInterceptor retryInterceptor() {
        return RetryInterceptorBuilder.stateless()
            .maxAttempts(3)
            .backOffOptions(1000, 2.0, 10000)
            .build();
    }

    @Bean
    public SimpleRabbitListenerContainerFactory rabbitListenerContainerFactory(
            ConnectionFactory connectionFactory) {
        SimpleRabbitListenerContainerFactory factory =
            new SimpleRabbitListenerContainerFactory();
        factory.setConnectionFactory(connectionFactory);
        factory.setAdviceChain(retryInterceptor());
        return factory;
    }
}
```

## Common Patterns

### 1. Request-Reply

```java
// Publisher
@Service
public class PaymentService {
    private final RabbitTemplate rabbitTemplate;

    public PaymentResult processPayment(Payment payment) {
        return (PaymentResult) rabbitTemplate.convertSendAndReceive(
            "payment-exchange",
            "process.payment",
            payment
        );
    }
}

// Consumer
@Component
public class PaymentProcessor {
    @RabbitListener(queues = "payment-requests")
    public PaymentResult processPayment(Payment payment) {
        // Process payment
        return new PaymentResult(/*...*/);
    }
}
```

### 2. Publish-Subscribe

```java
// Publisher
@Service
public class OrderService {
    private final RabbitTemplate rabbitTemplate;

    public void createOrder(Order order) {
        rabbitTemplate.convertAndSend(
            "order-exchange",
            "orders.created",
            order
        );
    }
}

// Multiple Consumers
@Component
public class InventoryConsumer {
    @RabbitListener(queues = "inventory-orders")
    public void updateInventory(Order order) {
        // Update inventory
    }
}

@Component
public class NotificationConsumer {
    @RabbitListener(queues = "notification-orders")
    public void sendNotification(Order order) {
        // Send notification
    }
}
```

### 3. Work Queues (Competing Consumers)

```java
@Configuration
public class WorkQueueConfig {
    @Bean
    public Queue workQueue() {
        return new Queue("work-queue");
    }
}

// Multiple instances will share work
@Component
public class Worker {
    @RabbitListener(queues = "work-queue",
                   concurrency = "3-5")
    public void processWork(Task task) {
        // Process task
    }
}
```

## Performance Tuning

### 1. Batch Operations

```java
@Configuration
public class RabbitConfig {
    @Bean
    public SimpleRabbitListenerContainerFactory batchFactory() {
        SimpleRabbitListenerContainerFactory factory =
            new SimpleRabbitListenerContainerFactory();
        factory.setBatchSize(100);
        factory.setBatchListener(true);
        return factory;
    }
}

@Component
public class BatchConsumer {
    @RabbitListener(queues = "orders",
                   containerFactory = "batchFactory")
    public void handleBatch(List<Message> messages) {
        // Process batch
    }
}
```

### 2. Connection Pool

```yaml
spring:
  rabbitmq:
    listener:
      simple:
        concurrency: 5
        max-concurrency: 10
    cache:
      channel:
        size: 25
```

### 3. Publisher Confirms

```java
@Configuration
public class RabbitConfig {
    @Bean
    public RabbitTemplate rabbitTemplate(
            ConnectionFactory connectionFactory) {
        RabbitTemplate template = new RabbitTemplate(connectionFactory);
        template.setConfirmCallback((correlation, ack, reason) -> {
            if (!ack) {
                // Handle nack
            }
        });
        return template;
    }
}
```

## Monitoring and Management

```java
@Configuration
public class MonitoringConfig {
    @Bean
    public Queue deadLetterQueue() {
        return QueueBuilder.durable("dead-orders")
            .withArgument("x-queue-mode", "lazy")
            .withArgument("x-max-length", 10000)
            .withArgument("x-message-ttl", 604800000) // 1 week
            .build();
    }
}
```

## Bottom Line

1. Use appropriate exchange types
2. Implement proper error handling
3. Consider message persistence needs
4. Monitor queue depths and consumer health
5. Use dead letter queues for failed messages

Remember:

- Messages should be small and focused
- Don't use RabbitMQ for file transfer
- Always handle consumer errors
- Monitor queue depths and consumer lag
- Consider message TTL and queue limits
