---
name: event-sourcing-cqrs
description: Apply Event Sourcing and CQRS principles — from Greg Young's CQRS Documents, Alexey Zimarev's Hands-On Domain-Driven Design with .NET Core, and Microsoft's Azure Architecture patterns — when designing commands, write-side state, IHoldState interfaces, applier functions, event payloads, stream structures, aggregate boundaries, read models, or projections. Use when asked about what belongs in state vs events, reviewing an applier for correctness, deciding whether a field is write-side or read-side, sizing an IHoldState interface, designing a new command handler, writing a query handler, understanding why write-side state should be minimal, or any CQRS/ES architectural decision. Always activate this skill for ES/CQRS questions rather than relying on general knowledge alone.
---

# Event Sourcing and CQRS (Greg Young, Alexey Zimarev)

Apply this skill for any question about CQRS command/query separation, write-side state design, applier correctness, event payload design, stream structure, aggregate boundaries, read model design, or projections. Principles drawn from Greg Young's *CQRS Documents*, Zimarev's *Hands-On Domain-Driven Design with .NET Core*, the KurrentDB/EventStore documentation, and Microsoft's Azure Architecture patterns.

---

## Core Philosophy

**The event log is the source of truth.** State is a derived projection of events — a read-optimised view computed by replaying the event stream.

> "Current state is a left fold of previous behaviours." — Greg Young

Every field in write-side state must be derivable purely by replaying events. If a field cannot be produced by applying events in sequence, it does not belong on the write side.

**CQRS separates the write model from the read model.** Before CQRS, a single service handles both:
```
CustomerService: MakePreferred, GetCustomer, GetPreferred, ChangeLocale, Create, Edit
```
After CQRS:
```
CustomerWriteService:  MakePreferred, ChangeLocale, Create, Edit
CustomerReadService:   GetCustomer, GetPreferredCustomers, GetCustomersWithName
```

> "Command and Query Responsibility Segregation... extends CQS from the method level to the object and architectural level." — Greg Young

CQRS restores the Ubiquitous Language. CRUD architectures reduce every domain to four verbs and make DDD impossible — the domain becomes "a glorified Excel spreadsheet."

> "For most systems CQRS adds risky complexity. CQRS should only be used on specific portions of a system (bounded contexts), never the entire system." — Martin Fowler

Use it where the domain is genuinely complex or where reads and writes need to scale independently. Prefer traditional CRUD everywhere else.

---

## CQRS: The Write Side

### Commands

Commands are **requests** to the system — imperative, rejectable, carrying only the data needed for that operation.

**Imperative tense, always.** Imperative signals that the system is allowed to reject the request. If the system cannot reject it, it is not a command — use an event.

```
✓ RelocateCustomer    ✗ CustomerRelocated  (that's an event)
✓ PlaceSale           ✗ SaleCompleted      (that's an event)
✓ DeactivateItem      ✗ ItemDeactivated    (that's an event)
```

**Name from use cases, not CRUD.** `ChangeAddress` is a data-update verb. `RelocateCustomer`, `CorrectAddress`, and `UpdateDeliveryAddress` may all update the same field but represent different domain operations with different invariants, different authorization, and different audit trails. Investing in precise command names pays back in domain insight.

> "This process in naming can lead to great amounts of domain insight." — Greg Young

**Carry only the data the operation needs.** Not the full object state. A command is not a DTO of the aggregate.

**Include at least one aggregate ID.** Every state-changing command must route to a specific aggregate.

**Let clients originate UUIDs.** Having the client generate the aggregate ID (a `Guid.NewGuid()` at the UI layer) is extremely valuable in distributed systems — it enables idempotency and retry safety without server-side duplication checks.

**Avoid Verify/Validate/Check as command prefixes.** `VerifyProductExists` implies trying, not acting. Use `ReserveProducts` — the command internally verifies preconditions. The name should describe the business action, not the check that guards it.

**Commands can be rejected. Events cannot.** This is the sharpest distinction between the two.

### Application Service: The Write-Side Orchestrator

The application service is the entry point for all write-side operations. It follows a strict Load → Execute → Save pattern:

```csharp
public class ClassifiedAdsApplicationService : IApplicationService
{
    public Task Handle(object command) =>
        command switch
        {
            V1.Create cmd       => HandleCreate(cmd),
            V1.SetTitle cmd     => HandleUpdate(cmd.Id, c => c.SetTitle(ClassifiedAdTitle.FromString(cmd.Title))),
            V1.UpdatePrice cmd  => HandleUpdate(cmd.Id, c => c.UpdatePrice(Price.FromDecimal(cmd.Price, cmd.Currency, _currencyLookup))),
            V1.RequestToPublish cmd => HandleUpdate(cmd.Id, c => c.RequestToPublish()),
            _                   => Task.CompletedTask
        };

    private Task HandleUpdate(Guid id, Action<ClassifiedAd> update) =>
        this.HandleUpdate(_store, new ClassifiedAdId(id), update);
}

// Generic Load → Execute → Save used by all handlers
public static async Task HandleUpdate<T, TId>(this IApplicationService service,
    IAggregateStore store, TId aggregateId, Action<T> operation)
    where T : AggregateRoot<TId>
{
    var aggregate = await store.Load<T, TId>(aggregateId);
    if (aggregate == null) throw new InvalidOperationException($"Entity {aggregateId} not found");
    operation(aggregate);
    await store.Save<T, TId>(aggregate);
}
```

The application service never contains domain logic. It only orchestrates: load aggregate, call domain method, persist result.

### Task-Based UI

CQRS works best with a task-based UI — one that guides users through specific operations rather than exposing raw entity fields for editing. Task-based UIs map naturally to commands:

- A "Deactivate" action leads to a screen asking for a reason → produces `DeactivateInventoryItem { Comment }`.
- An address form shows different options: "Relocate", "Correct Typo", "Change Delivery Only" → each produces a different command.

> "Microsoft identified three usability problems with CRUD UIs: users don't construct an adequate mental model, long-time users never master common procedures, users must work hard to figure out each feature." — Greg Young (citing Microsoft research)

---

## CQRS: The Read Side

### Queries and DTOs

Queries return data. They **never modify state**. The read model is a completely separate concern from the domain model.

> "Queries never alter data. Instead, they return data transfer objects (DTOs) that present the required data in a convenient format, without any domain logic." — Microsoft

Read models are flat, denormalized, purpose-built for specific screens:

```csharp
public class ClassifiedAdDetails
{
    public Guid ClassifiedAdId { get; set; }
    public string Title { get; set; }
    public decimal Price { get; set; }
    public string CurrencyCode { get; set; }
    public string Description { get; set; }
    public string SellersDisplayName { get; set; }
    public string[] PhotoUrls { get; set; }
}
```

No domain objects. No business logic. No ORM mapping to aggregate structure. Developers building the read side do not need to understand the domain model.

Query models name operations with `Get` prefix:
```csharp
public static class QueryModels
{
    public class GetPublicClassifiedAd    { public Guid ClassifiedAdId; }
    public class GetPublishedClassifiedAds { public int Page; public int PageSize; }
    public class GetOwnersClassifiedAds   { public Guid OwnerId; public int Page; public int PageSize; }
}
```

### Thin Read Layer

The write side repository has essentially only one read method: `GetById`. All other query methods are read-side concerns:

**Smells indicating read concerns polluting the write side:**
- Repository has more than a handful of query methods (paging, sorting, filtering)
- Domain objects expose getters for DTO-building
- Eager loading / prefetch paths driven by query needs
- Multiple aggregate roots loaded to assemble a single DTO
- ORM configured around read patterns rather than domain behaviour

### Eventual Consistency

The read model may lag behind the write model. This is acceptable and normal. Design the system so that:
- The UI acknowledges commands (accepted/rejected) without waiting for the read model to update
- Read models are rebuildable from scratch at any time by replaying events
- Event handlers are idempotent — processing the same event twice produces the same read model state

---

## Write-Side State: Minimal by Design

### The Diagnostic Question

Before adding any field to `IHoldState`, ask:

> *Would a command handler fail or produce incorrect events without this field?*

If no, the field does not belong on the write side. Write-side state has one purpose: give command handlers the minimum information they need to enforce business invariants.

**What belongs:**
- Fields that determine whether a command is valid or invalid
- Fields that prevent duplicate transitions (`Status`, `IsConfirmed`)
- Fields that guard domain rules (`TotalAmount` for refund limits, `Quantity` for stock checks)
- Aggregate lifecycle / status fields

**What does not belong:**
- Display labels and formatted strings (`SubtotalDisplay`, `LastModifiedLabel`)
- Derived values trivially computable from other fields (`TotalItems = Items.Count`)
- Business policies pre-evaluated at projection time (`HasFreeShippingEligibility`)
- Fields carried for convenience or reporting
- Timestamps computed during replay — non-deterministic, breaks rebuild

---

## Multiple IHoldState Interfaces

A single aggregate can have **multiple focused `IHoldState` interfaces**, each purpose-built for a specific command handler or group of handlers. A 45-field `IHoldOrderState` is a write-side smell.

### Pattern: Separate Applier Class per State Slice

```csharp
// Focused interface — only what the refund handler needs
public interface IHoldRefundOrderState
{
    OrderStatus Status { get; }
    PaymentReference PaymentReference { get; }
    Money TotalAmount { get; }
}

// Separate applier class replaying the same event stream
// but projecting only the three fields the refund handler cares about
public class RefundOrderAppliers : IApply<IHoldRefundOrderState>
{
    public IHoldRefundOrderState Apply(IHoldRefundOrderState state, OrderPlaced @event) =>
        state with { Status = OrderStatus.Active };

    public IHoldRefundOrderState Apply(IHoldRefundOrderState state, PaymentCaptured @event) =>
        state with
        {
            PaymentReference = @event.PaymentReference,
            TotalAmount = @event.Amount
        };

    // Events irrelevant to refund invariants get no-op appliers
    public IHoldRefundOrderState Apply(IHoldRefundOrderState state, ItemAdded @event) => state;
    public IHoldRefundOrderState Apply(IHoldRefundOrderState state, AddressUpdated @event) => state;
}
```

A `RefundOrderAppliers` class **replays the same Order event stream** but only projects the three fields needed for refund processing. The mechanism is separate applier classes — not the concrete state record implementing multiple interfaces (which is a different, less ES-idiomatic approach).

### Domain Function Signature

```csharp
public static Seq<IEvent> Refund(
    OrderId id,
    RefundRequest request,
    IHoldRefundOrderState state)   // focused slice, not a 45-field type
{
    if (state.Status != OrderStatus.Active)
        return Seq(new RefundRejected(...));
    if (request.Amount > state.TotalAmount)
        return Seq(new RefundRejected(...));
    return Seq(new RefundInitiated(...));
}
```

**Benefits:**
- Each handler's dependencies are declared at the interface boundary — invariants are readable at a glance
- Test setup is minimal: populate three fields, not forty-five
- Handlers are independent: a new command adds a new state slice, not new fields to a shared blob
- The concrete state record can evolve without breaking every handler

---

## Aggregate Design

### The Two Modes: Apply vs Load

All aggregate state transitions happen through two paths:

- **`Apply(event)`** — called during command processing: mutate state via `When()`, validate invariants, record in uncommitted changes.
- **`Load(history)`** — called during rehydration: mutate state via `When()` only, increment `Version`, never record changes.

```csharp
public abstract class AggregateRoot<TId>
{
    public TId Id { get; protected set; }
    public int Version { get; private set; } = -1;  // -1 = no events yet

    private readonly List<object> _changes = new();

    // Command processing path: mutate + validate + record
    protected void Apply(object @event)
    {
        When(@event);
        EnsureValidState();
        _changes.Add(@event);
    }

    // Rehydration path: mutate only, no recording
    public void Load(IEnumerable<object> history)
    {
        foreach (var e in history) { When(e); Version++; }
    }

    protected abstract void When(object @event);
    protected abstract void EnsureValidState();

    public IEnumerable<object> GetChanges() => _changes.AsEnumerable();
    public void ClearChanges() => _changes.Clear();
}
```

`Version` starts at -1. It increments once per loaded event. When saving, the store checks this version for optimistic concurrency — if another writer has appended events since this aggregate was loaded, the save fails and the command retries.

### EnsureValidState: State-Specific Invariants

Invariant rules differ by state. Not all fields are required at all times — they are only enforced at the point of a transition:

```csharp
protected override void EnsureValidState()
{
    var valid = Id != null && OwnerId != null &&
        State switch
        {
            ClassifiedAdState.PendingReview =>
                Title != null && Text != null && Price?.Amount > 0,
            ClassifiedAdState.Active =>
                Title != null && Text != null && Price?.Amount > 0 && ApprovedBy != null,
            _ => true
        };

    if (!valid)
        throw new DomainExceptions.InvalidEntityState(this, $"Post-checks failed in state {State}");
}
```

### Aggregate Repository Contract

```csharp
public interface IAggregateStore
{
    Task<bool> Exists<T, TId>(TId aggregateId);
    Task Save<T, TId>(T aggregate) where T : AggregateRoot<TId>;
    Task<T> Load<T, TId>(TId aggregateId) where T : AggregateRoot<TId>;
}
```

`Save`: get stream name → get uncommitted changes → append with `expectedVersion = aggregate.Version` → clear changes.
`Load`: get stream name → read all events from stream → create blank instance (private constructor) → call `aggregate.Load(events)`.

The only production query that should run against an event store:
```sql
SELECT * FROM EVENTS WHERE AggregateId = @id ORDER BY Version
```

---

## Appliers: Pure Projection Functions

### The Purity Rule

Appliers must be **pure functions**: given the same event and prior state, they always produce the same new state. An impure applier breaks the fundamental ES guarantee — that you can replay the event log at any time and reconstruct write-side state deterministically.

### What Appliers Must Never Do

- Call `DateTime.Now`, `Guid.NewGuid()`, or any non-deterministic function
- Make database calls or cause I/O of any kind
- Evaluate business rules or encode policies (`HasFreeShippingEligibility = total > 50m`)
- Set display-layer fields (formatted strings, labels, UI hints)
- Mutate state in place — return new state via `with` expressions

### What Appliers Must Do

- Project event data onto exactly the state fields command handlers need
- Return new state, not modified old state
- Handle every event type — no-op for events irrelevant to this state slice

```csharp
// WRONG: mutation, display data, business policy, non-determinism
public IHoldCartState Apply(IHoldCartState state, ItemAdded @event)
{
    state.Items.Add(new CartItem(@event.ProductId, @event.Quantity, @event.UnitPrice));
    state.SubtotalDisplay = $"{state.Items.Sum(i => i.UnitPrice * i.Quantity):C}"; // read-side
    state.LastModifiedLabel = $"Updated {DateTime.Now:f}";                         // non-deterministic
    state.HasFreeShippingEligibility = state.Items.Sum(...) > 50m;                 // business policy
    return state;
}

// CORRECT: pure, immutable, minimal
public IHoldCartState Apply(IHoldCartState state, ItemAdded @event) =>
    state with { Items = state.Items.Add(new CartItem(@event.ProductId, @event.Quantity, @event.UnitPrice)) };
```

**If you need a timestamp:** capture it in the event payload at command dispatch time — not by calling `DateTime.Now` during replay.

---

## Events: Facts About the Domain

### Design Principles

Events are facts — immutable recordings of what happened. They are not instructions, not DTOs, not view models.

> "It is absolutely imperative that events always be verbs in the past tense as they are part of the Ubiquitous Language." — Greg Young

**Past tense, always:** `OrderPlaced`, `PaymentCaptured`, `ItemAdded`, `CustomerRelocated`. Not `PlaceOrder`, `CapturePayment`, `AddItem`. The tense matters linguistically: past tense says the domain has no time machine. It happened.

**Capture business intent, not just state change:**
```
WEAKER:  SeatsRemainingChanged { int NewCount }
STRONGER: SeatsReserved { int Quantity, string CustomerName }
```
The intent-focused event enables more projections, meaningful audit trails, and new read models from historical data without changing the write side.

> "Design events to capture the business intent behind each change in addition to the resulting state." — Microsoft

**Events make implicit side effects explicit.** In a CRUD system, "relocating a customer" silently updates a field. In ES, it produces `CustomerRelocated` — a named, versioned, domain concept that other systems can subscribe to.

### Events vs Write-Side State: Where Does ProductName Go?

When a customer adds an item, the event should carry `ProductName` and `ProductCategory` — not write-side state.

```csharp
public record CartItemAdded(
    Guid CorrelationId, Guid CausationId, Guid CartId,
    Guid ProductId,
    string ProductName,       // snapshot of name at time of addition
    string ProductCategory,   // snapshot of category at time of addition
    int Quantity, Money UnitPrice)
    : Event(CorrelationId, CausationId);
```

The event is historically accurate: even if the product catalogue later renames the item, the order history reflects what the customer actually saw. The write-side `IHoldCartState` only carries `ProductId` and `Quantity` if needed for invariant checks. The CartView projection reads name and category directly from the event payload — no catalogue join required.

| Location | What goes here |
|---|---|
| `CartItemAdded` event | ProductName, ProductCategory (snapshot facts) |
| `IHoldCartState` | ProductId, Quantity — only if needed for invariants |
| CartView projection | All display fields, built from event payload |

### No Delete — Use Reversal Transactions

> "It is not possible to jump into the time machine and say that an event never occurred. It is necessary to model a delete explicitly as a new transaction... known as a Reversal Transaction." — Greg Young

Compensating events (`ReservationCancelled`, `OrderRefunded`) preserve the audit trail and show that an object *was* in a prior state at a specific point in time. The append-only constraint also distributes far more easily — fewer locks, better horizontal scaling.

### Events Cannot Be Modified — Versioning Strategies

Events are permanent once written. When domain concepts evolve:

1. **Tolerant deserialization** — consumers ignore unknown fields, use defaults for missing ones. Handles additive non-breaking changes.
2. **Versioned event types** — `Events.V1.ClassifiedAdPublished`, `Events.V2.ClassifiedAdPublished`. Consumers dispatch on version.
3. **Upcasting** — register transformation functions that convert old schemas to current during deserialization. Chain upcasters; application code only handles the latest version. Stored events remain unchanged.
4. **In-place migration** — rewrite historical events in the store. Last resort only — breaks immutability and undermines the audit trail.

```csharp
public class ClassifiedAdUpcasters : IProjection
{
    public async Task Project(object @event)
    {
        switch (@event)
        {
            case ClassifiedAdPublished e:
                var photoUrl = await _getUserPhoto(e.OwnerId);
                var v1Event = new V1.ClassifiedAdPublished
                {
                    Id = e.Id, OwnerId = e.OwnerId, ApprovedBy = e.ApprovedBy,
                    SellersPhotoUrl = photoUrl  // field absent from v0
                };
                // Appended to separate upcasted stream; original stream untouched
                await _store.AppendEvents("UpcastedClassifiedAdEvents", ExpectedVersion.Any, v1Event);
                break;
        }
    }
}
```

---

## Projections

### The Projection Pattern

Projections subscribe to the event stream and build denormalized read documents:

```csharp
public class ClassifiedAdDetailsProjection : IProjection
{
    public Task Project(object @event) =>
        @event switch
        {
            ClassifiedAdCreated e =>
                Create(async () => new ClassifiedAdDetails
                {
                    Id = e.Id.ToString(),
                    SellerId = e.OwnerId,
                    SellersDisplayName = await _getUserDisplayName(e.OwnerId)
                }),
            ClassifiedAdTitleChanged e =>
                UpdateOne(e.Id, ad => ad.Title = e.Title),
            ClassifiedAdPriceUpdated e =>
                UpdateOne(e.Id, ad => { ad.Price = e.Price; ad.CurrencyCode = e.CurrencyCode; }),
            // Cross-aggregate: handles events from UserProfile aggregate
            UserDisplayNameUpdated e =>
                UpdateWhere(x => x.SellerId == e.UserId, x => x.SellersDisplayName = e.DisplayName),
            _ => Task.CompletedTask  // tolerant reader: unknown events are silently ignored
        };
}
```

### ProjectionManager

```csharp
public class ProjectionManager
{
    public async Task Start()
    {
        var position = await _checkpointStore.GetCheckpoint();
        _subscription = _connection.SubscribeToAllFrom(position, settings, EventAppeared);
    }

    private async Task EventAppeared(EventStoreCatchUpSubscription _, ResolvedEvent resolvedEvent)
    {
        if (resolvedEvent.Event.EventType.StartsWith("$")) return; // skip system events
        var @event = resolvedEvent.Deserialize();
        await Task.WhenAll(_projections.Select(x => x.Project(@event)));
        await _checkpointStore.StoreCheckpoint(resolvedEvent.OriginalPosition.Value);
    }
}
```

Subscribes to `$all`. Filters system events. Dispatches to all projections in parallel. Persists checkpoint after each event — on restart, resumes from the saved position.

### Projections Are Rebuildable

The checkpoint + subscription model means any read model can be dropped and rebuilt from position 0. This is a first-class capability: use it when deploying new projections, fixing bugs in existing ones, or adding new read models against historical data.

### Idempotency

Event delivery is at-least-once. Projection handlers must be idempotent:
- Design mutations to be safe to repeat
- Or track the last processed sequence number per handler and skip duplicates

### Cross-Aggregate Projections

A single projection can subscribe to events from multiple aggregates and join data that would require a SQL join in a CRUD system. `ClassifiedAdDetailsProjection` handles both `ClassifiedAd` events and `UserProfile.UserDisplayNameUpdated` — no join query needed at read time.

---

## Streams and Aggregates

### Stream Naming

```
{category}-{aggregateId}
```

Examples: `order-3f2a1b4c`, `customer-9d8e7f6a`, `classified-ad-12345678`.

The `-` separator enables the `$by_category` system projection, which creates `$ce-order`, `$ce-customer` streams automatically — allowing projections to subscribe to all events for an aggregate type without subscribing to `$all`.

Never prefix custom stream names with `$` — reserved for system streams.

### Aggregate ID as the Only Partition Point

> "No matter how many aggregates exist or how they may change structure, the Aggregate ID is the only partition point in the system." — Greg Young

All events for an aggregate go into one stream. The stream is ordered by version. No other partitioning scheme is needed on the write side.

### Optimistic Concurrency

Pass `expectedVersion = aggregate.Version` when appending events. If another command appended since this aggregate was loaded, the append fails. The command handler reloads the aggregate and retries. This is the correct concurrency mechanism — not pessimistic locking.

`ExpectedVersion.Any` skips the check — use only when idempotency is guaranteed at the application level.

### Rolling Snapshots

> "A Rolling Snapshot is a denormalization of the current state of an aggregate at a given point in time... used as a heuristic to prevent the need to load all events for the entire history." — Greg Young

Rules:
- **Develop without snapshotting first.** Add as a performance enhancement once aggregate streams grow large.
- **Store snapshots in a separate table**, not inline in the event stream — prevents concurrency failures when a snapshot is taken while a concurrent write occurs.
- **Use the Memento pattern** for snapshot serialization — insulates the domain from structural changes over time.
- **Snapshots are an optimization, not a replacement for the event stream.** The event stream remains the source of truth.
- Read algorithm: read events backwards onto a stack until you hit a snapshot or the beginning; apply snapshot first; then apply stacked events.

> "It is relatively trivial to achieve one to two orders of magnitude of performance gain." — Greg Young

---

## Event Store vs Message Broker

> "Don't confuse an event store with an eventstream message broker. Message brokers such as Apache Kafka typically lack per-entity stream queries and optimistic concurrency. They work well as a distribution layer to fan out events to projections and external consumers, but they are not a substitute for an event store." — Microsoft

Use both together: the event store holds the canonical append-only log with optimistic concurrency; a message broker fans events out to downstream consumers asynchronously. Avoid two-phase commit between them by having a background process chase the event store's sequence number and publish to the broker.

---

## Testing Event-Sourced Systems

Given-When-Then maps directly to ES:

```csharp
// Given: prior events establish state
var ad = new ClassifiedAd(new ClassifiedAdId(id), new UserId(ownerId));
ad.SetTitle(ClassifiedAdTitle.FromString("Test ad"));
ad.UpdateText(ClassifiedAdText.FromString("Please buy my stuff"));
ad.UpdatePrice(Price.FromDecimal(100.10m, "EUR", currencyLookup));
ad.AddPicture(new Uri("http://localhost/storage/123.jpg"), new PictureSize(1200, 620));

// When: command executes
ad.RequestToPublish();

// Then: assert on resulting state (or events produced)
Assert.Equal(ClassifiedAdState.PendingReview, ad.State);
```

Invariant failures are tested by asserting thrown exceptions:
```csharp
[Fact]
public void Cannot_publish_without_title()
{
    ad.UpdateText(ClassifiedAdText.FromString("Please buy my stuff"));
    ad.UpdatePrice(Price.FromDecimal(100.10m, "EUR", currencyLookup));
    Assert.Throws<DomainExceptions.InvalidEntityState>(() => ad.RequestToPublish());
}
```

No database, no queue, no projections. Pure domain tests.

Also write integration tests for: projection idempotency, schema evolution / upcasting, and checkpoint resume behaviour.

---

## Naming Conventions (from Zimarev's codebase)

| Concept | Convention | Example |
|---------|-----------|---------|
| Events | Past-tense, grouped in static `Events` class | `ClassifiedAdCreated`, `ClassifiedAdTitleChanged`, `PictureAddedToAClassifiedAd` |
| Event versions | Nested version class | `Events.V1.ClassifiedAdPublished` |
| Commands | Imperative verb, versioned in `Contracts.V1` | `Create`, `SetTitle`, `UpdatePrice`, `RequestToPublish` |
| Stream name | `{AggregateName}-{id}` | `ClassifiedAd-<guid>` |
| Read models | Flat class named for use case | `ClassifiedAdDetails`, `PublicClassifiedAdListItem` |
| Query models | `Get` prefix + noun | `GetPublicClassifiedAd`, `GetPublishedClassifiedAds` |
| Application service | `{Aggregate}ApplicationService` | `ClassifiedAdsApplicationService` |

---

## Design Checklist

**Before adding a field to `IHoldState`:**
- [ ] Does a command handler need this to check an invariant?
- [ ] Can it be derived from other state at the call site?
- [ ] Is it a display, formatting, or reporting concern?
- [ ] Is it already in the event payload for read-side use?

**Before writing an applier:**
- [ ] Is it a pure function — no I/O, no non-determinism?
- [ ] Does it return new state via `with`, not mutate in place?
- [ ] Does it avoid encoding business rules or policies?
- [ ] Does every event type have a handler (no-op for irrelevant ones)?

**Before designing a command:**
- [ ] Is it imperative tense?
- [ ] Is it named from the use case, not CRUD?
- [ ] Does it carry only the data needed for this specific operation?
- [ ] Does it include the aggregate ID?
- [ ] Can the domain legitimately reject it? (If not, it may be an event, not a command.)

**Before designing an event:**
- [ ] Is the name past tense?
- [ ] Does it capture business intent, not just a field diff?
- [ ] Is the payload self-describing enough to understand in isolation?
- [ ] Can a projection build its read model from this event without external lookups?
- [ ] Would future projections be able to derive new information from it?

**Before designing a read model:**
- [ ] Is it a flat DTO — no domain objects, no business logic?
- [ ] Is it structured for query/display patterns, not for invariant enforcement?
- [ ] Is every field derivable from the event stream?
- [ ] Is the handler idempotent?

**Before applying CQRS/ES to a bounded context:**
- [ ] Is the domain complex enough to justify the overhead?
- [ ] Are read and write loads genuinely different in scale or shape?
- [ ] Does the team have experience with event-driven systems?
- [ ] Is auditability, historical reconstruction, or retroactive analysis required?

---

## When Not to Use CQRS / Event Sourcing

> "For most systems CQRS adds risky complexity." — Martin Fowler

> "Adopt event sourcing when its benefits, like auditability and historical reconstruction, justify the pattern's complexity. For most systems and most parts of a system, traditional data management is sufficient." — Microsoft

Skip CQRS/ES when:
- The domain is simple CRUD with no meaningful business invariants
- You are building a prototype, MVP, or short-lived system
- The team has no experience with event-driven systems
- Real-time consistency (not eventual consistency) is required
- The data is mostly static or reference data

Apply it selectively: a payment ledger or order-processing pipeline may justify ES. A user-preferences table does not.
