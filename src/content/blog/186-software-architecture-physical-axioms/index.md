---
title: "Software Architecture Has Physical Axioms"
summary: "Software architecture is not floating above physics. Voltage, bits, time, locality, failure, capacity, and energy all shape the systems we build."
date: "Jul 08 2026"
tags:
  - Architecture
  - Software Architecture
  - System Design
  - Computer Science
---

# Software Architecture Has Physical Axioms

Software architecture does have physical axioms.

At least that is my view.

In normal building architecture this is obvious. Buildings have gravity, wind, tension, compression, material fatigue, heat, cold, corrosion, and so on. Physics sets hard ground truths.

In software architecture, people often argue that this is different. Robert C. Martin makes this point in *Clean Architecture*: software is not constrained by physics in the same way. Instead, we have software built on software, built on more software. Libraries on runtimes on operating systems on instruction sets. Endless nesting. Endless abstraction.

I disagree with the strong version of that claim.

Software architecture is absolutely rooted in physics. The connection is just less visible. Software runs on matter: voltages, transistors, memory cells, clocks, heat, storage devices, networks, and time.

That is the case I want to make.

## The Short Version

The physical axioms of software architecture are not:

```text
Use microservices.
Use clean architecture.
Use CQRS.
Use event sourcing.
Use hexagonal architecture.
```

That would be nonsense.

The physical axioms are more basic:

```text
State must live somewhere.
Moving information takes time.
Moving information costs energy.
Computation is finite.
Storage is finite.
Concurrency creates ordering problems.
Components fail.
Distance matters.
Heat matters.
Noise exists.
```

From these facts, we do not derive one correct architecture. We derive constraints. And architecture is largely the art of arranging software so these constraints hurt in acceptable places.

This is why Neal Ford and Mark Richards are right when they say that software architecture is mostly about trade-offs. But I would add something:

> The trade-offs are not floating in the air. Many of them are anchored in physics.

Let's build the case from the bottom up.

## From Voltage To Bits

At the very bottom, computers are not made of `true` and `false`.

They are made of physical signals. Voltage levels. Currents. Transistors switching. Capacitors holding charge. Wires with resistance and capacitance. Nothing there is perfectly clean.

A logical `1` is not a metaphysical thing. It is usually a voltage range interpreted as high enough. A logical `0` is a voltage range interpreted as low enough.

Very roughly:

```text
low voltage range   -> logical 0
high voltage range  -> logical 1
undefined region    -> please do not live here
```

The exact values depend on the technology. The important point is that the computer forces a messy continuous physical world into a discrete symbolic world.

There is fluctuation. There is noise. There are thresholds. There are margins. A circuit is designed so that small physical imperfections do not immediately become logical errors. This is why digital electronics works so reliably at human scale.

A multiplexer, usually called a MUX, is a nice example. It takes several input signals and, based on selector bits, forwards one of them to the output.

```text
input A ----+
           |
input B ----+--> MUX --> output
           |
input C ----+

selector bits decide which input is forwarded
```

That sounds abstract, but physically it is implemented through transistors and wires. The selector signal controls which path is effectively open. Again: voltage, not magic.

From enough of these physical building blocks you get gates. From gates you get adders, registers, memory, instruction execution, caches, buses, and eventually the machine that runs your code.

This is the first important point:

> The bit is already an architectural achievement.

It is a deliberately engineered abstraction over physics. It hides voltage and gives us logic.

## From Bits To Logic

Once we have stable enough bits, Boolean algebra becomes useful. And here one has to be precise: Boolean algebra is George Boole, not Gottlob Frege.

But Frege absolutely belongs in the larger story. Frege's work on formal logic, especially predicate logic, helped create the intellectual ground on which modern formal reasoning stands. If Boole gives us algebra over truth values, Frege is one of the people who made symbolic logic powerful enough to describe structure, quantification, and inference in a much richer way.

Modern IT sits on this strange bridge:

```text
physics -> bits -> Boolean algebra -> formal logic -> programming languages
```

Of course this is simplified. There are many historical and technical layers missing. But as a mental model it works.

Programming languages then give us higher-level rules:

- values
- types
- functions
- objects
- modules
- interfaces
- control flow
- dispatch
- polymorphism
- encapsulation

These are not all directly "caused" by physics in a simple way. Nobody looks at a transistor and derives inheritance.

But they still sit on the same foundation. Every `if`, every predicate, every loop, every interface dispatch, every database index, every message in Kafka, every HTTP response, every TLS handshake, every model inference call, all of it eventually becomes physical state transitions.

So the question is not:

```text
Can we derive SOLID from voltage?
```

No, not in a useful way.

The better question is:

```text
Which architectural pressures are ultimately caused by physical constraints?
```

And there the answer is: a lot of them.

## Axiom 1: State Must Live Somewhere

State is not abstract. It needs a physical carrier.

It can live in:

- CPU registers
- memory
- disk
- object storage
- a database
- a queue
- a browser tab
- a cache
- another service
- a human's head, unfortunately

The location matters.

In-memory state is fast but volatile. Disk is slower but durable. A remote database is shared but introduces network latency. A cache is fast but can be stale. A message queue gives durability and decoupling, but now you have delivery semantics and ordering questions.

This immediately becomes architecture.

If you deploy five backend pods behind a load balancer and keep important user state only in process memory, then your architecture is making a physical claim:

```text
The same process will still exist and receive the next request.
```

In Kubernetes or any ephemeral cloud environment, that is a bad claim.

So we persist product state. We reconstruct context. We use databases, event logs, caches, and object stores. Not because some architecture book told us to. Because memory is physical, local, limited, and disposable.

This is why the question "where does state live?" is one of the deepest architecture questions.

## Axiom 2: Moving Information Takes Time

A local function call and a network call are not the same thing.

They may look similar in code:

```typescript
const user = getUser(id);
const user = await userService.getUser(id);
```

But physically they are completely different.

One may be a call inside the same process. The other may cross a network, hit a load balancer, pass through TLS, reach another machine, deserialize JSON, query a database, serialize again, and return over the network.

That difference is not taste. It is time.

This is why distributed systems are hard. This is why microservices are not just "classes deployed separately". This is why chatty APIs are bad. This is why batching, caching, colocating, denormalizing, and asynchronous messaging exist.

Architecture consequence:

```text
If two pieces of code talk constantly and synchronously,
their physical distance matters.
```

Sometimes the right architecture is to keep them together. Sometimes the right architecture is to split them and accept the cost because independent scaling, team ownership, or failure isolation matters more.

But it is always a trade-off against physical time.

## Axiom 3: Computation Is Finite

No machine has infinite CPU. No cluster has infinite capacity. No model provider has infinite throughput. No database has infinite write bandwidth.

This gives us scalability architecture.

We partition because one machine is not enough.

We replicate because one copy is not enough.

We queue because not all work can happen now.

We apply backpressure because accepting infinite work is a lie.

We rate-limit because one user or tenant can consume shared physical capacity.

We optimize algorithms because `O(n^2)` eventually becomes a bill, a latency problem, or an outage.

This is also why architecture cannot be separated from economics. Cloud bills are just physics translated into money. CPU cycles, memory, storage, network, GPU time, and energy are not opinions.

## Axiom 4: Concurrency Creates Ordering Problems

If one thing happens, then another thing happens, life is easy.

If ten things happen at the same time on different machines, life gets interesting.

Physical systems do not give us a single universal "now" that every component agrees on. Clocks drift. Messages arrive late. Retries duplicate work. A write may succeed while the response is lost. Two services may observe events in different orders.

This is where many architecture patterns come from:

- transactions
- locks
- optimistic concurrency
- idempotency keys
- event ordering
- sequence numbers
- sagas
- outbox pattern
- single-writer designs
- leader election

Again, this is not abstract purity. It is a response to the fact that state changes happen over time, and different components observe that time imperfectly.

Suppose a payment request times out.

Did the payment fail?

Maybe.

Did it succeed and only the response failed?

Also maybe.

So you need idempotency. You need a payment ID. You need the ability to ask the payment system what happened. You need to not charge twice just because a network response disappeared.

That is physics showing up in business logic.

## Axiom 5: Things Fail

Transistors fail. Disks fail. Network links fail. Power fails. Processes crash. Containers get killed. DNS breaks. Certificates expire. Humans deploy bad config. The model provider returns 429. The database becomes slow. The queue is full.

Failure is not an exception to architecture. It is one of its inputs.

This gives us:

- redundancy
- retries
- timeouts
- circuit breakers
- health checks
- bulkheads
- graceful degradation
- disaster recovery
- backups
- multi-region designs

The physical axiom is not "use a circuit breaker".

The axiom is:

```text
Dependencies can stop behaving as expected.
```

The architecture pattern is our response.

## Axiom 6: Abstractions Leak Because Costs Differ

The whole software stack is an abstraction machine.

And abstractions are good. Without them we would all be writing machine code, and even that is already an abstraction over circuits.

But abstractions leak when lower layers have different costs.

A method call and an RPC call can look similar in code, but their failure modes differ. A local list and a database result set can both be iterated, but one might load a million rows into memory. A cache can look like a map, but now the map can be stale, evicted, unavailable, or inconsistent with the source of truth.

Architecture is often about drawing boundaries where the cost difference matters.

If you hide a network call behind something that looks like a cheap property access, you are lying to the reader of the code. The physical world will eventually collect that debt.

This is one reason I like explicit boundaries. Not because ceremony is beautiful, but because some boundaries represent real changes in physics:

```text
same process -> different process
same machine -> different machine
same region  -> different region
memory       -> disk
cache        -> source of truth
read         -> side effect
```

These are not cosmetic distinctions.

## Zoomed-In Architecture

At a zoomed-in level, physics gives us many familiar design instincts.

Encapsulation is useful because uncontrolled state interactions are hard to reason about. The state has to live somewhere, and if everything can mutate it, you lose control over ordering and causality.

Immutability is useful because immutable values remove a class of time problems. If something cannot change, it cannot change underneath another reader.

Pure functions are useful because they do not depend on hidden physical state. Same input, same output. Very nice.

Interfaces are useful because they let us hide implementation details, but still define contracts at boundaries where implementations can vary.

But we should be careful not to overclaim. Physics does not command us to write object-oriented code or functional code. It does not say "prefer composition over inheritance". Those are higher-level human and design concerns.

What physics does say is more basic:

```text
state, time, mutation, communication, and failure are real.
```

Good code-level architecture makes those things visible and manageable.

## Zoomed-Out Architecture

At the system level, the physical influence becomes even more obvious.

### Components

Components should often be split where state ownership, failure domain, scaling needs, or latency requirements differ.

If reporting consumes huge CPU and memory, maybe it should not share the same runtime as checkout.

If account balance and portfolio holdings must change atomically together, maybe splitting them into two microservices is a bad idea.

This is physical architecture in disguise: capacity, locality, state, failure.

### Independent Deployability

Independent deployability is not only a team convenience.

A deployment is a physical change to running systems. Processes restart. Connections drain. Caches warm again. Migrations run. Traffic shifts. Something can fail.

If two components can be deployed independently, their change risk is less physically coupled.

Of course this adds other costs: versioning, compatibility, operational overhead. Again, trade-off.

### Scalability

Scalability exists because finite machines exist.

Vertical scaling means getting a bigger machine.

Horizontal scaling means adding more machines.

Partitioning means splitting the state or traffic so not every component handles everything.

Replication means creating more copies because one copy is a bottleneck or a risk.

None of this is purely conceptual. It is all about physical limits.

### Interoperability

Interoperability exists because different machines, runtimes, organizations, and languages need to agree on how to interpret bits.

That is what protocols are.

HTTP, TCP, JSON, Protobuf, SQL, OAuth, MCP, Kafka protocols, all of these are agreements about meaning across physical boundaries.

Without protocols, we just have voltage changes and bytes that nobody agrees on.

### Maintainability

Maintainability is less directly hardware-bound, but still not floating in the air.

Humans are part of the system. Human attention is finite. Human memory is limited. Teams have communication bandwidth. Cognitive load is real.

So architecture also has human physical limits in it. This is why a technically optimal runtime design can still be a terrible architecture if no team can understand, operate, or evolve it.

This is also where the building analogy becomes interesting again. Buildings are designed for bodies. Software systems are designed for machines and for minds.

## The Better Framing

The building analogy is still useful. Software is much more malleable than buildings. We can copy it nearly for free, move it around, replace parts quickly, and abstract absurdly well.

But that does not mean software architecture has no physical ground truth.

The ground truth is just lower, stranger, and easier to ignore. It does not tell us the final shape. It gives us the constraint space.

Physics says:

```text
There is no infinite CPU.
There is no zero-latency network.
There is no perfectly reliable component.
There is no free data movement.
There is no state without a carrier.
There is no concurrency without ordering consequences.
```

Software architecture starts from there and then adds business goals, team structure, regulations, delivery pressure, cost, product needs, and taste.

So yes, architecture is still about trade-offs.

But the deepest trade-offs are not arbitrary.

## Final Thought

The physical axioms of software architecture are not as visible as gravity in a building.

They are hidden behind layers:

```text
voltage
  -> bits
  -> gates
  -> instruction sets
  -> operating systems
  -> runtimes
  -> languages
  -> frameworks
  -> architecture diagrams
```

By the time we draw boxes and arrows, the physics has become almost invisible.

But it is still there.

Every arrow has latency. Every box needs capacity. Every stateful component stores bits somewhere. Every replicated system has consistency questions. Every side effect has ordering and retry problems. Every abstraction hides a cost profile.

That is the real connection.

Software architecture is not free from physics.

It is physics, logic, economics, and human organization stacked so high that we sometimes forget the bottom is still there.
