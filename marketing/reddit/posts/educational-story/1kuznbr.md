```json
{
  "id": "1kuznbr",
  "author": "trolleid",
  "category": "educational-story",
  "subreddit": "softwarearchitecture",
  "created_utc": 1748169909.0,
  "created_at": "2025-05-25T12:45:09+02:00",
  "permalink": "https://www.reddit.com/r/softwarearchitecture/comments/1kuznbr/eli5_how_does_consistent_hashing_work/",
  "link_url": "https://www.reddit.com/r/softwarearchitecture/comments/1kuznbr/eli5_how_does_consistent_hashing_work/",
  "is_self": true,
  "crosspost_parent": null,
  "removed_by_category": "reddit",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "93d31ce28251c8b0f828c3a334e28517a83ec2c7ae4f3504fadc434d9329d11e",
  "body_sha256": "26161a0febab3af131d32637c612785b4e831a53897e0c795de01caf7fd3663f",
  "body_characters": 15299
}
```

# Original title

ELI5: How does Consistent Hashing work?

## Original body

This contains an ELI5 and a deeper explanation of consistent hashing. I have added much ASCII art, hehe :) At the end, I even added a simplified example code of how you could implement consistent hashing.

# ELI5: Consistent Pizza Hashing 🍕

Suppose you're at a pizza party with friends. Now you need to decide who gets which pizza slices.

### The Bad Way (Simple Hash)

- You have 3 friends: Alice, Bob, and Charlie
- For each pizza slice, you count: "1-Alice, 2-Bob, 3-Charlie, 1-Alice, 2-Bob..."
- Slice #7 → 7 ÷ 3 = remainder 1 → Alice gets it
- Slice #8 → 8 ÷ 3 = remainder 2 → Bob gets it

```
With 3 friends:
Slice 7 → Alice
Slice 8 → Bob
Slice 9 → Charlie
```

**The Problem:** Your friend Dave shows up. Now you have 4 friends. So we need to do the distribution again.

- Slice #7 → 7 ÷ 4 = remainder 3 → Dave gets it (was Alice's!)
- Slice #8 → 8 ÷ 4 = remainder 0 → Alice gets it (was Bob's!)

```
With 4 friends:
Slice 7 → Dave (moved from Alice!)
Slice 8 → Alice (moved from Bob!)
Slice 9 → Bob (moved from Charlie!)
```

Almost EVERYONE'S pizza has moved around...! 😫

### The Good Way (Consistent Hashing)

- Draw a big circle and put your friends around it
- Each pizza slice gets a number that points to a spot on the circle
- Walk clockwise from that spot until you find a friend - he gets the slice.

```
           Alice
      🍕7       .
      .            .
     .               .
   Dave      ○       Bob
     .              🍕8
      .             .
       .           .
          Charlie

🍕7 walks clockwise and hits Alice
🍕8 walks clockwise and hits Charlie
```

**When Dave joins:**

- Dave sits between Bob and Charlie
- Only slices that were "between Bob and Dave" move from Charlie to Dave
- Everyone else keeps their pizza! 🎉

```
           Alice
      🍕7       .
      .            .
     .               .
   Dave      ○       Bob
     .              🍕8
      .             .
       .          Dave
          Charlie

🍕7 walks clockwise and hits Alice (nothing changed)
🍕8 walks clockwise and hits Dave (change)
```

## Back to the real world

This was an ELI5 but the reality is not much harder.

- Instead of pizza slices, we have **data** (like user photos, messages, etc)
- Instead of friends, we have **servers** (computers that store data)

With the _"circle strategy"_ from above we distribute the data evenly across our servers and when we add new servers, not much of the data needs to relocate. This is exactly the goal of consistent hashing.

## In a "Simplified Nutshell"

1. **Make a circle** (hash ring)
2. **Put servers around the circle** (like friends around pizza)
3. **Put data around the circle** (like pizza slices)
4. **Walk clockwise** to find which server stores each piece of data
5. **When servers join/leave** → only nearby data moves

That's it! Consistent hashing keeps your data organized, also when your system grows or shrinks.

So as we saw, consistent hashing solves problems of database partitioning:

- Distribute equally across nodes,
- When adding or removing servers, keep the "relocating-efforts" low.

### Why It's Called Consistent?

Because it's consistent in the sense of adding or removing one server doesn't mess up where everything else is stored.

## Non-ELI5 Explanatiom

Here the explanation again, briefly, but non-ELI5 and with some more details.

### Step 1: Create the Hash Ring

Think of a circle with points from 0 to some large number. For simplicity, let's use 0 to 100 - in reality it's rather 0 to 2^32!

```
                    0/100
                      │
               95 ────┼──── 5
                     ╱│╲
                90 ╱  │  ╲ 10
                  ╱   │   ╲
              85 ╱    │    ╲ 15
                ╱     │     ╲
           80 ─┤      │      ├─ 20
              ╱       │       ╲
          75 ╱        │        ╲ 25
            ╱         │         ╲
       70 ─┤          │          ├─ 30
          ╱           │           ╲
      65 ╱            │            ╲ 35
        ╱             │             ╲
   60 ─┤              │              ├─ 40
      ╱               │               ╲
  55 ╱                │                ╲ 45
    ╱                 │                 ╲
50 ─┤                 │                 ├─ 50
```

### Step 2: Place Databases on the Ring

We distribute our databases evenly around the ring. With 4 databases, we might place them at positions 0, 25, 50, and 75:

```
                    0/100
                   [DB1]
               95 ────┼──── 5
                     ╱│╲
                90 ╱  │  ╲ 10
                  ╱   │   ╲
              85 ╱    │    ╲ 15
                ╱     │     ╲
           80 ─┤      │      ├─ 20
              ╱       │       ╲
    [DB4] 75 ╱        │        ╲ 25 [DB2]
            ╱         │         ╲
       70 ─┤          │          ├─ 30
          ╱           │           ╲
      65 ╱            │            ╲ 35
        ╱             │             ╲
   60 ─┤              │              ├─ 40
      ╱               │               ╲
  55 ╱                │                ╲ 45
    ╱                 │                 ╲
50 ─┤               [DB3]               ├─ 50
```

### Step 3: Find Events on the Ring

To determine which database stores an event:

1. Hash the event ID to get a position on the ring
2. Walk clockwise from that position until you hit a database
3. That's your database

```
Example Event Placements:

Event 1001: hash(1001) % 100 = 8
8 → walk clockwise → hits DB2 at position 25

Event 2002: hash(2002) % 100 = 33
33 → walk clockwise → hits DB3 at position 50

Event 3003: hash(3003) % 100 = 67
67 → walk clockwise → hits DB4 at position 75

Event 4004: hash(4004) % 100 = 88
88 → walk clockwise → hits DB1 at position 0/100
```

## Minimal Redistribution

Now here's where consistent hashing shines. When you add a fifth database at position 90:

```
Before Adding DB5:
Range 75-100: All events go to DB1

After Adding DB5 at position 90:
Range 75-90:  Events now go to DB5 ← Only these move!
Range 90-100: Events still go to DB1

Events affected: Only those with hash values 75-90
```

Only events that hash to the range between 75 and 90 need to move. Everything else stays exactly where it was. No mass redistribution.

The same principle applies when removing databases. Remove DB2 at position 25, and only events in the range 0-25 need to move to the next database clockwise (DB3).

## Virtual Nodes: Better Load Distribution

There's still one problem with this basic approach. When we remove a database, all its data goes to the next database clockwise. This creates uneven load distribution.

The solution is _virtual nodes_. Instead of placing each database at one position, we place it at multiple positions:

```
Each database gets 5 virtual nodes (positions):

DB1: positions 0, 20, 40, 60, 80
DB2: positions 5, 25, 45, 65, 85
DB3: positions 10, 30, 50, 70, 90
DB4: positions 15, 35, 55, 75, 95
```

Now when DB2 is removed, its load gets distributed across multiple databases instead of dumping everything on one database.

## When You'll Need This?

Usually, you will not want to actually implement this yourself unless you're designing a single scaled custom backend component, something like designing a custom distributed cache, design a distributed database or design a distributed message queue.

Popular systems do use consistent hashing under the hood for you already - for example Redis, Cassandra, DynamoDB, and most CDN networks do it.

## Implementation in JavaScript

Here's a complete implementation of consistent hashing. Please note that this is of course simplified.

```javascript
const crypto = require("crypto");

class ConsistentHash {
  constructor(virtualNodes = 150) {
    this.virtualNodes = virtualNodes;
    this.ring = new Map(); // position -> server
    this.servers = new Set();
    this.sortedPositions = []; // sorted array of positions for binary search
  }

  // Hash function using MD5
  hash(key) {
    return parseInt(
      crypto.createHash("md5").update(key).digest("hex").substring(0, 8),
      16
    );
  }

  // Add a server to the ring
  addServer(server) {
    if (this.servers.has(server)) {
      console.log(`Server ${server} already exists`);
      return;
    }

    this.servers.add(server);

    // Add virtual nodes for this server
    for (let i = 0; i < this.virtualNodes; i++) {
      const virtualKey = `${server}:${i}`;
      const position = this.hash(virtualKey);
      this.ring.set(position, server);
    }

    this.updateSortedPositions();
    console.log(
      `Added server ${server} with ${this.virtualNodes} virtual nodes`
    );
  }

  // Remove a server from the ring
  removeServer(server) {
    if (!this.servers.has(server)) {
      console.log(`Server ${server} doesn't exist`);
      return;
    }

    this.servers.delete(server);

    // Remove all virtual nodes for this server
    for (let i = 0; i < this.virtualNodes; i++) {
      const virtualKey = `${server}:${i}`;
      const position = this.hash(virtualKey);
      this.ring.delete(position);
    }

    this.updateSortedPositions();
    console.log(`Removed server ${server}`);
  }

  // Update sorted positions array for efficient lookups
  updateSortedPositions() {
    this.sortedPositions = Array.from(this.ring.keys()).sort((a, b) => a - b);
  }

  // Find which server should handle this key
  getServer(key) {
    if (this.sortedPositions.length === 0) {
      throw new Error("No servers available");
    }

    const position = this.hash(key);

    // Binary search for the first position >= our hash
    let left = 0;
    let right = this.sortedPositions.length - 1;

    while (left < right) {
      const mid = Math.floor((left + right) / 2);
      if (this.sortedPositions[mid] < position) {
        left = mid + 1;
      } else {
        right = mid;
      }
    }

    // If we're past the last position, wrap around to the first
    const serverPosition =
      this.sortedPositions[left] >= position
        ? this.sortedPositions[left]
        : this.sortedPositions[0];

    return this.ring.get(serverPosition);
  }

  // Get distribution statistics
  getDistribution() {
    const distribution = {};
    this.servers.forEach((server) => {
      distribution[server] = 0;
    });

    // Test with 10000 sample keys
    for (let i = 0; i < 10000; i++) {
      const key = `key_${i}`;
      const server = this.getServer(key);
      distribution[server]++;
    }

    return distribution;
  }

  // Show ring state (useful for debugging)
  showRing() {
    console.log("\nRing state:");
    this.sortedPositions.forEach((pos) => {
      console.log(`Position ${pos}: ${this.ring.get(pos)}`);
    });
  }
}

// Example usage and testing
function demonstrateConsistentHashing() {
  console.log("=== Consistent Hashing Demo ===\n");

  const hashRing = new ConsistentHash(3); // 3 virtual nodes per server for clearer demo

  // Add initial servers
  console.log("1. Adding initial servers...");
  hashRing.addServer("server1");
  hashRing.addServer("server2");
  hashRing.addServer("server3");

  // Test key distribution
  console.log("\n2. Testing key distribution with 3 servers:");
  const events = [
    "event_1234",
    "event_5678",
    "event_9999",
    "event_4567",
    "event_8888",
  ];

  events.forEach((event) => {
    const server = hashRing.getServer(event);
    const hash = hashRing.hash(event);
    console.log(`${event} (hash: ${hash}) -> ${server}`);
  });

  // Show distribution statistics
  console.log("\n3. Distribution across 10,000 keys:");
  let distribution = hashRing.getDistribution();
  Object.entries(distribution).forEach(([server, count]) => {
    const percentage = ((count / 10000) * 100).toFixed(1);
    console.log(`${server}: ${count} keys (${percentage}%)`);
  });

  // Add a new server and see minimal redistribution
  console.log("\n4. Adding server4...");
  hashRing.addServer("server4");

  console.log("\n5. Same events after adding server4:");
  const moved = [];
  const stayed = [];

  events.forEach((event) => {
    const newServer = hashRing.getServer(event);
    const hash = hashRing.hash(event);
    console.log(`${event} (hash: ${hash}) -> ${newServer}`);

    // Note: In a real implementation, you'd track the old assignments
    // This is just for demonstration
  });

  console.log("\n6. New distribution with 4 servers:");
  distribution = hashRing.getDistribution();
  Object.entries(distribution).forEach(([server, count]) => {
    const percentage = ((count / 10000) * 100).toFixed(1);
    console.log(`${server}: ${count} keys (${percentage}%)`);
  });

  // Remove a server
  console.log("\n7. Removing server2...");
  hashRing.removeServer("server2");

  console.log("\n8. Distribution after removing server2:");
  distribution = hashRing.getDistribution();
  Object.entries(distribution).forEach(([server, count]) => {
    const percentage = ((count / 10000) * 100).toFixed(1);
    console.log(`${server}: ${count} keys (${percentage}%)`);
  });
}

// Demonstrate the redistribution problem with simple modulo
function demonstrateSimpleHashing() {
  console.log("\n=== Simple Hash + Modulo (for comparison) ===\n");

  function simpleHash(key) {
    return parseInt(
      crypto.createHash("md5").update(key).digest("hex").substring(0, 8),
      16
    );
  }

  function getServerSimple(key, numServers) {
    return `server${(simpleHash(key) % numServers) + 1}`;
  }

  const events = [
    "event_1234",
    "event_5678",
    "event_9999",
    "event_4567",
    "event_8888",
  ];

  console.log("With 3 servers:");
  const assignments3 = {};
  events.forEach((event) => {
    const server = getServerSimple(event, 3);
    assignments3[event] = server;
    console.log(`${event} -> ${server}`);
  });

  console.log("\nWith 4 servers:");
  let moved = 0;
  events.forEach((event) => {
    const server = getServerSimple(event, 4);
    if (assignments3[event] !== server) {
      console.log(`${event} -> ${server} (MOVED from ${assignments3[event]})`);
      moved++;
    } else {
      console.log(`${event} -> ${server} (stayed)`);
    }
  });

  console.log(
    `\nResult: ${moved}/${events.length} events moved (${(
      (moved / events.length) *
      100
    ).toFixed(1)}%)`
  );
}

// Run the demonstrations
demonstrateConsistentHashing();
demonstrateSimpleHashing();
```

## Code Notes

The implementation has several key components:

**Hash Function**: Uses MD5 to convert keys into positions on the ring. In production, you might use faster hashes like Murmur3.

**Virtual Nodes**: Each server gets multiple positions on the ring (150 by default) to ensure better load distribution.

**Binary Search**: Finding the right server uses binary search on sorted positions for O(log n) lookup time.

**Ring Management**: Adding/removing servers updates the ring and maintains the sorted position array.

Do not use this code for real-world usage, it's just sample code. A few things that you should do different in real examples for example:

- **Hash Function**: Use faster hashes like Murmur3 or xxHash instead of MD5
- **Virtual Nodes**: More virtual nodes (100-200) provide better distribution
- **Persistence**: Store ring state in a distributed configuration system
- **Replication**: Combine with replication strategies for fault tolerance