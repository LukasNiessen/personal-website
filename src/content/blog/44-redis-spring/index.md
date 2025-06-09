---
title: 'Redis with Spring Boot: Cache, Pub/Sub, and Beyond'
summary: 'Redis is more than a cache. Learn how to use it effectively with Spring Boot for caching, messaging, and data structures.'
date: 'June 9 2025'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Redis
  - Spring Boot
  - Caching
  - Messaging
  - Architecture
---

# Redis with Spring Boot: Cache, Pub/Sub, and Beyond

Redis is often called a cache, but it's much more. Let's explore its capabilities and how to use it effectively with Spring Boot.

## What is Redis?

Redis is an in-memory data store that supports:

- **Key-Value Storage:** Simple key-value pairs
- **Data Structures:** Lists, sets, sorted sets, hashes
- **Pub/Sub Messaging:** Real-time communication
- **Streams:** Event-driven data pipelines
- **Geospatial Indexing:** Location-based queries

## Why Redis?

1. **Speed:** In-memory operations are lightning-fast.
2. **Versatility:** Supports multiple use cases (cache, queue, etc.).
3. **Simplicity:** Easy to set up and use.
4. **Scalability:** Cluster mode for horizontal scaling.

## Common Use Cases

### 1. Caching

```plaintext
Before:
Database → Application → User

After:
Database → Redis Cache → Application → User
```

### 2. Session Storage

```plaintext
Before:
Session stored in application memory (not scalable).

After:
Session stored in Redis (shared across instances).
```

### 3. Pub/Sub Messaging

```plaintext
Publisher → Redis → Subscriber(s)
```

### 4. Leaderboards

```plaintext
Sorted sets for ranking players or items.
```

## Setting Up Redis with Spring Boot

### Dependencies

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

### Configuration

```yaml
# application.yml
spring:
  redis:
    host: localhost
    port: 6379
    password: yourpassword
```

### Basic Usage

#### Storing and Retrieving Data

```java
@Service
public class RedisService {
    private final StringRedisTemplate redisTemplate;

    public RedisService(StringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    public void save(String key, String value) {
        redisTemplate.opsForValue().set(key, value);
    }

    public String get(String key) {
        return redisTemplate.opsForValue().get(key);
    }
}
```

#### Caching with Annotations

```java
@Service
public class UserService {
    @Cacheable(value = "users", key = "#id")
    public User getUserById(Long id) {
        // Simulate database call
        return userRepository.findById(id).orElseThrow();
    }

    @CacheEvict(value = "users", key = "#id")
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
}
```

### Pub/Sub Messaging

#### Publisher

```java
@Service
public class MessagePublisher {
    private final RedisTemplate<String, String> redisTemplate;

    public MessagePublisher(RedisTemplate<String, String> redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    public void publish(String channel, String message) {
        redisTemplate.convertAndSend(channel, message);
    }
}
```

#### Subscriber

```java
@Component
public class MessageSubscriber {
    @EventListener
    public void handleMessage(String message) {
        System.out.println("Received: " + message);
    }
}

@Configuration
public class RedisConfig {
    @Bean
    public RedisMessageListenerContainer container(
            RedisConnectionFactory connectionFactory,
            MessageListenerAdapter listenerAdapter) {
        RedisMessageListenerContainer container = new RedisMessageListenerContainer();
        container.setConnectionFactory(connectionFactory);
        container.addMessageListener(listenerAdapter, new PatternTopic("my-channel"));
        return container;
    }

    @Bean
    public MessageListenerAdapter listenerAdapter(MessageSubscriber subscriber) {
        return new MessageListenerAdapter(subscriber, "handleMessage");
    }
}
```

## Advanced Features

### 1. Expiring Keys

```java
redisTemplate.opsForValue().set("key", "value", Duration.ofMinutes(10));
```

### 2. Distributed Locks

```java
public boolean acquireLock(String key, String value, long timeout) {
    return redisTemplate.opsForValue().setIfAbsent(key, value, Duration.ofMillis(timeout));
}

public void releaseLock(String key, String value) {
    String currentValue = redisTemplate.opsForValue().get(key);
    if (value.equals(currentValue)) {
        redisTemplate.delete(key);
    }
}
```

### 3. Leaderboards

```java
redisTemplate.opsForZSet().add("leaderboard", "player1", 100);
redisTemplate.opsForZSet().add("leaderboard", "player2", 200);
Set<String> topPlayers = redisTemplate.opsForZSet().reverseRange("leaderboard", 0, 10);
```

## Common Pitfalls

### 1. Overusing Redis

- Don't use Redis as your primary database.
- Avoid storing large binary data.

### 2. Key Management

- Use consistent naming conventions (e.g., `app:module:key`).
- Set TTLs for temporary data.

### 3. Memory Usage

- Monitor memory with `INFO memory`.
- Use eviction policies (`allkeys-lru`, `volatile-lru`, etc.).

## Monitoring and Management

### 1. Redis CLI

```bash
redis-cli
127.0.0.1:6379> INFO
127.0.0.1:6379> KEYS *
```

### 2. Spring Actuator

```yaml
management:
  endpoints:
    web:
      exposure:
        include: redis
```

### 3. Redis Insights

- GUI tool for monitoring Redis instances.

## Bottom Line

1. Use Redis for speed-critical operations (cache, session, pub/sub).
2. Avoid overloading Redis with non-essential data.
3. Monitor memory and key usage regularly.
4. Leverage Spring Boot's integration for simplicity.

Remember: Redis is a powerful tool, but like any tool, it works best when used for the right job.
