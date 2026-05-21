---
name: test-driven-development
description: Apply Test-Driven Development to drive outside-in design in small steps. Centers on the London/mockist school (Freeman & Pryce's GOOS, Sandro Mancuso's outside-in teaching) with Kent Beck's classical foundations and Mark Seemann's pragmatic heuristics. Covers sociable vs solitary unit tests and when to prefer each (anticipated refactoring → sociable). Use when starting a new feature, designing object interactions, building a vertical slice end-to-end, deciding what to test next, choosing the test boundary before refactoring, or rescuing a design that resists testing.
---

# Test-Driven Development for Outside-In Design

Use TDD when starting any non-trivial feature, designing how objects collaborate, growing a system in small verifiable steps, or letting tests reveal design problems before they become expensive. This skill emphasizes **outside-in TDD** — driving the design from the user-visible boundary inward, one failing test at a time.

## Core Philosophy

**TDD is a design technique, not a testing technique.** The tests are a side effect; the real product is a design that is easy to change. If tests pass but the design is rotten, TDD has failed regardless of coverage.

**Listen to the tests.** Difficulty writing a test is feedback about the design, not the test. Hard-to-test code is hard-to-change code.

**Small steps beat large leaps.** The discipline is to take the smallest step that visibly progresses toward the goal. Speed comes from never being stuck or rolling back significant work.

**Red, Green, Refactor — in that order, every time.** Skipping a phase compounds into rot.

**Outside-in over inside-out** (when the design is non-trivial). Start from the user-facing boundary and let each test pull the next collaborator into existence. This avoids speculative infrastructure and ensures every piece exists because something needs it.

---

## The TDD Cycle (Beck)

```
        ┌──────────────────┐
        │  Write a failing │
        │      test        │  ← Red
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │  Make it pass    │
        │  (simplest way)  │  ← Green
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │  Refactor without│
        │  changing tests  │  ← Refactor
        └────────┬─────────┘
                 │
                 └──────────► back to Red
```

### Beck's Three Laws of TDD
1. You may not write production code unless it is to make a failing unit test pass.
2. You may not write more of a unit test than is sufficient to fail (compilation failures count).
3. You may not write more production code than is sufficient to pass the currently failing test.

These laws sound extreme but enforce the small-steps discipline. The point is not legalism — it is to make "I am about to write more than the test demands" a visible, conscious decision.

---

## The Two Schools

### Classical / Detroit (Beck)
- Test from the **state** of the system after the action.
- Prefer **real collaborators** where possible; mock only at I/O boundaries.
- "Triangulate" toward a general implementation with multiple examples.
- Design emerges from refactoring.

### London / Mockist (Freeman & Pryce, Mancuso)
- Test from the **interactions** between objects.
- Mock **collaborators** to isolate the unit under test.
- Mocking forces explicit design of **roles and contracts** at each step.
- Design is *driven* by tests, not just *emerging* from them.

**Outside-in TDD belongs primarily to the London school.** The two are not enemies — many practitioners blend them — but the disciplined outside-in flow described here is London in spirit.

---

## Sociable vs Solitary Unit Tests

A related but distinct distinction (Jay Fields, *Working Effectively with Unit Tests*; Martin Fowler, *UnitTest* bliki):

- **Solitary test** — exercises one class in complete isolation. Every collaborator is mocked, no matter how trivial. Each test owns its target class; the class boundary IS the test boundary.
- **Sociable test** — exercises a unit composed of multiple cooperating classes. Mocks live only at **architectural seams** (I/O, time, randomness, external services). Internal collaborators are real instances.

The two schools above bias toward different defaults:
- London/mockist → solitary by default.
- Classical/Detroit → sociable by default.

### The refactor-stability consequence

**Sociable tests survive structural refactoring within their unit. Solitary tests do not.**

When you rename a class, extract a helper, split one class into three, or replace `switch` with polymorphism — solitary tests break because the mocked class boundaries no longer match the code. Sociable tests stay green because their mocks are at the architectural boundary, which didn't move.

This is not a minor detail. It is often the *dominant* cost of solitary testing: every internal refactor pays test-rewrite tax. Over a system's lifetime, that tax dwarfs the cost of the slightly slower or slightly less-localizable sociable tests.

### Heuristic: anticipated refactoring → sociable

When the code you are testing is likely to be refactored — and most code is, eventually — write the tests sociable. Specifically:

- Mock at I/O, network, time, randomness, external services. **Not** at every internal class boundary.
- Let test names describe *behavior* (`DpShipper_WithRates_ReturnsRatesFromRepository`) not class-internals (`Selector_CallsDpProvider`).
- When the refactor happens, only the test *setup* (constructor wiring) changes. Test methods stay identical.

The case where solitary is genuinely better:
- The class under test is a stable, well-understood unit unlikely to be restructured.
- Precise failure localization is high-value (a 1000-test suite where you need to know *exactly* which class broke).
- The collaborators are slow, non-deterministic, or have complex setup.

### What "unit" means

In sociable testing, the **unit** is a *behavior* — a coherent piece of system functionality — not a class. A unit may span 1 class or 5; what matters is that the test mocks at the architectural seam, treats the inside as an implementation detail, and verifies the behavior the user (or caller) actually observes.

This is the framing behind Kent Beck's quip that "a unit test is a test that doesn't talk to anything you wouldn't run on an airplane" — it's about *fast and isolated from infrastructure*, not *one class*.

### Worked illustration

Imagine a calculation flow with a `Selector` that today dispatches via `switch (type)`. Tomorrow, you replace the switch with polymorphism: `Selector` + 3 `Provider` classes.

**Solitary tests:** test methods reference `mockProvider.Verify(...)` (boundary at the provider class). When the polymorphism lands, the mocked-collaborator boundary is *new* — the old tests don't apply. You rewrite the selector tests and add new provider tests.

**Sociable tests:** test methods reference `mockRepository.Verify(...)` (boundary at the repository — the architectural seam). When the polymorphism lands, the repository boundary is *unchanged*. The selector still ends up calling the repository (now via a real provider in the middle). The same `Verify` assertions still hold. Only the constructor changes (you now wire up the providers).

The sociable suite stays green with a constructor edit. The solitary suite needs rewriting. **Both verify the same end-state behavior** — but the cost asymmetry is enormous.

---

## Outside-In, Step by Step (Double-Loop TDD)

The canonical outside-in flow has two nested loops.

```
OUTER LOOP (acceptance test — slow, end-to-end)
│
├─ 1. Write a failing acceptance test for the feature.
│
│   INNER LOOP (unit tests — fast, focused)
│   │
│   ├─ 2. Pick the outermost object the acceptance test exercises.
│   ├─ 3. Write a failing unit test for one behavior of that object.
│   ├─ 4. Discover the collaborators it needs — mock them.
│   ├─ 5. Make the unit test pass.
│   ├─ 6. Refactor.
│   ├─ 7. Repeat for next behavior of this object.
│   │
│   └─ When the object is complete, move inward to a mocked collaborator
│      and repeat the inner loop for it. Replace its mock with the real
│      thing in the acceptance test as each layer becomes real.
│
└─ 8. When all collaborators exist, the acceptance test passes.
```

### Walking through the flow

**1. Failing acceptance test.** Express the feature at the system boundary — HTTP endpoint, CLI command, user gesture. It will fail because nothing exists yet. That's the point: the failure tells you what to build next.

**2. Walking skeleton.** Before the first real feature, get an end-to-end pipeline running with the thinnest-possible implementation (a hardcoded response, a single endpoint). This proves the deployment path, integration points, and tooling are in place.

**3. Start at the boundary object.** What is the first object the system needs to handle this request? A controller, a command handler, an entry point. Write a unit test for its first responsibility.

**4. Let mocks reveal the design.** When that object needs to do something it doesn't know how to do, mock a collaborator that *would* know. The mock's interface is a *design decision* — you are inventing the role you need.

**5. Make it pass with the simplest code that uses the mock.**

**6. Refactor.** Names, structure, duplication. Keep tests green.

**7. Now go inward.** The mock you just invented points at an object that doesn't exist. Make it exist by repeating the inner loop for it. Inside *its* tests, mock *its* collaborators in turn.

**8. Replace mocks with real objects in the acceptance test** as each layer becomes real. Eventually the acceptance test passes against the real implementation end-to-end.

This is **Sandro Mancuso's double-loop TDD** and **Freeman & Pryce's "growing the system"** in one description.

---

## Listening to the Tests

This is the central design feedback loop of London-school TDD.

| Test Pain | Likely Design Problem |
|---|---|
| Test setup requires many mocks | Too many collaborators — class is doing too much (SRP) |
| Mocks return mocks return mocks | Train wreck — violates Law of Demeter |
| Test reaches into private state to assert | Behavior should be observable via the public API |
| Mock verifies a chain of calls | Method is procedural; the abstraction is wrong |
| Adding a new feature breaks unrelated tests | Coupling is too tight; shared mutable state likely |
| The test is hard to name | The behavior is not a coherent unit |
| Setup is duplicated across many tests | Missing abstraction — extract a builder or helper |
| You don't know what to mock | The object's responsibilities are unclear |

**When the test resists you, fix the design — not the test.** This is the single most important habit in mockist TDD.

---

## Test Doubles (Meszaros via Freeman & Pryce)

Distinguish the kinds of fakes; use the right one.

- **Dummy** — a placeholder. Never called. Exists only to satisfy a parameter list.
- **Stub** — returns canned answers. Used for indirect inputs ("when asked X, return Y").
- **Fake** — a working implementation simpler than the real one (in-memory repository, fake clock).
- **Spy** — records calls for later inspection.
- **Mock** — pre-programmed with expectations; fails the test if not called as expected. Used to verify **outgoing interactions** that matter for behavior.

**Stubs check what comes in; mocks check what goes out.** Use mocks for collaborators whose interaction is part of the contract under test. Use stubs for collaborators that merely supply data.

**Don't mock what you don't own.** Wrap third-party libraries in your own interfaces, then mock the wrapper. Direct mocks of external code are brittle and tie your tests to the library's API.

**Don't mock value objects, DTOs, or pure functions.** They have no behavior to verify; use real instances.

---

## Beck's Patterns for Small Steps

When the gap between red and green feels too large, Beck's *TDD by Example* gives three moves:

### Fake It (Till You Make It)
Return a hardcoded value to make the test pass. Then write the next test that forces a real implementation.

```csharp
[Fact] public void Sum_OfTwoNumbers_IsCorrect()
    => Adder.Add(2, 3).Should().Be(5);

// Step 1 (faked):
public static int Add(int a, int b) => 5;

// Step 2: add another test that forces generalization.
[Fact] public void Sum_OfDifferentNumbers_IsCorrect()
    => Adder.Add(10, 7).Should().Be(17);

// Now you must implement:
public static int Add(int a, int b) => a + b;
```

### Triangulate
When uncertain about the abstraction, write two or three examples that force the right generalization. Each new example moves the implementation closer to the real algorithm.

### Obvious Implementation
When the implementation is genuinely obvious (a simple delegation, a clear formula), write it directly. Do not fake it for ceremony's sake. Honesty about the size of the step matters more than the size itself.

**Pick the smallest move that visibly progresses.** Faking is for when you're stuck on the design. Triangulation is for when you don't know the algorithm. Obvious implementation is for when both are clear.

---

## The Test List

Before writing any test, write a list of all the tests you think you'll need for this feature. This is a **scratch list**, not a plan. As you work:
- Add tests as you discover them.
- Cross off tests as you implement them.
- Reorder by which test would teach you the most or be easiest first.

The list externalizes working memory and prevents "what was I trying to do?" loss during a long session. It is private — throw it away when the feature is done.

---

## Refactoring Discipline

**Refactor only when green.** Changing structure and behavior at once means you cannot tell which is broken when a test fails.

**Each refactor is a tiny atomic change** — rename, extract method, inline variable. Run tests after each. If they fail, undo and try smaller.

**Refactor every cycle.** Resisting the urge to clean up "later" is what separates working TDD from "test-after-coding".

**Refactor tests too.** Test code is first-class. Duplication in tests rots; clear test code documents the system.

**Listen to refactoring pain.** If you can't easily rename, extract, or split — the design is too rigid. The pain itself is information.

---

## When to Mock, When Not To

Mock:
- Collaborators that perform I/O (DB, network, FS, clock).
- Collaborators whose interaction is the behavior being tested ("did we publish the event?").
- Collaborators not yet implemented in outside-in flow.
- Slow, non-deterministic, or external dependencies.

Do not mock:
- Value objects, DTOs, pure functions.
- The system under test itself.
- Third-party libraries directly — wrap and mock the wrapper.
- Things you could just use the real version of cheaply (in-memory collections, simple data structures).

**A useful rule:** mock at architectural seams (I/O, time, randomness, external systems). Use real objects within a unit's own bounded responsibility.

---

## Test Design Principles

### FIRST (Beck via Clean Code)
- **Fast** — milliseconds, so you run them constantly.
- **Independent** — any order, any subset.
- **Repeatable** — same result every time, every environment.
- **Self-validating** — pass/fail, no manual interpretation.
- **Timely** — written just before the code, not later.

### Arrange-Act-Assert (Given-When-Then)
Each test has three visible sections:
```csharp
[Fact]
public void Withdraw_MoreThanBalance_Throws()
{
    // Arrange (Given)
    var account = Account.WithBalance(100m);

    // Act (When)
    Action act = () => account.Withdraw(150m);

    // Assert (Then)
    act.Should().Throw<InsufficientFundsException>();
}
```

### One concept per test
Not "one assert" — *one concept*. A test can have multiple asserts if they verify one logical outcome. It should not test two unrelated things.

### Name tests to read as specifications
`Withdraw_MoreThanBalance_Throws` reads like a requirement. `TestWithdraw1` does not. Test names are documentation that runs.

### Use builders for test data
When test setup grows beyond a few lines, extract a builder:
```csharp
var order = OrderBuilder.AnOrder()
    .ForCustomer("c-42")
    .WithLineItem("sku-1", quantity: 2)
    .Build();
```
Builders encode defaults, isolate tests from constructor churn, and read as domain prose.

---

## Property-Based and Approval Testing (Seemann)

Example-based tests prove behavior for specific inputs. Two complementary techniques:

### Property-based testing (FsCheck, Hedgehog, Hypothesis)
Express invariants the code must satisfy over an *infinite* domain; the framework generates random inputs to falsify them.

```csharp
// Property: reverse(reverse(xs)) == xs
[Property] public void DoubleReverse_IsIdentity(int[] xs)
    => Enumerable.Reverse(Enumerable.Reverse(xs)).Should().Equal(xs);
```

Strong for pure functions, value objects, and the functional core.

### Approval / characterization tests
Capture the current output of code as the "approved" output; future runs compare against it. Indispensable for refactoring legacy code under a safety net before you can write proper specs.

---

## Common TDD Pitfalls

- **Writing tests after the code.** You will write fewer, less probing tests, and you will miss the design feedback. This is "Test-After Development", not TDD.
- **Skipping the refactor step.** Tests pass, code rots. Within a few cycles the design has degraded beyond recovery.
- **Testing implementation details.** Tests fail on harmless refactorings. Test behavior visible through the public API.
- **Mocking everything.** "Mock everything" tests verify implementation, not behavior, and break on every change.
- **Mock-then-implement-mock.** Mocking the same method you're testing. Test the real thing.
- **Mocking value objects.** Just use them.
- **Brittle setup.** Tests with 50 lines of setup are unmaintainable. Refactor the design or the test helpers.
- **Forgetting acceptance tests.** Unit tests alone don't prove the system works.
- **Tests that never fail.** A test that has never failed has not been verified to test anything. Make it fail first.
- **Slow test suites.** A multi-minute suite stops being run; tests stop being trusted. Optimize ruthlessly.
- **Test code worse than production code.** Test code IS code. Refactor it; name it; structure it.

---

## TDD and Outside-In: Why It Works

Outside-in TDD with mocks produces:

- **No speculative code.** Every class, every method, every field exists because some test demanded it.
- **Designed-in modularity.** Mock-driven design forces explicit roles, contracts, and seams.
- **Fast test suites.** Unit tests don't touch I/O; mock collaborators are nanoseconds.
- **Living documentation.** Tests describe behavior at every level, from acceptance to unit.
- **Confident refactoring.** Tests cover behavior, not structure; structure is free to change.
- **Discoverable design.** The act of writing the next test pulls the next abstraction into focus.

The cost is discipline. The cycle is fast but unforgiving — every shortcut is paid back later.

---

## A Worked Outside-In Example (Sketch)

Feature: "POST /reservations creates a reservation if capacity is available."

1. **Acceptance test (fails)**: POST a reservation, expect 201 + saved record.
2. **Pick the boundary**: `ReservationsController`. Test: `Post_WithValidReservation_Returns201`.
3. **The controller needs to decide and persist**. Mock `IReservationService`. Make the test pass by delegating to it.
4. **Refactor**.
5. **Next inner step**: implement `ReservationService`. Test: `Reserve_WhenCapacityAvailable_ReservesAndReturnsSuccess`.
6. **The service needs to check capacity and persist**. Mock `ICapacityChecker` and `IReservationRepository`.
7. **Continue inward** until repository and capacity checker are implemented (these touch real I/O — test with in-memory fakes or integration tests).
8. **Replace mocks in the acceptance test** with the real wiring. The acceptance test passes against the real stack.
9. **Add the unhappy paths** as additional acceptance tests, repeating the inner loop wherever new behavior is needed.

Each commit along the way is shippable. The design emerged; nothing speculative was built.

---

## Quick Application Checklist

Before each cycle:
- [ ] Is there a failing test? (If not, write one — don't write production code.)
- [ ] Is the test small enough that a few lines of production code will make it pass?
- [ ] Have you written the *next* test on your test list, not all of them at once?

After making green:
- [ ] Did you do the minimum to pass? (No speculative code.)
- [ ] Have you refactored? (Names, duplication, structure.)
- [ ] Are tests still green after the refactor?
- [ ] Did the test pain reveal a design issue worth addressing?

For the suite as a whole:
- [ ] Is it fast (seconds, not minutes)?
- [ ] Is each test FIRST?
- [ ] Are the tests readable as specifications?
- [ ] Do tests cover behavior, not implementation?
- [ ] Are mocks at architectural seams, not everywhere?
- [ ] Have I avoided mocking what I don't own?

For outside-in specifically:
- [ ] Is there an acceptance test driving the work?
- [ ] Am I working from the boundary inward, layer by layer?
- [ ] Does each new mock represent a real role I would name in a design conversation?
- [ ] Have I replaced mocks with real implementations as inner layers became real?

---

## Reading

- Kent Beck, *Test-Driven Development by Example* (2002) — the foundational text. Read it twice.
- Steve Freeman & Nat Pryce, *Growing Object-Oriented Software, Guided by Tests* (2009) — the canonical outside-in / London-school book. The worked example is essential.
- Sandro Mancuso, *The Software Craftsman* (2014) — context for outside-in within the craftsmanship movement.
- Sandro Mancuso, talks on outside-in TDD and "TDD: where did it all go wrong" — corrective for common misapplications.
- Vladimir Khorikov, *Unit Testing Principles, Practices, and Patterns* (Manning, 2020) — the rigorous companion to this skill, covering what makes a *good* test. See the `unit-testing-principles` skill.
- Mark Seemann, *Code That Fits in Your Head* (2021) — pragmatic TDD heuristics, property-based testing, fits with the fractal-architecture skill.
- Gerard Meszaros, *xUnit Test Patterns* (2007) — test smells and test-double taxonomy.
- Michael Feathers, *Working Effectively with Legacy Code* (2004) — characterization tests, seams, getting legacy code under test.

**Related skill:** For evaluating test *quality* — when reviewing a PR, deciding what to mock, or resolving disagreements about test style — see the **unit-testing-principles** skill (Khorikov's framework: the four pillars, three styles, observable behavior vs implementation details, managed vs unmanaged dependencies).
- Martin Fowler, *Mocks Aren't Stubs* (essay) — the classic distinction between the two schools.
