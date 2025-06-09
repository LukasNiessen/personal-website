---
title: 'Kafka with Spring Boot: From Basics to Production'
summary: 'Understanding Apache Kafka through Spring Boot, with real-world patterns and production considerations.'
date: 'May 30, 2023'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Kafka
  - Spring Boot
  - Messaging
  - Streaming
  - Architecture
---

# Kafka with Spring Boot: From Basics to Production

Kafka isn't just a message queue—it's a distributed streaming platform. Let's see how to use it effectively with Spring Boot.

## Core Concepts

```plaintext
Key Components:
┌─────────────┐
│   Topic     │─► Stream of records
├─────────────┤
│  Partition  │─► Ordered sequence
├─────────────┤
│   Offset    │─► Position in partition
├─────────────┤
│ Consumer    │─► Reads records
│   Group     │
└─────────────┘
```

## Basic Setup

```yaml
# application.yml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    consumer:
      group-id: my-group
      auto-offset-reset: earliest
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
```

```java
@Configuration
public class KafkaConfig {
    @Bean
    public NewTopic ordersTopic() {
        return TopicBuilder.name("orders")
                         .partitions(3)
                         .replicas(2)
                         .build();
    }

    @Bean
    public ProducerFactory<String, Order> producerFactory() {
        Map<String, Object> config = new HashMap<>();
        config.put(ProducerConfig.ACKS_CONFIG, "all");
        config.put(ProducerConfig.RETRIES_CONFIG, 3);
        // More configs...

        return new DefaultKafkaProducerFactory<>(config);
    }
}
```

## Publishing Messages

### Simple Producer

```java
@Service
public class OrderService {
    private final KafkaTemplate<String, Order> kafkaTemplate;

    public void createOrder(Order order) {
        kafkaTemplate.send("orders", order.getId(), order);
    }
}
```

### Advanced Producer

```java
@Service
public class OrderService {
    private final KafkaTemplate<String, Order> kafkaTemplate;

    public void createOrder(Order order) {
        ProducerRecord<String, Order> record = new ProducerRecord<>(
            "orders",
            null, // Partition (null = let Kafka decide)
            order.getId(), // Key
            order, // Value
            RecordHeaders() // Custom headers
        );

        ListenableFuture<SendResult<String, Order>> future =
            kafkaTemplate.send(record);

        future.addCallback(new ListenableFutureCallback<>() {
            @Override
            public void onSuccess(SendResult<String, Order> result) {
                log.info("Sent order {} to partition {} at offset {}",
                    order.getId(),
                    result.getRecordMetadata().partition(),
                    result.getRecordMetadata().offset());
            }

            @Override
            public void onFailure(Throwable ex) {
                log.error("Failed to send order {}", order.getId(), ex);
            }
        });
    }
}
```

## Consuming Messages

### Simple Consumer

```java
@Component
public class OrderConsumer {
    @KafkaListener(topics = "orders")
    public void handleOrder(Order order) {
        // Process order
    }
}
```

### Advanced Consumer

```java
@Component
public class OrderConsumer {
    @KafkaListener(
        topics = "orders",
        containerFactory = "orderKafkaListenerContainerFactory"
    )
    public void handleOrder(
            ConsumerRecord<String, Order> record,
            Acknowledgment ack) {
        try {
            String key = record.key();
            Order order = record.value();
            Headers headers = record.headers();

            processOrder(order);

            // Manual commit
            ack.acknowledge();
        } catch (Exception e) {
            // Handle error
            // Don't ack - message will be redelivered
        }
    }
}

@Configuration
public class KafkaConsumerConfig {
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Order>
            orderKafkaListenerContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, Order> factory =
            new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        factory.getContainerProperties().setAckMode(AckMode.MANUAL);
        return factory;
    }
}
```

## Error Handling

### Dead Letter Topic

```java
@Configuration
public class KafkaConfig {
    @Bean
    public DeadLetterPublishingRecoverer recoverer(
            KafkaTemplate<String, Order> template) {
        return new DeadLetterPublishingRecoverer(template,
            (record, ex) -> new TopicPartition("orders.DLT",
                                             record.partition()));
    }

    @Bean
    public ConsumerRecordRecoverer recoverer() {
        return new DeadLetterPublishingRecoverer(template);
    }

    @Bean
    public DefaultErrorHandler errorHandler(DeadLetterPublishingRecoverer recoverer) {
        return new DefaultErrorHandler(
            recoverer,
            new FixedBackOff(1000L, 2) // Retry twice with 1s delay
        );
    }
}
```

### Retry Policy

```java
@Configuration
public class KafkaConfig {
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Order>
            retryContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, Order> factory =
            new ConcurrentKafkaListenerContainerFactory<>();

        factory.setRetryTemplate(new RetryTemplate() {{
            setRetryPolicy(new SimpleRetryPolicy(3));
            setBackOffPolicy(new ExponentialBackOffPolicy() {{
                setInitialInterval(1000L);
                setMultiplier(2.0);
                setMaxInterval(10000L);
            }});
        }});

        return factory;
    }
}
```

## Common Patterns

### 1. Transactional Messages

```java
@Configuration
public class KafkaConfig {
    @Bean
    public ProducerFactory<String, Order> producerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "tx-");
        return new DefaultKafkaProducerFactory<>(props);
    }
}

@Service
public class OrderService {
    @Transactional
    public void createOrder(Order order) {
        // DB transaction
        orderRepository.save(order);

        // Kafka transaction
        kafkaTemplate.executeInTransaction(t ->
            t.send("orders", order.getId(), order));
    }
}
```

### 2. Streaming Operations

```java
@Configuration
public class KafkaStreamsConfig {
    @Bean
    public KStream<String, Order> processOrders(
            StreamsBuilder streamsBuilder) {
        KStream<String, Order> orders =
            streamsBuilder.stream("orders");

        // Process stream
        orders.filter((key, order) -> order.getAmount() > 1000)
              .mapValues(order -> enrichOrder(order))
              .to("large-orders");

        return orders;
    }
}
```

### 3. Consumer Groups

```java
// Multiple consumers in same group
@Component
public class OrderConsumer {
    @KafkaListener(
        topics = "orders",
        groupId = "order-processors",
        concurrency = "3"
    )
    public void processOrder(Order order) {
        // Process order
    }
}
```

## Performance Tuning

### 1. Batch Processing

```java
@Configuration
public class KafkaConfig {
    @Bean
    public ConsumerFactory<String, Order> consumerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 500);
        props.put(ConsumerConfig.FETCH_MIN_BYTES_CONFIG, 1024 * 1024);
        return new DefaultKafkaConsumerFactory<>(props);
    }
}

@Component
public class BatchOrderConsumer {
    @KafkaListener(topics = "orders")
    public void processBatch(List<Order> orders) {
        // Process batch of orders
    }
}
```

### 2. Producer Tuning

```yaml
spring:
  kafka:
    producer:
      batch-size: 16384
      buffer-memory: 33554432
      compression-type: lz4
      acks: all
```

### 3. Consumer Tuning

```yaml
spring:
  kafka:
    consumer:
      fetch-min-size: 1
      fetch-max-wait: 500
      max-poll-records: 500
      auto-commit-interval: 1000
```

## Monitoring and Management

```java
@Configuration
public class MonitoringConfig {
    @Bean
    public KafkaListenerEndpointRegistry endpointRegistry() {
        return new KafkaListenerEndpointRegistry();
    }

    @Bean
    public MeterBinder kafkaConsumerMetrics(
            KafkaListenerEndpointRegistry registry) {
        return new KafkaConsumerMetrics(registry);
    }
}
```

## Bottom Line

1. Use appropriate partitioning strategy
2. Implement proper error handling
3. Consider message ordering requirements
4. Monitor consumer lag
5. Use dead letter topics for failed messages

Remember:

- Keys determine partition assignment
- Order is only guaranteed within a partition
- Watch out for consumer lag
- Monitor disk usage and network throughput
- Consider message retention policy
