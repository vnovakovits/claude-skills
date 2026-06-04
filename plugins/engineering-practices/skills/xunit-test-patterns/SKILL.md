---
name: xunit-test-patterns
description: Apply Gerard Meszaros's "xUnit Test Patterns: Refactoring Test Code" (2007) — the canonical catalogue of test-automation patterns, the test-double taxonomy (Dummy, Stub, Spy, Mock, Fake), test smells, fixture strategies, and result-verification patterns. Use when writing or refactoring test code; diagnosing brittle, slow, erratic, or obscure tests; choosing and naming a test double; designing fixtures (fresh vs shared, Object Mother, Test Data Builder, setup styles); structuring the four-phase test; deciding where to draw the test boundary (subcutaneous / layer / round-trip); faking out-of-process dependencies (in-memory fake database, back-door manipulation); or rescuing a test suite that has become a maintenance burden. Complements test-driven-development (the workflow), unit-testing-principles (what makes a test good), and test-data-patterns (builders and mothers).
---

# xUnit Test Patterns (Gerard Meszaros)

Apply this skill when the question is **"is this test code any good, and how do I make it better?"** — naming and choosing test doubles, shaping fixtures, killing duplication and flakiness, and deciding what boundary a test should exercise. Meszaros's book is the source of the vocabulary the whole industry now uses (he coined *Test Double*, *Mock Object* in its precise sense, *Fake Object*, *Object Mother*, *Mystery Guest*, *Assertion Roulette*). This skill is the catalogue; pair it with **test-driven-development** for the red/green/refactor workflow and **unit-testing-principles** for the four-pillars trade-off analysis.

## Core Philosophy

**Test code is production code.** It is read, changed, and relied upon for the life of the system. It deserves the same care — naming, structure, DRY-ness — and the same refactoring discipline.

**Tests must be cheap to maintain, or they get deleted or ignored.** The dominant long-term cost of a test suite is maintenance, not authoring. Every pattern in the book ultimately serves *maintainability* and *trust*.

**A test is a specification, not just a check.** Its first job is to communicate intent to the next reader. If a test passes but no one can tell what requirement it encodes, it has failed at its primary job.

**Tests should fail for exactly one reason, and that reason should be obvious.** Defect localization — a failing test pointing straight at the cause — is what makes a suite a safety net rather than an alarm that everyone learns to ignore.

### Qualities of a good automated test
Fully automated · Self-checking (no human reading output) · Repeatable (any order, any number of times, any environment) · Robust (survives unrelated change) · Simple (tests one thing) · Fast · **and above all: do no harm** — the act of testing must not corrupt the system or other tests.

---

## The Four-Phase Test

Every test, regardless of framework, has four phases. Keep them visible and in order; blank lines or comments mark the seams.

```
1. Setup    — establish the fixture (the SUT and everything it needs)
2. Exercise — invoke the System Under Test (SUT)
3. Verify   — assert the outcome (state or behaviour)
4. Teardown — release any fixture that would otherwise leak
```

This is the structural sibling of Arrange-Act-Assert / Given-When-Then. The key discipline: **don't interleave the phases.** A test that exercises, asserts, exercises again, asserts again is usually two tests wearing one coat (the *Eager Test* smell).

**Testcase Class organisation** — three strategies, choose per cohesion:
- *Testcase Class per Class* — default; one test class per production class.
- *Testcase Class per Feature* — group tests by feature/behaviour spanning classes.
- *Testcase Class per Fixture* — one class per distinct starting state, so all its tests share one Implicit Setup. Powerful for state machines with several "given" states.

---

## Test Doubles — the canonical taxonomy

**Test Double** is the umbrella term (like "stunt double") for any pretend object standing in for a real collaborator. The five kinds are *not* interchangeable; pick by **what role the double plays in the test**.

| Double | Purpose | Verifies? | Use when |
|---|---|---|---|
| **Dummy** | Fills a parameter slot; never actually used | No | The SUT requires an argument irrelevant to this test |
| **Test Stub** | Feeds the SUT *indirect inputs* (canned return values) | No | You need to control what a query returns to drive a path |
| **Test Spy** | A stub that also *records* the calls it received, for later assertion | After (by the test) | You want behaviour verification but prefer assert-at-the-end |
| **Mock Object** | Pre-programmed with *expectations*; checks calls as they happen, fails fast | During (by the mock) | The outgoing call **is** the behaviour under test |
| **Fake Object** | A real, working, lighter-weight implementation | No (you assert on its state) | The real thing is slow/awkward — e.g. in-memory database |

Sharper distinctions Meszaros draws:
- **Stub vs Mock** (the Fowler "Mocks Aren't Stubs" line): a **Stub** provides *indirect input* — you ask it for data. A **Mock** verifies *indirect output* — you check that the SUT sent it the right message. Stubs answer queries; mocks confirm commands. (`unit-testing-principles` sharpens this with managed/unmanaged dependencies.)
- **Configurable vs Hard-Coded Test Double** — a Hard-Coded double has its behaviour baked in (a hand-written `FakeOliveServiceV3`); a Configurable double is set up per-test (Moq's `Setup(...).Returns(...)`). Hard-coded doubles read cleanly and are reusable; configurable doubles are flexible but verbose. Prefer hand-rolled fakes for collaborators reused across many tests; configurable mocks for one-off interaction checks.
- A **Saboteur** is a stub that throws, to exercise error paths. A **Responder** is the happy-path stub.

**Don't double what you don't own** — wrap a third-party API in your own interface and double the wrapper.

---

## Fixture Strategies

The **fixture** is everything you build before exercising the SUT. The central tension is **Fresh Fixture vs Shared Fixture**.

- **Fresh Fixture** (default, strongly preferred) — each test builds and tears down its own fixture. Maximises independence and repeatability; no inter-test coupling. Can be *Transient* (in-memory) or *Persistent* (rebuilt in the DB each time).
- **Shared Fixture** — many tests reuse one fixture (a *Prebuilt Fixture*, a class-level setup, a seeded database). Faster, but the source of most *Erratic Test* smells (Interacting Tests, Test Run War, Unrepeatable Test). Only share **immutable** fixtures, and never let one test's writes be visible to another.

**Setup styles:**
- *Inline Setup* — build the fixture inside the test. Most explicit; risks duplication.
- *Delegated Setup* — extract a **Creation Method** (`CreateActiveShipment(...)`) called from each test. The pragmatic default once setup repeats.
- *Implicit Setup* — a `setUp`/constructor that runs before every test in the class. Good with *Testcase Class per Fixture*; risks the *General Fixture* / *Mystery Guest* smell if it builds more than each test needs.
- *Lazy Setup*, *SuiteFixture Setup*, *Setup Decorator*, *Chained Tests* — heavier shared-fixture mechanisms; use sparingly.

**Creating test data — and the bridge to `test-data-patterns`:**
- **Object Mother** — a factory class of named, ready-made domain objects (`Builders.AnActiveShipment()`). Centralises canonical examples.
- **Test Data Builder** — a fluent, defaulted builder (`new ShipmentBuilder().WithCarrier(x).IsDropOff().Build()`) that states only what matters and defaults the rest. The antidote to the *constructor-with-twelve-arguments* and *Irrelevant Information* smells.
- **Parameterized / Anonymous Creation Method** — generate distinct, irrelevant values so the reader knows "the specific value doesn't matter."
- **Automated Teardown** — track what was created and tear it down generically, rather than fragile hand-written teardown.

> This project's stack is **chained Fixture + Object Mother + Test Data Builder** — see the `test-data-patterns` skill and `Acacia.Test.Unit/.../Builders/`.

---

## Result Verification

- **State Verification** — exercise the SUT, then assert on resulting state / return value. The default; least coupled to implementation.
- **Behaviour Verification** — assert on the calls the SUT made to its doubles (Spy or Mock). Necessary only when the outgoing call *is* the observable behaviour (a command to an external system). Over-using it produces *Fragile Tests*.
- **Custom Assertion** — a domain assertion (`ShouldBeAnActiveShipmentFor(id)`) that hides comparison detail and improves the failure message. Define one when the same multi-step assertion recurs.
- **Verification Method** — an extracted method bundling the Verify phase, for reuse and intent.
- **Expected Object** — assert one whole expected object equivalent in a single comparison, rather than field-by-field (FluentAssertions `BeEquivalentTo`). Excludes non-deterministic fields (ids, timestamps) explicitly.
- **Delta Assertion** — assert on the *change* relative to a baseline, not absolute values, when the starting state is shared/unknown.
- **Guard Assertion** — a precondition assert (`result.Should().NotBeNull()`) placed before the real assertions so a null/empty doesn't throw a confusing NRE deep in the Verify phase.
- **Unfinished Test Assertion** — `Assert.Fail("not implemented")` so a stubbed-out test can't masquerade as passing.

Avoid **Assertion Roulette**: many bare asserts with no messages, so a failure doesn't tell you *which* one fired. Give asserts reasons / use one logical assertion per concept.

---

## Out-of-Process Dependencies (Databases, Services, Files)

- **Back Door Manipulation** — set up or verify state through a *back door* (direct DB write/read) rather than the SUT's front door. *Back Door Setup* seeds preconditions; *Back Door Verification* confirms a persisted side effect. (Acacia's acceptance tests seed EventStore directly — back-door setup.)
- **Database Sandbox** — every developer/run gets an isolated database, so tests never collide. (Testcontainers gives a per-run sandbox.)
- **Table Truncation Teardown** / **Transaction Rollback Teardown** — reset persistent state between tests cheaply.
- **Fake Database** — an in-memory implementation of the repository/persistence seam, for *fast* tests that still cross the persistence boundary logically. The single highest-leverage pattern for turning slow integration tests into fast ones — when the persistence abstraction is fakeable.

---

## Where to Draw the Test Boundary

Meszaros names the strategic choices that decide *how much of the system a test exercises* — directly relevant to outside-in TDD's "what is the acceptance test?".

- **Round-Trip Test** — drives the SUT through its **public/front-door** API and verifies through the same. Robust to internal change; the default for outside-in.
- **Layer-Crossing Test** — uses a Test Double at a layer boundary to isolate a layer.
- **Layer Test** — tests one architectural layer in isolation, doubling the layers below.
- **Subcutaneous Test** — exercises the system **just beneath the UI/skin** (e.g. the controller or application service), skipping only the thinnest delivery layer. Gives most of the coverage of an end-to-end test at a fraction of the cost — the sweet spot for an outside-in driver when full end-to-end is slow or needs infrastructure.

**Heuristic:** drive the inner red/green loop with the *fastest boundary that still tests the behaviour you care about* (often subcutaneous), and keep a thin layer of full end-to-end tests purely as a *fidelity gate* (routing, wiring, serialization, real external contract). This is the test pyramid expressed as boundary choices.

---

## Test Smells (and their fixes)

Meszaros groups smells into three families: **Code** (you see it reading the test), **Behaviour** (you see it running the tests), **Project** (you see it across the team over time).

### Code smells
- **Obscure Test** — the test is hard to understand. Sub-species:
  - *Mystery Guest* — the test depends on external data/state not visible in the test body (a file, a shared DB row). Fix: in-line the relevant data or use a clearly-named Creation Method.
  - *Eager Test* — verifies many behaviours at once. Fix: split, one concept per test.
  - *General Fixture* — setup builds far more than the test needs. Fix: minimise the fixture / Testcase Class per Fixture.
  - *Irrelevant Information* — the test shows data that doesn't matter to it. Fix: Test Data Builder defaults + Anonymous values.
  - *Hard-Coded Test Data* — magic values whose meaning/uniqueness is unclear. Fix: named constants / generated anonymous values.
  - *Indirect Testing* — testing a class through another class. Fix: test it directly.
- **Conditional Test Logic** — `if`/`for`/`switch`/try-catch in a test. The test may not test what you think, and reads ambiguously. Fix: remove branches; parameterise into separate cases; use Guard Assertions instead of `if`.
- **Test Code Duplication** — same arrange/act copied around. Fix: Creation Methods, Custom Assertions, builders.
- **Test Logic in Production** — test-only hooks (`if (testMode)`) leaking into production code. Fix: dependency injection / seams, never `testMode` flags.
- **Hard-to-Test Code** — tight coupling, statics, hidden construction. The design feedback of TDD; fix the design, don't contort the test.

### Behaviour smells
- **Assertion Roulette** — can't tell which assert failed. Fix: assertion messages, Expected Object, one concept per test.
- **Erratic Test** — passes sometimes. Sub-species: *Interacting Tests* (one depends on another's leftovers), *Test Run War* (shared fixture contention between concurrent runs), *Unrepeatable Test* (can't run twice), *Resource Leakage / Optimism* (depends on a resource it doesn't own/clean), *Nondeterministic Test* (time, randomness, ordering). Fix: Fresh Fixture, isolation, control the clock/RNG, automated teardown.
- **Fragile Test** — breaks on changes that didn't change behaviour. Sub-species: *Interface / Behaviour / Data / Context Sensitivity*, *Overspecified Software* (over-mocking — asserting call sequences/internals). Fix: assert observable behaviour, mock only at true external seams.
- **Frequent Debugging** — a failure doesn't localise; you must debug to find the cause. Symptom of too-coarse tests / poor defect localisation. Fix: smaller, focused tests.
- **Slow Tests** — the suite stops being run. Fix: Fake Object for I/O, fewer end-to-end tests, faster boundary.
- **Manual Intervention** — a test needs a human to set up or check. Fix: automate fully.

### Project smells
- **Production Bugs** (tests missed them), **High Test Maintenance Cost**, **Buggy Tests**, **Developers Not Writing Tests** — usually downstream consequences of the code/behaviour smells above; treat the root cause, not the symptom.

---

## Principles of Test Automation

- **Write the Tests First** — they drive design and guarantee testability.
- **Design for Testability** — testability is a first-class design goal (seams, DI, pure functions).
- **Use the Front Door First** — prefer the public API; reserve back-door manipulation for setup/verification you can't do through the front door. Over-using back doors creates *Overspecified Software*.
- **Communicate Intent** — the test reads as a specification; names say *what* not *how*.
- **Don't Modify the SUT** — no test-only subclasses/flags that change the behaviour you're verifying.
- **Keep Tests Independent** — no ordering or shared mutable state between tests.
- **Isolate the SUT** — control its context (time, randomness, collaborators) so outcomes are deterministic.
- **Minimize Test Overlap** — each behaviour covered once; avoid many tests failing for one bug.
- **Minimize Untestable Code** — push logic out of GUIs/constructors/statics into testable units (functional core / imperative shell).
- **Keep Test Logic Out of Production Code.**
- **Verify One Condition per Test** — one *concept*, not literally one assert.
- **Test Concerns Separately** — different behaviours → different tests.
- **Ensure Commensurate Effort and Responsibility** — writing a test shouldn't be wildly harder than writing the code; if it is, that's design feedback.

---

## Quick Application Checklist

When writing a test:
- [ ] Are the four phases (Setup / Exercise / Verify / Teardown) clearly separated?
- [ ] Does the name state the behaviour (what), not the mechanics (how)?
- [ ] Is the fixture **fresh** and **minimal** — only what this test needs?
- [ ] Right double for the role? (Dummy / Stub for inputs, Spy / Mock for output behaviour, Fake for slow deps.)
- [ ] Am I verifying **observable behaviour**, not call sequences or internals?
- [ ] One concept verified? Any `if`/`for`/`try` to remove?
- [ ] Any Mystery Guest, Irrelevant Information, or Hard-Coded Data to hide behind a builder/constant?
- [ ] Is this the **fastest boundary** that still tests the behaviour I care about?

When reviewing a suite:
- [ ] Erratic/flaky tests → find the shared mutable fixture or uncontrolled time/RNG.
- [ ] Fragile tests breaking on refactors → over-mocking / asserting internals.
- [ ] Assertion Roulette → add messages / Expected Object.
- [ ] Slow suite → introduce Fake Objects / move tests down the pyramid.
- [ ] Duplicated setup → extract Creation Methods, builders, Custom Assertions.

---

## Related skills

- **test-driven-development** — the red/green/refactor and outside-in *workflow*; this skill is the pattern/​smell *catalogue* that workflow draws on.
- **unit-testing-principles** (Khorikov) — the four pillars, observable-behaviour-vs-implementation, and managed/unmanaged dependencies — the rigorous "is this test *worth it*?" lens on top of Meszaros's vocabulary.
- **test-data-patterns** — Object Mother + Test Data Builder in depth (this project's fixture stack).
- **refactoring** — the mechanics for cleaning test code, which is production code.

## Reading

- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code* (Addison-Wesley, 2007) — the source; also the online catalogue at xunitpatterns.com.
- Martin Fowler, *Mocks Aren't Stubs* (essay) — the stub/mock distinction.
- Kent Beck, *Test-Driven Development by Example* (2002).
- Vladimir Khorikov, *Unit Testing Principles, Practices, and Patterns* (2020).
