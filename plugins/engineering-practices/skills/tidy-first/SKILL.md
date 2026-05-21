---
name: tidy-first
description: Apply Kent Beck's "Tidy First?" approach — small structure changes (tidyings) separated from behavior changes, sequenced as "first / after / later / never", informed by software design as an economic activity (coupling, cohesion, optionality, discount rate). Use when about to make a behavior change in messy code, when reviewing a tangled PR, when deciding whether to clean up now or later, or when thinking about software design as a long-running investment decision rather than a craft aesthetic.
---

# Tidy First? (Kent Beck, 2023)

Apply this skill when standing in front of messy code about to make a change — should you tidy first, after, later, or never? The book's central insight: software design is the *art of structuring options*, and tidyings are small, cheap, reversible structural changes whose timing matters more than their content.

## Core Philosophy

**Two kinds of change: structure and behavior.** Behavior changes alter what the software does — what users see. Structure changes do not. Mixing them in one commit makes reasoning, reviewing, and reverting harder.

**Software design is an economic activity.** Every design decision is an investment. The question is not "is this clean?" but "is the value I expect from this tidying greater than its cost, discounted for time and risk?"

**Coupling and cohesion are the only design concepts that matter.** Everything else is downstream. A change in module A that forces a change in module B is coupling. Things that change together being together is cohesion. The cost of change scales with coupling; the cost of comprehension drops with cohesion.

**Tidyings are small and reversible.** A tidying is the smallest structural change you can make. If a tidying takes more than a few minutes, it's not a tidying — it's a refactor.

**Tidying is optional.** The book is *Tidy First?* with a question mark. Not every mess deserves cleaning; not every clean spot pays for itself. The discipline is choosing.

---

## Structure Changes vs Behavior Changes

**Never mix them in one commit.**

Why:
- Reviewers can't tell what's substantive change.
- Reverts blunder back perfectly-fine structural improvements (or, worse, leave them with their behavior change reverted).
- Debugging is harder: did the test fail because of the structure change or the behavior change?
- The team's review velocity drops because structure-change diffs look like noise around real changes.

**The rule:** structure changes go in their own commits, labeled as such (`tidy: extract function`, `tidy: rename`, `tidy: guard clause`). Behavior changes get their own commits, with green tests on both sides.

A pull request can contain multiple commits of each kind — interleaved is fine as long as each commit is purely one or the other.

---

## The Tidyings Catalog

Each is small. Each is reversible. Apply with a test safety net.

### Guard Clauses
Replace nested conditionals with early returns for edge cases.
```csharp
// Before
if (account != null)
{
    if (account.IsActive)
    {
        // do work
    }
}

// After
if (account == null) return;
if (!account.IsActive) return;
// do work
```

### Dead Code
Delete it. Don't comment it out. Git remembers.

### Normalize Symmetries
When you have two pieces of code doing the same thing in different ways, pick one form and apply consistently. Symmetry reduces cognitive load: one pattern, one place to look.

### New Interface, Old Implementation
When the existing interface is awkward but the implementation is fine, write a new interface that callers will like, implemented by delegating to the old one. Migrate callers gradually; remove the old interface when none remain. (A miniature Strangler Fig.)

### Reading Order
Reorder the methods in a file so they read top-to-bottom: high-level first, helpers below. Newspaper layout. Pure rearrangement; no logic change.

### Cohesion Order
Group related methods near each other. Move methods so the file reads as logical clusters rather than chronological history.

### Move Declaration and Initialization Together
When a variable is declared at the top of a method and initialized many lines later, move them together at the point of use.

### Explaining Variable
Extract a complex sub-expression into a well-named local variable.

### Explaining Constant
Replace a magic number with a named constant.

### Explicit Parameters
Convert hidden inputs (instance fields, globals, ambient state) into explicit method parameters. Makes the dependency visible.

### Chunk Statements
Add blank lines between conceptually distinct groups of statements within a method. Visual grouping that signals "these belong together".

### Extract Helper
Pull a self-contained block into a private helper method.

### One Pile
When code is scattered and entangled, the temptation is to clean one piece at a time. Sometimes the right move is the opposite: pile all the related code into one big mess in one place. With everything visible, the cuts become obvious. Then divide.

### Explaining Comments
Some comments stay — those that explain *why*, hidden constraints, surprising consequences. Add them while you're touching the code.

### Delete Redundant Comments
Comments that restate the code, or that the code now disproves, are noise. Delete them.

---

## The Four Timings

For any tidying you've spotted, choose:

### Tidy First
Tidy *before* making the behavior change. Best when:
- The behavior change would be hard or risky without the tidying.
- The tidying clarifies what the behavior change should be.
- You're confident the tidying is right.

The risk: scope creep. You came to fix a bug; you spend the afternoon refactoring.

### Tidy After
Tidy *after* making the behavior change. Best when:
- You learned something from the behavior change that informs the tidying.
- The behavior change exposed the mess.
- You're already in the area.

The risk: never getting around to it. Tidyings deferred to "after" are often deferred forever.

### Tidy Later
Tidy in a *separate session*, possibly different day, definitely different commit/PR. Best when:
- You're under time pressure for the behavior change.
- The tidying is substantial enough that mixing it in would dominate the diff.
- The team prefers to review structure and behavior separately.

The risk: forgetting. Capture the tidying as a small follow-up task, not just a mental note.

### Never Tidy
Recognize that some messes don't deserve cleaning. Best when:
- The code is about to be deleted.
- The code is in a corner you'll never visit again.
- The tidying is more about aesthetics than economics.

The risk: under-tidying. The mess compounds elsewhere.

**The decision is not "should I tidy?" — it's "when?".**

---

## Software Design as an Economic Activity

The book's deeper layer. Beck argues that design decisions are investment decisions, governed by economic logic.

### Coupling
Coupling is the property that a change to A forces a change to B. The cost of change scales with the size of the coupled set.

Reduce coupling by:
- Hiding implementation behind interfaces.
- Reducing the surface area of contracts.
- Eliminating shared mutable state.
- Localizing decisions where they belong.

### Cohesion
Cohesion is the property that things that change together are together. High cohesion reduces the cost of comprehension and the number of places a change must touch.

Increase cohesion by:
- Grouping related fields, methods, and modules.
- Splitting modules that change for different reasons (SRP).
- Pulling together things that referenced from far apart.

### Optionality / Real Options Theory
Every decision either preserves or eliminates options for future change. **The value of a decision today is not just its immediate payoff — it's also the options it preserves.**

- Reversible decisions are cheap (their downside is bounded).
- Irreversible decisions are expensive (their downside is unbounded).
- Defer irreversible decisions until you must make them ("the last responsible moment").
- A small upfront cost that preserves a future option may be a great investment, even if the option is never exercised.

This is the economic argument for clean code, modularity, and refactoring: they preserve options. Code that locks you into one solution forecloses futures.

### Discount Rate
Money (or effort) tomorrow is worth less than money today, because of:
- Uncertainty (we may not need the cleanup if we delete the code).
- Opportunity cost (the cleanup time could go elsewhere).
- Risk (the cleanup itself could break things).

The discount rate justifies *some* deferral of tidying. But it doesn't justify infinite deferral, because:
- Compounding mess increases the cost of every future change.
- A team's discount rate is often higher than it should be — short-termism is a bug, not a feature.

### Cost vs Benefit of Tidying

| Cost of tidying | Benefit |
|---|---|
| Time spent now | Cheaper changes later |
| Risk of introducing bugs | Better comprehension |
| Review/merge overhead | Optionality preserved |
| | Reduced compound interest on debt |

The art is judging the asymmetry. A 5-minute tidying that makes the next 6 months' work measurably cheaper is a great trade. A 2-day refactor whose downstream payoff is unclear is not.

---

## The Theory in One Sentence

**Software design is structuring code so that future changes are cheap, and the only useful concepts for that are coupling and cohesion.**

Everything else — patterns, principles, refactorings, tidyings — is in service of reducing coupling, increasing cohesion, and preserving optionality.

---

## Common Mistakes

- **Mixing structure and behavior in one commit.** The single most common — and most easily fixed — mistake.
- **"Boy Scout Rule" applied indiscriminately.** Not every mess deserves cleaning right now.
- **"It's not my mess." It is now.** You're touching the code.
- **Tidying as procrastination.** Tidying instead of doing the work you came to do.
- **Tidying as perfectionism.** Endless polish on a piece of code that will change next sprint.
- **Skipping tidying under time pressure.** Compound interest on the mess will cost more than the deferred tidying would have.
- **Tidying without a test safety net.** Risky. Get tests first.

---

## Quick Application Checklist

When approaching a behavior change in messy code:
- [ ] Have I identified the smallest tidyings that would make the behavior change cheaper or safer?
- [ ] Have I decided the timing for each — first / after / later / never?
- [ ] Am I separating tidying commits from behavior-change commits?
- [ ] Is each tidying small enough to be obviously safe?
- [ ] Are there tests covering the area?

For each tidying:
- [ ] Is this small (minutes, not hours)?
- [ ] Is this reversible?
- [ ] Does it reduce coupling or increase cohesion?
- [ ] Or does it just preserve an option I care about?
- [ ] Is the benefit greater than the cost (including review and risk)?

For the design as a whole:
- [ ] Have I increased optionality (made future changes easier)?
- [ ] Have I deferred irreversible decisions?
- [ ] Have I tracked mess that I chose not to tidy (so it doesn't disappear from memory)?

---

## Reading

- **Kent Beck**, *Tidy First? A Personal Exercise in Empirical Software Design* (2023) — the source.
- **Kent Beck**, *Tidy First?* Substack — ongoing essays elaborating the theory, particularly on coupling, cohesion, and the economic frame.
- **Martin Fowler**, *Refactoring* (2018) — the companion catalog of larger structural moves.
- **Hyrum Wright**, *Hyrum's Law* — context for irreversibility of public interfaces.
- **Nat Pryce & Steve Freeman**, *Growing Object-Oriented Software, Guided by Tests* — for the test-first context Tidy First sits within.
