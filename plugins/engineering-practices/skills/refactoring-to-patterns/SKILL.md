---
name: refactoring-to-patterns
description: Apply Joshua Kerievsky's "Refactoring to Patterns" — the discipline of arriving at Gang of Four design patterns through refactoring driven by smells, not by upfront design. Includes the "refactor to / toward / away from a pattern" framing, the economic argument against pattern over-use, and the specific refactorings whose targets are named patterns (Factory, Strategy, Observer, Composite, Adapter, Template Method, State, Null Object). Use when a smell genuinely warrants a pattern, when undoing speculative pattern over-engineering, or when teaching the right time to introduce patterns.
---

# Refactoring to Patterns (Joshua Kerievsky)

Apply this skill when a code smell justifies introducing a design pattern — but not before. The book bridges Fowler's refactorings and the Gang of Four patterns: Fowler tells you the named moves; the GoF tells you the named destinations; Kerievsky shows when the move is worth the destination.

## Core Philosophy

**Patterns are destinations, not starting points.** GoF patterns were extracted from successful designs after the fact. Using them as upfront templates produces "patternitis" — code that is more complex than the problem requires, in service of nominal compliance with a pattern that no smell asked for.

**Refactor toward patterns when a smell demands it.** A pattern earns its complexity when the alternative (status quo) has cost that the pattern eliminates. If the status quo has no cost, the pattern adds cost without offsetting benefit.

**Refactor away from patterns when they no longer earn their keep.** Patterns extracted speculatively, patterns that don't fit the actual variation, patterns whose flexibility is never exercised — these should be *inlined*, not preserved.

**Three directions of refactoring** with respect to a pattern:
- **Refactoring TO a pattern** — full move, smell to pattern.
- **Refactoring TOWARD a pattern** — partial move; useful when full commitment isn't justified yet.
- **Refactoring AWAY FROM a pattern** — undo a pattern that's not pulling its weight.

**The economic argument.** Every pattern has a complexity cost. The cost is justified only by the cost it eliminates elsewhere. A pattern is worth introducing when:

```
cost_of_status_quo  >  cost_of_pattern  +  cost_of_refactoring_to_it
```

If the right side is bigger, the pattern is a net loss.

---

## When to Refactor TO a Pattern

The trigger is always a smell. Match the smell to a destination:

| Smell | Refactor toward |
|---|---|
| Duplicated code with slight variations | **Template Method**, **Strategy** |
| Conditional logic that grows with new variants (switches, if-chains on type) | **Strategy**, **State**, **Polymorphism** |
| Complex constructors with many parameters or option combinations | **Builder**, **Creation Method** |
| Many similar classes for related concepts | **Factory Method**, **Abstract Factory** |
| Repeated null checks scattered across callers | **Null Object** |
| Hardcoded notifications between objects | **Observer** |
| Incompatible interfaces blocking integration | **Adapter** |
| One/many distinctions handled with type checks | **Composite** |
| Repeated calculation logic dispatched by type | **Strategy** |
| Behavior that changes based on object state | **State** |
| Class with optional behaviors that need to combine | **Decorator** |
| Hardcoded primitive sequences that look like a small language | **Interpreter** |

---

## Selected Refactorings (with their pattern targets)

### Replace Constructors with Creation Methods
**Smell:** multiple constructors with similar signatures that are hard to tell apart.
**Move:** introduce static "creation methods" (named factory methods) that describe what kind of object they produce.
**Toward pattern:** Factory Method (when the choice of subclass enters), Builder (when the construction is complex).
```csharp
// Before
new Loan(commitment: 1_000_000m, term: 365, riskRating: 3);
new Loan(commitment: 1_000_000m, outstanding: 500_000m, term: 365);

// After
Loan.NewTermLoan(commitment: 1_000_000m, term: 365, riskRating: 3);
Loan.NewRevolver(commitment: 1_000_000m, outstanding: 500_000m, term: 365);
```

### Replace Conditional Logic with Strategy
**Smell:** type-coded branching for different algorithms.
**Move:** extract each branch into a Strategy class; let composition choose.
**Toward pattern:** Strategy.
```csharp
// Before
public decimal CalculateInterest(LoanType type) =>
    type switch {
        LoanType.TermLoan => commitment * rate * term / 365,
        LoanType.Revolver => outstanding * rate * term / 365,
        LoanType.AdvisedLine => max(commitment, outstanding) * rate * fee,
        _ => 0
    };

// After
public decimal CalculateInterest() => strategy.CalculateInterest(this);
// where strategy : IInterestStrategy and each type has its own implementation.
```

### Replace State-Altering Conditionals with State
**Smell:** an object's methods all start with a switch on a status field.
**Move:** introduce State subclasses that each represent one status, with their own methods.
**Toward pattern:** State.

### Introduce Null Object
**Smell:** scattered null checks (`if (x == null) ...`) repeated at many call sites.
**Move:** introduce a class whose instances behave as "nothing" — empty methods, no-op behavior. Replace nulls with the Null Object.
**Toward pattern:** Null Object.

### Replace Hard-Coded Notifications with Observer
**Smell:** when X happens, X explicitly notifies Y and Z by name; adding W means editing X.
**Move:** make X a Subject that maintains a list of observers; Y, Z, and future W register themselves.
**Toward pattern:** Observer.

### Unify Interfaces with Adapter
**Smell:** two classes that conceptually do the same thing but have different APIs, forcing callers to branch.
**Move:** wrap one in an Adapter that exposes the other's interface; callers depend on the common shape.
**Toward pattern:** Adapter.

### Replace Implicit Tree with Composite
**Smell:** a tree-structured concept (file system, document outline, UI hierarchy) modeled with ad-hoc parent/child references.
**Move:** introduce a Component interface; leaves and composites both implement it; uniform recursive operations.
**Toward pattern:** Composite.

### Compose Method
**Smell:** a method that mixes high-level intent with low-level details.
**Move:** extract the low-level details into helper methods; the original method reads as a sequence of named steps at one level of abstraction.
**Toward pattern:** none (basic Fowler); but supports many other patterns by making intent visible.

### Move Embellishment to Decorator
**Smell:** a class with optional features whose presence is flagged or conditionally invoked.
**Move:** extract each embellishment into a Decorator class that wraps the base; combine them by composition.
**Toward pattern:** Decorator.

### Form Template Method
**Smell:** several similar methods across subclasses; each has the same overall structure but differs in steps.
**Move:** define a template method in the parent that calls abstract or hookable steps; subclasses implement just the differing steps.
**Toward pattern:** Template Method.

### Encapsulate Composite with Builder
**Smell:** clients constructing complex Composite trees with verbose, error-prone code.
**Move:** introduce a Builder with a fluent or step-wise API.
**Toward pattern:** Builder (composing Composite).

### Replace Implicit Language with Interpreter
**Smell:** parsing or evaluating sequences that look suspiciously like a small DSL, with conditional logic interpreting them.
**Move:** model the DSL with expression classes; evaluation becomes polymorphic.
**Toward pattern:** Interpreter.
*(Warning: Interpreter has high cost. Justified only for genuinely repeated DSL-like structures.)*

---

## Refactoring AWAY from Patterns

Sometimes a pattern was introduced speculatively and never paid off. Kerievsky explicitly endorses backing out:

### Inline Singleton
**Smell:** a Singleton was introduced for global access, but the global access turns out to be undesirable (testability, hidden coupling), and there's no genuine need for "exactly one instance".
**Move:** replace the Singleton with a plain object; pass it as a parameter where it's needed.

### Replace Strategy with Inline Code
**Smell:** a Strategy hierarchy was introduced for variation that never materialized — one strategy, one consumer, no flexibility used.
**Move:** inline the strategy's method back into the consumer; delete the hierarchy.

### Inline Class
**Smell:** an abstract base class with one subclass; an interface with one implementation that's never substituted.
**Move:** collapse the abstraction; merge the types.

**General principle:** *flexibility you don't use is debt, not asset.* The complexity is real; the option-value, on closer inspection, was illusory.

---

## The Pattern-Happy Phase (and Beyond)

Kerievsky names a developmental arc most engineers move through:

1. **Pre-pattern.** No vocabulary for design; reinvents the wheel.
2. **Pattern-happy.** Just learned GoF. Inserts patterns everywhere. Code is over-engineered but tries hard.
3. **Pattern-aware.** Knows when to use, when not. Reaches for a pattern only when a smell demands it.
4. **Refactoring-driven.** Lets the smells point at the pattern. Doesn't preempt; doesn't over-commit. Removes patterns that don't earn their keep.

The book is largely an attempt to compress the journey from stage 2 to stage 4.

---

## Common Mistakes

- **Designing patterns upfront.** "We'll need a Strategy here." You don't yet. Wait for the second variation.
- **Pattern-name preening.** "I introduced an Observer." So what — does the codebase benefit? If yes, the pattern earned its keep. If no, you renamed a problem.
- **Forcing patterns into a language where they don't fit.** Some GoF patterns assume OO constraints that don't exist in functional languages (e.g., Strategy is "pass a function" in functional code; a class is overkill).
- **Keeping a pattern after the variation collapses.** Two strategies became one; the Strategy hierarchy now has one implementation. Inline it.
- **Combining many patterns in one place.** Pattern-rich code is hard to follow. Each pattern adds vocabulary; too much vocabulary is unintelligible.
- **Refactoring TO a pattern without tests.** As with all refactorings — get tests first.

---

## Pragmatic Cheat-Sheet

| If the variation is… | Then… |
|---|---|
| Hypothetical, single instance | Don't introduce a pattern. |
| Real, two instances | Maybe a pattern; usually still too early. |
| Real, three or more instances | Yes, refactor to pattern. |
| Was real, now collapsed to one | Refactor away from pattern. |

(Rule of three for patterns — direct cousin of the rule of three for refactoring duplication.)

---

## Quick Application Checklist

Before introducing a pattern:
- [ ] Is there a specific smell I'm responding to?
- [ ] Is the smell currently costing me — duplication, fragility, hard-to-change behavior?
- [ ] Have I considered simpler alternatives (Extract Method, Move Method, Introduce Parameter Object)?
- [ ] Is the variation real (multiple existing cases), not speculative?
- [ ] Will the pattern's complexity cost less than the smell's ongoing cost?

When refactoring toward a pattern:
- [ ] Do I have tests covering the current behavior?
- [ ] Am I taking small steps (Fowler refactorings) toward the pattern, not one big leap?
- [ ] Have I named the destination?

When considering removing a pattern:
- [ ] Is the flexibility being used today?
- [ ] Is it likely to be used in the foreseeable future?
- [ ] If not — what's stopping me from inlining it?

---

## Reading

- **Joshua Kerievsky**, *Refactoring to Patterns* (2004) — the source. Combines smells, refactorings, and patterns into one workflow.
- **Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides**, *Design Patterns: Elements of Reusable Object-Oriented Software* (1994) — "Gang of Four", the pattern catalog. Read for vocabulary; don't take as prescriptions.
- **Martin Fowler**, *Refactoring* (2nd ed., 2018) — the partner volume of named refactorings.
- **Robert C. Martin**, *Agile Software Development: Principles, Patterns, and Practices* (2002) — patterns in the context of SOLID and TDD.
- **Steve Freeman & Nat Pryce**, *Growing Object-Oriented Software, Guided by Tests* (2009) — patterns emerging from tests rather than being imposed.
