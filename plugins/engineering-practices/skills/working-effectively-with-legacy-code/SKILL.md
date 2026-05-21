---
name: working-effectively-with-legacy-code
description: Apply Michael Feathers's techniques for changing code that lacks tests — characterization tests, seams (object/link/preprocessor), dependency-breaking refactorings (Sprout Method, Extract Interface, Subclass and Override, Wrap Method, Break Out Method Object), effect sketches, and the Legacy Code Change Algorithm. Use when modifying inherited code without test coverage, when adding features to brittle code, when fixing bugs in code you don't yet understand, or when carving test points out of a tightly-coupled mess.
---

# Working Effectively with Legacy Code (Michael Feathers)

Apply this skill whenever you must change code that has no tests — which is most code in most codebases. The discipline solves the classic legacy-code dilemma: you need tests to change safely, but you need to change the code to make it testable. Feathers shows how to break that cycle.

## Core Philosophy

**Legacy code is simply code without tests.** Not "old code", not "ugly code", not "code I didn't write". If you cannot change it confidently because there's no safety net, it is legacy.

**The legacy-code dilemma.** To change code safely you need tests. To test code that wasn't designed for testing, you usually need to change it. The discipline is to make the smallest, safest changes to introduce test points, then refactor under the safety they provide.

**Conservative change.** When changing code you don't fully understand, prefer techniques that minimize risk per step — even if they are uglier than the "ideal" refactor. Get under test first; refactor toward beauty later.

**Characterize, don't specify.** When the existing behavior is undocumented, write tests that capture *what the code does* (right or wrong), not what it should do. Once captured, you can refactor with confidence and *then* change behavior deliberately.

---

## The Legacy Code Change Algorithm

Feathers's algorithm for any change to legacy code:

1. **Identify change points.** Where in the code does the new behavior need to live? Where does the bug live?
2. **Find test points.** Where could you place a test that exercises the change point? You may need to break dependencies to reach a testable point.
3. **Break dependencies.** Use the techniques below to introduce seams that allow the change point to be tested in isolation.
4. **Write tests.** Characterization tests (for current behavior) and / or new behavior tests.
5. **Make changes and refactor.** Now that tests cover the area, change behavior and clean up.

The algorithm is deliberately conservative. Steps 2 and 3 may dominate the work; that's normal for severely legacy code.

---

## Seams

A **seam** is a place where you can alter behavior without editing the code at that point. Seams are how you isolate the system under test from collaborators it would otherwise drag along.

Three kinds, by language:

### Object Seams (OO languages)
Change behavior by substituting one object for another. Achieved by:
- Polymorphism — override a virtual method, or implement an interface.
- Dependency injection — pass collaborators in rather than constructing them.
- Subclass and override — for testing, subclass the production code and override the awkward method.

This is the seam type you'll use 90% of the time in modern code.

### Link Seams
Change behavior at link time. Replace the library / object file linked in. Common in C, C++, statically-linked languages.

### Preprocessor Seams
Change behavior at preprocess time (`#define`, `#ifdef`). C/C++ only. Use sparingly — they obscure code.

**Every change to legacy code starts with finding a seam.** If no seam exists, your first move is to create one.

---

## Dependency-Breaking Techniques

The catalog of refactorings that introduce seams without changing observable behavior. The most-used handful:

### Sprout Method / Sprout Class
**When:** You need to add behavior, but the existing method is too tangled to safely modify.
**How:** Write the new behavior as a new method (or class) — fully test-driven. Call it from the existing method at one well-chosen point. The new code is clean and tested; the old mess is unchanged.

### Wrap Method / Wrap Class
**When:** You need behavior *around* an existing method (logging, validation, additional call).
**How:** Rename the existing method (e.g., add an underscore), create a new method with the old name that calls the renamed one plus the new behavior. Callers see the same signature; the new behavior wraps the old.

### Extract Interface
**When:** A class is hard-coded as a dependency and you need to substitute it in tests.
**How:** Define an interface containing the methods callers actually use. Make the existing class implement it. Change consumers to depend on the interface. Now you can substitute a fake in tests.

### Subclass and Override Method
**When:** A method has an awkward dependency (database, network, time) that you can't easily inject.
**How:** Subclass the production class *in test code only*; override the awkward method to return canned data. Test the subclass; the overridden method is the seam.

### Break Out Method Object
**When:** A long, complex method uses many instance fields and is impossible to extract pieces from.
**How:** Create a new class. Move the method into it. Pass the original object's relevant state as constructor parameters. Now the method's logic can be decomposed and tested.

### Parameterize Constructor / Parameterize Method
**When:** Construction logic or method logic depends on a hard-coded collaborator.
**How:** Add an overloaded constructor / method that accepts the collaborator as a parameter. The old form delegates to the new form with a default. Tests use the new form with a fake.

### Extract and Override Call / Factory Method
**When:** A method calls something untestable (e.g., `new DatabaseConnection()`).
**How:** Extract the awkward call into its own method. Subclass and override that method in tests to return a fake. (`Extract and Override Factory Method` is the same move for object construction.)

### Introduce Instance Delegator
**When:** A static method is called everywhere and you need to fake it.
**How:** Add an instance method that delegates to the static method. Replace static calls with instance calls. Now the dependency is injectable and overridable.

### Introduce Static Setter
**When:** A singleton is used everywhere, and you need to swap it in tests.
**How:** Add a static method to override the singleton instance (for tests). Reset it in test teardown.

### Replace Function with Function Pointer / Delegate
**When:** (Procedural / C.) A function is called directly and you need to swap it for tests.
**How:** Introduce a function pointer; tests assign a fake. Production assigns the real function.

### Supersede Instance Variable
**When:** An instance variable is set in a constructor you can't easily change, and you need a different value for tests.
**How:** Add a method to replace the instance variable. Tests call it after construction.

---

## Characterization Tests

The most important practice. When you don't know what code does, **write tests that document what it currently does** — not what it should do.

**Procedure:**
1. Use the code under test.
2. Observe its output for a given input.
3. Write a test that asserts the observed output.
4. Run the test. It passes (because you wrote the assertion to match reality).
5. Repeat for varying inputs until the behavior is well-covered.

**Important:** characterization tests document *current* behavior, including bugs. The bug shows up as a test asserting the buggy output. When you fix the bug, *that test fails* — and you update it to assert correct behavior. Until then, the test acts as a brake against accidentally changing behavior you don't yet understand.

Tools that help:
- **Approval testing** (Llewellyn Falco) — capture output to a file, mark as "approved", subsequent runs compare against it.
- **Golden Master testing** — same idea, particularly for batch / report output.

---

## Effect Sketches

A diagram of which variables and methods are affected by a change. Drawn as you analyze code.

**How:**
1. Start with the variable or method you'd modify.
2. Sketch arrows to everything it could affect.
3. Continue until the sketch shows all places downstream of your change.

Why: tells you where to place tests (covering the affected outputs) and what could break. Especially useful in large, twisty methods.

In modern IDEs, "Find Usages" and call-graph tools partially automate this. Pen and paper still beat them when you need to think.

---

## Useful Heuristics

- **Don't fix what you can't test.** Get tests around it first. Otherwise you have no way to know if your fix introduced a new bug.
- **Lean on the compiler.** When making a structural change, deliberately break compilation in a way that forces the compiler to point you at every site that needs the change.
- **Preserve signatures.** Conservative refactorings keep public APIs identical. Change behavior in callees, not interfaces.
- **Test what you can.** If you can't test the awkward method, test what's around it. Some coverage is better than none.
- **Identify "pinch points".** Places where a wide change can be tested by a narrow test — concentrate testing effort there.
- **Don't rewrite.** Legacy rewrites almost always under-estimate the implicit knowledge encoded in the old system. Refactor under tests; strangler-fig over time; rewrite only as last resort.

---

## Strangler Fig Pattern (Fowler / Feathers)

For replacing legacy systems incrementally:

1. **Wrap the legacy boundary.** Put a façade in front so callers go through a single interface.
2. **Route new behavior to new code.** Each new feature is implemented in the new system.
3. **Gradually re-route old behavior.** Move existing behaviors from legacy to new, one slice at a time, behind the façade.
4. **Eventually delete the legacy.** When the last behavior moves, the old code is dark and can be removed.

The strangler fig grows around its host tree, eventually replacing it without ever toppling it. Same with legacy code.

---

## Common Mistakes

- **Big-bang rewrites.** "We'll start clean." You won't. The bugs, edge cases, and tribal knowledge in the old code will catch you out repeatedly.
- **Refactoring without characterization tests.** Hope-based refactoring breaks things invisibly.
- **Aggressive cleanup.** Trying to make the code beautiful in one pass. Take a smaller pass. Then another.
- **Mocking the system under test.** A legitimate temptation when the SUT has too many dependencies. Better: break a dependency to reduce them.
- **Hiding behind "it's legacy"**. Some code can be tested; the difficulty is exaggerated. Try harder before giving up.
- **Avoiding the area.** Untested code grows worse with neglect. Visit, add a test, leave a little better.

---

## Quick Application Checklist

Before changing legacy code:
- [ ] Have I identified the specific change point?
- [ ] Have I identified a test point where I can verify the change?
- [ ] Are there dependencies between the change point and the test point that need breaking?
- [ ] What seams already exist? Which can I introduce?
- [ ] Have I written characterization tests for the current behavior?

While changing:
- [ ] Am I taking the smallest steps possible?
- [ ] Am I preserving signatures where possible to minimize risk?
- [ ] Am I committing frequently?
- [ ] Are tests still green after each step?

After changing:
- [ ] Did I leave the area better — at minimum, with test coverage that didn't exist before?
- [ ] Are characterization tests still passing? (If not, behavior changed somewhere unexpected.)

---

## Reading

- **Michael Feathers**, *Working Effectively with Legacy Code* (2004) — the canonical reference. 24 dependency-breaking techniques cataloged with mechanics.
- **Martin Fowler**, *Refactoring* (2nd ed., 2018) — the partner volume; many overlapping techniques.
- **Llewellyn Falco**, ApprovalTests library — for approval / golden-master testing.
- **Sandro Mancuso**'s talks on legacy code under TDD — practical demonstrations.
- **Emily Bache**, *The Coding Dojo Handbook* — exercises for practicing characterization tests (Gilded Rose kata, Trip Service kata, etc.).
- **Nicolas Carlo & Maxime Brunet**, *Understanding Legacy Code* (newsletter, online) — modern essays on the topic.
