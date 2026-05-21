---
name: unit-testing-principles
description: Apply Vladimir Khorikov's unit testing framework from "Unit Testing Principles, Practices, and Patterns" (Manning, 2020). Covers the four pillars (protection against regressions, resistance to refactoring, fast feedback, maintainability) and their unavoidable trade-offs, the three styles of unit testing (output-based, state-based, communication-based), observable behavior vs implementation details as the line that separates good and bad tests, mocks vs stubs with strict verification rules, the managed vs unmanaged dependency distinction (the most useful heuristic for deciding what to mock), what code is worth testing (high domain significance × high complexity), and the anti-patterns that produce brittle test suites. Use when evaluating test quality, reviewing tests in a PR, deciding what to mock, writing tests for a new feature, choosing between unit and integration tests, or resolving disagreements about test style. Complements the test-driven-development skill (which focuses on workflow).
---

# Unit Testing Principles (Vladimir Khorikov)

Apply this skill when you want to evaluate whether tests are *good* — not just whether they pass. The central premise: a good test gives you confidence to refactor, catches regressions, runs fast, and is easy to read. These four goals are in tension; the discipline is choosing the right trade-off.

## Core Philosophy

**The goal of unit testing is sustainable growth of the codebase.** Tests that survive refactoring let you keep changing the system. Tests that break on every internal change are a tax, not an asset.

**A good test is hard to write.** If a test is trivial, either the code is trivial (no domain value) or you are testing the wrong thing. The friction of testing complex code is the design feedback TDD aims for; the absence of friction is a sign the test does not earn its keep.

**Tests should target observable behavior, not implementation details.** This single principle subsumes most of Khorikov's other rules.

**Code coverage is not the metric.** A codebase with 100% coverage of trivial getters, mocked-everything orchestration tests, and brittle assertions is worse than one with 60% coverage of high-significance domain logic tested at the boundary.

---

## The Four Pillars of a Good Unit Test

Every unit test sits somewhere in a four-dimensional space:

### 1. Protection Against Regressions
Does the test catch bugs?
- Maximized by: covering substantial domain logic, asserting on real outcomes, exercising many code paths.
- Hurt by: testing trivial code, mocking everything away, asserting only on intermediate steps.

### 2. Resistance to Refactoring
Does the test survive internal restructuring of the production code?
- Maximized by: targeting observable behavior, asserting on results not interactions, using real collaborators where possible.
- Hurt by: mocking internal classes, asserting on private state, verifying call sequences.

### 3. Fast Feedback
Does the test run in milliseconds, so the developer runs it constantly?
- Maximized by: avoiding I/O, keeping setup minimal, focusing on pure logic.
- Hurt by: real databases, real network calls, large fixtures.

### 4. Maintainability
Is the test easy to read and change?
- Maximized by: clear naming, minimal setup, one concept per test, no conditional logic in tests.
- Hurt by: complex mocks, hundred-line setups, intertwined assertions.

### The unavoidable trade-off

**You cannot maximize all four pillars simultaneously.** Khorikov's central insight: the product `protection × resistance × feedback × maintainability` has a ceiling. To gain in one dimension you sacrifice another.

|  | Protection | Resistance | Feedback | Maintainability |
|---|---|---|---|---|
| **End-to-end test** | HIGH | HIGH | LOW | MEDIUM |
| **Good unit test** (output- or state-based, sociable) | MEDIUM-HIGH | HIGH | HIGH | HIGH |
| **Mockist unit test** (communication-based, solitary) | LOW (verifies calls, not outcomes) | LOW (breaks on refactor) | HIGH | MEDIUM |
| **Trivial test** (getter/setter) | NEAR-ZERO | HIGH | HIGH | LOW value despite being green |

**Khorikov's prescription:** sacrifice *fast feedback* before sacrificing the others. Integration tests are slower than unit tests; that is acceptable. Sacrificing resistance to refactoring (the mockist trap) corrodes the suite over time.

### The "Test Is Useful" Inequality

Combine: a test is *useful* only when `Protection × Resistance > 0`. A test that mocks everything has high refactor-resistance but near-zero protection (it only verifies calls happened). A test that asserts on internals has high protection but zero resistance (any refactor breaks it). Either way, the product is zero. Such tests are net-negative — they slow you down without catching anything.

---

## The Three Styles of Unit Testing

Every unit test belongs to one of three styles. They differ dramatically in how they score against the four pillars.

### 1. Output-based (functional) — **best**
Call a function with input; assert on returned value. The function has no side effects.

```csharp
[Fact]
public void Add_TwoPositiveNumbers_ReturnsTheirSum()
{
    var result = Calculator.Add(2, 3);
    result.Should().Be(5);
}
```

- **Protection: high.** Asserts on real outcomes.
- **Resistance: highest.** No internals are touched; refactor freely.
- **Feedback: highest.** Pure functions, no I/O.
- **Maintainability: highest.** No setup, no mocks, trivial to read.

**Only possible when the code under test is a pure function.** This is the most powerful argument for the *functional core, imperative shell* design pattern: push business logic to pure functions and your best tests appear naturally.

### 2. State-based — **good**
Call a method; assert on the resulting state of the object (or returned value derived from new state).

```csharp
[Fact]
public void Deposit_PositiveAmount_IncreasesBalanceByThatAmount()
{
    var account = new Account(initialBalance: 100m);

    account.Deposit(50m);

    account.Balance.Should().Be(150m);
}
```

- **Protection: good** — assertions on real state.
- **Resistance: good** — but slightly weaker; the *shape* of the state is now part of the contract.
- **Feedback: high** — no I/O.
- **Maintainability: good** — straightforward to read; setup is the object construction.

**Most OO unit tests are this style.** It is the natural form when the unit has lifecycle / mutable state.

### 3. Communication-based (mockist) — **worst**
Mock collaborators; verify which calls were made.

```csharp
[Fact]
public void PlaceOrder_Always_AsksPaymentGatewayToCharge()
{
    var gateway = new Mock<IPaymentGateway>();
    var sut = new OrderProcessor(gateway.Object);

    sut.PlaceOrder(someOrder);

    gateway.Verify(g => g.Charge(It.IsAny<Payment>()), Times.Once);
}
```

- **Protection: low** — verifies that a call happened, not that the call did the right thing.
- **Resistance: low** — any refactor of how the unit communicates with collaborators breaks the test.
- **Feedback: high** — mocks are fast.
- **Maintainability: medium** — mock setup is verbose.

**Use only at the boundary with unmanaged dependencies** (see below). Inside the system, prefer state-based or output-based.

### Practical Rule

When writing a test, in priority order:
1. **Can I make the code-under-test pure and test output-based?** Restructure if you can.
2. **Otherwise, test state-based.** Construct the object, exercise, assert on resulting state.
3. **Communication-based** only where mandatory: verifying an outgoing call to an unmanaged dependency that is part of the system's contract with the outside world.

---

## Observable Behavior vs Implementation Details

This is the line that separates good tests from bad ones. **Tests should depend only on observable behavior.**

### What is observable behavior?
- The public API of the class (method signatures and their contracts).
- The values returned to callers.
- Side effects callers can verify (state changes visible through the public API; messages sent to known unmanaged dependencies).
- The behavior that clients of the class depend on.

### What is an implementation detail?
- Private methods.
- Internal helper classes used only by this class.
- The specific algorithm chosen (so long as outputs are unchanged).
- The internal sequence of operations.
- Which internal classes are instantiated.
- How the class delegates work to internal collaborators.

### The test for "is this observable?"
**Could a different reasonable implementation pass this test?** If yes, it tests behavior. If no, it tests implementation.

```csharp
// Tests behavior:
result.Should().Be(150m);                      // any impl that returns 150 passes
order.Status.Should().Be(OrderStatus.Placed);  // any impl reaching Placed state passes

// Tests implementation:
mockHelper.Verify(x => x.Calculate(...));      // breaks if we inline the helper
calculator.PrivateBalance.Should().Be(150m);   // assumes the private field exists
mockA.InSequence(seq).Verify(...);             // assumes a specific call order
```

When tests fail on implementation refactors, the test suite is corroding. Each refactor incurs a tax. The fix is not to refactor less; it is to make tests assert on observable behavior only.

---

## Mocks vs Stubs (Strict Rules)

Khorikov revives Meszaros's distinction with sharper rules:

- **Stub** — substitutes an *incoming query* with canned data. ("What's the user's account balance? Returns $100.")
- **Mock** — verifies an *outgoing command* was issued. ("Did we send the confirmation email?")

### Rule 1: Use stubs for queries; use mocks for commands

This maps directly to Bertrand Meyer's Command-Query Separation (CQS):
- **Queries** return values, no side effects → stubbed (provide input).
- **Commands** cause side effects, no return → mocked (verify they happened).

### Rule 2: Never verify on stubs

If you find yourself doing `stubRepo.Verify(x => x.GetById(123))`, the test is over-specifying. The fact that the SUT happens to call `GetById` is internal. Tomorrow we may cache, denormalize, or compose differently. The behavior the caller observes is the *result* — assert on that.

```csharp
// BAD — verifying on a stub
stubRepo.Setup(x => x.GetById(123)).Returns(someUser);
sut.DoSomething(123);
stubRepo.Verify(x => x.GetById(123), Times.Once);   // overspecification

// GOOD — assert on outcome
stubRepo.Setup(x => x.GetById(123)).Returns(someUser);
var result = sut.DoSomething(123);
result.Should().Be(expected);
```

### Rule 3: Mock only at unmanaged-dependency boundaries

This is the most useful heuristic in the book (see next section). Mocking internal classes you own is the single most common cause of brittle tests.

---

## Managed vs Unmanaged Dependencies — the Key Heuristic

Khorikov's most useful contribution. The rule for what to mock:

### Managed dependency
- Used *only* by your application.
- Its state is visible only through your application.
- The application controls the schema / structure.
- Examples: your application's database, your application's filesystem store, an in-memory cache scoped to your process.

**Test with: real instances (integration tests) or real-ish fakes (in-memory DB, in-memory FS).**
**Do NOT mock.** A mock of a managed dependency loses the test's protection — you no longer verify that the SUT and the DB actually compose correctly.

### Unmanaged dependency
- Shared with other systems.
- Its API contract is *external* — changing it affects others.
- You don't own the data shape; you communicate with it.
- Examples: payment gateway, email service, SMS provider, message broker (shared with other apps), third-party APIs, OS-level services consumed across processes.

**Test with: mocks.** Communication-based testing is appropriate here — verifying the outgoing call is part of the system's contract with the outside world.

### Applied examples

| Dependency | Managed or Unmanaged? | How to test |
|---|---|---|
| PostgreSQL DB owned by this app | Managed | Real DB in integration tests |
| Redis cache used only by this app | Managed | Real Redis or in-memory fake |
| Stripe payment API | Unmanaged | Mock; verify charge calls |
| Sendgrid email API | Unmanaged | Mock; verify send calls |
| RabbitMQ topic consumed by 5 apps | Unmanaged | Mock; verify publish |
| Local filesystem under your data dir | Managed (usually) | Real FS or in-memory FS |
| Internal microservice you own | Managed if you control the contract; Unmanaged if it's truly versioned-and-shared | Depends |
| Clock / time | Unmanaged (system service) | Mock (use `IClock`) |
| Random | Unmanaged | Mock |

This is sharper than "mock at architectural seams" because it distinguishes seams that protect your application's correctness (where you want real interaction, slower but stronger tests) from seams that protect your contract with the outside world (where mocks verify your end of the contract).

---

## What Should Be Tested

Not everything is worth testing. Khorikov's framework places code on two axes:

- **Domain significance** — does it embody business rules?
- **Complexity** — does it have non-trivial logic (branches, calculations, sequences)?

```
                          ┌─────────────────────────┬─────────────────────────┐
                          │ Low complexity          │ High complexity         │
   ┌──────────────────────┼─────────────────────────┼─────────────────────────┤
   │ High significance    │ Test if cheap           │ DEFINITELY test         │
   │                      │ (value objects, etc.)   │ (highest ROI)           │
   ├──────────────────────┼─────────────────────────┼─────────────────────────┤
   │ Low significance     │ Skip — not worth it     │ Refactor to reduce      │
   │                      │                         │ complexity, OR test     │
   │                      │                         │ (controllers go here)   │
   └──────────────────────┴─────────────────────────┴─────────────────────────┘
```

### Categories

1. **Domain logic** (high significance + high complexity) — comprehensive unit tests; output-based or state-based.
2. **Algorithmic / utility code** (low significance + high complexity) — unit-test or refactor away.
3. **Trivial value objects** (high significance + low complexity) — test if cheap, often covered transitively.
4. **Orchestration / controllers** (low significance + medium complexity) — integration tests, one happy path each. Unit-testing a controller usually requires mocking everything, producing low-value mockist tests.
5. **Infrastructure / glue** (low + low) — covered transitively by integration tests, don't direct-test.
6. **Third-party code** — don't test.

### "Trivial code is a sign of trivial design"

If a test is too easy to write, ask: *is this code actually doing anything?* Code that's pure delegation usually doesn't need its own test — the test for the thing it delegates to covers it. The most valuable tests are the ones where writing the test forced you to think about the design.

---

## Anti-patterns Khorikov Calls Out

- **Testing private methods.** If a private method is complex enough to test, extract it to a class with a public API. Then it becomes a tested unit.
- **Code coverage as a goal.** Coverage doesn't measure protection. 100% coverage with all communication-based tests provides near-zero protection. Use coverage only as a leak detector (no tests at all in area X), never as a target.
- **Testing trivial code.** Getters, setters, single-line delegations. Wastes maintenance time, doesn't improve correctness.
- **Asserting on intermediate steps.** Couples the test to implementation. Test the final outcome.
- **Solitary fundamentalism.** Treating "one class per test" as a rule produces brittle suites. The unit is a behavior; it may span multiple classes.
- **Brittle tests breaking on every refactor.** Symptom of testing implementation details. Fix by reasserting at the observable boundary.
- **Mocking your own code.** A mock of an internal class freezes the relationship. When you change that relationship, the test breaks even though behavior is identical.
- **`if` statements in tests.** Each test should describe one scenario; conditionals indicate two tests merged.
- **Test names that describe HOW.** `Sum_Should_Call_Add_Method` couples to implementation. `Sum_OfPositiveNumbers_ReturnsCorrectTotal` describes behavior.
- **Verifying on stubs.** Overspecification; tests get tied to call patterns instead of outcomes.
- **Excessive Setup.** A test that needs 50 lines of setup is testing too much, or the SUT has too many dependencies (design feedback).
- **Multiple acts (when/then) per test.** Each test exercises one transition. Multiple "When" blocks = multiple tests.
- **One test per public method.** The unit is a *behavior*, not a method. One method may have several behaviors (different inputs, different states) — each gets its own test.

---

## The Test Pyramid (Khorikov's Variant)

Same shape, sharper definition:

```
                ┌───────────────────────────┐
                │  E2E tests                │  Few — one or two happy paths
                │  (full system, real       │  through the whole stack
                │   unmanaged deps)         │
                ├───────────────────────────┤
                │  Integration tests        │  Some — verify code works with
                │  (SUT + managed deps      │  real managed dependencies
                │   like real DB)           │  + mocks for unmanaged
                ├───────────────────────────┤
                │  Unit tests               │  Most — output-based ideally,
                │  (sociable, classical;    │  state-based otherwise;
                │   no I/O, no mocks of     │  sociable across internal
                │   managed deps)           │  collaborators
                └───────────────────────────┘
```

**Don't replace unit tests with integration tests** because mocking is annoying — that's a sign your design has too many unmanaged dependencies, or you're mocking what you shouldn't.

**Don't double-up.** Integration tests verify collaboration with managed deps; unit tests verify domain logic. Each scenario should be covered by one or the other, not both.

---

## Functional Core, Imperative Shell

Khorikov is a strong advocate (alongside Gary Bernhardt and Mark Seemann). The pattern:

- **Functional core:** pure functions; no I/O, no mutation, no side effects. Decisions, calculations, business rules.
- **Imperative shell:** orchestrates I/O — reads from the DB, calls services, writes results. Thin; mostly delegates to the core.

Why this matters for testing:
- The functional core is **trivially output-based testable**. Highest pillar scores.
- The imperative shell is **integration-tested** with the real managed dependencies.
- You almost never write communication-based unit tests, because the only "communication" is between the shell and unmanaged deps (which is what integration tests cover).

This is the design-level solution to the testability problem. Push business logic out of orchestration code; orchestration code becomes thin enough to not need direct unit tests.

---

## Worked Example: Refactoring a Mockist Test

```csharp
// BEFORE — communication-based (low protection, low resistance)
[Fact]
public void Reserve_WithSufficientCapacity_CallsRepoSave()
{
    var repo = new Mock<IReservationRepository>();
    var capacityChecker = new Mock<ICapacityChecker>();
    capacityChecker.Setup(x => x.HasCapacity(date, 2)).Returns(true);
    var service = new ReservationService(repo.Object, capacityChecker.Object);

    service.Reserve(new ReservationRequest(date, 2));

    repo.Verify(x => x.Save(It.IsAny<Reservation>()), Times.Once);  // implementation detail
    capacityChecker.Verify(x => x.HasCapacity(date, 2), Times.Once); // stub being verified
}

// AFTER — state-based (high protection, high resistance)
[Fact]
public void Reserve_WithSufficientCapacity_ReturnsConfirmedReservation()
{
    var repo = new InMemoryReservationRepository();                  // managed dep, real fake
    var capacityChecker = new InMemoryCapacityChecker(date, capacity: 10);  // managed dep
    var service = new ReservationService(repo, capacityChecker);

    var result = service.Reserve(new ReservationRequest(date, 2));

    result.Status.Should().Be(ReservationStatus.Confirmed);
    repo.GetByDate(date).Should().HaveCount(1);                     // outcome, not interaction
    capacityChecker.RemainingFor(date).Should().Be(8);              // outcome, not interaction
}
```

The second version:
- Survives any refactor of *how* the service implements capacity check or persistence.
- Catches more bugs (verifies the actual capacity was decremented, the reservation was actually saved with the right state).
- Has zero mocks of internal classes.
- Reads as a clear specification.

---

## How This Skill Relates to Others

- **test-driven-development** — the *workflow* (red/green/refactor, outside-in). This skill is about what makes the tests *themselves* good once you've decided to write one. Both are useful; they answer different questions.
- **clean-code** — F.I.R.S.T from Bob Martin. Khorikov is more rigorous and trade-off-aware (F.I.R.S.T treats every quality as separately maximizable; Khorikov treats them as a system of trade-offs).
- **fractal-architecture / Seemann** — *Code That Fits in Your Head* shares Khorikov's view that functional core / imperative shell is the structural answer to testability.
- **hexagonal-clean-architecture** — provides the architectural seams. Khorikov's managed/unmanaged distinction is the practical rule for what to mock across those seams.
- **behavior-driven-development** — BDD's outer loop sits at the integration / E2E tier; this skill governs the unit tier.

---

## Quick Application Checklist

For every new test:

- [ ] Does it test observable behavior (something a client of this code would see), not implementation details?
- [ ] What style is it — output-based / state-based / communication-based? Have I chosen the strongest viable style?
- [ ] If it uses mocks, are they only at *unmanaged*-dependency boundaries?
- [ ] If it uses stubs, am I verifying anything on them? (I should not be.)
- [ ] Could a reasonable alternative implementation of the SUT pass this test? (If no, I'm coupled to implementation.)
- [ ] Is the code being tested high-significance OR high-complexity? (If neither, why am I testing it?)
- [ ] Does the test name describe *what* the behavior is, not *how* it is implemented?
- [ ] Is there any `if` / `for` / `switch` in the test body? (There should not be.)
- [ ] Could a colleague read this test and understand the requirement it encodes?

For an existing test suite (review):

- [ ] What's the ratio of output-based : state-based : communication-based?
- [ ] Where are the mocks placed — at every class boundary, or only at unmanaged deps?
- [ ] Are there any verifications on stubs?
- [ ] Are there obvious "tests that broke because of a refactor" complaints in PR history?
- [ ] Is there high-significance code without tests?
- [ ] Is there low-significance code with extensive tests (wasted effort)?
- [ ] Are integration tests doubling up on what unit tests already cover?

---

## Reading

- **Vladimir Khorikov**, *Unit Testing Principles, Practices, and Patterns* (Manning, 2020) — the canonical text.
- **Vladimir Khorikov**, blog at enterprisecraftsmanship.com — extensive essays; many topics expand on the book.
- **Vladimir Khorikov**, Pluralsight courses (*Unit Testing: The Big Picture*, *Pragmatic Unit Testing*, etc.).
- **Vladimir Khorikov**, YouTube talks on unit testing best practices — accessible summaries of the book.
- **Gerard Meszaros**, *xUnit Test Patterns* (2007) — the lexicon and pattern catalog Khorikov builds on.
- **Martin Fowler**, *Mocks Aren't Stubs* (essay) — the foundational distinction.
- **Gary Bernhardt**, *Boundaries* (2012 talk) — functional core, imperative shell.
- **Mark Seemann**, *Code That Fits in Your Head* (2021) — overlapping themes on testability and design.
- **Steve Freeman & Nat Pryce**, *Growing Object-Oriented Software, Guided by Tests* — the canonical opposite view (Khorikov is openly critical of mockist TDD; reading both is worthwhile).
