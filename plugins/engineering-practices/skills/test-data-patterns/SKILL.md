---
name: test-data-patterns
description: Apply the family of test arrangement patterns — Test Data Builder (Nat Pryce & Steve Freeman, GOOS 2009), Object Mother (Peter Schuh, popularised by Martin Fowler 2006), Arrange-Act-Assert (Bill Wake, 2001), Given-When-Then (Dan North, 2006), and chained Test Fixtures — that keep test setup readable, expressive, and robust to change. Covers fluent builders with sensible defaults, semantic builder methods, the Builder + Mother combination, AAA vs GWT, when to introduce a builder, anti-patterns (constructor-with-twelve-params, mystery guests, irrelevant setup), and the project's `Fixture.Given().When().Then()` convention. Use when writing or reviewing tests, when test setup is bloating, when constructors keep growing, when copy-pasted arrangement makes a test suite hostile to refactor, or when teaching juniors why "just newing it up in the test" stops working past a certain complexity.
---

# Test Data Patterns

Apply this skill when test setup is starting to dominate test bodies, when an object's constructor grows past ~3 parameters, when test data is being copy-pasted between tests, or when reviewing a PR whose tests are technically correct but unreadable. The goal isn't elegant fluent APIs — it's tests that **read like specifications** and **survive refactoring** of the production types they construct.

## Core Philosophy

**Test code is production code.** The same readability and maintainability standards apply. A test that takes 30 lines to set up obscures the behavior it claims to verify.

**Setup is incidental; behavior is essential.** Every line of arrangement that isn't relevant to the scenario steals attention from the line that is. The patterns in this skill are tools for pushing irrelevant setup out of view.

**Test data construction is a design smell amplifier.** When a builder needs 20 `WithX` methods just to construct a domain object, the object is probably doing too much. The friction is feedback.

**Patterns combine.** Builder + Mother + Fixture is the canonical stack: the Fixture frames the test, the Mother names canonical starting points, and the Builder customises the variations.

---

## Pattern 1 — Test Data Builder (Pryce & Freeman, GOOS Ch. 22)

A fluent class whose only job is constructing one type of domain object. Sensible defaults; `WithX` methods for the dimensions that vary; a terminal `Build()` that returns the constructed object.

### Canonical form (matches `OliveV3ShipmentBuilder`)

```csharp
public sealed class OliveV3ShipmentBuilder
{
    private Guid id = Guid.NewGuid();
    private decimal totalPriceExVat = 10m;
    private bool isPaid = true;
    // ... sensible defaults for every field

    public OliveV3ShipmentBuilder WithId(Guid value) { id = value; return this; }
    public OliveV3ShipmentBuilder WithTotalPriceExVat(decimal value) { totalPriceExVat = value; return this; }

    public IOliveServiceV3.Shipment Build() => new(/* ... */);
}
```

### Three rules that make a builder pay for itself

1. **Sensible defaults for every field.** Every constructor argument has a default the tests don't have to think about. Tests state only the dimensions that matter to the scenario.
2. **Fluent setters return `this`.** Chaining keeps construction on one expression. No intermediate variables.
3. **Terminal `Build()` returns the real type.** Not the builder. Tests consume the production type, not a test-only wrapper.

### Semantic methods over generic setters

When the same setter is invoked with the same value across many tests, name the *meaning*, not the value:

```csharp
// Less clear
builder.WithStatus(IOrchidService.CollectionResponse.Statuses.Scheduled)

// Clearer (matches OrchidCollectionBuilder)
builder.IsScheduled()
builder.IsBooked()
builder.IsCancelled()
```

A semantic method is just a `WithX(specific value)` with a name that reads like a domain fact. Reach for it when:
- The value is an enum or sentinel string
- The state name carries domain meaning
- Tests will check the same condition repeatedly

### Coordinated setters

When one logical state requires changing several fields together, encapsulate the coordination in the builder, not in every test:

```csharp
public OliveV3ShipmentBuilder IsDropOff()
{
    isDropOff = true;
    isCollection = false;   // mutually exclusive — builder enforces it
    return this;
}
```

Tests no longer have to know which fields are coupled. The builder is the place that knowledge lives.

### When a builder earns its place

Introduce one when **any** of these are true:
- The constructed type has 4+ parameters.
- The same construction is duplicated across 3+ tests.
- Most tests vary 1–2 dimensions and don't care about the rest.
- The production type's constructor changes often, breaking many tests at once.

Do **not** introduce one when:
- A record with 1–2 fields is constructed directly with named arguments — that's already readable.
- The test is the only place that type is constructed (no leverage).

---

## Pattern 2 — Object Mother (Schuh, Fowler 2006)

A static factory exposing **named, canonical** test objects. Object Mothers answer the question "what's a typical X for a test?" — they give the suite a shared vocabulary of scenarios.

### Canonical form (matches `Builders` static class)

```csharp
public class Builders
{
    public static NewCollectionRequestedBuilder NewCollectionRequested(Guid shipment, Guid threePl) =>
        new(shipment, threePl);

    public static OrchidNewCollectionRequestBuilder OrchidRebookRequest(Guid shipment) =>
        new(shipment);
}
```

Tests then read:

```csharp
var request = Builders.NewCollectionRequested(shipmentId, threePlId)
    .WithSomeVariation()
    .Build();
```

### Mother + Builder is the right combination

A *pure* Object Mother returns a fully constructed object — but then varying it forces the test to mutate the result or call a different mother method. A *pure* Builder requires every test to know the minimum identifying inputs.

The combination resolves both: **the Mother method takes the few identifying inputs the scenario must supply** (the shipment ID, the customer ID), **returns a pre-configured Builder**, and the test fluently varies whatever else it cares about.

This is how the Acacia codebase uses them, and it's the recommended default.

### When to add a Mother method

Add one when:
- A specific *scenario* (not just a type) is referenced by name across multiple tests — "a rebook request", "a cancelled collection".
- The naming makes a test read like a sentence.
- The required-vs-optional inputs of the scenario are stable.

Keep the Mother thin. It should compose builders, not encode complex assertions or behavior.

---

## Pattern 3 — Arrange-Act-Assert (Bill Wake, 2001)

The structural test pattern. Three clearly-separated phases — visually, mentally, sometimes by blank line.

```csharp
[Fact]
public void Discount_AppliedToOrder_ReducesTotal()
{
    // Arrange
    var order = new OrderBuilder().WithSubtotal(100).Build();
    var discount = new PercentageDiscount(10);

    // Act
    var total = order.ApplyDiscount(discount).Total;

    // Assert
    total.Should().Be(90);
}
```

### Three discipline rules

1. **One action per test.** If you need two `Act` lines, you have two tests.
2. **Arrange is bounded.** When Arrange grows past ~5 lines, push setup into a builder or fixture. Long Arrange sections are a code smell.
3. **Assert one logical thing.** Multiple `.Should()` calls are fine *if they verify one logical outcome*. Asserting unrelated facts in one test is a smell.

AAA is the **default** structure when a test is purely state-based or output-based.

---

## Pattern 4 — Given-When-Then (Dan North, 2006)

The semantic alternative to AAA, from BDD. The phases align with AAA but the *naming* shifts the test from "code under test" to "behavior under test".

```csharp
// Given a customer with a draft shipment
// When the customer cancels the shipment
// Then a cancellation request is raised
```

GWT is preferable when:
- The test is verifying *domain behavior* (state transition, business rule) rather than a code-level mechanic.
- The scenario benefits from being readable by a non-developer.
- The codebase is already event-sourced or behavior-oriented (Acacia: yes).

AAA and GWT are not in conflict — many teams write GWT-named tests with an AAA internal structure. The Acacia codebase uses a chained Fixture that *enforces* GWT structure, which is the next pattern.

---

## Pattern 5 — Chained Fixture (`Fixture.Given().When().Then()`)

A fixture object whose API is the GWT phases themselves. Tests cannot accidentally drift out of the structure.

### Canonical form (Acacia style)

```csharp
[Fact]
public void StatusIsActiveShipment_CancelShipmentConsumed_DraftShipmentCancellationRequestedRaised()
{
    var shipmentId = Guid.NewGuid();
    Fixture
        .Given(new HoldCancelShipmentStateTest {
            ShipmentId = shipmentId,
            ProcessState = ProcessState.ActiveShipment,
            ThreePlId = "PH"
        })
        .When(new Commands.CancelShipment(Guid.NewGuid(), Guid.NewGuid(), shipmentId))
        .Then((result, message, _) =>
            result.Map(x => x
                .Should()
                .HaveCount(2)
                .And.ContainEquivalentOf(/* expected event */)));
}
```

### Why it works for event-sourced / state-machine domains

- The `Given` slot is exactly the aggregate state — modeled by the `IHoldXState` interface.
- The `When` slot is exactly a command or upstream event — the domain's `IMessage`.
- The `Then` slot inspects the produced events.
- The test name mirrors the same `State_Trigger_Outcome` shape — a third instance of the same pattern.

This triple alignment (test name ↔ fixture chain ↔ domain logic signature) is why the pattern fits Acacia so well.

### When to use a chained fixture vs plain AAA

Use a chained fixture when:
- The system under test is a state machine, aggregate, or event handler — anything that takes (state, trigger) → (new events / new state).
- You want the suite to enforce structural consistency across many tests.
- The domain is being modeled in DDD style (Acacia).

Don't use one when:
- The unit under test is a pure function or a small algorithm — AAA is lighter.
- The test needs lifecycle hooks, parallel actions, or a setup that doesn't fit the Given/When/Then shape.

### Variants

The project also has a `ConsumerBasedFixture` that uses MassTransit's `ITestHarness` for testing consumers. This is a *fixture* (lifecycle-managed test infrastructure) without the chained API — different problem, different shape. Don't try to fit everything into one fixture.

---

## Pattern 6 — Arrangement (Test Setup Facade)

A class whose responsibility is setting up the **entire test world for one handler/command scenario**: the IDs the test cares about, the seeding calls into fake repositories, the shared constants used in assertions, and a `Command` (or request) property that assembles from those IDs.

Where a Builder constructs *one object*, an Arrangement wires together the *whole Arrange phase* of a test — including multiple fakes that must share the same IDs.

### Canonical form (matches `CopyDraftShipmentArrangement`)

```csharp
public sealed class CopyDraftShipmentArrangement
{
    // Test-owned IDs — all downstream usage references these, not inline Guid.NewGuid()
    public Guid SourceDraftId { get; } = Guid.NewGuid();
    public Guid NewShipmentId { get; } = Guid.NewGuid();
    public Guid CustomerId    { get; }

    // Shared field constants — seeding methods write them; assertions read them
    public const string ShipperName    = "Alice Shipper";
    public const string ShipperEmail   = "alice.shipper@example.com";
    // ... one const per copyable source field

    private readonly TestCopyDraftShipmentRepository _copyRepo;
    private readonly TestDraftShipmentQuotesRepository _quotesRepo;

    public CopyDraftShipmentArrangement(
        Guid customerId,
        TestCopyDraftShipmentRepository copyRepo,
        TestDraftShipmentQuotesRepository quotesRepo)
    { ... }

    // The Arrange-phase entry point for every test
    public CopyDraftShipmentCommand Command =>
        new(SourceDraftId, NewShipmentId, CustomerId, _itineraryId, []);

    // Fluent seeding — each method seeds one aspect into the fakes and returns this
    public CopyDraftShipmentArrangement WithCollectionSource() { _copyRepo.Given(...); return this; }
    public CopyDraftShipmentArrangement WithShipperDetails()   { _copyRepo.Given(...); return this; }
    public CopyDraftShipmentArrangement WithNotes()            { _copyRepo.Given(...); return this; }
    // ...
}
```

Tests then read:

```csharp
[Fact]
public async Task Copy_FullyPopulatedSource_EmitsPerFieldEventsOnNewDraft()
{
    var arrangement = Arrange()
        .WithCollectionSource()
        .WithShipperDetails()
        .WithDelivery()
        .WithNotes()
        .WithInsurance()
        .WithMatchingCollectionItinerary();

    var result = await sut.Handle(arrangement.Command).Run();

    result.IsSucc.Should().BeTrue();
    var shipper = v3Repository.RaisedEvents.OfType<ShipperDetailsAdded>()
                              .Single(e => e.DraftShipmentId == arrangement.NewShipmentId);
    shipper.Name.Should().Be(CopyDraftShipmentArrangement.ShipperName);
}
```

Per-test variants use C# record `with` — no new arrangement class, no new method:

```csharp
var result = await sut.Handle(arrangement.Command with { CustomerId = OtherCustomerId }).Run();
```

### What makes an Arrangement earn its place

Reach for it when **all three** of these are true:

1. **Multiple fakes must share the same IDs.** If the command contains `SourceDraftId` and the repository mock must be seeded with that same `SourceDraftId`, the Arrangement is the only place to own both without repeating the ID in each test.
2. **The command contract is volatile.** Adding or removing a field on a record command forces updates everywhere the command is constructed. With an Arrangement, only `Command` changes — test methods are untouched.
3. **Tests vary along one or two dimensions.** The Arrangement provides sensible defaults for everything else; `With*` methods activate the dimensions that matter; `with` expressions handle point deviations.

Don't introduce one when:
- Only data construction is needed (a Builder suffices).
- There is a single test — the overhead is not paid back.
- Fakes don't share IDs (no coordination problem to solve).

### Arrangement vs Builder — the distinction

| | Builder | Arrangement |
|---|---|---|
| Constructs | One type | The full test world |
| Returns | The production type (via `Build()`) | Itself (fluent) + a `Command` property |
| Owns IDs | No — tests supply them | Yes — IDs are fields on the Arrangement |
| Owns fakes | No | Yes — seeding calls go through the Arrangement |
| Per-test variation | `.WithX(value)` then `.Build()` | C# record `with` on the command |
| When contract changes | Every Builder call must update | Only `Command` property changes |

### Arrangement vs Chained Fixture — the distinction

A Chained Fixture (`Fixture.Given().When().Then()`) enforces Given-When-Then *structure* — the fixture is the test. An Arrangement only handles the **Arrange** phase of plain AAA tests — the test method still contains its own Act and Assert. Use the Chained Fixture when you want structural enforcement across many tests on a state machine; use an Arrangement when you want flexible, composable setup that feeds into plain `async Task` test methods.

---

## How the patterns combine — the canonical Acacia stack

```csharp
[Fact]
public void Rebook_Initiated_RebookConfirmedRaised()
{
    var shipmentId = Guid.NewGuid();
    var threePlId  = Guid.NewGuid();

    Fixture                                                   // ← Pattern 5 (chained fixture)
        .Given(/* state */)
        .When(
            Builders.NewCollectionRequested(shipmentId, threePlId)   // ← Pattern 2 (mother)
                .WithCarrierId(carrierId)                            // ← Pattern 1 (builder)
                .Build())
        .Then((result, _, _) => result.Should().BeRebookConfirmed());
}
```

Reads top-to-bottom as a specification: *given this state, when this thing happens, then this fact follows*. Almost no incidental code; every line either names a scenario or asserts an outcome.

---

## Anti-patterns

### 1. The 12-parameter constructor invocation in every test

```csharp
// Bad
var shipment = new Shipment(Guid.NewGuid(), Guid.NewGuid(), "GBP", 10m, 12m, 2m,
    20m, false, true, false, true, false, DateTimeOffset.UtcNow.AddDays(1), "", []);
```

When this appears in 20 tests, every constructor change cascades through all 20. Introduce a builder.

### 2. The Mystery Guest (Meszaros, xUnit Test Patterns)

A test depends on data created elsewhere — a shared fixture file, a database seed, a static field — and the reader cannot see what state the test starts in. Always make `Given` / Arrange explicit, even at the cost of repetition.

### 3. Irrelevant setup polluting the scenario

If a test asserts a discount calculation, the customer's address shouldn't appear in the Arrange. A builder with sensible defaults removes it; the test names only what matters.

### 4. The God Mother

A static Mother class with 100 methods, no domain organisation, names that overlap (`StandardCustomer`, `RegularCustomer`, `NormalCustomer`). Group by aggregate; prune duplicates aggressively.

### 5. Builders that mutate the returned object

Don't. `Build()` should return a fresh object each call. Subsequent `.WithX()` calls on the same builder must not affect already-built instances.

### 6. Asserting on the builder

`builder.WithStatus(X).Build().Status.Should().Be(X)` — tests the builder, not the production code. The builder is infrastructure; trust it, or test it once in isolation.

### 7. Logic in the builder

Builders construct data. They don't validate, normalize, or compute derived values. If they do, they hide bugs that should be visible in tests. The production type does that work.

### 8. Hidden randomness

`Guid.NewGuid()` as a default is fine *if the test doesn't care about the value*. The moment a test asserts on an ID, it must specify it. Tests that pass on Tuesday and fail on Wednesday because of random data are worse than no tests.

---

## When to introduce each pattern — heuristic table

| Symptom | Reach for |
|---|---|
| Constructor with 4+ args appearing in tests | Test Data Builder |
| Same scenario set up across tests | Object Mother method |
| Tests verifying state-machine transitions | Chained Fixture |
| Tests with vague names like `Test1`, `WorksCorrectly` | Given-When-Then naming |
| Long Arrange sections drowning the Act/Assert | Builder + Mother to push setup out of view |
| A handful of related fields mutated together | Coordinated setter on the builder |
| Tests that read "magically" but you don't know why | The Mother is hiding too much — push detail back into the test |
| Adding a field to a command broke N test callsites | Arrangement — owns command construction and IDs in one place |
| Fake repository must be seeded with the same ID used in the command | Arrangement — the only pattern that co-owns IDs and fakes |
| Tests vary one dimension of a multi-field command | Arrangement + C# record `with` for point overrides |

---

## Relationship to other skills

- **unit-testing-principles (Khorikov)** — covers *what to test* and *test quality dimensions*. This skill covers *how to construct test data ergonomically*. Complementary: even Khorikov's well-targeted tests need readable arrangement.
- **test-driven-development** — covers the *workflow* (red/green/refactor, outside-in). Builders make the inner-loop "arrange" cheap enough for the workflow to flow.
- **behavior-driven-development** — Given/When/Then is BDD vocabulary; the chained Fixture is the unit-testing-level adoption of BDD's structure.
- **clean-code** — small functions, meaningful names. Builders and Mothers are how those principles apply to test code.
- **refactoring** — *Extract Test Data Builder* and *Introduce Object Mother* are refactorings; this skill is when and why to apply them.

---

## Codebase-specific conventions

### Acacia

- **Builders live in `Acacia.Test.Unit/Builders/`** for shared types, or `Acacia.Test.Unit/<Aggregate>/Builders/` for aggregate-specific types.
- **Builders are `sealed`** unless there's a reason to inherit.
- **Static `Builders` Mother class** sits inside the relevant subfolder, exposing factory methods that return aggregate-specific builders.
- **Test naming follows `State_Trigger_Outcome`** (e.g. `StatusIsActiveShipment_CancelShipmentConsumed_DraftShipmentCancellationRequestedRaised`) — same shape as the chained Fixture.
- **Comments belong in tests, not production code** — explanatory comments on regression tests are encouraged.
- **FluentAssertions** for assertions; `BeEquivalentTo` / `ContainEquivalentOf` with `Excluding` and custom `Using<DateTime>` comparators for time tolerance.
- **Reqnroll (BDD)** lives in `Acacia.Test.Behavior` — different layer; the chained Fixture is for unit-level GWT, Reqnroll is for feature-level GWT.

### Olive

- **Arrangements live in `Olive.Test.Unit/V3/<Feature>/TestHelpers/`** alongside the other test helpers for that feature (e.g. `CopyDraftShipmentArrangement` sits next to `TestCopyDraftShipmentRepository`).
- **Arrangements are `sealed`** with a constructor that takes the customer ID and the relevant fake repositories.
- **A factory helper on the test class** (`private CopyDraftShipmentArrangement Arrange() => new(OwnerCustomerId, copyRepository, quotesRepository)`) keeps test bodies from repeating the constructor arguments.
- **Constants for source field values** live as `public const` on the Arrangement — seeding methods write them; assertion lambdas read them by name (e.g. `CopyDraftShipmentArrangement.ShipperName`).
- **Per-test command overrides** use C# record `with` on `arrangement.Command`, not a new `With*` method.
- **Arrangements suit command-handler tests** where the handler takes a primitive-shaped command and multiple fake repositories must share the same IDs.
- **Domain-function tests** (pure functions, no fakes) don't need Arrangements — use direct construction with named arguments or a Builder.

---

## Quick Application Checklist

Before writing a new test:
- [ ] Is there already a builder for the type I'm constructing? Use it.
- [ ] Is there a Mother factory method for this scenario? Use it.
- [ ] Does the test fit `Given → When → Then`? Use the Fixture.
- [ ] Do multiple fakes need to share the same IDs as the command? Use an Arrangement.

When reviewing a test:
- [ ] Is the Arrange section under ~5 lines? If not, push setup into a builder.
- [ ] Does the test name read as `State_Trigger_Outcome` (or `Given_When_Then`)?
- [ ] Are all the values in Arrange relevant to the scenario? Irrelevant ones belong in builder defaults.
- [ ] Is there exactly one logical Act?
- [ ] Does the Assert verify behavior or implementation? (Khorikov — see unit-testing-principles.)

When introducing a builder:
- [ ] Sensible defaults for every field?
- [ ] `WithX` methods return `this`?
- [ ] `Build()` returns the production type, fresh each call?
- [ ] Semantic methods (`IsScheduled`, `IsDropOff`) for repeated states?
- [ ] Coordinated setters where fields are coupled?
- [ ] No logic / validation / computation in the builder?

When introducing a Mother method:
- [ ] Does it name a *scenario*, not a *type*?
- [ ] Does it return a builder (not a built object) so the test can customise?
- [ ] Does it take only the identifying inputs the scenario must supply?
- [ ] Is it grouped by aggregate / domain area?

---

## Reading

- **Steve Freeman & Nat Pryce**, *Growing Object-Oriented Software, Guided by Tests* (Addison-Wesley, 2009), especially Chapter 22 — the canonical Test Data Builder.
- **Martin Fowler**, [*ObjectMother*](https://martinfowler.com/bliki/ObjectMother.html) (2006) — short and definitional.
- **Bill Wake**, [*3A — Arrange, Act, Assert*](https://xp123.com/articles/3a-arrange-act-assert/) (2001) — the originating blog post.
- **Dan North**, [*Introducing BDD*](https://dannorth.net/introducing-bdd/) (2006) — origin of Given-When-Then.
- **Gerard Meszaros**, *xUnit Test Patterns* (Addison-Wesley, 2007) — the comprehensive catalogue: Mystery Guest, Test Data Builder, Object Mother, Creation Method, and dozens more, with names and trade-offs.
- **Vladimir Khorikov**, *Unit Testing Principles, Practices, and Patterns* (Manning, 2020) — pairs with this skill; covers test quality where this covers test ergonomics.
