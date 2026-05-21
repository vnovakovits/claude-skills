---
name: refactoring
description: Apply Martin Fowler's refactoring discipline — changing the internal structure of code without changing its observable behavior — using the named refactorings catalog (Extract Function, Move Method, Replace Conditional with Polymorphism, etc.) and the code-smells catalog (Long Method, Feature Envy, Primitive Obsession, etc.). Use when cleaning code under a test safety net, responding to a code smell, preparing code for a new feature, or as the third step of every TDD cycle.
---

# Refactoring (Martin Fowler)

Apply this skill whenever you need to change the structure of existing code without changing its observable behavior — to prepare code for a new feature, to eliminate a smell, to recover a clearer design, or as the third leg of the Red-Green-Refactor cycle. Refactoring is a disciplined practice, not "cleaning up": small steps, tests after each, and a catalog of named moves.

## Core Philosophy

**Refactoring is the discipline of changing structure without changing behavior.** If behavior changes, it isn't refactoring — it's editing.

**Two hats** (Beck). At any moment you wear one of two hats: the **adding-features hat** (behavior change, tests turn red then green) or the **refactoring hat** (no behavior change, all tests stay green). Switching hats is fine; wearing both at once is dangerous. Mixing them means you cannot tell what broke the test.

**Small steps, tests after each.** A refactoring is a sequence of tiny, individually-safe transformations. If a step breaks a test, undo and try smaller. Big-bang refactorings are not refactorings — they are rewrites with optimism.

**Refactor for a reason.** Refactor to make the next change easier, to eliminate a smell that's costing comprehension, or as part of a TDD cycle. Refactoring for its own sake is yak-shaving.

**Refactoring is an economic activity.** Time invested in refactoring is justified by faster future change. Code that won't change again doesn't earn refactoring.

---

## When to Refactor

- **The Rule of Three** (Beck). The first time you do something, just do it. The second, wince and duplicate. The third, refactor.
- **Preparatory refactoring** — when adding a feature is hard, first refactor to make it easy, *then* add the feature easily.
- **Comprehension refactoring** — as you read code to understand it, refactor what you learn into the code so the next reader doesn't have to relearn it.
- **Litter-pickup refactoring** — when you find a mess, leave it slightly better than you found it (Boy Scout Rule).
- **Planned refactoring** — for accumulated debt that needs deliberate cleanup, with explicit team buy-in.
- **Long-term refactoring** — large changes done in small increments alongside feature work (Branch by Abstraction, Strangler Fig).
- **As part of TDD** — every Red-Green is followed by Refactor.
- **In code review** — review pressure surfaces refactoring opportunities.

---

## When NOT to Refactor

- **Code you're about to throw away.** No payoff.
- **Code without tests** — first add characterization tests (see the Legacy Code skill), then refactor.
- **Just-before-a-release** with no test safety net — the risk-reward is bad.
- **A rewrite is cheaper than the refactor.** Rare, but real. Be honest.

---

## The Smells Catalog (Fowler & Beck)

Recognizable patterns that indicate refactoring opportunities. When you see one, reach for specific refactorings.

| Smell | Refactor toward |
|---|---|
| **Mysterious Name** | Rename Variable / Function / Field |
| **Duplicated Code** | Extract Function, Pull Up Method, Form Template Method |
| **Long Function** | Extract Function, Replace Temp with Query, Decompose Conditional |
| **Long Parameter List** | Introduce Parameter Object, Preserve Whole Object, Replace Parameter with Query |
| **Global Data** | Encapsulate Variable |
| **Mutable Data** | Encapsulate Variable, Combine Functions into Transform, Change Reference to Value |
| **Divergent Change** (one class changed for many reasons) | Split Phase, Move Function, Extract Class |
| **Shotgun Surgery** (one change touches many classes) | Move Function, Move Field, Combine Functions into Class, Inline Class |
| **Feature Envy** | Move Function, Extract Function |
| **Data Clumps** | Extract Class, Introduce Parameter Object |
| **Primitive Obsession** | Replace Primitive with Object, Replace Type Code with Subclasses |
| **Repeated Switches** | Replace Conditional with Polymorphism |
| **Loops** | Replace Loop with Pipeline (filter, map, reduce) |
| **Lazy Element** (a class/function adding no value) | Inline Function, Inline Class, Collapse Hierarchy |
| **Speculative Generality** | Collapse Hierarchy, Inline Function, Remove Dead Code |
| **Temporary Field** | Extract Class, Introduce Special Case |
| **Message Chains** (train wrecks) | Hide Delegate, Extract Function |
| **Middle Man** (a class that just forwards calls) | Remove Middle Man, Inline Function |
| **Insider Trading** (classes know each other's privates) | Move Function, Move Field, Hide Delegate, Replace Delegation with Subclass |
| **Large Class** | Extract Class, Extract Superclass, Replace Type Code with Subclasses |
| **Alternative Classes with Different Interfaces** | Change Function Declaration, Move Function, Extract Superclass |
| **Data Class** | Move Function, Encapsulate Record |
| **Refused Bequest** | Push Down Method, Push Down Field, Replace Subclass with Delegate |
| **Comments** (explaining what code does) | Extract Function (so the function name replaces the comment) |

---

## The Refactorings Catalog (Selected)

A few of the most-used. Each has *mechanics* — a script of small steps in the book. Use IDE refactoring tools where available; they preserve behavior automatically.

### Composing Methods

- **Extract Function** — the most-used refactoring. Take a fragment of code and turn it into a function whose name explains its purpose.
- **Inline Function** — when a function's body is as clear as its name, eliminate the indirection.
- **Extract Variable** — when an expression is hard to understand, give parts of it names.
- **Inline Variable** — when a variable name adds nothing the expression doesn't already say.
- **Change Function Declaration** — rename, add/remove parameters, change parameter order.
- **Encapsulate Variable** — wrap a piece of data behind get/set functions; gives a single place to add policy.
- **Rename Variable / Field / Function** — names are the lowest-friction way to improve clarity.

### Moving Features
- **Move Function** — when a function references another module's data more than its own.
- **Move Field** — when a field would be better placed elsewhere.
- **Move Statements into Function** / **Move Statements to Callers** — adjust the level of abstraction.
- **Slide Statements** — group related code vertically.
- **Split Loop** — when one loop does two things.
- **Replace Loop with Pipeline** — express transformations as map/filter/reduce.
- **Remove Dead Code** — code that no one calls is liability with no value.

### Organizing Data
- **Replace Primitive with Object** — turn `decimal price` into `Money`; `string email` into `EmailAddress`. The single most useful refactor for domain richness.
- **Replace Temp with Query** — replace a temporary variable with a function call.
- **Extract Class** — when a class has data and behavior serving two purposes.
- **Inline Class** — when a class no longer pays for itself.
- **Hide Delegate** — when a client must call a delegate of a server.

### Simplifying Conditional Logic
- **Decompose Conditional** — extract the condition, the then-branch, the else-branch into named functions.
- **Replace Nested Conditional with Guard Clauses** — flatten deeply nested ifs by returning early on edge cases.
- **Replace Conditional with Polymorphism** — when a type tag drives a switch, push the variation into subclasses.
- **Introduce Special Case** — instead of repeatedly checking for null / sentinel, pass a special-case object that behaves correctly.
- **Introduce Assertion** — make an implicit assumption explicit.

### Refactoring APIs
- **Separate Query from Modifier** — split functions that do both.
- **Remove Flag Argument** — `render(true)` becomes `renderForSuite()` and `renderForSingleTest()`.
- **Preserve Whole Object** — pass the object rather than several of its fields.
- **Replace Function with Command** — when a function gets complex enough to need helper methods / lifecycle, make it an object.

### Dealing with Inheritance
- **Pull Up Method / Field** — common behavior into the superclass.
- **Push Down Method / Field** — specific behavior into subclasses.
- **Replace Type Code with Subclasses** — when a type field switches behavior.
- **Replace Subclass with Delegate / Replace Superclass with Delegate** — favor composition when inheritance no longer fits.

---

## Mechanics: The Small-Steps Discipline

Each refactoring in Fowler's book has explicit *mechanics* — a step-by-step procedure. Example, Extract Function:

1. Create a new function. Name it after intent.
2. Copy the code fragment to the new function.
3. Compile.
4. Look for variables that are local in scope to the source; pass them as parameters.
5. Look for variables modified inside the fragment; return them.
6. Compile.
7. Replace the original fragment with a call to the new function.
8. Test.

Each step is reversible; each step keeps the code compiling; tests pass after every meaningful step. **This is how you refactor without breaking things.**

---

## Tools

Modern IDEs automate many refactorings (Rename, Extract Method, Inline, Move, Change Signature) and guarantee behavior preservation. **Use them.** Manual refactorings are error-prone; IDE refactorings are not.

For .NET: ReSharper, Rider, Visual Studio's built-in refactor menu, dotnet-format.
For Java: IntelliJ IDEA.
For most languages: the language server has at least Rename and Extract.

---

## Refactoring and Testing

Refactoring depends on tests. Without them:
- You cannot detect when a step changes behavior.
- Each refactor becomes a leap of faith.
- Refactoring legacy code requires writing characterization tests first (see the Legacy Code skill).

**If a refactor is hard to test, the design is too coupled.** That coupling is *itself* a refactoring target — usually broken by introducing seams (Extract Interface, Introduce Parameter, Replace Constructor with Factory).

---

## Common Mistakes

- **Refactoring without tests.** Hoping nothing breaks. It breaks.
- **Mixing refactoring with feature work** in one commit. You can no longer review or revert independently.
- **Big-bang refactorings.** Days-long branches that diverge and become un-mergeable.
- **Refactoring for purity, not for change.** SOLID violations that nobody pays for are not worth refactoring.
- **Premature abstraction.** Speculative generality — extracting interfaces for "future flexibility" that never arrives.
- **Refactoring without understanding the code first.** Read it, run it, write a characterization test, *then* refactor.
- **IDE-disabled refactoring** (e.g., dynamic languages without rename safety). Use extra care; lean on tests harder.

---

## Quick Application Checklist

Before refactoring:
- [ ] Are there tests covering the code I'm about to change?
- [ ] Am I wearing the refactoring hat or the feature hat? (Pick one.)
- [ ] Do I have a specific smell or future change in mind, or am I yak-shaving?

During refactoring:
- [ ] Am I taking the smallest step possible?
- [ ] Are tests green after each step?
- [ ] Am I committing frequently (per refactoring, or per pair)?
- [ ] When in doubt, am I using the IDE's automated refactor rather than editing by hand?

After refactoring:
- [ ] Are tests green?
- [ ] Is the diff focused (no feature work mixed in)?
- [ ] Did I leave the code in a better state?
- [ ] Have I committed before starting the next thing?

---

## Reading

- **Martin Fowler**, *Refactoring: Improving the Design of Existing Code*, 2nd ed. (2018, with Kent Beck) — the catalog. The 2nd edition uses JavaScript for examples; the patterns are universal.
- **Joshua Kerievsky**, *Refactoring to Patterns* (2004) — extends Fowler with refactorings whose targets are GoF patterns.
- **Michael Feathers**, *Working Effectively with Legacy Code* (2004) — refactoring code that lacks tests.
- **Kent Beck**, *Tidy First?* (2023) — the economic and decision-making framing for small structural changes.
- **Refactoring catalog online**: refactoring.com — Fowler's catalog with diagrams, free.
