---
name: event-sourcing-cqrs
description: Apply Event Sourcing and CQRS principles — from Greg Young, the EventStore blog, and Alexey Zimarev's Hands-On Domain-Driven Design with .NET Core — when designing write-side state, IHoldState interfaces, applier functions, event payloads, stream structures, aggregate boundaries, or read-side projections. Use when asked about what belongs in state vs events, reviewing an applier for correctness, deciding whether a field is write-side or read-side, sizing an IHoldState interface, designing a new command handler, understanding why write-side state should be minimal, or any CQRS/ES architectural decision. Always activate this skill for ES/CQRS questions rather than relying on general knowledge alone.
---

# Event Sourcing and CQRS (Greg Young, Alexey Zimarev)

Apply this skill for any question about write-side state design, applier correctness, event payload design, stream structure, aggregate boundaries, or the split between write-side and read-side concerns. The principles here are drawn from Greg Young's original CQRS/ES writings, the EventStore blog, and Zimarev's *Hands-On Domain-Driven Design with .NET Core*.

## Core Philosophy

**The event log is the source of truth.** State is a derived projection of events — a read-optimised view computed by replaying the event stream.

> "Current state is a left fold of previous behaviours." — Greg Young

This has a critical corollary: every field in write-side state must be derivable purely from events. If a field cannot be produced by applying events in sequence, it does not belong on the write side.

**CQRS separates the write model from the read model.** Commands flow through the write side (state + domain functions + event persistence). Queries flow through the read side (projections + query store). These are distinct concerns with distinct state shapes.

---

## Write-Side State: Minimal by Design

### The Diagnostic Question

Before adding any field to `IHoldState`, ask:

> *Would a command handler fail or produce incorrect events without this field?*

If no, the field does not belong on the write side. Write-side state has one job: give command handlers the minimum information needed to enforce business invariants.

### What Belongs

- Fields that determine whether a command is valid or invalid
- Fields that prevent duplicate transitions (`IsConfirmed`, `Status`)
- Fields that guard domain rules (`TotalAmount` for refund validation, `Quantity` for stock checks)
- Aggregate lifecycle status

### What Does Not Belong

- Display labels and formatted strings (`SubtotalDisplay`, `LastModifiedLabel`)
- Derived values trivially computable from existing state (`TotalItems = Items.Count`)
- Business policies pre-evaluated at projection time (`HasFreeShippingEligibility`)
- Fields carried for convenience or historical reporting
- Timestamps computed at replay time — non-deterministic, breaks replay

---

## Multiple IHoldState Interfaces

A single aggregate can and should have **multiple focused `IHoldState` interfaces**, each purpose-built for a specific command handler or group of handlers. A 45-field `IHoldOrderState` is a write-side smell.

### Pattern

```csharp
// Focused interface — only what the refund handler needs
public interface IHoldRefundOrderState
{
    OrderStatus Status { get; }
    PaymentReference PaymentReference { get; }
    Money TotalAmount { get; }
}

// Separate applier class replaying the same event stream
// but projecting only the three fields above
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

    // Events irrelevant to refund invariants → no-op appliers
    public IHoldRefundOrderState Apply(IHoldRefundOrderState state, ItemAdded @event) => state;
    public IHoldRefundOrderState Apply(IHoldRefundOrderState state, AddressUpdated @event) => state;
}
```

A `RefundOrderAppliers` class **replays the same Order event stream** but only sets the three fields needed for the refund handler. Events irrelevant to refund processing get no-op appliers. The mechanism is separate applier classes — not the concrete state record implementing multiple interfaces.

### Domain Function Signature

```csharp
public static Seq<IEvent> Refund(
    OrderId id,
    RefundRequest request,
    IHoldRefundOrderState state)   // focused slice, not a 45-field god type
{
    if (state.Status != OrderStatus.Active)
        return Seq(new RefundRejected(...));
    if (request.Amount > state.TotalAmount)
        return Seq(new RefundRejected(...));
    return Seq(new RefundInitiated(...));
}
```

### Benefits

- Each handler's dependencies are declared at the interface boundary — invariants are readable at a glance
- Test setup is minimal: populate three fields, not forty-five
- Handlers are independent: a new command adds a new state slice, not new fields to a shared blob
- The concrete state record can evolve without breaking every handler

---

## Appliers: Pure Projection Functions

### The Purity Rule

Appliers must be **pure functions**: given the same event and prior state, they always produce the same new state. This is non-negotiable. The entire value of event sourcing is that you can replay the event log at any time and reconstruct write-side state deterministically. An impure applier breaks this.

### What Appliers Must Never Do

- Call `DateTime.Now`, `Guid.NewGuid()`, or any non-deterministic function
- Make database calls, trigger I/O, or cause side effects of any kind
- Evaluate business rules or policies (the $50 free-shipping threshold lives in the domain function, not here)
- Set display-layer fields (formatted strings, labels, UI hints belong in read-side projections)
- Mutate state in place — return new state via `with` expressions

### What Appliers Must Do

- Project event data onto exactly the state fields command handlers need
- Handle every event type — no-op appliers for events that don't affect this state slice
- Return new state, not the modified old one

### Corrected Applier

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
    state with
    {
        Items = state.Items.Add(new CartItem(@event.ProductId, @event.Quantity, @event.UnitPrice))
    };
```

**If you need a timestamp,** capture it in the event payload at command dispatch time — not by calling `DateTime.Now` during replay.

---

## Events: Facts About the Domain

### Design Principles

Events are facts — statements about what happened, in past tense. They are not instructions, DTOs, or view models.

**Naming:** Past tense verbs. `OrderPlaced`, `PaymentCaptured`, `ItemAdded`, `RefundInitiated`. Not `PlaceOrder`, `AddItem`, `ProcessRefund`.

**Payload:** Capture the facts needed to understand the event in isolation. Think of each event as a newspaper headline with enough detail to reconstruct what happened.

**Immutability:** Events are never modified after being written. The stream is append-only.

### Events vs Write-Side State: Where Does ProductName Go?

A common question: *should `ProductName` and `ProductCategory` be in the `CartItemAdded` event, or in `IHoldCartState`?*

**In the event.** Events record facts at a point in time — when the customer added this item, the product had this name and category. Capturing that in the event is historically accurate: it creates a snapshot that remains correct even if the product catalogue later changes.

```csharp
public record CartItemAdded(
    Guid CorrelationId,
    Guid CausationId,
    Guid CartId,
    Guid ProductId,
    string ProductName,       // snapshot of name at time of addition
    string ProductCategory,   // snapshot of category at time of addition
    int Quantity,
    Money UnitPrice)
    : Event(CorrelationId, CausationId);
```

The write-side `IHoldCartState` only needs `ProductId` and `Quantity` (if the handler checks for duplicates or quantity limits). Display name and category are read-side concerns — the CartView projection reads them directly from the event payload. No catalogue join needed at query time.

| Location | What goes here |
|---|---|
| `CartItemAdded` event | ProductName, ProductCategory (snapshot facts) |
| `IHoldCartState` | ProductId, Quantity — only if needed for invariants |
| CartView projection | Joins event fields into a queryable read model |

### Facts vs Derived Values

Prefer recording raw facts over pre-computing derived values:

```csharp
// AVOID: stores derived values that change when business rules change
public record OrderTotalled(Money Subtotal, Money Tax, Money GrandTotal, ...)

// PREFER: record raw facts; compute at read time
public record OrderTotalled(Seq<LineItem> Items, TaxRate TaxRate, ...)
```

---

## Event Versioning

Events are immutable once written. Domain concepts change over time:

- **Add a new event version** for breaking schema changes: `OrderPlacedV2`. Never modify an existing event record.
- **Keep old events** in the codebase for backward compatibility; projections handle all versions.
- **Upcasters** can transform old events on read when the old schema is truly obsolete.
- Never break existing event deserialization — streams are permanent records.

---

## Streams and Aggregates

### Stream Naming

```
{category}-{id}
```

Examples: `order-3f2a1b4c`, `customer-9d8e7f6a`, `cart-12345678`. The category is the aggregate type in lowercase. Category-level subscriptions let projections subscribe to all events for a type efficiently.

### Aggregate Boundaries

An aggregate is the **consistency boundary** for a command. Its event stream contains everything needed to reconstruct write-side state for invariant checking. When designing boundaries:

- Keep aggregates narrow — one consistency concern per aggregate
- Avoid aggregates that span multiple business processes
- Large event streams slow replay; snapshots mitigate this but add complexity

### Optimistic Concurrency

Pass the expected stream version when appending events. If another command has written since you read, the append fails and the command retries. This is the correct concurrency mechanism — not pessimistic locking.

---

## Read Side: Projections

### Contract

Read-side projections are:
- **Eventually consistent** — they may lag behind the write side
- **Idempotent** — replaying the same event twice produces the same document
- **Rebuildable** — drop and rebuild from the event stream at any time
- **Read-optimised** — structured for query patterns, not for invariant enforcement

### What Goes Here

Display fields, computed totals, formatted strings, joined data — everything that doesn't pass the diagnostic question belongs in a read-side projection, not in write-side state.

```csharp
public class CartProjection(ICartRepository repository)
    : IHandler<CartItemAdded>
{
    public Task Handle(CartItemAdded @event) =>
        repository.Update(@event.CartId, cart => cart with
        {
            Items = cart.Items.Add(new CartViewItem(
                @event.ProductId,
                @event.ProductName,      // read directly from event payload
                @event.ProductCategory,  // no catalogue lookup needed
                @event.Quantity,
                @event.UnitPrice))
        });
}
```

---

## Design Checklist

**Before adding a field to `IHoldState`:**
- [ ] Does a command handler need this to check an invariant?
- [ ] Is it derivable from other state at the call site?
- [ ] Is it a display, formatting, or reporting concern?
- [ ] Is it already in an event payload for read-side use?

**Before writing an applier:**
- [ ] Is it a pure function — no I/O, no non-determinism?
- [ ] Does it return new state via `with`, not mutate in place?
- [ ] Does it avoid encoding business rules or policies?
- [ ] Does every event type have a handler (no-op for irrelevant ones)?

**Before designing an event:**
- [ ] Is the name past tense?
- [ ] Does it record facts rather than derived values?
- [ ] Is the payload self-describing enough to understand in isolation?
- [ ] Can a projection build its read model from this event without external lookups?
