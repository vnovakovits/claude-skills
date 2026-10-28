---
name: philosophy-of-software-design
description: Apply John Ousterhout's "A Philosophy of Software Design" (2018; 2nd ed. 2021) — design as the fight against complexity. Covers complexity's symptoms (change amplification, cognitive load, unknown unknowns) and causes (dependencies, obscurity), strategic vs tactical programming, deep vs shallow modules, information hiding and leakage, temporal decomposition, somewhat-general-purpose interfaces, different layer different abstraction, pass-through methods, pulling complexity downwards, defining errors out of existence, design it twice, comments as design, and the red-flags catalogue. Adds the deletion test, depth as leverage, and "one adapter is a hypothetical seam, two is a real one". Use when designing or reviewing a module, class or API; when deciding whether to split or merge code; when an interface feels as complex as its implementation; when handling error cases; when weighing classitis or many small methods; or when a codebase is getting harder to change.
---

# A Philosophy of Software Design (John Ousterhout)

Apply this skill when designing or reviewing the *shape* of code: what a module exposes, what it hides, where one module ends and the next begins, and how errors cross its interface. Ousterhout's single theme is **complexity**: every design decision either adds to it or removes it, and good design is the steady removal of it. The skill also carries a few sharpening ideas from Matt Pocock's `codebase-design` skill (the deletion test, depth as leverage, the adapter rule for seams).

## Core Philosophy

**Complexity is the enemy.** Complexity is anything about a system's structure that makes it hard to understand or change. It isn't measured by size: a large system can be simple to work in, and a small one can be miserable. What counts is the complexity of each part weighted by how much time developers spend in it.

**Complexity is incremental.** No single shortcut makes a system complex; hundreds of small ones do. That is why "it's only a little hack" is the most expensive sentence in software, and why removing complexity needs a standing habit rather than a cleanup sprint.

**Modules should be deep.** The best modules hide a lot of functionality behind a simple interface. The interface is a cost every caller pays; the functionality is the benefit. Design to maximise the benefit per unit of cost.

**It is more important for a module to have a simple interface than a simple implementation.** When complexity is unavoidable, pull it down into the module, where one person handles it once, instead of pushing it up to every caller.

**Working code isn't enough.** Strategic programming treats the design as the primary product and invests continuously (Ousterhout suggests 10–20% of development time) in keeping it clean. Tactical programming does whatever gets this feature working fastest, and its debt compounds.

---

## The Nature of Complexity

**Three symptoms:**

| Symptom | What it looks like |
| --- | --- |
| **Change amplification** | A simple change requires edits in many places (a colour hard-coded in forty pages). |
| **Cognitive load** | How much a developer must know to make a change safely: APIs, side effects, conventions, global state. |
| **Unknown unknowns** | It isn't obvious *what* needs to change or what you need to know. The worst of the three: you can't even tell you are missing something. |

**Two causes:**

- **Dependencies** — code that cannot be understood or changed in isolation. Some are unavoidable; design aims to make them few, simple and obvious.
- **Obscurity** — important information isn't obvious: vague names, undocumented invariants, inconsistent conventions, hidden side effects.

Every recommendation below reduces one of these causes.

---

## Strategic vs Tactical Programming

- **Tactical** — finish the task as fast as possible; design is incidental. Each shortcut seems cheap. Together they produce a system nobody can change. The **tactical tornado** is the prolific developer whose fast output others spend months cleaning up.
- **Strategic** — the goal is a great design that also works. Make small, continuous investments: find the simplest design for each new class, write the documentation, fix a design problem when you notice it instead of working around it.
- When modifying existing code, ask *"is the current design still the best one, given this change?"*, not *"what's the smallest change that works?"*. If every change is the minimal patch, the design decays by construction.

---

## Deep and Shallow Modules

A **module** is anything with an interface and an implementation: a function, class, package or service. Its **interface** is everything a caller must know to use it correctly — the signatures (formal part) and also invariants, side effects, ordering constraints, error behaviour and performance characteristics (informal part).

**Deep module:** a small interface over a lot of functionality. Ousterhout's examples are Unix file I/O (five calls hiding file systems, caching, devices and scheduling) and a garbage collector (no interface at all).

**Shallow module:** an interface nearly as complex as what it does. It costs a caller as much to learn as it saves. A method that only forwards to another is the extreme case.

```csharp
// Shallow: the caller learns a new name and saves nothing.
public void AddNullValueForAttribute(string attribute) => data[attribute] = null;
```

**Classitis.** "Classes are good, so more classes are better" produces many shallow classes, each simple on its own but complex in aggregate. The classic case is Java's three-object dance to read a buffered object stream: buffering should have been the default, not a separate class every caller must know to add.

### What "depth" measures

Ousterhout draws a module as a rectangle: the top edge is the interface (cost), the area is the functionality (benefit). It is tempting to read that as *lines of implementation per line of interface*. That reading rewards padding the implementation and ignores the informal interface, so don't use it.

A sharper reading (Matt Pocock's): **depth is leverage** — how much behaviour a caller, or a test, can use per unit of interface it must learn. Depth produces **leverage** for callers (one implementation pays back across every call site and test) and **locality** for maintainers (a change, a bug fix, or the knowledge of a decision lives in one place).

### Tests for depth

- **The deletion test** (Pocock). Imagine deleting the module and inlining it into its callers. If the complexity disappears, the module was a pass-through. If the same complexity reappears across many callers, the module was earning its keep.
- **The interface is the test surface.** Callers and tests should cross the same interface. Needing to test *past* it — into private helpers — suggests the module is the wrong shape.
- **One adapter is a hypothetical seam; two adapters is a real one** (Pocock). An interface with a single implementation buys indirection, not flexibility. Introduce the seam when a second implementation actually exists (a real fake for tests counts), not in anticipation of one.

---

## Information Hiding and Leakage

**Information hiding.** Each module should encapsulate a few design decisions — a data format, an algorithm, a protocol detail — so nothing outside depends on them. Hidden knowledge can change without touching callers.

**Information leakage** is the opposite: one decision is reflected in several modules. Two classes that both know a file format leak, even if neither exposes it publicly. Fix it by merging the modules that share the knowledge, or by pulling the knowledge into one module both use.

**Temporal decomposition** is the common cause of leakage: structuring code by the order things happen (read the file, modify it, write it back) instead of by the knowledge each step needs. Reader and writer both end up knowing the format. Decompose by *knowledge*, not by *time*.

**Overexposure.** If the common case forces callers to learn about rare features, the interface is too wide. Give the common case defaults that need no thought.

**Private isn't hidden.** Making fields private and adding getters and setters for each of them exposes the same decisions through a different syntax.

---

## Interfaces Worth Having

**Somewhat general-purpose.** Implement today's needs, but give the module an interface general enough to serve more than one caller. A text editor's buffer should offer `Insert(position, text)` and `Delete(range)`, not `Backspace()` and `DeleteSelection()`; the UI builds those from the general operations. Ask:

- What is the simplest interface that covers all my current needs?
- In how many situations will this method be used? (One? It's probably too special.)
- Is this API easy to use for my current needs? (If callers need lots of glue, it's too general.)

**Different layer, different abstraction.** Adjacent layers that offer the same abstraction add a layer of cost with no benefit. Red flags:

- **Pass-through methods** — a method that only calls another with the same signature. Merge the layers, or give each a distinct responsibility.
- **Pass-through variables** — a value threaded through a chain of methods that don't use it, to reach one that does. Use a shared context object or restructure.
- **Decorators** — often shallow by design. Before writing one, consider adding the feature to the underlying class, or to the caller.

Interface duplication is fine when it adds functionality: a dispatcher that routes one signature to many implementations is deep.

**Pull complexity downwards.** Configuration parameters are a common way to push complexity up: they ask callers to make decisions the module is better placed to make. Compute a sensible value inside; expose a parameter only when callers genuinely know better.

### Together or apart?

Bring code together when the pieces share information, when combining simplifies the interface, or when it removes duplication. Separate general-purpose code from special-purpose code. **Length alone is rarely a reason to split a method.** Split when the result is two methods that each make sense without reading the other; if they must be read together (*conjoined methods*), the split made things worse.

---

## Define Errors Out of Existence

Exceptions are among the worst sources of complexity: every one a module throws becomes part of its interface and a path every caller must handle (and rarely tests). Reduce the number of places that must deal with them.

1. **Define the error out of existence.** Change the semantics so the "error" is a normal case. Ousterhout's examples: an `unset` that guarantees the variable no longer exists, instead of throwing when it was never there; Unix letting you delete an open file (the name goes now, the data when the last handle closes). In .NET, `Dictionary.Remove(key)` returns `false` rather than throwing; `string.Substring` with an out-of-range index throws — a clamping overload would serve most callers better.
2. **Mask the exception.** Handle it low down so higher layers never see it, as TCP retransmits lost packets.
3. **Aggregate exceptions.** Handle many exceptions in one place, higher up, with one handler, instead of one handler per call site.
4. **Just crash.** For errors that are rare and not worth handling (out of memory, corrupted internal state), fail fast rather than pretending to recover.
5. **Design special cases out of existence.** A text selection that always exists, possibly empty, removes the "no selection" branches throughout the editor.

Don't overdo it: errors that callers genuinely need to act on must stay in the interface. The aim is to stop *manufacturing* errors that the module could have absorbed.

---

## Design It Twice

Before settling on an interface, sketch at least two radically different designs and compare them on simplicity of interface, generality and efficiency. The first idea is rarely the best; the comparison often produces a third design better than both. It costs an hour on a design that will be paid for over years. When working with agents, the alternatives can be drafted in parallel and compared side by side.

---

## Comments, Names and Obviousness

**Comments describe what isn't obvious from the code.** Interface comments say what a module does and what a caller must know (the informal interface) without describing the implementation. Implementation comments say *why*, not *what*. A comment that repeats the code is noise.

**Write the comments first.** Writing the interface comment before the code is a design tool: if it is hard to describe simply, the abstraction is wrong.

**Names should create a clear image and be consistent.** If a good name is hard to pick, that is a design signal: the thing may be doing too much or not be a coherent concept.

**Code should be obvious.** A reader's first guess about what code does should be right. Things that make code non-obvious: event-driven control flow without documentation, generic containers (`Pair<int,int>`) in place of named types, a declared type that differs from the allocated one, and code that violates the reader's expectations.

---

## Red Flags

Ousterhout's summary catalogue. Each is a symptom to investigate, not a rule to obey mechanically.

| Red flag | Signal |
| --- | --- |
| **Shallow Module** | The interface isn't much simpler than the implementation. |
| **Information Leakage** | The same design decision appears in several modules. |
| **Temporal Decomposition** | Structure follows execution order, not information. |
| **Overexposure** | Callers of common features must learn about rare ones. |
| **Pass-Through Method** | A method does little except forward to a similar method. |
| **Repetition** | The same non-trivial code appears in several places. |
| **Special-General Mixture** | Special-purpose code is tangled into a general mechanism. |
| **Conjoined Methods** | Two methods can only be understood together. |
| **Comment Repeats Code** | The comment adds nothing the code doesn't say. |
| **Implementation Documentation Contaminates Interface** | Interface comments describe internals callers don't need. |
| **Vague Name** | The name is too imprecise to convey useful information. |
| **Hard to Pick Name** | No precise, intuitive name comes to mind. |
| **Hard to Describe** | A complete description of the variable or method has to be long. |
| **Nonobvious Code** | Behaviour or meaning can't be understood quickly. |

---

## Reviewing a Design Through This Lens

For each module in the change:

1. **State its interface** in full, formal and informal. How much must a caller know?
2. **Apply the deletion test.** Would inlining it remove complexity or spread it?
3. **List the design decisions it hides.** If the answer is "none", it is probably shallow. If another module knows the same decision, that is leakage.
4. **Count its seams.** Each interface with a single implementation: is there a real second adapter, or is it speculative?
5. **Trace its errors.** Which exceptions cross the interface? Could any be defined away, masked or aggregated?
6. **Check the comments.** Could you write a short, complete interface comment? Does it describe behaviour or implementation?

Report findings by red-flag name, quoting the code, with the suggested direction (merge, hide, generalise, pull down, define away).

---

## Where Ousterhout Disagrees with Other Skills

- **clean-code** (Robert C. Martin) — Ousterhout argues against splitting functions until they are a few lines long (it produces shallow, conjoined methods) and against treating comments as failures. The two published a written debate on these points. Use Ousterhout's depth test to decide when a small function is a good one.
- **fractal-architecture** (Mark Seemann) — Seemann sizes code to fit working memory and favours small units. The two meet in the middle: a deep module keeps the *interface* small enough to fit in your head, whatever the implementation size.
- **test-driven-development** — Ousterhout worries that TDD encourages tactical, feature-at-a-time design. Counter it by doing the design work (interface first, design it twice) between cycles, and by testing through the module's interface rather than its internals.
- **solid-principles** — interface segregation favours narrow, client-specific interfaces; Ousterhout favours fewer, deeper ones. They agree that an interface should carry only what its callers need. They differ on how many modules it takes.

## How This Skill Pairs with Others

- **working-effectively-with-legacy-code** (Feathers) — the origin of *seam*. Feathers introduces seams to get legacy code under test; this skill asks whether a seam belongs in the design at all.
- **refactoring** (Fowler) — *Middle Man* and *Inline Class* are the moves for pass-through methods and shallow modules; *Extract Class* is the move against information leakage.
- **domain-modeling-made-functional** — "make illegal states unrepresentable" is the type-level version of defining errors out of existence.
- **hexagonal-clean-architecture** — ports and adapters are seams; apply the two-adapter rule before adding a port.
- **unit-testing-principles** — testing through observable behaviour is the same idea as "the interface is the test surface".

---

## Quick Application Checklist

Designing a module:
- [ ] Can I state its interface, including the informal parts, in a few sentences?
- [ ] Does it hide at least one real design decision?
- [ ] Is the common case simple, with defaults for the rest?
- [ ] Is the interface somewhat general-purpose rather than tied to one caller?
- [ ] Did I sketch at least two alternatives before choosing?
- [ ] Have I pulled unavoidable complexity down rather than up into configuration?

Reviewing a change:
- [ ] Does any new module fail the deletion test?
- [ ] Does any new interface have only one adapter and no second in sight?
- [ ] Are there pass-through methods or variables?
- [ ] Is any design decision now known by two modules?
- [ ] Could any new exception be defined away, masked or aggregated?
- [ ] Is this a strategic change, or the smallest patch that works?

---

## Reading

- **John Ousterhout**, *A Philosophy of Software Design* (Yaknyam Press, 2018; 2nd ed. 2021) — the reference for this skill. Short, opinionated, and grounded in his Stanford CS 190 course.
- **John Ousterhout & Robert C. Martin**, *A Philosophy of Software Design vs Clean Code* (github.com/johnousterhout/aposd-vs-clean-code, 2024) — a written debate on method length, comments and TDD, with each author's rewrite of the same example.
- **David Parnas**, "On the Criteria To Be Used in Decomposing Systems into Modules" (CACM, 1972) — the origin of information hiding, and the first case against decomposing by processing steps.
- **Matt Pocock**, `codebase-design` skill (github.com/mattpocock/skills) — depth as leverage, the deletion test, and the two-adapter rule for seams.
- **Michael Feathers**, *Working Effectively with Legacy Code* (2004) — the origin of the *seam* concept.
