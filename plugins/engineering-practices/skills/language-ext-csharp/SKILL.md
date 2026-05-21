---
name: language-ext-csharp
description: Apply the LanguageExt functional programming library for C# (LanguageExt 4.x — the `Aff<T>` / `Eff<T>` era, before LanguageExt 5's `K<F, A>` redesign). Covers the core types (`Option<T>`, `Either<L,R>`, `Validation<F,T>`, `Fin<T>`, `Aff<T>`, `Eff<T>`, `Seq<T>`, `Map<K,V>`, `Lst<T>`, `Set<T>`); idiomatic C# patterns for null-elimination, errors-as-values, applicative vs monadic composition, async effect chaining via LINQ-from, pattern matching with named arguments, the Prelude shortcut imports, and the railway-oriented programming style; common pitfalls (`ValueUnsafe`, mixing nulls with Option, calling `.Run()` on the wrong thread); and how LanguageExt's surface differs between v3 / v4 / v5. Use this skill when reading, writing, or reviewing C# code that uses LanguageExt — including any code touching `Option<>`, `Either<>`, `Validation<>`, `Aff<>`, `Eff<>`, `Seq<>`; when seeing `using static LanguageExt.Prelude;` in a file; when the code has `from … in … select …` over non-LINQ-collection types; when debugging async effects or composing repository calls; when a developer is new to LanguageExt and needs to know the idiomatic version of a familiar pattern (null-check, try/catch, Task<T>); when choosing between `Either` and `Validation` for error handling; when deciding whether to use `Match`, `Bind`, `Map`, or `Apply`. Complements `domain-modeling-made-functional` (DMMF is the design lens, this skill is the C#-specific mechanics) and `clean-code` (use both when refactoring imperative code into the functional style). Skip if the code does not import LanguageExt and you are not migrating it; skip for pure F# / Scala / Kotlin questions (LanguageExt is a C# library).
---

# LanguageExt in C# (4.x)

LanguageExt brings functional types to C#. Olive uses it extensively to encode nulls (`Option<T>`), error tracks (`Either<L,R>`, `Validation<F,T>`), async effects (`Aff<T>`), and immutable collections (`Seq<T>`). This skill captures the mechanical idioms — what to import, what to write, what to avoid — for the LanguageExt 4.x era.

Version note: this skill targets **LanguageExt 4.x**, where async effects are `Aff<T>` and sync effects are `Eff<T>`. LanguageExt 5 reworks the abstraction into `K<F, A>` and renames much of the surface; the conceptual model carries over but the syntax doesn't. If a file you're looking at uses `Aff` / `Eff` / `Prelude.SuccessAff`, you're on 4.x and this skill applies directly.

## Core types

### `Option<T>` — "this value may not exist"

The first line of defense against `null`. An `Option<T>` is either `Some(value)` or `None` — never `null`.

```csharp
using LanguageExt;
using static LanguageExt.Prelude;   // brings Some / None / Optional / etc. into scope

Option<string> found   = Some("Alice");
Option<string> missing = None;
Option<string> maybe   = Optional(possiblyNullString);   // null -> None, non-null -> Some
```

Consume with `Match` (preferred), `IfSome` / `IfNone`, or LINQ syntax:

```csharp
var greeting = found.Match(
    Some: name => $"Hello, {name}",
    None: () => "Hello, stranger");

found.IfSome(name => Console.WriteLine(name));
var name = missing.IfNone("default");
```

Transform with `Map` (apply to inner value) and `Bind` (apply a function that itself returns `Option<>`):

```csharp
Option<int> length = found.Map(s => s.Length);                 // Option<string> -> Option<int>
Option<User> user  = userId.Bind(id => repository.Find(id));   // Option<Guid> -> Option<User>
```

### `Either<L, R>` — "success or failure" (typed failure)

Two-track railway: `Right(value)` for success, `Left(error)` for failure. By convention, `R` is the success type. The error type is part of the signature — callers see exactly what can go wrong.

```csharp
public Either<DomainError, Order> PlaceOrder(UnvalidatedOrder o) { ... }

var result = PlaceOrder(o);
var status = result.Match(
    Right: order => $"Placed #{order.Id}",
    Left:  error => $"Rejected: {error.Message}");
```

`Map` transforms the Right side; `MapLeft` transforms the Left side; `Bind` chains another `Either`-returning operation (short-circuits on Left). `BiMap` transforms both sides at once.

### `Validation<F, T>` — like Either but **accumulates** failures

`Either<>` short-circuits on the first error; `Validation<>` collects every error so you can report them all at once. Use it for input parsing and multi-field validation where the user wants the full list.

```csharp
public static Validation<Error, Order> Parse(OrderDto dto) =>
    (ParseEmail(dto.Email),
     ParseAddress(dto.Address),
     ParseLines(dto.Lines))
        .Apply((email, addr, lines) => new Order(email, addr, lines));
```

If all three parses succeed → `Success` carrying an `Order`. If any fail → `Fail` carrying every error that fired. The trick is **`Apply` (applicative composition)** rather than `Bind` (monadic short-circuit). LINQ `from` on `Validation<>` does monadic composition — use `Apply` or `.Apply(…)` chains when you want both errors.

### `Fin<T>` — the result of running an effect

`Aff<T>.Run()` returns `Fin<T>` — essentially `Either<Error, T>` with `Succ` / `Fail` cases. You'll see it as the boundary between functional and imperative code.

```csharp
Fin<int> outcome = await myAff.Run();
return outcome.Match(
    Succ: value => Ok(value),
    Fail: error => StatusCode(500, error.Message));
```

### `Aff<T>` — async effect with built-in error track

`Task<T>` blended with `Either<Error, T>`. Replaces `Task<T>` + try/catch + bespoke result types in the imperative style. Errors are part of the type; nothing throws across an `Aff` boundary unless it's a panic.

```csharp
Aff<Customer> getCustomer = customerRepository.Read(id);   // returns Aff<Customer>

Aff<Seq<IEvent>> workflow =
    from id     in Parser.Parse(rawId).ToAff(Error.Many)
    from state  in shipmentRepository.Read(id).ToAff()
    from events in shipmentRepository.UpdateAff(id, s => DraftShipment.Foo(s))
    select events;

Fin<Seq<IEvent>> result = await workflow.Run();
```

Constructors:
- `SuccessAff(value)` — already-succeeded effect.
- `FailAff<T>(Error.New("..."))` — already-failed effect.
- `Aff(async () => …)` — wrap an async lambda.
- `myTask.ToAff()` — adapt a `Task<T>`.
- `someValidation.ToAff(Error.Many)` — adapt a `Validation<Error, T>`.
- `someEither.ToAff()` — adapt an `Either<Error, T>`.

`RetryWhile(Schedule.recurs(n), shouldRetry)` is the LanguageExt-native retry combinator — far cleaner than imperative retry loops.

### `Eff<T>` — sync effect with built-in error track

Same as `Aff<T>` but for synchronous code. Use when the operation doesn't need to await anything but you still want errors-as-values.

### `Seq<T>` — immutable sequence

The default LanguageExt sequence type. Cheaper than `List<T>` for chained operations; immutable; structurally compared.

```csharp
Seq<int> xs = Seq(1, 2, 3);
Seq<int> empty = LanguageExt.Seq<int>.Empty;
Seq<int> doubled = xs.Map(x => x * 2);
Seq<int> evens = xs.Filter(x => x % 2 == 0);
Option<int> first = xs.Find(x => x > 1);
Option<int> head = xs.HeadOrNone();
```

Use `Seq<T>` over `List<T>` / `IEnumerable<T>` when you want immutability and to participate in LanguageExt LINQ chains.

### `Lst<T>`, `Map<K,V>`, `Set<T>`, `HashMap<K,V>`, `HashSet<T>`

Immutable persistent collections. `Lst<T>` is a singly-linked list; `Map<K,V>` is a balanced tree map; `HashMap<K,V>` is a hash map. All immutable, all share structure on updates (`map.Add(k, v)` returns a new map without copying the whole thing).

## The Prelude

`using static LanguageExt.Prelude;` is the **single most important import** in any LanguageExt file. It brings the shortcut functions into scope: `Some`, `None`, `Right`, `Left`, `Success<E,T>`, `Fail<E,T>`, `Optional`, `Seq`, `Set`, `Map`, `Lst`, `unit`, `SuccessAff`, `FailAff`, and many more.

Without it you'd write `LanguageExt.Prelude.Some(x)`. With it you write `Some(x)`. Always add it.

If you also need LINQ extensions on these types, also `using LanguageExt;`.

## LINQ for monadic composition

LINQ's `from … select …` syntax works on **any** LanguageExt monad — `Option`, `Either`, `Validation`, `Aff`, `Eff`, `Try`, `IO`, `Lst`, `Seq`. The semantics: each `from` is a monadic bind. Failures short-circuit.

```csharp
// Option
var fullAddress =
    from street  in Optional(maybeStreet)
    from city    in Optional(maybeCity)
    from country in Optional(maybeCountry)
    select $"{street}, {city}, {country}";   // Option<string>; None if any is None

// Aff (Olive's most common shape)
var workflow =
    from id     in Parser.Parse(rawId).ToAff(Error.Many)
    from state  in shipmentRepository.Read(id).ToAff()
    from events in shipmentRepository.UpdateAff(id, ApplyDomainOp)
    from _      in eventPublisher.Publish(events).ToUnit().ToAff()
    select events;
```

The pattern: **each line is one named effect**; the whole block reads as a workflow. Use `let` for pure intermediate computations:

```csharp
var workflow =
    from raw in Source()
    let trimmed = raw.Trim()
    from validated in Validate(trimmed)
    select validated;
```

## Applicative composition: collecting errors

LINQ binds short-circuit. For **collecting** errors (typically with `Validation<>`), use **applicative** composition via `Apply` or tuple `.Apply(…)`:

```csharp
// SHORT-CIRCUITS at first failure — only the first error reported.
var parsed =
    from email   in ParseEmail(dto.Email)
    from address in ParseAddress(dto.Address)
    select new Order(email, address);

// COLLECTS all failures — every error reported in one shot.
var parsed =
    (ParseEmail(dto.Email),
     ParseAddress(dto.Address))
        .Apply((email, address) => new Order(email, address));
```

Rule of thumb:
- **Each step depends on the previous one**: use LINQ (monadic). The downstream step needs the upstream value to even attempt.
- **Steps are independent**: use `Apply` (applicative). Both should always run and any errors should aggregate.

## Pattern matching: prefer named arguments

`Match` takes positional `(succ, fail)` or named `(Succ: …, Fail: …)` arguments. **Named is more readable**; use it.

```csharp
result.Match(
    Succ: value => Ok(value),
    Fail: error => StatusCode(500, error.Message));

option.Match(
    Some: x => $"Got {x}",
    None: () => "empty");

either.Match(
    Right: r => HandleRight(r),
    Left:  l => HandleLeft(l));
```

## Common idioms

### Adapt nullable to Option

```csharp
Option<string> maybeName = Optional(dto.Name);            // null -> None
Option<DateTime> maybeDate = Optional(record.DueDate);    // null -> None for reference types and nullable value types
```

### Adapt `Task<T>` / `Validation<>` / `Either<>` to `Aff<T>` (so they compose in a LINQ workflow)

```csharp
from id      in Parser.Parse(rawId).ToAff(Error.Many)     // Validation -> Aff
from state   in shipmentRepository.Read(id).ToAff()       // Task<T?> -> Aff<Option<T>>, depending on impl
from result  in someEither.ToAff()                        // Either<Error, T> -> Aff<T>
```

`.ToAff(Error.Many)` is the magic call that turns a `Validation<Error, T>` into an `Aff<T>` where any failures become an `Aff` error.

### Chain an Aff that needs a value plus a side-effect

```csharp
var workflow =
    from events in shipmentRepository.UpdateAff(id, ApplyDomain)
    from _      in eventPublisher.Publish(events).ToUnit().ToAff()
    select events;
```

`ToUnit()` discards a return value when you only care about the effect.

### Running an Aff at the boundary

```csharp
Fin<T> result = await myAff.Run();
return await result.Match(
    Succ: value => Task.FromResult(Ok(value)),
    Fail: error => failureResultBuilder.HandleFailureAsync(...));
```

`.Run()` is the boundary — call it once, at the top of the workflow, where you bridge to imperative code (controller, handler).

### Constructing Seq

```csharp
Seq<int> xs   = Seq(1, 2, 3);
Seq<int> none = LanguageExt.Seq<int>.Empty;
Seq<int> one  = Seq1(42);                  // single-element Seq
```

`Seq1(x)` is shorter than `Seq(x)` for a single element and prevents the array-of-one allocation.

### Constructing Map / Set

```csharp
Map<string, int> m = Map(("a", 1), ("b", 2));
Set<int> s = Set(1, 2, 3);
```

### Filtering + extracting in one pass

```csharp
Seq<int> validIds = ids.Map(ParseInt).Somes();   // Seq<Option<int>>.Somes() -> Seq<int>
```

`.Somes()` collapses an `IEnumerable<Option<T>>` into the `T` values where present. Useful idiom.

## The "Execute" pattern (Olive-specific)

Olive has a recurring pattern for validating domain operations:

```csharp
state.Execute(
    guardFunc:   s => MyValidator.Validate(s, input),     // Validation<Error, Unit>
    domainAction: () => Seq<IEvent>(new SomethingHappened(...)),
    rejectionAction: (reasons, codes) => Seq<IEvent>(new SomethingRejected(reasons, codes)));
```

This is `state.Execute` from `StateExtensions` — it runs the guard, and if validation passes calls `domainAction`; otherwise calls `rejectionAction` with the accumulated reasons and outcome codes. It's a thin wrapper over `Validation<Error, Unit>.Match` that returns the right event sequence.

Use it when a domain operation has both a success event and a rejection event with the same outcome shape.

## Common pitfalls

### `ValueUnsafe()` is a code smell

`Option<T>.ValueUnsafe()` (and `Either<L,R>.LeftUnsafe()` / `.RightUnsafe()`) bypass the type system. If the option is `None`, `ValueUnsafe()` returns `default(T)` — `null` for reference types — which is exactly the bug Option exists to prevent. Use `Match` or `IfNone` instead.

The only legitimate use: a context where you've **just verified** the value is `Some` via pattern matching and need to extract for ergonomic reasons. Even then, restructuring the code is usually better.

### Don't mix nullable and Option

If a method takes `Option<T>`, the caller's value should already be an `Option<T>`. Don't pass `Optional(maybeNull)` deep into business logic — convert at the boundary.

### Don't use `.IsSome` / `.Value` for branching

```csharp
// Bad: imperative pattern leaks through
if (option.IsSome) {
    var value = option.Value;
    // ...
}

// Good: functional shape
option.Match(
    Some: value => { /* ... */ },
    None: () => { /* ... */ });
```

`.IsSome` is fine for assertions in tests; not for branching in production code.

### Pick the right error monad

- `Either<L, R>` — single failure, short-circuit. Use for workflows.
- `Validation<F, T>` — collect every failure. Use for input parsing.
- Mixing them up gives surprising behavior. If you find yourself wanting to *both* short-circuit *and* collect, you probably need two layers (parse with `Validation`, then bind to a workflow with `Either` / `Aff`).

### `Aff<T>` is not `Task<T>`

They look alike in code (both used with `await`), but `Aff<T>` has a built-in error track. Don't:

- Call `.Run().Result` synchronously — blocks and may deadlock.
- Throw exceptions in an `Aff` for domain errors — use `FailAff`.
- Wrap a failing `Task` and expect the exception to propagate as a regular C# exception — it becomes the `Aff` error track.

Always `await aff.Run()` at the boundary, then pattern-match the `Fin<T>`.

### Forgetting `using static LanguageExt.Prelude;`

Without it: `LanguageExt.Prelude.Some(x)`. With it: `Some(x)`. If you see verbose `LanguageExt.Prelude.` prefixes everywhere, that's the missing import.

### `Optional(x)` where `x` is not nullable

`Optional` only makes sense for **nullable inputs** — `T?`, `Nullable<T>`, reference types. If `x` is `int`, `Optional(x)` always returns `Some(x)` — pointless. Use `Some(x)` directly.

### Imports for LINQ extensions

For LINQ syntax over `Option` / `Either` / `Aff`, you generally need both:

```csharp
using LanguageExt;
using static LanguageExt.Prelude;
```

Without `using LanguageExt;` the extension methods that power `SelectMany` / `Select` for these types won't resolve, and you'll get cryptic compiler errors about "no overload for `Select`".

### Disambiguating `Seq<T>`

`LanguageExt.Seq<T>` collides with `System.Net.Mail.Seq` and a few other names. If the compiler complains:

```csharp
LanguageExt.Seq<T>.Empty
```

or alias at the top of the file:

```csharp
using LSeq = LanguageExt.Seq;
```

## Choosing between types

| You want… | Use |
|---|---|
| "This might be missing." | `Option<T>` |
| "This might fail; one error matters." | `Either<L, R>` |
| "This might fail; show every error." | `Validation<F, T>` |
| "Async with a typed failure." | `Aff<T>` |
| "Sync with a typed failure (no `await`)." | `Eff<T>` |
| "Result of running an effect." | `Fin<T>` |
| "Immutable sequence." | `Seq<T>` |
| "Immutable map / dict." | `Map<K,V>` or `HashMap<K,V>` |
| "Immutable set." | `Set<T>` or `HashSet<T>` |

## When to use this skill vs related ones

| Question | Skill |
|---|---|
| "How should I model this aggregate so invalid states can't be constructed?" | `domain-modeling-made-functional` |
| "Should I throw or return Result here?" | `domain-modeling-made-functional` |
| "How do I write idiomatic Option / Either / Aff code in this C# file?" | **this skill** |
| "What does `.ToAff(Error.Many)` do?" | **this skill** |
| "Why do my error messages get lost in this LINQ chain?" | **this skill** (monadic vs applicative) |
| "How do I refactor this null-check pyramid?" | **this skill** + `clean-code` |
| "What's the cleanest way to compose 5 repository calls in a row?" | **this skill** (LINQ-from over Aff) |
| "Should this class have only one reason to change?" | `solid-principles` |

`domain-modeling-made-functional` is the *design* lens — it tells you what types your domain should have. This skill is the *mechanics* of using those types when the chosen library is LanguageExt 4.x.

## Further reading

- LanguageExt repo: https://github.com/louthy/language-ext — README, wiki, and `LanguageExt.Sample` projects.
- Paul Louth's blog posts on F# vs LanguageExt — the design philosophy carries over.
- Mark Seemann, *Code That Fits in Your Head* — pairs well; Mark uses minimalist functional C# without LanguageExt but the philosophy is identical.
- Scott Wlaschin's *Domain Modeling Made Functional* — F# but every type maps to a LanguageExt counterpart.
