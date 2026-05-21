---
name: behavior-driven-development
description: Apply Behavior-Driven Development (BDD) by Dan North, Gojko Adzic, Matt Wynne & Aslak Hellesøy, and Liz Keogh — covering the three practices (discovery, formulation, automation), three amigos workshops, Gherkin scenarios, Specification by Example, living documentation, Feature Injection, and pairing BDD with outside-in TDD. Use when starting a new feature, capturing requirements collaboratively, writing acceptance criteria, deciding what scenarios to automate, or fixing a "Cucumber suite" that has become a brittle UI-testing pile.
---

# Behavior-Driven Development

Apply BDD when starting a new feature, capturing requirements with business stakeholders, deciding what behavior to specify, writing acceptance criteria, or driving outside-in TDD with executable specifications. The central idea is **collaborative discovery of behavior** — not test syntax, not tooling, not Gherkin.

## Core Philosophy

**BDD is TDD done right.** Dan North coined the term in 2003-2006 after observing that "test-first" misled people into thinking TDD was about testing. He renamed and reframed it around *behavior* and *examples* to recover the original intent: TDD is a way to specify and design software, with tests as a side effect.

**Behavior is the unit of conversation.** Not classes, not methods, not stories — observable, testable behaviors a stakeholder can recognize.

**Examples sharpen requirements.** Abstract requirements ("the system shall...") are ambiguous; concrete examples ("given X, when Y, then Z") expose ambiguity immediately and become the specification.

**Living documentation.** Specifications that are continuously verified by execution stay accurate. Documentation that is not executed rots.

**Collaboration over ceremony.** The hardest, most valuable BDD work is the conversation between business, development, and testing — *before* anyone writes a scenario or a line of code. The Gherkin file is the smallest part.

---

## The Three Practices (Cucumber Book)

BDD has three practices, in order of importance:

### 1. Discovery
Three roles — business, development, testing (the **Three Amigos**) — meet to explore the requirement. They surface assumptions, find edge cases, agree on the scope of the next change.

This is where most of the value of BDD lies. The conversation matters more than any artifact it produces.

### 2. Formulation
The team captures the agreed examples in a shared language — typically Gherkin scenarios (Given/When/Then) — written in the *ubiquitous language* of the domain, not test syntax.

These scenarios serve as the specification: agreed before implementation, refined during, and verified after.

### 3. Automation
Some — not all — scenarios are wired up to run as automated tests, becoming executable specifications. Automated scenarios drive development (outside-in) and prevent regressions.

**The trap:** teams skip Discovery and Formulation, jump straight to Automation, and end up with a brittle Selenium suite they call "BDD". This is the most common failure mode.

---

## The Three Amigos

A discovery workshop with three perspectives. Not necessarily three people — could be more, could be roles played by the same person — but always three viewpoints:

- **Business** (PO, BA, customer) — *what* problem are we solving and why?
- **Development** (engineer) — *how* could we build this, what are the technical implications?
- **Testing** (QA, tester) — *what could go wrong*, what edge cases, what should we verify?

Each amigo asks different questions. The combination surfaces ambiguity quickly: the business says "obviously X", testing says "what about Y?", development says "Z would be expensive — do we need it?".

**Example mapping** (Matt Wynne) is a structured discovery technique:
- Yellow card: a user story.
- Blue cards: rules (acceptance criteria).
- Green cards: examples that illustrate each rule.
- Red cards: questions that block (need answering).

A 25-minute example-mapping session can replace hours of clarifying meetings later.

---

## Gherkin: The Common Syntax

Gherkin is a structured natural language for capturing scenarios. It is not a programming language; it is a conversation captured in a form that both humans and tools can read.

```gherkin
Feature: Cash withdrawal at ATM
  As an account holder
  I want to withdraw cash from an ATM
  So that I can have cash without going to a branch

  Background:
    Given my card is valid
    And the ATM has cash available

  Scenario: Account has sufficient funds
    Given my account balance is $100
    When I request $20
    Then the ATM should dispense $20
    And my account balance should be $80

  Scenario: Account has insufficient funds
    Given my account balance is $10
    When I request $20
    Then the ATM should not dispense cash
    And the ATM should display "Insufficient funds"
    And my account balance should be $10

  Scenario Outline: Withdrawal limits
    Given my account balance is $500
    When I request <amount>
    Then the ATM <should_dispense>

    Examples:
      | amount | should_dispense           |
      | $20    | should dispense $20       |
      | $200   | should dispense $200      |
      | $1000  | should refuse — over limit|
```

### Gherkin keywords
- **Feature** — what capability is being described.
- **Scenario** — one example of behavior.
- **Scenario Outline** + **Examples** — parameterized scenarios for data variations.
- **Background** — shared `Given` steps for all scenarios in a feature.
- **Given** — context / preconditions (state before the action).
- **When** — the action / event (one per scenario ideally).
- **Then** — the observable outcome.
- **And / But** — additional Given/When/Then steps.

---

## Writing Good Scenarios

This is where most BDD practice succeeds or fails.

### Declarative, not Imperative
Express *intent*, not *mechanics*.

```gherkin
# Bad — imperative, UI-coupled
When I open the browser
And I navigate to "/login"
And I enter "alice@example.com" into the "email" field
And I enter "password123" into the "password" field
And I click the button with id "submit"

# Good — declarative, intent-revealing
When Alice signs in with valid credentials
```

The imperative version breaks every time the UI changes, hides the intent, and mixes business specification with test automation detail. The declarative version expresses *what* matters; the step definition handles *how*.

### Ubiquitous language
The words in scenarios should match the words domain experts use in conversation — and the words used in the code.

```gherkin
# Bad — generic
When the user creates a new entry

# Good — domain-specific
When Alice places an order
```

### One When per scenario
A scenario captures one behavior. Multiple `When` steps mean multiple behaviors — split into multiple scenarios.

### Clear value in the title
The scenario title is documentation. "Withdrawal succeeds with sufficient funds" is useful; "Test 1" is not.

### Independent scenarios
Scenarios should not depend on each other. Each one sets up its own state via `Given`.

### Avoid testing implementation
Scenarios describe *what the system does* from a stakeholder's perspective. They do not name internal classes, database tables, or HTTP routes.

### Real examples, not placeholders
Use realistic data ("$20", "Alice", "Saturday 3pm"). Real values illuminate edge cases that "Customer X" hides.

### Five-ish scenarios per feature
If a feature has fifty scenarios, the feature is too big or the scenarios are too specific. Look for missing abstractions or rules to combine.

---

## Specification by Example (Gojko Adzic)

A book-length elaboration of BDD's collaborative-specification idea. The core practices:

1. **Derive scope from goals.** Start from business goals, not requested features. Many requested features serve goals badly.
2. **Specify collaboratively.** Three Amigos / example workshops — not requirements written by one party and handed to another.
3. **Illustrate using examples.** Concrete examples expose ambiguity; abstract requirements hide it.
4. **Refine the specification.** Remove ambiguity, simplify, find the essential examples.
5. **Automate validation without changing the specifications.** The specification is the canonical artifact; automation conforms to it.
6. **Validate frequently.** Run the scenarios on every build. Stale specifications are worse than no specifications.
7. **Evolve a documentation system.** Treat the body of scenarios as living documentation of system behavior, organized for discoverability.

Adzic's emphasis: the conversation produces understanding; the artifacts capture the understanding. Don't confuse the artifact for the value.

---

## Feature Injection (Chris Matts)

A complementary discovery technique focused on *what to build*:

1. **Hunt the value.** What outcome does the business want? (Not a feature — an outcome.)
2. **Inject features.** Work backward from the outcome: what features would deliver it? What's the minimum?
3. **Break down stories with examples.** For each feature, what concrete examples illustrate "done"?

Feature Injection prevents the common failure of building requested features that fail to deliver the underlying outcome.

---

## Living Documentation

When scenarios are executable and run on every build:

- They cannot lie about current behavior (a failing scenario blocks the build).
- They are organized by feature, readable by anyone.
- They form a queryable record of what the system does today.
- They onboard new team members faster than any wiki.
- They survive personnel turnover.

**Make scenarios discoverable.** Group by capability. Tag (e.g., `@billing`, `@core`, `@regression`). Render to readable HTML for stakeholders. The body of scenarios is a product in its own right.

---

## Outside-In with BDD: Layered Specification

BDD pairs naturally with outside-in TDD. The pattern:

```
ACCEPTANCE LAYER (BDD scenarios — business-readable)
│
│   Feature: <capability>
│     Scenario: <example>
│       Given/When/Then
│
│      [step definitions translate to a test harness]
│
└─ INNER LAYERS (developer TDD — unit / integration tests)
   │
   │   Test "ReservationService_WhenCapacityAvailable_Reserves"
   │   Test "CapacityChecker_WhenSpotsRemain_ReturnsTrue"
   │
   └─ … and so on, inward
```

The outer (BDD) loop drives behavior at the business level. Inner (TDD) loops drive design at the unit level. **One failing scenario at the top → many TDD cycles below → scenario passes** = one shippable feature.

This is the same double-loop pattern as outside-in TDD, but the outer loop is now expressed in stakeholder-readable language. The two skills are companions.

---

## BDD vs TDD vs ATDD

Frequently conflated.

- **TDD** — developer-facing, technical, fine-grained. Drives unit-level design.
- **BDD** — stakeholder-facing, behavioral, collaborative. Drives feature-level specification. Pairs with TDD inside.
- **ATDD (Acceptance Test-Driven Development)** — similar to BDD's outer loop. Some treat ATDD as a subset of BDD; others as a parallel discipline emphasizing the test-driven aspect over the discovery aspect.

In practice, modern BDD subsumes ATDD's automation discipline and adds the discovery and ubiquitous-language emphasis.

---

## Common Anti-patterns

- **"Cucumber as a UI testing framework."** Scenarios that click buttons, fill fields, and assert on DOM. Brittle, slow, and not specifications.
- **Scenarios written by developers alone.** Skips the collaboration that is the whole point.
- **Skipping Discovery; jumping to Automation.** Produces ceremony without insight.
- **Imperative scenarios.** Couple tests to UI mechanics; obscure intent.
- **One feature file per code module.** Couples specifications to implementation structure.
- **Step definition explosions.** Hundreds of step definitions, each used once. Symptom of imperative scenarios.
- **Hidden state in steps.** Scenario A's `Given` only works if Scenario B ran first. Breaks independence.
- **Scenarios that never fail.** A test that hasn't been seen to fail is not known to test anything.
- **Maintaining scenarios after the team stops reading them.** When stakeholders no longer review the scenarios, BDD has collapsed into expensive integration testing.
- **No conversation, only artifact.** The Gherkin file is meaningless if no Three Amigos session preceded it.
- **Using Gherkin for unit tests.** Gherkin is for behaviors stakeholders care about; xUnit-style tests are for everything else.
- **Specifying the UI shape.** "Then I see a green button" — green is not a business outcome.

---

## When to Use BDD — and When Not To

**Use BDD when:**
- The team and business need a shared understanding of behavior.
- Requirements have repeatedly drifted between intent and implementation.
- The domain is complex and worth modeling precisely.
- Living documentation has high value (regulatory, long-lived systems, distributed teams).
- You can secure regular collaboration time with business / domain experts.

**Don't use BDD when:**
- The domain is shallow (CRUD over a small data model).
- The team is small and co-located; conversations happen freely without ceremony.
- You cannot get business stakeholders to participate. (Then BDD becomes developers writing slow tests in Gherkin — worst of both worlds.)
- The system has no stable behavioral specification (rapid prototype, exploratory work).

---

## Tools

Tooling is the smallest part of BDD. Choose to fit the stack:

- **Cucumber** — Ruby (original); JS via cucumber-js; many ports.
- **SpecFlow** — historic .NET tool, now archived. .NET teams should use **Reqnroll** (the open-source successor).
- **Behave** — Python.
- **JBehave** — Java.
- **Behat** — PHP.
- **Lighter approaches** — for teams that resist Gherkin overhead, plain xUnit/NUnit with rich BDD-style naming (`Given...When...Then`) plus an Example-Mapping discipline can capture much of the value with less ceremony.

The tool is the smallest decision; the practice is the work.

---

## A Worked BDD Flow (Sketch)

Feature: "A customer can reserve a table at a restaurant."

1. **Discovery (Three Amigos, 30 min):**
   - Business: "Customers should be able to reserve tables online."
   - Testing: "What if the restaurant is closed that day? What about deposits? Cancellations?"
   - Development: "How far in advance? Per-table capacity, or total cover capacity?"
   - Output: a list of rules, examples, and parking-lot questions.

2. **Formulation (write the scenarios):**
   ```gherkin
   Feature: Table reservation
   
     Scenario: Reserve when capacity is available
       Given the restaurant has 10 covers free at 7pm on Saturday
       When Alice reserves a table for 2 at 7pm on Saturday
       Then the reservation should be confirmed
       And the restaurant should have 8 covers free at 7pm on Saturday
   
     Scenario: Reject when capacity is unavailable
       Given the restaurant has 1 cover free at 7pm on Saturday
       When Alice reserves a table for 2 at 7pm on Saturday
       Then the reservation should be rejected
       And the restaurant should still have 1 cover free at 7pm on Saturday
   ```

3. **Automation (outside-in):**
   - First scenario fails (no implementation).
   - Step definitions call into a thin acceptance harness.
   - From there, TDD drives `ReservationService`, then `CapacityChecker`, then `ReservationRepository` — exactly as in the outside-in-TDD skill.
   - Each layer's inner tests are unit-level; the outer scenario verifies the whole flow.

4. **Living documentation:**
   - The scenario file lives in the repo, runs on every build, and renders to a stakeholder-readable feature catalog.

---

## Quick Application Checklist

For the practice as a whole:
- [ ] Did the Three Amigos meet before scenarios were written?
- [ ] Were scenarios written collaboratively, or by one role in isolation?
- [ ] Do scenarios read like a stakeholder's description, not a tester's clickstream?
- [ ] Is the ubiquitous language consistent across scenarios, conversation, and code?
- [ ] Do business stakeholders still read the scenarios?
- [ ] Are scenarios run on every build, and treated as build-breaking when they fail?

For each scenario:
- [ ] Is the scenario title a clear, valuable statement of behavior?
- [ ] Is the scenario declarative, not imperative?
- [ ] Is there exactly one `When` describing one behavior?
- [ ] Is it independent of other scenarios?
- [ ] Are examples concrete and realistic?
- [ ] Does it describe *what* the system does, not *how* it does it?
- [ ] Is it about behavior stakeholders care about, not internals?

For the suite:
- [ ] Is each feature file under ~5–10 scenarios? (More likely means missing abstractions.)
- [ ] Is the suite organized so stakeholders can find behavior by capability?
- [ ] Have you avoided coupling scenarios to UI element IDs and CSS selectors?
- [ ] Do step definitions speak the domain, not the test harness?

For the outside-in pairing:
- [ ] Is each scenario the entry point of an outside-in TDD cycle?
- [ ] Are inner-loop unit tests driving the design beneath the scenario?
- [ ] Does the scenario pass against the real stack once the inner layers are real?

---

## Reading

- Dan North, *Introducing BDD* (essay, 2006) — the canonical first description.
- Gojko Adzic, *Specification by Example* (2011) — case studies and patterns from many teams; the practitioner's reference.
- Gojko Adzic, *Bridging the Communication Gap* (2009) — earlier framing, focused on collaboration.
- Matt Wynne & Aslak Hellesøy, *The Cucumber Book* (2nd ed., 2017) — the practices (Discovery, Formulation, Automation) and tooling.
- Matt Wynne, *BDD Books: Discovery* (2019) — focuses on Example Mapping and the discovery phase specifically.
- Liz Keogh's writing on outcome-based BDD and the "Real Options" pattern.
- Chris Matts on Feature Injection — start with the value, work back to features.
- Dan North, *Accelerating Agile* talks — modern reflections on what worked and what didn't.
