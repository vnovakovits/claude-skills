---
name: domain-modeling-made-functional
description: Apply Scott Wlaschin's "Domain Modeling Made Functional" (Pragmatic Bookshelf, 2018) — the functional rendering of domain-driven design. Covers making illegal states unrepresentable through algebraic data types, designing workflows as type signatures (Command → AsyncResult<Events, DomainError>), modeling errors as values via the three-track railroad (domain errors / infrastructure errors / panics), single-case wrappers for primitive obsession, choice-of-states for aggregates, DTO-to-domain translation at bounded-context edges, persistence ignorance via functional-core/imperative-shell, dependency rejection (passing dependencies as functions instead of interfaces), and workflow composition by chaining typed steps. Use when designing a new domain workflow / aggregate / API endpoint in a typed language (F#, Scala, Kotlin, TypeScript, C# with records + LanguageExt); when reviewing a domain model and asking whether its invariants are encoded in the type system vs in runtime guards; when refactoring exception-based domain code to errors-as-values; when explaining "make illegal states unrepresentable" or "workflows as type signatures"; when looking at a record bristling with `Option<>` and sibling-exclusive bools and wondering if it should be a sum type; when a team uses OO DDD (Evans/Vernon) but wants to lean into the type system. Strong complement to `domain-driven-design`, `hexagonal-clean-architecture`, and `clean-code` — those handle the organizational and strategic side, this skill handles the type-encoding side. Skip for dynamically-typed codebases (Python, Ruby, vanilla JS) where the techniques don't have a compiler to back them; for strategic-DDD questions about bounded contexts and ubiquitous language (use `domain-driven-design`); for pure OO pattern questions (use `solid-principles`, `responsibility-driven-design`).
---

# Domain Modeling Made Functional

Scott Wlaschin's book is functional DDD: the same domain-modeling instinct as Evans/Vernon, applied with the rigor of a strong static type system. The thesis: **most domain bugs are illegal states the type system was never told to forbid.** Encode the constraints in types and the compiler becomes your domain expert.

The book uses F#, but every principle translates. C# with records + LanguageExt, Scala, Kotlin, TypeScript with discriminated unions — all work. Examples below favor C# since that's where most readers will land.

## Core philosophy

> "Make illegal states unrepresentable."  
> — Yaron Minsky, quoted by Wlaschin as the book's north star

You can encode a domain rule in three places:

1. **Runtime check** — `if (status == "Paid") throw...`. Cheapest, weakest. Fails only when exercised, only when a developer remembered to write the guard.
2. **Test** — captures the rule once. Drifts from the code. Only fires if the test is written and runs.
3. **Type** — the compiler enforces it on every line, in every PR, forever. Free, always-on, can't be bypassed.

Wlaschin's instinct is to push as much as possible from (1) and (2) up to (3). When you do, whole categories of bug — "what if status is paid but price is null?", "what if both quote and schedule are missing?", "what if someone passes a `Guid` from a different aggregate?" — become uncompileable.

## Make illegal states unrepresentable

### Wrap primitives in single-case types

`Guid`, `string`, `int` carry no domain meaning. Wrap them so the compiler enforces what they are.

F#:
```fsharp
type CustomerId = CustomerId of Guid
type EmailAddress = private EmailAddress of string
```

C#:
```csharp
public record CustomerId(Guid Value);

public record EmailAddress
{
    public string Value { get; }
    private EmailAddress(string v) { Value = v; }
    public static Either<Error, EmailAddress> Create(string raw) =>
        raw.Contains('@') ? Right(new EmailAddress(raw)) : Left(Error.New("not an email"));
}
```

The compiler now refuses to mix a `CustomerId` with an `OrderId`, or to construct an `EmailAddress` from arbitrary text. The factory is the only entry point — every `EmailAddress` in the system is necessarily valid by construction. The validator runs once at the boundary; nobody downstream needs to re-check.

### Sum types for state-dependent shapes

The textbook anti-pattern: one record with lots of `Option<>` and bools, where which fields are populated depends on the state.

```csharp
// Bad: optional fields encode state, but the compiler can't enforce coherence.
public record Order(
    OrderId Id,
    Option<DateTime> ValidatedAt,
    Option<Money> Price,
    Option<DateTime> PaidAt,
    Option<PaymentRef> Payment);
// Did "Paid but not Priced" just happen? Compiler shrugs.
// "Validated with no lines"? Sure, why not.
```

```csharp
// Better: each state is its own type with only the fields valid in that state.
public abstract record Order
{
    public sealed record Unvalidated(OrderId Id, Seq<RawLine> Lines)                                 : Order;
    public sealed record Validated  (OrderId Id, Seq<ValidatedLine> Lines)                           : Order;
    public sealed record Priced     (OrderId Id, Seq<PricedLine> Lines, Money Total)                 : Order;
    public sealed record Paid       (OrderId Id, Seq<PricedLine> Lines, Money Total, PaymentRef P)   : Order;
}
```

`Order.Paid` requires a `PaymentRef`. You cannot construct a paid order without payment. State machines are no longer a runtime convention — they're enforced by `record` constructors.

### Algebraic data types

- **Product types** (records, tuples) — combine fields with AND. `Address = Street AND City AND ZipCode`.
- **Sum types** (discriminated unions / sealed hierarchies) — choose between alternatives with OR. `PaymentMethod = Cash OR Card OR BankTransfer`.

Prefer many small precise types over one big optional-laden type. When you find yourself writing `record Foo(Option<A>, Option<B>, Option<C>, bool D)` — stop. There's a sum type hiding in there.

## Workflows as type signatures

Wlaschin's central design move: **write the workflow's type signature first.** The signature *is* the design.

F#:
```fsharp
PlaceOrder :
    CheckProductExists                  // dependency
    -> CheckAddressExists               // dependency
    -> GetProductPrice                  // dependency
    -> CreateOrderAcknowledgment        // dependency
    -> SendOrderAcknowledgment          // dependency
    -> PlaceOrderCommand
    -> AsyncResult<PlaceOrderEvent list, PlaceOrderError>
```

Read top-down: this workflow takes five capabilities, then a command, and returns an async result that is either a list of domain events or a typed domain error. Every collaborator and every outcome is named. No surprises.

The C#/LanguageExt rendering:
```csharp
public interface IPlaceOrder
{
    Aff<Either<PlaceOrderError, Seq<PlaceOrderEvent>>> Handle(PlaceOrderCommand command);
}
```

Then implement step by step, each step a total function whose type fits the next step's input:

```
validateOrder : UnvalidatedOrder -> AsyncResult<ValidatedOrder, ValidationError>
priceOrder    : ValidatedOrder   -> Result<PricedOrder, PricingError>
acknowledge   : PricedOrder      -> Async<PricedOrder>
createEvents  : PricedOrder      -> Seq<PlaceOrderEvent>
```

Each step's output type matches the next step's input. The pipeline of types is the workflow.

## Errors as values: the three-track railroad

Three kinds of failure, and they belong on different tracks:

1. **Domain errors** — *expected* outcomes. "Order rejected because address is invalid." "Insufficient funds." "Quote no longer available." These are part of the spec. They belong in the `Result` return type as a sum of specific named cases.
2. **Infrastructure errors** — IO failed. Database unreachable. HTTP timeout. Orthogonal to the domain. Propagate as effects (`Async`, `Aff`, `IO`); retry/circuit-break at the imperative shell.
3. **Panics** — bugs. "This should never happen." Index out of bounds. Null where the contract said non-null. Let them throw — exceptions are the correct tool for *unrecoverable programmer errors*.

The most common mistake is conflating (1) and (3). Throwing for "order rejected" turns the rejection into an out-of-band signal the caller has to guess about. Returning `Either<AddressInvalid, Order>` makes the rejection part of the contract.

```csharp
// Bad: caller has no idea what can throw or why.
public Order PlaceOrder(UnvalidatedOrder o) { ... throw new InvalidAddressException(); ... }

// Good: signature lists the failure modes by name.
public Either<PlaceOrderError, Order> PlaceOrder(UnvalidatedOrder o);

public abstract record PlaceOrderError
{
    public sealed record AddressInvalid(string Reason)        : PlaceOrderError;
    public sealed record ProductOutOfStock(ProductId Id)      : PlaceOrderError;
    public sealed record PaymentDeclined(string Reason)       : PlaceOrderError;
}
```

Now every caller pattern-matches on `PlaceOrderError`. Adding a new failure mode breaks every caller until they handle it — exactly what you want.

## Total functions

A *total* function handles every input. A *partial* function blows up on some inputs (throws, returns null, hangs).

Wlaschin's rule: domain functions must be total. The compiler helps by:

- **Pattern-matching exhaustively** on sum types (compiler warns on missing cases).
- **Returning `Either`/`Option`** instead of throwing for "no answer".
- **Wrapping primitives** so invalid inputs can't be constructed in the first place.

```csharp
// Bad: partial. Some statuses panic silently when the enum grows.
string Describe(OrderStatus s) => s switch
{
    OrderStatus.Draft => "draft",
    OrderStatus.Paid  => "paid"
    // Cancelled added later — what does this return? Default? Throw?
};

// Good: exhaustive. Compiler warns if a case is added later.
string Describe(OrderStatus s) => s switch
{
    OrderStatus.Draft     => "draft",
    OrderStatus.Paid      => "paid",
    OrderStatus.Cancelled => "cancelled",
};
```

For C# enums you'll need the `_ => throw new UnreachableException()` fallthrough — that's a genuine panic for the "new-enum-case-was-added-but-we-forgot-this-switch" bug. For sum types (sealed record hierarchies), exhaustiveness is enforced by the language.

## DTOs at the boundary, domain types in the core

Serialization-friendly types and domain-constrained types are different jobs.

```
JSON/XML/SQL ─[DTO]─► Validate/Parse ─[Domain Type]─► Workflow ─► Events ─[DTO]─► JSON/Bus
```

- **DTOs**: `Guid Id`, `string Email`, `decimal? Amount`, nullable everywhere. They round-trip through serialization without complaint.
- **Domain types**: `OrderId`, `EmailAddress`, `Money`, non-null. They cannot represent an invalid state.
- **Translation functions** at the boundary: `DtoToDomain : OrderDto → Either<ValidationError, Order>` and `DomainToDto : Order → OrderDto`.

The domain never sees a raw DTO. By the time data is past the boundary, it is *certified* valid. Validation lives at exactly one place — the parser. Everything inside trusts it.

## Functional core, imperative shell — and dependency rejection

Wlaschin's rendering of hexagonal/ports-and-adapters:

```
┌─────────────── Imperative Shell ───────────────┐
│  HTTP / DB / Bus / Files / Clock                │
│  ┌────── Functional Core ──────┐                │
│  │  Pure workflow functions:   │ ← dependencies │
│  │  Command → Events           │   passed in as │
│  │  No IO. No throwing.        │   functions    │
│  └─────────────────────────────┘                │
└─────────────────────────────────────────────────┘
```

**Dependency rejection** (Wlaschin's coinage, contra "injection"): instead of injecting an *interface* that the domain depends on, pass the *function the domain needs* as a parameter. The domain doesn't even know an interface exists.

```csharp
// OO style: domain knows about IPricingService.
public class PlaceOrder(IPricingService pricing) { ... }

// Functional style: domain takes the function it needs.
public static class PlaceOrder
{
    public static Either<Error, PricedOrder> Run(
        Func<ProductId, Money> getPrice,   // ← passed in
        ValidatedOrder order) => ...;
}
```

The domain layer has no `IPricingService` interface. It has a function shape. The imperative shell wires a concrete implementation at the boundary. The domain stays maximally portable and trivially testable — pass a lambda in the test, you're done.

## Workflow composition

Once each step has a clean type signature, composition is trivial:

F#:
```fsharp
let placeOrder =
    validateOrder
    >> Result.bind priceOrder
    >> Result.bind sendAcknowledgment
    >> Result.map createEvents
```

In C#/LanguageExt the LINQ syntax for `Either`/`Aff` gives the same shape:

```csharp
Aff<Either<PlaceOrderError, Seq<PlaceOrderEvent>>> PlaceOrder(PlaceOrderCommand cmd) =>
    from validated  in ValidateOrder(cmd)
    from priced     in PriceOrder(validated)
    from _          in SendAcknowledgment(priced)
    select CreateEvents(priced);
```

Failures short-circuit. The workflow reads as the design.

## Commands in, events out

Each workflow:

- **Input**: a `Command` record (one type per use case, carrying everything the workflow needs).
- **Output**: a sequence of `Event` values, typically a sum type with one case per event kind, wrapped in `Either` for domain failures and `Async`/`Aff` for effects.

```csharp
public record PlaceOrderCommand(CustomerId CustomerId, Seq<RawOrderLine> Lines, Address ShipTo);

public abstract record PlaceOrderEvent
{
    public sealed record OrderPlaced       (OrderId Id, Money Total)                 : PlaceOrderEvent;
    public sealed record ShippingScheduled (OrderId Id, Date EstimatedDelivery)      : PlaceOrderEvent;
    public sealed record CustomerCharged   (OrderId Id, Money Amount)                : PlaceOrderEvent;
}
```

The sum type lists *every* possible outcome. New event? Add a case, the compiler tells you everywhere that needs to handle it.

## State as a choice of states

Rather than one big mutable record with many optionals, model the aggregate as a discriminated union of *states*, each carrying only what's valid then:

```csharp
public abstract record Cart
{
    public sealed record Empty (CustomerId C)                                                : Cart;
    public sealed record Active(CustomerId C, NonEmptyList<CartLine> Lines)                  : Cart;
    public sealed record Locked(CustomerId C, NonEmptyList<CartLine> Lines, LockReason Why)  : Cart;
}
```

`Cart.Active` carries `NonEmptyList<CartLine>` — you cannot have an "Active" cart with zero lines, by construction. Locked carts carry a reason; empty carts don't. The shape of valid data and the shape of states are aligned.

This is the highest-leverage application of "illegal states unrepresentable": you encode the state machine in the type, and every operation that consumes the aggregate must pattern-match on which state it's in — which means it physically cannot ignore a state.

## Review checklist

When applying this lens to an existing design, ask:

1. **Are primitives wrapped?** Every `Guid`, `string`, `int` carrying domain meaning should have a name. `(Guid sourceId, Guid customerId)` is a primitive-obsession bug waiting to happen — swap two arguments and the compiler shrugs.
2. **Are sum types used for OR-states?** Look for records bristling with `Option<>` or sibling-exclusive bools — those are sum types in disguise. Same for tuple returns where only some combinations are legal.
3. **Does the workflow have a named, total type signature?** `Command → AsyncResult<Events, DomainError>`. Is the failure type a discriminated union of *specific* domain failures, or a generic `Error`/`Exception`? Specific is better — it tells the caller every way the workflow can refuse.
4. **Are domain errors values, not exceptions?** Grep for `throw` inside the domain. Each one is either a panic (fine, but make sure it's *truly* unreachable) or a domain failure that should become a `Result` case.
5. **Are dependencies passed as functions, not interfaces?** The domain layer should have no infrastructure interfaces. Functions in, events out. If the domain references `IRepository<>`, the abstraction is leaking.
6. **Are DTOs and domain types distinct?** If the API request type and the domain type are the same record, the validation/translation layer is missing — and either the DTO is too constrained or the domain is too loose.
7. **Are partial functions caught?** Pattern matches that don't cover every case. Methods that throw for "shouldn't happen". `default!` and `null!` everywhere. Each one is a question the type system isn't being asked.
8. **Could a tuple-of-Options be a sum type?** `(Option<A>, Option<B>)` has four states: (None,None), (Some,None), (None,Some), (Some,Some). If only two or three are legal — or if each combination means something semantically different — model the legal subset as a sum type. The compiler then forces every caller to handle every case.
9. **Are state-changing functions pure?** Domain functions take state in, return new state (or events) out. No `void` mutation. No `DateTime.UtcNow` inline — pass `now` as a parameter so tests can fix it.
10. **Does the state itself encode its lifecycle?** If `Order` is one record with `Option<PaidAt>` and `Option<CancelledAt>` and `Option<ShippedAt>` — those are states. Model them.

A "yes" to all of these means the design is in good Wlaschin shape. Anywhere you answer "no", there's a class of bugs the type system isn't catching yet.

## When to use this skill vs related ones

| Question | Skill |
|---|---|
| "What are the bounded contexts here?" / "What's the ubiquitous language?" | `domain-driven-design` (Evans/Vernon — strategic DDD) |
| "How do these objects collaborate?" / "Who owns this responsibility?" | `responsibility-driven-design` |
| "Where does this dependency live? Domain or infrastructure?" | `hexagonal-clean-architecture` |
| "Should this class have only one reason to change?" | `solid-principles` |
| "How do I model this aggregate so invalid states can't be constructed?" | **this skill** |
| "Should I throw, or return a Result, here?" | **this skill** |
| "How do I structure this workflow as a type signature first?" | **this skill** |
| "How do I refactor this exception-heavy code?" | **this skill** |
| "This record has eight optional fields and I'm losing track of the legal combinations." | **this skill** |

Wlaschin's perspective overlaps DDD but adds the type-driven angle. Use this skill when the *encoding of invariants* is the question. Use the others when the *organization of concepts* or the *placement of code* is the question.

## Further reading

- Scott Wlaschin, *Domain Modeling Made Functional* (Pragmatic Bookshelf, 2018) — the book.
- F# for Fun and Profit (fsharpforfunandprofit.com) — Wlaschin's site, with the "Designing with types" series and "Railway-oriented programming" essay that became chapters of the book.
- Mark Seemann's writing on `IO<>`-typed boundaries and functional architecture in C# — a practical bridge for .NET shops on the OO-to-functional path.
