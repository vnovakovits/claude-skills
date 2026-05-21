---
name: domain-driven-design
description: Apply Domain-Driven Design (DDD) by Eric Evans and Vaughn Vernon when modeling complex business domains, designing aggregates, structuring bounded contexts, choosing between entities and value objects, or aligning code with domain language. Covers strategic design (ubiquitous language, bounded contexts, context mapping), tactical building blocks (entities, value objects, aggregates, domain events, services, repositories, factories), supple design, and refactoring toward deeper insight.
---

# Domain-Driven Design (Eric Evans)

Apply DDD when modeling complex business domains, designing system boundaries, deciding what is an entity vs a value object, structuring aggregates, or aligning code with the language of domain experts. DDD is about *tackling complexity in the heart of software* — when the domain is simple, simpler approaches are better.

## Core Philosophy

**The model is the heart of the software.** Code, conversations, and diagrams should all express the same model. When they diverge, the model is failing.

**Software complexity comes from the domain, not the technology.** The hardest problem is understanding what the business actually does and encoding it faithfully.

**Knowledge crunching is continuous.** Designers, developers, and domain experts iterate on a shared model. Insights emerge over time; the model evolves.

**Embrace breakthroughs.** Periodically, accumulated learning reveals a much better model. Refactor toward it rather than patch the old one.

---

## Strategic Design

Strategic design addresses the structure of the system as a whole — how large systems are partitioned and how parts relate.

### Ubiquitous Language

A shared, rigorous language used by developers and domain experts alike, in conversation, documentation, AND code.
- Class names, method names, and event names come straight from this language.
- If a domain expert says "Shipment", code says `Shipment` — not `Parcel`, not `Package`, not `Order`.
- The language evolves as understanding deepens. When the term changes, the code changes.
- When developers and experts use different words for the same thing, miscommunication is guaranteed.

### Bounded Context

An explicit boundary within which a particular model applies. The same term (`Customer`, `Product`) can mean different things in different contexts — and that is fine, as long as the boundary is explicit.
- A bounded context typically aligns with a team, a deployment unit, or a subsystem.
- Inside a bounded context, the ubiquitous language is consistent and unambiguous.
- Across bounded contexts, translation is required.

### Subdomains

The business itself is divided into subdomains:
- **Core Domain** — the part that differentiates the business; invest heavily here, do not outsource.
- **Supporting Subdomains** — necessary but not differentiating; build but don't over-invest.
- **Generic Subdomains** — solved problems (auth, billing, notifications); buy or use off-the-shelf when possible.

Bounded contexts often map onto subdomains, but the mapping is not always 1:1.

### Context Mapping

When multiple bounded contexts exist, their relationships must be modeled explicitly. Common patterns:

- **Partnership** — two teams succeed or fail together; cooperative planning.
- **Shared Kernel** — a small subset of the model is shared and jointly maintained. High coordination cost; use sparingly.
- **Customer/Supplier** — downstream context's needs drive upstream's priorities; formal contract.
- **Conformist** — downstream conforms to the upstream model without translation. Cheap but locks in coupling.
- **Anticorruption Layer (ACL)** — a translation layer that protects the downstream model from the upstream's concepts. Pay this cost when the upstream model is messy or legacy.
- **Open Host Service** — upstream offers a well-defined protocol for many consumers.
- **Published Language** — a shared, well-documented language (e.g., a schema) used for inter-context communication.
- **Separate Ways** — explicit decision to not integrate; each context goes its own way.
- **Big Ball of Mud** — unstructured, undocumented context. Wrap with an ACL if you have to integrate.

A **context map** is a diagram of these relationships. Draw it; show it to stakeholders.

### Distillation

Identify and protect the core domain. Strip away supporting concerns from core code. Make core models cleaner, more expressive, and more carefully maintained than the periphery.

---

## Tactical Design — Building Blocks

Patterns for expressing the model in code, within a bounded context.

### Entity

An object defined by **identity**, not attributes. Two entities with identical attributes but different IDs are different objects. Entities have a lifecycle.
- `Customer` with id `42` is the same entity regardless of whether the name field changes.
- Identity is established at creation and is immutable.
- Equality is by ID.

### Value Object

An object defined by its **attributes**, not identity. Two value objects with identical attributes are interchangeable. Immutable.
- `Money(100, USD)`, `Address("...")`, `DateRange(start, end)`.
- No setters; operations return new instances.
- Equality is by attribute equality.
- Strongly prefer value objects over primitive types for domain concepts (primitive obsession is a smell).

**The choice between Entity and Value Object is a modeling decision.** Ask: "Does this thing's identity matter, or only its current values?" Money is a value object; a bank account is an entity.

### Aggregate

A cluster of associated entities and value objects, treated as a single unit for the purpose of data changes. Each aggregate has one **aggregate root** — the only entity outside code may reference.

**Aggregate rules (Vaughn Vernon's "Effective Aggregate Design"):**

1. **Model true invariants in consistency boundaries.** An aggregate exists to enforce an invariant that must hold transactionally. If there is no such invariant, you may not need an aggregate.
2. **Design small aggregates.** Prefer many small aggregates over few large ones. Large aggregates have contention, scaling, and lock-issue problems.
3. **Reference other aggregates by identity, not by object reference.** An `Order` holds `CustomerId`, not a `Customer` reference.
4. **Update one aggregate per transaction.** If multiple aggregates must change, use **eventual consistency** via domain events.

The aggregate root enforces invariants and exposes the only public surface. External code calls methods on the root; internal entities are accessed only through the root.

### Domain Event

A record of something that happened in the domain that domain experts care about. Past tense, named in domain language.
- `OrderPlaced`, `PaymentReceived`, `ShipmentDispatched`.
- Immutable; carries the data needed by handlers.
- Used to propagate change across aggregates, contexts, or systems.
- Enables eventual consistency and event-driven integrations.

### Domain Service

When an operation does not belong naturally to any entity or value object — typically because it involves multiple of them — model it as a stateless **domain service**.
- Named in domain language (`TransferFunds`, `CalculateRoute`).
- Operates on domain objects; lives in the domain layer.
- Distinct from **application services** (which orchestrate use cases and live in the application layer) and **infrastructure services** (which deal with technical concerns).

### Repository

A collection-like abstraction for accessing aggregates. Hides persistence details from the domain.
- One repository per aggregate root.
- Methods speak the domain (`FindActiveCustomersInRegion`), not SQL.
- Returns aggregate roots, not raw rows.
- Implementation lives in the infrastructure layer; interface lives in the domain layer.

### Factory

Encapsulates the logic of creating complex objects or aggregates.
- Use when construction is non-trivial (multi-step, requires validation, choice of subtype).
- Can be a static factory method on the class, a separate factory class, or a builder.
- Ensures invariants hold at creation time.

### Module

A logical grouping of related model elements (a package or namespace in code).
- Named in domain language.
- Cohesive: things inside change together; things outside don't.
- Low coupling: depends on as few other modules as possible.

---

## Layered Architecture (and Variants)

DDD assumes a layered architecture:

1. **User Interface / Presentation** — displays information, accepts input.
2. **Application** — coordinates use cases, manages transactions; thin.
3. **Domain** — the model: entities, value objects, aggregates, domain services, domain events. **The heart of the software.**
4. **Infrastructure** — persistence, messaging, third-party integrations.

**Dependencies flow inward.** Domain depends on nothing. Application depends on domain. Infrastructure depends on domain (implements interfaces defined there). UI depends on application.

**Hexagonal / Onion / Clean Architecture** are all variations that strengthen the inward dependency rule. DDD is compatible with all of them.

---

## Supple Design

Patterns that make a model easy to use, change, and reason about.

### Intention-Revealing Interfaces
Names of classes and methods describe what they accomplish, not how. A caller can use them without reading the implementation.

### Side-Effect-Free Functions
Where possible, model operations as pure functions that return new state. Combine freely without unintended consequences. Especially valuable on value objects.

### Assertions
Make invariants and post-conditions explicit and enforced. State what must be true; fail fast if it isn't.

### Standalone Classes
Reduce a class's dependencies. The fewer concepts a class touches, the easier it is to understand in isolation.

### Closure of Operations
When a method's return type is the same as its argument type (or owner type), operations compose cleanly. `Money + Money → Money` is closed.

### Declarative Design (Specification Pattern)
Express business rules as declarative objects that can be combined, evaluated, and reused. `IsEligibleForDiscount` is a Specification, not buried in an if/else.

---

## Refactoring Toward Deeper Insight

The model is never "done". Common signals it's time to refactor the model:

- **Repeated awkwardness** in the code — the model is fighting you.
- **A new use case** exposes a concept the model doesn't represent.
- **Domain experts use a word** that has no code counterpart — make it explicit.
- **A breakthrough conversation** with an expert reveals the real shape of the problem.

**Conceptual contours** — refactor along the natural seams of the domain, not arbitrary structural lines. Good models have joints that match how the domain actually changes.

---

## CQRS and Event Sourcing (Frequent Companions)

Not strictly part of DDD but often paired with it.

- **CQRS (Command-Query Responsibility Segregation)** — separate the write model (commands, aggregates, invariants) from the read model (queries, projections, denormalized views). Use when reads and writes have very different shapes or scaling needs.
- **Event Sourcing** — persist state as a sequence of domain events; current state is derived by replaying events. Provides perfect audit, temporal queries, and natural domain-event integration. Significant complexity cost — apply selectively.

---

## When NOT to Use DDD

DDD is heavyweight. It is the wrong tool when:
- The domain is shallow (CRUD over a small data model).
- The application is generic (a thin wrapper over a database).
- The team lacks access to domain experts.
- The team is too small to absorb the overhead.

Apply DDD where the business complexity is real and worth modeling carefully — the core domain. Use simpler approaches for supporting and generic subdomains.

---

## Common Mistakes

- **Anemic domain model.** Entities with only getters/setters; logic in services. The model is a data structure, not a domain model.
- **Treating DDD as a tactical-patterns checklist.** Aggregates and repositories without ubiquitous language or bounded contexts produce ceremony without insight.
- **One bounded context for the whole system.** Forces one model to do everything; concepts get overloaded.
- **Aggregates too large.** Loading and locking become painful; performance and contention suffer.
- **Cross-aggregate transactions.** Violates aggregate boundaries; reach for domain events and eventual consistency instead.
- **Skipping the ACL.** Letting an external model leak into your domain pollutes the model with concepts that don't belong.
- **Treating value objects as primitives.** `decimal price` instead of `Money price` loses meaning and creates primitive obsession.
- **Ignoring domain events.** Coupling aggregates and contexts directly leads to brittle, monolithic designs.

---

## Quick Application Checklist

- [ ] Is the ubiquitous language used consistently in code, conversation, and documentation?
- [ ] Have you identified bounded contexts and drawn a context map?
- [ ] Have you distinguished core, supporting, and generic subdomains?
- [ ] Is each domain concept an entity or a value object — and is that distinction correct?
- [ ] Are aggregates small, with clear roots and explicit invariants?
- [ ] Do you reference other aggregates by ID, not by reference?
- [ ] Do you update one aggregate per transaction?
- [ ] Are domain events used for cross-aggregate coordination?
- [ ] Do repositories return aggregates and speak in domain terms?
- [ ] Does the domain layer depend on nothing technical?
- [ ] Are external/legacy systems wrapped in an anticorruption layer?
- [ ] Is the core domain getting more design attention than the periphery?
- [ ] Have you refactored toward deeper insight when the model felt awkward?

---

## Reading

- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003) — the original.
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013) — practical tactics; "Effective Aggregate Design" essays.
- Vaughn Vernon, *Domain-Driven Design Distilled* (2016) — short intro.
- Scott Wlaschin, *Domain Modeling Made Functional* (2018) — DDD with strong type systems.
