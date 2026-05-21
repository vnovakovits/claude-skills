---
name: hexagonal-clean-architecture
description: Apply Alistair Cockburn's Hexagonal Architecture (Ports and Adapters), Jeffrey Palermo's Onion Architecture, and Robert C. Martin's Clean Architecture — the family of architectural styles that put the domain at the center, push frameworks and I/O to the edges, and enforce inward-pointing dependencies. Use when structuring a non-trivial application, separating business logic from delivery and persistence, deciding where ports live and how adapters plug in, or testing domain logic without spinning up infrastructure.
---

# Hexagonal / Clean Architecture

Apply this skill when structuring a non-trivial application that will have more than one delivery mechanism (HTTP, message queue, CLI), persistence target, or external integration — or simply when you want business logic that is independent of frameworks, testable in isolation, and resistant to infrastructure churn.

## Core Philosophy

**The domain is the center of the universe.** Frameworks, databases, UIs, and external services orbit it. The domain depends on nothing; everything depends on the domain.

**Dependencies point inward.** Outer layers know about inner layers; inner layers never know about outer layers. The compile-time / source-code dependency graph respects this rule absolutely.

**The application is independent of:**
- Frameworks (it can run without ASP.NET, Spring, Rails)
- UI (you can replace HTTP with CLI or message queue)
- Database (you can swap Postgres for an in-memory store for tests)
- External services (you can substitute fakes)
- Anything outside its own abstractions

**Three names, one idea.**
- **Hexagonal Architecture** (Alistair Cockburn, 2005) — "Ports and Adapters". The earliest name.
- **Onion Architecture** (Jeffrey Palermo, 2008) — concentric rings, dependencies inward.
- **Clean Architecture** (Robert C. Martin, 2017) — same structure, additional emphasis on Use Cases and the Dependency Rule.

The differences are presentation, not substance. We will use the terms interchangeably; the patterns are siblings.

---

## The Diagram (Clean Architecture Variant)

```
                     ┌──────────────────────────────────────────┐
                     │   Frameworks & Drivers                   │
                     │   (Web, DB, devices, external APIs)      │
                     │  ┌────────────────────────────────────┐  │
                     │  │   Interface Adapters               │  │
                     │  │   (Controllers, Gateways,          │  │
                     │  │    Presenters, Repositories impl)  │  │
                     │  │  ┌──────────────────────────────┐  │  │
                     │  │  │   Application / Use Cases    │  │  │
                     │  │  │  (orchestration of           │  │  │
                     │  │  │   domain behavior)           │  │  │
                     │  │  │  ┌─────────────────────────┐ │  │  │
                     │  │  │  │   Entities / Domain     │ │  │  │
                     │  │  │  │   (enterprise business  │ │  │  │
                     │  │  │  │    rules; pure)         │ │  │  │
                     │  │  │  └─────────────────────────┘ │  │  │
                     │  │  └──────────────────────────────┘  │  │
                     │  └────────────────────────────────────┘  │
                     └──────────────────────────────────────────┘

                          ────────────────►  dependencies
                                     (never reverse)
```

---

## The Layers

### Entities / Domain (innermost)
- Pure business concepts and rules.
- Enterprise-wide — would apply even if you were running on paper.
- No knowledge of HTTP, databases, frameworks, time-of-day, randomness.
- Aggregates, entities, value objects, domain services, domain events (see the DDD skill).
- Testable with zero infrastructure — instantiate, call, assert.

### Use Cases / Application
- Application-specific business rules. Orchestrates entities to fulfill a use case.
- One use-case class per scenario (`PlaceOrder`, `CancelReservation`, `IssueRefund`).
- Defines **ports** (interfaces) for everything outside its world: repositories, external services, time, randomness.
- Knows about entities; does not know about HTTP, SQL, or any specific framework.
- Testable with in-memory or mocked adapters.

### Interface Adapters
- Translates between the application's data shapes and the outside world's data shapes.
- **Inbound adapters:** HTTP controllers, message-queue listeners, CLI handlers, scheduled-job runners. They turn external requests into use-case calls.
- **Outbound adapters:** repository implementations, external API clients, file-system writers. They implement the ports defined by the application.
- Knows about both the application's interfaces and the framework's specifics.

### Frameworks & Drivers (outermost)
- ASP.NET, Spring, Express, Rails, EF Core, the database itself, the message broker.
- Glued in via the adapters; the inner layers never see them.

---

## Ports and Adapters

The term comes from Cockburn's original formulation; it remains the clearest mental model.

**A port is an interface owned by the application** — defined in terms the application cares about, in the application's vocabulary. Examples:
- `IOrderRepository.Save(Order o)`
- `IEmailSender.Send(EmailMessage m)`
- `IClock.Now`

**An adapter is an implementation of a port** that connects to a specific technology:
- `SqlOrderRepository : IOrderRepository`
- `SmtpEmailSender : IEmailSender`
- `SystemClock : IClock`

```
       (Application defines what it needs)
                     │
                     ▼
           ┌────────PORT────────┐
           │  IOrderRepository  │
           └────────────────────┘
                ▲           ▲
                │           │
    ┌───────────┴┐         ┌┴───────────────┐
    │ SqlOrder    │         │ InMemoryOrder  │
    │ Repository  │         │ Repository     │
    │ (prod)      │         │ (tests)        │
    └─────────────┘         └────────────────┘
       (adapters implement what the application needs)
```

**Crucial:** the port lives in the *application* (inner) layer; the adapter lives in the *infrastructure* (outer) layer. This is the Dependency Inversion Principle in action — the high-level module owns the contract; the low-level module conforms.

### Driving (Primary) vs Driven (Secondary) Ports

Cockburn distinguishes:
- **Driving ports** — the application's API. The outside world calls in through them. Inbound adapters call driving ports.
- **Driven ports** — the application's required collaborators. The application calls out through them. Driven ports are implemented by outbound adapters.

```
            ┌───────────────────────┐
HTTP ─────► │ Driving               │
ctrl        │   Port                │
            │   (use case)          │
            │                       │
            │             Driven ───┼──► IRepository ──► SqlRepo
            │             Port      │
            └───────────────────────┘
```

---

## The Dependency Rule

> *Source code dependencies must point only inward, toward higher-level policies.*
> *Nothing in an inner circle can know anything about something in an outer circle.*
> — Robert C. Martin

Practical consequences:
- The domain layer has no `using System.Web` / `import org.springframework`.
- The application layer has no SQL, no HTTP types, no framework annotations.
- Repository interfaces live with the application (inner); implementations live in infrastructure (outer).
- Domain events are pure data; their handlers may live in any layer, but the events themselves are domain artifacts.

**Test:** if you can compile and run the domain and application layers with the infrastructure project absent, the dependency rule is being honored.

---

## Boundary Data and Mapping

Data crossing layers should not carry inner-layer concerns to outer layers or vice versa.

- **DTOs at the boundary.** Controllers receive DTOs, map to domain commands, call the use case, map the domain result back to a DTO. Domain entities do not get serialized directly.
- **Don't put framework attributes on domain types.** No `[Table]`, `[Column]`, `[JsonProperty]` on `Order`. Map at the boundary.
- **Different DTOs for different boundaries.** The HTTP DTO and the persistence DTO are usually different — model each to its boundary, not to a shared "data" abstraction.

The mapping is annoying. It is also the price of independence. Frameworks change; your domain shouldn't.

---

## Testing Strategy

Hexagonal/Clean architectures yield a testing pyramid that mirrors the layer structure.

- **Domain / unit tests** — instantiate entities and value objects directly, call methods, assert. Zero infrastructure. Microseconds each.
- **Use case tests** — instantiate use cases with in-memory fakes for ports. Drive the use case; assert state changes and recorded interactions.
- **Adapter tests** — verify that each adapter correctly implements its port against the real technology (real DB, real HTTP). Fewer in number; slower.
- **End-to-end tests** — full stack, one of each happy path. Slowest; fewest.

The split is natural because the architecture already isolates concerns; tests fall along the same seams.

---

## Common Implementations

### Two-project (minimal)
```
src/
├── MyApp.Domain/           // entities + use cases + ports
└── MyApp.Infrastructure/   // adapters + composition root
```

### Three-project (typical)
```
src/
├── MyApp.Domain/           // entities, value objects, domain services
├── MyApp.Application/      // use cases, ports
├── MyApp.Infrastructure/   // adapter implementations
└── MyApp.Host/             // composition root, HTTP, wiring
```

### Larger (DDD-aligned)
```
src/
├── BoundedContextA.Domain/
├── BoundedContextA.Application/
├── BoundedContextA.Infrastructure/
├── BoundedContextB.Domain/
├── BoundedContextB.Application/
├── BoundedContextB.Infrastructure/
└── Shared/                   // truly cross-cutting, used sparingly
```

The project layout is not the architecture — but it makes the architecture enforceable: the project references will only compile if the dependency rule is honored.

---

## What This Buys You

- **Independent testability.** Domain and application tests run in milliseconds.
- **Replaceable infrastructure.** Swap Postgres for SQL Server, REST for gRPC, ASP.NET for minimal APIs — without touching the domain.
- **Long-lived business logic.** Frameworks come and go; the domain endures.
- **Bounded change radius.** Most changes touch one layer.
- **Compatibility with DDD.** Aggregates live in the domain; use cases in the application; repositories as ports. Hexagonal is the natural home for DDD.
- **Functional core, imperative shell.** Decisions in the domain (pure); side effects at the adapters (impure). Matches the pattern Seemann emphasizes.

---

## What This Costs

- **More code.** DTOs, ports, mappers — there is more scaffolding than a naïve "controller calls repository" design.
- **More files.** The project structure has more moving parts.
- **Indirection.** Reading a flow goes through several layers. Some teams find this annoying for trivial CRUD.

**When to skip it:** for genuinely simple CRUD over a small model, the layered ceremony costs more than it saves. Apply hexagonal to the parts of your system that have non-trivial business logic; allow simpler structures where the value is shallow.

---

## Common Mistakes

- **Letting framework types leak into the domain.** EF entities used as domain entities; HTTP DTOs returned from use cases. Map at the boundary.
- **Putting repository interfaces in the infrastructure layer.** Defeats DIP — the high-level should own the contract.
- **Use cases that reach across into other use cases.** Use cases compose only through the domain; calling another use case directly produces tight coupling.
- **One mega-use-case ("DoEverything")** that orchestrates many concerns. One use case per scenario, named for what the user is trying to do.
- **Sharing DTOs between boundaries.** "Read" and "write" shapes differ; presentation and persistence shapes differ. Use different DTOs.
- **Putting business rules in adapters.** Validations and policies belong in the domain, not in the HTTP controller or the repository.
- **Excessive abstraction.** Interfaces with one implementation, never substituted — speculative DIP. Apply ports where substitution matters (tests, alternative tech).
- **Confusing "layers" with "tiers".** Layers are about source code organization; tiers are about deployment. A monolith can have all layers in one process.

---

## Quick Application Checklist

For structure:
- [ ] Does the domain compile without infrastructure?
- [ ] Are repository interfaces (and other ports) defined in the application/domain, implemented in infrastructure?
- [ ] Are framework annotations absent from domain types?
- [ ] Are DTOs present at every external boundary, with explicit mapping?

For each module:
- [ ] Is the dependency direction inward only?
- [ ] Are inbound adapters thin (translate, call use case, translate back)?
- [ ] Are outbound adapters thin (implement port, translate to technology)?
- [ ] Are use cases focused (one scenario each, named for user intent)?
- [ ] Is business logic in entities and domain services, not in adapters?

For testing:
- [ ] Domain tests with no mocks needed?
- [ ] Use-case tests with in-memory adapters?
- [ ] Adapter tests against real technology?
- [ ] End-to-end tests on happy paths only?

---

## Reading

- **Alistair Cockburn**, *Hexagonal Architecture* (2005 essay) — the original. Available at alistair.cockburn.us.
- **Jeffrey Palermo**, *The Onion Architecture* (2008 blog series) — jeffreypalermo.com.
- **Robert C. Martin**, *Clean Architecture: A Craftsman's Guide to Software Structure and Design* (2017) — the most-cited modern formulation; introduces use cases prominently.
- **Vaughn Vernon**, *Implementing Domain-Driven Design* (2013) — chapters on architecture pair DDD with hexagonal.
- **Tom Hombergs**, *Get Your Hands Dirty on Clean Architecture* (2019) — practical, code-heavy walkthrough.
- **Mark Seemann**, *Dependency Injection Principles, Practices, and Patterns* (2019) — the technique that makes hexagonal compose at runtime.
- **Herberto Graça**, "Explicit Architecture" essay — synthesizes hexagonal, onion, clean, and DDD into one coherent diagram.
