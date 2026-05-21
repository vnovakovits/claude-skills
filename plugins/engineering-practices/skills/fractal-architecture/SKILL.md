---
name: fractal-architecture
description: Apply heuristics from Mark Seemann's "Code That Fits in Your Head" (2021) — fractal architecture, working-memory limits, cyclomatic complexity ceilings, vertical slices, encapsulation through invariants, functional core / imperative shell, checklists, and sustainable software engineering. Use when designing, decomposing, sizing methods/classes, deciding what fits in working memory, or evaluating whether code is sustainable over the long term.
---

# Code That Fits in Your Head (Mark Seemann)

Apply these heuristics when writing or reviewing code, sizing methods and classes, deciding how to decompose a problem, designing APIs, or assessing whether a codebase can be maintained sustainably. The central question is: **"Does this code fit in my head?"** If you can't hold a unit's behavior in working memory, you can't reason about it confidently.

## Core Philosophy

**Software engineering is a craft constrained by human cognition.** The limits of working memory — not language features, not paradigms — are the binding constraint on code quality.

**Code is read far more than written, and reasoning about it is the most expensive activity.** Optimize the reading experience first; the writing will follow.

**Sustainable code preserves the team's ability to keep changing it.** Speed today that destroys speed tomorrow is not engineering, it is borrowing.

**Heuristics over rules.** Seemann offers numeric thresholds (7±2, ≤ 80 chars, CC ≤ 7), but they are starting points — defaults to deviate from with reason, not laws to obey blindly.

---

## Working Memory: The Binding Constraint

Miller's law (1956): humans hold roughly **7 ± 2 chunks** in working memory at once. Cowan (2001) refined this to about **4 ± 1** for unrelated items.

Implications for code:
- A method whose behavior depends on more than ~7 interacting elements (variables, branches, calls) exceeds working memory; you can't reason about it without re-reading and note-taking.
- Every name a reader has to keep "in mind" while reading a method is a chunk.
- Cyclomatic complexity, parameter count, nesting depth, and method length are all proxies for working-memory load.

**The reader's working memory is the budget you are designing against.** Spend it deliberately.

---

## Fractal Architecture

**Good code is self-similar at every scale.** Zoom in to a method and it fits in your head. Zoom out to the class — it fits in your head. Zoom out to the module, the bounded context, the system. At every level, the structure stays comprehensible because each level abstracts the level below it into a few named chunks.

```
System          → a handful of bounded contexts
Context         → a handful of modules
Module          → a handful of classes
Class           → a handful of methods
Method          → a handful of statements
```

At each zoom level, the rule is the same: **about seven things**, well-named, working together. Names at the higher level summarize the entire structure below them. A reader navigates the system by repeatedly zooming in only where needed — never holding the whole tree in mind at once.

**This is the most important idea in the book.** Every other heuristic supports it.

### Implications
- A method that does not abstract its details behind a clear name is a leak in the fractal — readers must look inside.
- A class with 30 methods is not a chunk; it's an explosion.
- A module with no clear summarizing concept forces readers to keep all its classes in mind.
- Folder structure, namespace structure, file structure, and class structure should all participate in the fractal.

---

## Numeric Heuristics (Defaults to Deviate from with Reason)

| Metric | Default ceiling | Rationale |
|---|---|---|
| Cyclomatic complexity per method | ≤ 7 | All paths fit in working memory |
| Method length | ≤ 24 lines | Fits one editor screen; sized for the eye |
| Line length | ≤ 80 chars | Comfortable in split views; forces clear naming |
| Method parameters | ≤ 3 | Beyond, group into a parameter object |
| Items per "chunk" (class methods, folder files, etc.) | ≤ 7 | Working memory |
| Indentation depth | ≤ 3 levels | Each level is a chunk |

These are heuristics, not absolutes. **Deviate when you have a reason — but the default should be the heuristic, and the deviation should be justifiable.**

### The 80×24 rule
Methods should fit in an 80-character-wide, 24-line-tall window. Originally the size of a classic terminal; today the size of a half-screen editor split. Code that fits in such a window can be read without scrolling — a small but real cognitive savings on every read.

---

## Encapsulation: Invariants, Pre- and Post-conditions

Seemann's strongest emphasis after fractal structure. Encapsulation is **not** "private fields with getters and setters". It is **making it impossible for a class's state to be invalid**.

### Invariants
Statements about an object that must always be true. Enforced at every constructor and every mutator.

```csharp
public sealed class Reservation
{
    public Reservation(DateTime at, int quantity)
    {
        if (quantity < 1)
            throw new ArgumentOutOfRangeException(nameof(quantity));
        At = at;
        Quantity = quantity;
    }

    public DateTime At { get; }
    public int Quantity { get; }   // invariant: always ≥ 1
}
```

### Preconditions
What callers must satisfy before calling. Stated explicitly (guard clauses), checked at the boundary, then trusted thereafter.

### Postconditions
What callers can rely on after the call returns. Document them; let callers depend on them.

### Make illegal states unrepresentable
The strongest form of encapsulation: design the types so invalid states cannot exist. A `NonEmptyList<T>` is better than checking for emptiness everywhere. An `EmailAddress` value object that validates on construction means downstream code never asks "is this a valid email?"

---

## Vertical Slices and the Walking Skeleton

**Walk the entire stack early.** Before going wide, build a vertical slice from request to database to response — even if trivial — and deploy it. This:
- Surfaces integration risk immediately.
- Establishes the full pipeline (build, test, deploy).
- Gives stakeholders something to react to.

**Add features as full vertical slices, not by completing horizontal layers.**

Seemann's example — a restaurant reservation system — is built one vertical slice at a time: first a happy-path POST endpoint that does nothing useful, then validation, then persistence, then querying, then constraints. Each commit is shippable.

---

## Functional Core, Imperative Shell

A pattern Seemann emphasizes (drawing from Gary Bernhardt's lecture of the same name):

- **Functional core** — pure functions, no I/O, no mutation. Decisions, calculations, transformations. Easy to test, easy to reason about.
- **Imperative shell** — orchestrates I/O, persistence, external calls. Thin; mostly delegates decisions to the functional core.

This pushes uncertainty (databases, networks, time) to the edges and keeps the decision-making code total, deterministic, and trivially testable.

---

## Total Functions and Avoiding Null

A **total function** is defined for every input in its declared domain. A partial function (one that throws for some inputs, returns null for others) breaks the abstraction.

Strategies:
- Use option/maybe types (`Maybe<T>`, `T?` with non-nullable references in C# 8+, `Option<T>`).
- Use specific types that make invalid inputs impossible (no `int age` if negatives are forbidden — use `NaturalNumber`).
- Throw with a meaningful exception when inputs violate documented preconditions — but keep this at the boundary.

**Don't return null.** Don't pass null. Null is a partial-function symptom.

---

## API Design

APIs are read more carefully than internal code. Design them as if the reader has only the signature.

- **Names communicate intent.** A method named `GetTotal` should not have side effects. A method named `Save` should not return data the caller needs.
- **Command-Query Separation** (Bertrand Meyer): a method either changes state or returns a value, never both.
- **Pre/postcondition documentation is part of the API.** XML doc / Javadoc on public APIs is non-negotiable.
- **Argument objects** when more than three parameters cluster naturally.
- **Avoid boolean flags.** `Render(true)` is opaque; split into two methods.
- **Constructors should establish invariants.** Don't leave objects half-built.
- **Prefer immutability** for value-like types.

---

## Testing

Seemann is a long-time TDD advocate, but pragmatic about it.

- **Write tests during development**, not weeks later. Tests-after rarely match tests-first in quality.
- **Tests document behavior.** A passing test is a specification you can rely on.
- **Mock at the boundary, not inside.** Mocking your own classes leads to brittle tests coupled to implementation.
- **Use property-based testing** (FsCheck, Hedgehog) for the functional core — properties express invariants better than examples.
- **Approval / characterization tests** for legacy code without specs — capture current behavior, then refactor under the safety net.
- **Tests that pass are not enough; tests must also be readable.** Tests are first-class code; refactor them too.
- **Trust the suite.** If you don't trust it, fix the suite. A green build that you doubt is worse than a red build.

---

## Hierarchical Organization

The fractal extends to file and folder structure:

- Each folder holds a small, comprehensible number of items.
- Each file holds one or a few cohesive types.
- Each type holds a small number of methods.
- Names at each level *summarize* the level below.

When a folder has 50 files, the abstraction at that level has failed — readers can no longer chunk it. Split.

---

## Trust Mechanisms

Code is trustworthy when the team is confident in it. Trust comes from:

- **Automated tests** — fast, reliable, comprehensive enough to catch regressions.
- **Static analysis** — compilers, linters, analyzers. Run on every build. Treat warnings as errors.
- **Code review** — second pair of eyes, knowledge-sharing, design pressure.
- **Pair / mob programming** — continuous review; faster knowledge transfer.
- **Continuous integration** — every commit verified, automatically.
- **Checklists** — for routine quality (see below).

Trust is the currency that lets a team change software quickly. Spend on trust mechanisms upfront; reap dividends forever after.

---

## Checklists

Drawing on Atul Gawande's *The Checklist Manifesto*: for routine, repeatable tasks, even experts benefit from a written checklist. Examples Seemann recommends:

- **Pull request checklist:** all tests pass, code reviewed, build green, no analyzer warnings, public API documented.
- **Production deployment checklist:** migrations applied, feature flags configured, monitoring in place, rollback plan documented.
- **Definition of done:** what "complete" means for a unit of work.

Checklists trade autonomy for reliability — a good trade for tasks that must be done correctly every time.

---

## Working with Legacy Code

Most software engineers work in codebases older than themselves. Seemann's advice:

- **Characterization tests first.** Before changing legacy code, capture its current behavior in tests. Then refactor against the safety net.
- **Strangler Fig pattern.** Wrap the legacy boundary; route new behavior to the new code; gradually re-route old behavior; eventually delete the legacy.
- **Small steps.** Refactor in commits small enough to revert easily.
- **Don't rewrite from scratch unless the cost is well-understood and accepted.** Rewrites underestimate the implicit knowledge encoded in the old system.

---

## Decomposition: When Something Doesn't Fit

Symptoms that a unit has exceeded working memory:
- You re-read it more than twice to understand it.
- You take notes while reading.
- Tests for it are long and convoluted.
- The name doesn't accurately summarize what it does.
- Adding a feature requires touching many parts of it.

Responses:
- **Extract method** for a coherent chunk with a name.
- **Extract class** for a coherent set of fields and methods.
- **Replace conditional with polymorphism** when type-switches accumulate.
- **Introduce parameter object** when arguments cluster.
- **Replace primitive with value object** when meaning is lost in raw types.
- **Inline** when an abstraction adds noise without value.

---

## Cognitive Load Categories

From educational psychology (Sweller); Seemann applies it to code:

- **Intrinsic load** — inherent complexity of the problem. Cannot be reduced; must be respected.
- **Extraneous load** — complexity added by poor design (bad names, scattered code, hidden dependencies). Eliminate this.
- **Germane load** — effort building useful mental models. Encourage this through clear structure and naming.

**Bad code wastes the reader's working memory on extraneous load.** Clean code spends it on intrinsic and germane load.

---

## Sustainability

A central theme. The question is not "can I ship today?" but "can we keep shipping a year from now?"

Sustainable practices:
- Keep tests green continuously.
- Refactor opportunistically (the Boy Scout Rule).
- Pay down technical debt before it compounds.
- Document decisions, not just code (ADRs — Architecture Decision Records).
- Invest in build, deploy, and feedback loops — short loops compound.
- Resist the urge to optimize prematurely; resist the urge to architect speculatively.

**The goal is software the team can keep changing.** Every decision should be evaluated against that.

---

## Smells / Anti-patterns

- **Method too long** — exceeds the 24-line ceiling without good reason.
- **Method too complex** — cyclomatic complexity > 7.
- **Too many parameters** — > 3 with no parameter object.
- **Primitive obsession** — domain meanings carried as `string`, `int`, `decimal`.
- **Long-living mutable state** — invariants get violated; reasoning collapses.
- **Anemic encapsulation** — public setters, no invariants.
- **Partial functions** — methods that return null or throw for some legal inputs.
- **Side effects in query methods** — violates CQS; readers can't trust signatures.
- **God classes** — too many methods; not a chunk.
- **Wide folders** — too many files at one level; the fractal has broken.

---

## Quick Application Checklist

For each method, class, module, ask:

- [ ] Does this unit fit in working memory? (Could I summarize what it does in one sentence?)
- [ ] Are there ≤ ~7 chunks at this level?
- [ ] Is cyclomatic complexity ≤ 7?
- [ ] Does the method fit in 80×24?
- [ ] Are parameters ≤ 3 (or grouped into a parameter object)?
- [ ] Are invariants enforced — can the object exist in an invalid state?
- [ ] Are preconditions stated explicitly at the boundary?
- [ ] Are functions total — or have I documented the partiality?
- [ ] Have I avoided returning or passing null?
- [ ] Is decision-making code free of I/O (functional core)?
- [ ] Does the public API name communicate intent (Command-Query Separation)?
- [ ] Are tests fast, readable, and trusted?
- [ ] Does the structure at this scale match the structure one zoom level up?
- [ ] Have I removed extraneous cognitive load (bad names, scattered code, hidden dependencies)?

---

## Reading

- Mark Seemann, *Code That Fits in Your Head: Heuristics for Software Engineering* (2021) — the source.
- Mark Seemann, *Dependency Injection Principles, Practices, and Patterns* (2019, with Steven van Deursen) — companion on DI.
- Mark Seemann's blog at blog.ploeh.dk — extensive essays on fractal architecture, encapsulation, functional design.
- Gary Bernhardt, *Boundaries* (2012 talk) — functional core, imperative shell.
- Atul Gawande, *The Checklist Manifesto* (2009) — the checklist case.
- Michael Feathers, *Working Effectively with Legacy Code* (2004) — characterization tests, seams.
