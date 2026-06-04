---
name: art-of-unit-testing
description: Apply Roy Osherove's "The Art of Unit Testing" (Manning — 2nd ed. 2013 in C#/.NET, 3rd ed. 2024 in JavaScript) — the practitioner's guide to writing trustworthy, maintainable, readable unit tests. Centers on Osherove's broad unit-of-work definition (entry point → observable exit point), his three-part test-naming convention (UnitOfWork_StateUnderTest_ExpectedBehavior), the stub-vs-mock distinction by whether you assert against the double, the one-mock-per-test rule, designing for testability via seams (dependency injection, Extract-and-Override), and getting legacy code under test. Use when writing/naming/structuring a unit test, choosing stub vs mock, isolating the SUT, deciding what a "unit" is, designing seams for testability, making a test suite trustworthy-maintainable-readable, or attacking untested legacy code.
---

# The Art of Unit Testing (Roy Osherove)

Apply this skill when the question is **"how do I write *this* unit test well — what do I call it, how do I structure it, and what do I fake?"** Osherove's book is the practitioner's field manual: less a taxonomy (that's Meszaros) and less a trade-off calculus (that's Khorikov) than a set of concrete, opinionated, repeatable habits for the test you are about to type. Its single most-cited contribution — and the main reason to reach for this skill — is the **three-part naming convention**.

This skill deliberately overlaps with `unit-testing-principles` (Khorikov) and `xunit-test-patterns` (Meszaros); where it does, it states **Osherove's distinct position** rather than repeating theirs. Read the "Where Osherove differs" notes inline.

## Core Philosophy

**A unit test is automated, fast, isolated, repeatable, self-checking, and consistent.** Osherove's working definition: a unit test exercises a *unit of work* in the system and then checks a single *end result* of that unit. If the assumptions about the end result turn out wrong, the unit test has failed. A unit test runs entirely in memory, controls its own world, and gives the same answer no matter who runs it, in what order, on which machine.

**The opposite of a good unit test is an *integration test*** — anything that touches a real database, network, file system, threads, or the system clock, or whose result depends on something you don't fully control. Integration tests are valuable, but they are a *different thing* with different speed and trust characteristics, and they must live apart (see Trust, below). Osherove's line: if you can't run it on an airplane with the laptop lid almost closed, it isn't a unit test.

**The whole point is confidence to change code.** A test you don't trust, can't read, or can't afford to maintain is worse than no test — it actively slows the team. The three pillars (Trustworthy, Maintainable, Readable) are the standard every test must meet.

**Good tests are a design and documentation artifact, not just a safety net.** A well-named, well-structured test is the clearest specification of what a unit is supposed to do. The next reader should learn the requirement from the test name alone.

---

## The Unit of Work — Osherove's Definition (read this first)

This definition is load-bearing for everything else in the skill, especially naming.

> **A unit of work is the sum of actions that take place between the invocation of an entry point (a public method) and a single noticeable *end result* — an observable *exit point* — by a test of that system.**

A unit of work can span one method, several methods, even several classes — what matters is the *public entry point* you call and the *observable exit point* you check. There are exactly **three kinds of exit point**, and every unit test verifies exactly one of them:

| Exit point | What the unit does | How you verify it | Double needed |
|---|---|---|---|
| **1. Return value** | The entry point returns a value or throws | Assert on the return value / exception | None (or a stub feeding input) |
| **2. State change** | The unit changes observable state of the system | Call the entry point, then query state through the public API and assert | None (or a stub feeding input) |
| **3. Call to a third-party** | The unit calls out to a dependency you don't control (logger, email, payment gateway) | Verify the outgoing call with a **mock** | A **mock** |

Why this framing matters:
- It tells you **what to assert** (one exit point) before you write a line.
- It tells you **whether you need a mock at all**: only exit point #3 needs one. Return-value and state-based tests need *no mock* — at most a stub to feed input.
- It is the source of the **first segment of the test name**.

**Where Osherove differs:** Khorikov's "output / state / communication" three styles map almost one-to-one onto these three exit points — that is not a coincidence; both descend from the same idea. Osherove frames it as *exit points of a unit of work* (practitioner, naming-oriented); Khorikov frames it as *styles scored against four pillars* (analytical). Use Osherove's framing to **decide what to assert and what to name the test**; use Khorikov's to **judge whether the test earns its keep**.

---

## The Three Pillars

Every test must be all three. When a test is failing the team in some way, diagnose which pillar it violates.

### Trustworthy — you believe a green test means working code, and a red test means a real bug
Achieve it by:
- **No logic in the test** (no `if`/`for`/`switch`/`while`/try-catch). Logic introduces the possibility that the *test* is buggy. (See Maintainability — this pillar and that one share the rule.)
- **Testing one concern per test**, so a failure is unambiguous.
- **Not testing through other untested code** — if the arrangement runs a pile of unverified logic, a pass proves little.
- **Separating unit from integration tests** so flakiness never contaminates the unit suite.
- **Never ignoring or commenting out a failing test.** A `[Fact(Skip="...")]` with no ticket is a lie the suite tells the team.
- **Avoiding "happy-only" coverage** — the bug paths are where the value is.

### Maintainable — the test doesn't cost more to keep than it's worth
Achieve it by:
- **Testing public contracts, not privates.** Tests bound to private methods break on every refactor.
- **Avoiding over-specification** — chiefly *over-mocking* (asserting on interactions that aren't the unit's purpose). Over-specified tests fail when behavior is unchanged.
- **Removing duplication** with factory/helper methods and parameterized tests, so a constructor change touches one place.
- **Keeping arrangement out of sight** when it's not the point of the test (extract a `Create…` helper or a builder).
- **Avoiding "constrained non-determinism"** — `DateTime.Now`, `Guid.NewGuid()`, random data that makes the same test produce different inputs each run. Inject the clock/RNG; assert on known values.

### Readable — the next person understands the requirement without a debugger
Achieve it by:
- **The naming convention** (next section) — the single biggest readability lever.
- **Arrange-Act-Assert** with the three blocks visibly separated.
- **Naming variables for their role** (`stubAuthService`, `mockEmailSender`, `expectedTotal`).
- **One assert-concept per test**, with FluentAssertions messages where a bare assert wouldn't localize.
- **No magic values** — name the constant or use an anonymous-value helper so the reader knows whether the value matters.

---

## THE NAMING CONVENTION (the centerpiece)

Osherove's enduring contribution. A unit-test name has **three parts separated by underscores**:

```
UnitOfWork_StateUnderTest_ExpectedBehavior
```

(equivalently stated as `MethodUnderTest_Scenario_ExpectedBehaviour`). Source: Roy Osherove, *Naming standards for unit tests*, https://osherove.com/blog/2005/4/3/naming-standards-for-unit-tests.html

1. **UnitOfWork** — the entry point / method / feature being exercised (the "what am I testing").
2. **StateUnderTest** — the scenario, condition, or inputs under which you're exercising it (the "given").
3. **ExpectedBehavior** — the observable end result you expect (the "then" — a return value, a state change, or a call to a collaborator).

The name reads as a sentence and is a *micro-specification*. When it fails in the runner, the name alone should tell you **what broke, under what condition, and what was supposed to happen** — without opening the test.

### Before / after

```csharp
// BAD — names that tell you nothing on failure
[Fact] public void Test1() { ... }
[Fact] public void TestWithdraw() { ... }
[Fact] public void WithdrawWorks() { ... }
[Fact] public void Sum_Should_Call_Add() { ... }   // describes HOW, not behavior

// GOOD — UnitOfWork_StateUnderTest_ExpectedBehavior
[Fact] public void Withdraw_AmountExceedsBalance_ThrowsInsufficientFunds() { ... }
[Fact] public void Withdraw_AmountWithinBalance_ReducesBalanceByAmount() { ... }
[Fact] public void IsValidLogFileName_EmptyFileName_ReturnsFalse() { ... }
[Fact] public void IsValidLogFileName_ValidExtension_ReturnsTrue() { ... }
[Fact] public void Sum_TwoPositiveNumbers_ReturnsTheirSum() { ... }   // describes behavior
[Fact] public void AnalyzeFile_TooManyLines_CallsWebServiceWithError() { ... } // exit point #3
```

**Reading the segments back against the unit-of-work model:** the third segment names which *exit point* you're verifying. `ReducesBalanceByAmount` → state change. `ThrowsInsufficientFunds` / `ReturnsTheirSum` → return value (or exception). `CallsWebServiceWithError` → call to a third-party (so this test, and only this test, will need a mock).

> This project's convention is the structurally identical `State_Trigger_Outcome` for aggregate tests, mirroring the `Fixture.Given(state).When(trigger).Then(outcome)` chain and the domain `Handle(trigger, state) → events` signature (see `Acacia.Test.Unit/.../CancelShipmentTests.cs` and the `test-data-patterns` skill). Same three-part spirit, project-local order.

> **Where Osherove differs:** Khorikov *softened* on naming in later writing (preferring plain English sentences over the rigid three-underscore form), and Meszaros speaks of names that "state the behavior." Osherove is the one who **codified the strict three-part underscore convention** — it is *his* signature. When the team wants a single mechanical rule that any developer applies the same way, this is it.

---

## Arrange-Act-Assert

Every unit test has three visible blocks, in order, separated by blank lines:

```csharp
[Fact]
public void Withdraw_AmountExceedsBalance_ThrowsInsufficientFunds()
{
    // Arrange
    var account = new Account(balance: 100m);

    // Act
    Action act = () => account.Withdraw(150m);

    // Assert
    act.Should().Throw<InsufficientFundsException>();
}
```

Rules Osherove attaches to AAA:
- **One Act per test.** Two "Act" blocks = two units of work = two tests (the *Eager Test* smell in Meszaros's vocabulary).
- **Arrange should be small.** If it isn't, extract it to a factory/helper so the test reads as Act-Assert with named setup. Large inline arrangement is a readability and maintainability smell.
- **Assert one concern.** Multiple asserts are fine *if they describe one logical end result*; asserting two unrelated results is two tests.

---

## Test Doubles — the Osherove way (stub vs mock, by who asserts)

Osherove cuts through the taxonomy with one practitioner's distinction. Memorize it:

- **Fake** is the *umbrella term* — any object that stands in for a real one. (Same role as Meszaros's "Test Double.")
- A **stub** is a fake you **do NOT assert against**. It exists to *replace an incoming dependency* — to feed the unit of work its *indirect input* so you can drive a code path. You can have **as many stubs as you like** in a test.
- A **mock** is a fake you **DO assert against**. It exists to verify an *outgoing call* — the unit's *indirect output*, i.e. exit point #3. The assertion (`mock.Verify(...)`) is the *whole point* of the test.

> **The defining line, in one sentence:** the difference between a stub and a mock is **whether the test asserts against it.** The *same* fake object can be a stub in one test and a mock in another — it depends on the role it plays *in that test*. This is Osherove's sharpest, most memorable formulation, and it is subtly different from how the others draw the line.

> **Where Osherove differs:**
> - **vs Meszaros:** Meszaros distinguishes five doubles by *construction and capability* (Dummy/Stub/Spy/Mock/Fake). Osherove collapses them to *two roles by intent* — assert against it (mock) or not (stub) — with "fake" as the umbrella. Osherove's "fake" = Meszaros's "Test Double"; Osherove's "mock" absorbs Meszaros's Spy+Mock.
> - **vs Khorikov:** Khorikov draws the *same* stub=input / mock=output line, then adds the crucial *managed-vs-unmanaged dependency* rule for **which** outgoing calls deserve a mock (only unmanaged ones). **Osherove tells you the role; Khorikov tells you whether that role is justified.** Use both: name the double by Osherove (is it asserted against?), then sanity-check by Khorikov (is the thing I'm mocking actually an external/unmanaged dependency, or am I freezing an internal relationship I'll regret?).

### The one-mock-per-test rule

> **Use at most ONE mock per test. Every other fake in that test is a stub.**

A test verifies *one* end result. Exit point #3 ("the unit calls a third party") is a single end result, so it needs a single mock. If a test asserts against two mocks, it is verifying two outgoing interactions — that's two units of work, hence two tests. More practically: **the more interactions you assert, the more over-specified and fragile the test becomes.** Every mocked interaction is a fact about *how* the unit works that the test now freezes in place; the next refactor breaks it. Stubs are free (they only feed input); mock assertions are expensive (they pin down behavior), so spend exactly one.

```csharp
[Fact]
public void AnalyzeFile_TooManyLines_CallsWebServiceWithError()
{
    // Arrange
    var stubLog = new Mock<IFileNameProvider>();              // STUB — feeds input, not asserted
    stubLog.Setup(l => l.GetFileName()).Returns("bigfile.txt");
    var mockWebService = new Mock<IWebService>();             // MOCK — the one we assert against

    var analyzer = new LogAnalyzer(stubLog.Object, mockWebService.Object)
    {
        LineCountToTriggerError = 10
    };

    // Act
    analyzer.Analyze(linesInFile: 15);

    // Assert  (exactly one mock, asserted once)
    mockWebService.Verify(
        w => w.LogError(It.Is<string>(s => s.Contains("Too many lines"))),
        Times.Once);
}
```

Note `stubLog` is *never* verified — verifying it would be over-specification (Khorikov: "never verify a stub"). Only the genuine exit point is asserted.

---

## SUT and Dependencies — values, stubs, mocks

When you set out to test a unit of work, classify each thing it touches:

- **Plain values / value objects / DTOs** → pass the **real** thing. Never fake data; it has no behavior to fake.
- **Incoming dependencies** (the unit *reads* from them — a config provider, a repository query, a clock) → **stub** them to feed the input that drives the scenario in segment 2 of the name.
- **Outgoing dependency** (the unit *calls* it as its purpose — the third party at exit point #3) → **mock** the one whose call is the behavior under test.

The classification *is* the test design. Once you know which dependency is the outgoing one, you know you have (at most) one mock, the rest are stubs, and the third name-segment describes that mock's expected call.

---

## Designing for Testability — Seams

Untestable code is code with no **seam** — no place to substitute a fake for a real dependency. Osherove's testability techniques are about *introducing seams*. (This is the same "seam" concept Michael Feathers uses — see the legacy section and the `working-effectively-with-legacy-code` skill.)

### Dependency injection — the preferred seams
Make dependencies replaceable from outside, in rough order of preference:
1. **Constructor injection** — the dependency is required; pass it in the constructor. The default and cleanest seam.
2. **Property (setter) injection** — the dependency is optional or has a sensible default; expose a settable property.
3. **Factory / parameter injection** — pass the dependency (or a factory for it) as a method parameter, or obtain it from an injectable factory. Useful when the lifetime is per-call.

```csharp
// No seam — untestable: news-up its own dependency
public class LogAnalyzer
{
    public bool Analyze(string fileName)
        => new FileExtensionManager().IsValid(fileName);   // hard-wired, cannot fake
}

// Seam via constructor injection — testable
public class LogAnalyzer(IExtensionManager manager)
{
    public bool Analyze(string fileName) => manager.IsValid(fileName);
}
```

### Extract-and-Override — the lightweight seam
When DI is heavy-handed (or you're working in legacy code you can't restructure freely), **extract the awkward bit into a virtual method, then override it in a test-only subclass.** This creates a seam *without* adding a constructor parameter or interface.

```csharp
public class LogAnalyzer
{
    public bool Analyze(string fileName) => GetExtension(fileName) == ".log";

    // the seam: a virtual method a test can override
    protected virtual string GetExtension(string fileName)
        => Path.GetExtension(fileName);                     // the real, hard-to-test bit
}

// test-only subclass overrides the seam — no DI, no interface needed
private sealed class TestableLogAnalyzer(string stubbedExtension) : LogAnalyzer
{
    protected override string GetExtension(string fileName) => stubbedExtension;
}

[Fact]
public void Analyze_NonLogExtension_ReturnsFalse()
{
    var analyzer = new TestableLogAnalyzer(".txt");
    analyzer.Analyze("whatever.txt").Should().BeFalse();
}
```

Extract-and-Override is Osherove's favorite *low-ceremony* way to fake **incoming** values, and the bridge to getting legacy code under test before you've earned the right to refactor it. (It is Feathers's *Subclass and Override Method*.)

### The trade-off of isolation (mocking) frameworks
Mocking frameworks (Moq, NSubstitute, FakeItEasy) make stubs and mocks cheap — but cheapness is a trap:
- **They make over-specification easy.** Because verifying a call is one line, teams verify *everything*, producing fragile, over-specified tests. The framework's convenience is exactly the danger.
- **They tempt you to test implementation.** A mock framework lets you assert on internal interactions that aren't observable behavior. Resist; assert only the genuine exit point.
- **Heavy/"unconstrained" frameworks** that can fake statics, sealed types, and non-virtuals (e.g. profiler-based ones) let you avoid designing seams at all — which *hides* the design feedback that hard-to-test code is giving you. Osherove's stance: prefer **constrained** frameworks that force you to introduce real seams (DI, interfaces, virtuals), because the friction is informative.

**Heuristic:** use a mocking framework for the *one* outgoing interaction you're verifying; hand-roll or use simple fakes/stubs for the incoming dependencies you reuse across many tests (Meszaros's *Hard-Coded* vs *Configurable* double trade-off).

---

## Writing Maintainable Tests

- **No logic in tests.** No `if`, `for`, `while`, `switch`, or `try/catch`. A branch means the test exercises more than one case (split it / parameterize), and any logic can itself be buggy — undermining trust. To assert "it throws," use FluentAssertions `Should().Throw<T>()`, never a hand-rolled try-catch.
- **One concern per test.** If you're tempted to assert a second, unrelated end result, write a second test. Defect localization depends on it.
- **Don't test private methods.** Privates are implementation detail; test them *through* the public entry point that uses them. If a private is so complex it begs for a direct test, that's design feedback — extract it to its own class with a public contract, then test that. (Don't reach for reflection or `[InternalsVisibleTo]` to poke privates — that bakes implementation into the test.)
- **Kill duplication.** Repeated arrangement → a `Create…` factory method or a Test Data Builder (see `test-data-patterns`). Repeated test bodies differing only in data → a parameterized test:

```csharp
[Theory]
[InlineData("file.log", true)]
[InlineData("file.txt", false)]
[InlineData("", false)]
public void IsValidLogFileName_VariousNames_ReturnsExpected(string name, bool expected)
    => LogNameValidator.IsValid(name).Should().Be(expected);
```
  (Note: a `[Theory]` is the *sanctioned* way to cover multiple cases — it is not "logic in the test," because there is still no branching inside the test body.)
- **Avoid constrained non-determinism.** Anything that varies run-to-run — `DateTime.Now`, `Guid.NewGuid()`, `Random`, current culture, ambient environment — makes the test's input change underneath it. Inject an `IClock` / seed / id-generator, and assert against the known value you fed in.
- **Keep the Arrange small and the Assert focused** so the test reads top-to-bottom as a specification.

---

## Trust — keep the suite believable

A test suite is only an asset if the team *believes* it. Erosion of trust is how good suites die.

- **No flaky / erratic tests in the unit suite.** A test that passes sometimes trains everyone to ignore red. Find the cause (shared state, uncontrolled time/RNG, ordering, real I/O) and fix it or move the test to the integration suite.
- **Separate unit tests from integration tests** — different projects/folders/CI stages. The unit suite must be *all green, all fast, all the time*; mixing in slow/occasionally-red integration tests destroys that guarantee. (Acacia already splits these: `Acacia.Test.Unit` vs `Acacia.Test.Integration` / `Acacia.Test.Docker`.)
- **Never comment out or `Skip` a failing test silently.** Either fix it, or delete it with a tracked follow-up. A disabled test is invisible rot.
- **Tests must be independent** — any order, any subset, no shared mutable state. A test that only passes after another ran is not trustworthy.
- **A test that has never been seen to fail proves nothing.** Make a new test fail first (wrong assertion, or red before the code exists) so you know it can.

---

## Working with Legacy Code

Osherove devotes the book's hardest chapter to introducing tests into code that has none, and explicitly hands off to **Michael Feathers's *Working Effectively with Legacy Code*** for the deep technique. (See the `working-effectively-with-legacy-code` skill.)

The practitioner's playbook:
- **Find the seams.** Where can you substitute a fake? If there are none, your first job is to *create* one — minimally, with the least risky change.
- **Prefer the least-invasive seam first.** Extract-and-Override often beats a big DI refactor when the code is fragile and untested, precisely because it changes less.
- **Test the easy parts first.** Map the components by *how hard to test* × *how risky/important*. Start where you get coverage cheaply to build a safety net, then tackle the gnarly high-value parts once you have *some* tests guarding you.
- **Characterize before you change.** Pin current behavior with tests (even if "current" is buggy) so a refactor that should preserve behavior provably does. (Feathers's *characterization tests* — also in the TDD skill's approval-testing note.)
- **Break dependencies just enough** to get the unit under test — Sprout/Wrap Method, Extract Interface, Subclass-and-Override. Don't redesign the world; earn the right to refactor by first getting a test around the change point.

> **Where Osherove differs / complements:** Osherove gives the *attitude and the on-ramp* (find seams, easy parts first, prefer Extract-and-Override, when to bring in a framework); Feathers gives the *exhaustive catalogue of dependency-breaking moves*. Use Osherove to decide where to start and how aggressive to be; use `working-effectively-with-legacy-code` for the specific surgical technique.

---

## The Organizational "Art"

The book's later chapters are about making unit testing *stick in a team* — the part that's an art, not a mechanic.

- **Tests belong in CI.** A test that doesn't run on every push, automatically, with a red build on failure, is decoration. The build going red must *mean something* and *stop the line*.
- **The test pyramid.** Many fast unit tests at the base, fewer integration tests in the middle, a thin layer of slow end-to-end tests at the top. Inverting it (mostly slow UI/integration tests) yields a suite too slow to run and too flaky to trust. Unit tests — fast, isolated, in-memory — are the broad base; this skill governs that base. (Khorikov's and Meszaros's pyramids agree.)
- **Cost/benefit of test maintenance is real.** Every test is a liability as well as an asset; a brittle, over-specified, or duplicated test can cost more than it catches. Periodically *delete* tests that no longer earn their keep (redundant, testing trivia, or pinned to dead implementation). Refactor test code as ruthlessly as production code — it *is* production code.
- **Gaining team buy-in** is a change-management problem, not a technical one: start with a champion, demonstrate value on a real pain point, measure (fewer regressions, faster change), make it the path of least resistance, and don't mandate from on high without support. Expect and address resistance ("no time to test," "QA's job," "my code works").
- **A failing test should never be the new normal.** The moment a red build is routine, the suite has stopped being a safety net.

---

## Quick Application Checklist

Before writing a test:
- [ ] What is the **unit of work** — the public entry point I'm calling?
- [ ] Which of the **three exit points** am I verifying (return value / state change / call to a third party)? (Exactly one.)
- [ ] Does that tell me whether I need a **mock at all** (only exit point #3) and that I have **at most one**?

While writing it:
- [ ] Is the name `UnitOfWork_StateUnderTest_ExpectedBehavior` (three parts), and does the third part name the exit point?
- [ ] Are **Arrange / Act / Assert** visibly separated, with exactly one Act?
- [ ] Is every fake correctly a **stub** (not asserted) except the **single mock** (asserted)? Are stub/mock variables named for their role?
- [ ] Am I passing **real values**, stubbing **incoming** deps, mocking the **one outgoing** dep?
- [ ] Any **logic** (`if`/`for`/`switch`/`try`)? Any **non-determinism** (`DateTime.Now`, `Guid.NewGuid()`, `Random`)? Remove both.
- [ ] Am I testing through the **public contract**, not a private?

For the suite (Trustworthy/Maintainable/Readable):
- [ ] Unit tests **separated** from integration tests; unit suite all-green-all-fast?
- [ ] Any **flaky**, **skipped**, or **commented-out** tests to fix or delete?
- [ ] Any **over-specified** tests (verifying interactions that aren't the exit point) to relax?
- [ ] Any **duplicated arrangement** to fold into a builder/factory or `[Theory]`?
- [ ] Does each test **fail for one reason**, and does its **name** tell you which on failure?

---

## Related skills

- **test-driven-development** — the *workflow* (red/green/refactor, outside-in). Osherove is largely **test-after-friendly and tool-agnostic about workflow**: his subject is the *quality of the test you write*, whenever you write it. Use TDD for *when/how to drive design with tests*; use this skill for *naming, structuring, and faking* the individual test.
- **unit-testing-principles** (Khorikov) — the *analytical* lens (four pillars, observable behavior, **managed vs unmanaged** dependencies). Osherove and Khorikov agree that stub=input / mock=output; Osherove adds the memorable **"a mock is the fake you assert against"** and the **one-mock-per-test** rule, while Khorikov adds **which** outgoing calls deserve a mock. Name the double with Osherove; justify it with Khorikov.
- **xunit-test-patterns** (Meszaros) — the *taxonomy and smell catalogue* (five doubles, four-phase test, fixtures, named smells). Osherove **collapses Meszaros's five doubles into two roles** (stub vs mock, by who asserts) and is far more prescriptive about **naming**. Use Meszaros for precise vocabulary and the smell names; use Osherove for the opinionated day-to-day rules.
- **test-data-patterns** — Object Mother + Test Data Builder, the project's `Fixture.Given().When().Then()` convention. This is the concrete machinery for Osherove's "kill duplication / keep Arrange small / avoid irrelevant information" maintainability rules.
- **working-effectively-with-legacy-code** (Feathers) — the deep catalogue of seams and dependency-breaking moves. Osherove points here for legacy work; he supplies the *strategy* (easy parts first, least-invasive seam, Extract-and-Override), Feathers supplies the *technique*.

## Reading

- **Roy Osherove**, *The Art of Unit Testing, Second Edition* (Manning, 2013) — the canonical edition, with all examples in **C#/.NET**. The reference for this skill.
- **Roy Osherove**, *The Art of Unit Testing, Third Edition* (Manning, 2024) — updated and rewritten with **JavaScript** examples; same principles, modern stack. Read the 2nd for C# code, the 3rd for the refreshed thinking.
- **Roy Osherove**, *Naming standards for unit tests* (2005) — https://osherove.com/blog/2005/4/3/naming-standards-for-unit-tests.html — the original source of `UnitOfWork_StateUnderTest_ExpectedBehavior`.
- **Roy Osherove**, ArtOfUnitTesting.com and his blog — supplementary articles and the book's sample code.
- **Michael Feathers**, *Working Effectively with Legacy Code* (2004) — the companion for the legacy chapter (seams, characterization tests).
- **Gerard Meszaros**, *xUnit Test Patterns* (2007) — the double taxonomy and smell catalogue Osherove simplifies.
- **Vladimir Khorikov**, *Unit Testing Principles, Practices, and Patterns* (2020) — the rigorous trade-off companion; sharpens *which* dependencies to mock.
- **Martin Fowler**, *Mocks Aren't Stubs* (essay) — the foundational stub/mock distinction both Osherove and Khorikov build on.
