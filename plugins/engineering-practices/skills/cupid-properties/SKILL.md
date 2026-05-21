---
name: cupid-properties
description: Apply Dan North's CUPID properties (Composable, Unix philosophy, Predictable, Idiomatic, Domain-based) — a 2022 alternative framing to SOLID, oriented toward "joyful code" and properties to lean toward rather than principles to obey. Use when evaluating code quality, when SOLID feels like a rulebook rather than a guide, or when looking for a complementary lens that emphasizes ergonomics, composability, and fit with the surrounding ecosystem.
---

# CUPID Properties (Dan North, 2022)

Apply this skill when evaluating or designing code with an emphasis on *ergonomics, composability, and joy* — what code feels like to work with, not just whether it satisfies abstract principles. CUPID is Dan North's 2022 response to the perception that SOLID had become a rulebook recited without understanding.

## Core Philosophy

**Properties, not principles.** SOLID names principles — discrete rules. CUPID names *properties* — qualities to lean toward, never fully achieved, useful as directions of travel. You don't "comply with" CUPID; you cultivate it.

**Joy as a quality signal.** Joyful code is easier to read, easier to change, more satisfying to work with — and not coincidentally, it tends to be more correct. When code resists you, the discomfort is design feedback. CUPID names the properties that make code feel right.

**Born from critique.** North spent a decade observing that SOLID was often invoked as cargo-cult — "make it SOLID" as a vague approval, "this violates LSP" as a vague objection — without people understanding the underlying tensions. CUPID is intended to invite design judgment rather than rule-checking.

**Complementary, not opposed.** CUPID does not replace SOLID. Many CUPID-joyful designs satisfy SOLID; many SOLID-clean designs are CUPID-joyful. Use both as lenses.

---

## C — Composable

**Code is composable when it plays well with others.**

Composable code:
- Has a small, focused surface area.
- Uses few dependencies.
- Has clear, intention-revealing interfaces.
- Doesn't impose its worldview on callers — no framework take-overs, no "you must inherit from us".
- Is easy to combine: outputs of one fit inputs of another.
- Doesn't surprise you when combined with other code.

**Smells against composability:**
- Frameworks that require you to inherit from base classes throughout your domain.
- Libraries with sprawling APIs and 30-parameter constructors.
- Code that pulls in transitive dependencies for trivial use.
- Modules that grab the global state and refuse to let go.

**Heuristics:**
- A function that takes a few primitives and returns a value composes better than one that requires an `IConfigurationManager`.
- A library with a narrow API and clear semantics composes better than one with 200 methods.
- Pure functions compose like Lego; effectful methods compose like clay.

---

## U — Unix Philosophy

**Each piece does one thing well.**

The Unix tradition: small tools, each focused, designed to be combined. `grep` doesn't try to be `sort`; `sort` doesn't try to be `awk`. Each does one thing brilliantly, with clear inputs (stdin), clear outputs (stdout), clear errors (stderr).

Applied to code:
- A class that does one thing in the domain — not a "Manager" that does everything.
- A function with one obvious purpose, not a procedure with seven concerns.
- A service with one responsibility, not a kitchen-sink container of operations.

**Pipelines over monoliths.** Many Unix-philosophy designs are pipelines: input flows through a series of transformations, each one specialized, none knowing about the others. The whole is simple; each piece is simple; the composition is in the pipeline structure.

**Smells against Unix philosophy:**
- "Service" classes with 30 methods spanning unrelated concerns.
- Functions with `and` in their names (`saveAndNotify`, `validateAndConvert`).
- Configuration objects with options for everything.

**Connection to SRP:** Unix philosophy is SRP at the tool/function level, expressed as a positive design instinct rather than a rule.

---

## P — Predictable

**The code does what it says and you can trust it.**

Predictable code:
- Has clear behavior implied by names and types.
- Is deterministic where possible — same inputs, same outputs.
- Doesn't have hidden side effects.
- Fails the same way every time when it fails.
- Is observable — you can tell what it's doing without reading its implementation.
- Is testable — you can verify its behavior.

**Predictability is a 2x2 axis** (North):

```
                  observable
                      ▲
                      │  predictable
                      │  + transparent
       opaque         │
        ────────────────────────── deterministic
       chaos          │  predictable
       (bad)          │  but opaque
                      │
                  unobservable
```

The goal is the upper-right: deterministic *and* observable. Even if a system can't be fully deterministic (concurrency, IO, time), it can be observable — emit events, log decisions, expose state.

**Smells against predictability:**
- Methods named `Process` that do unpredictable things.
- Functions with hidden side effects (logging, file writes, database mutations the name doesn't reveal).
- Type signatures that hide possible exceptions.
- "Sometimes it returns null, sometimes throws."
- Race conditions, time-dependent behavior, randomness without seeding.

**Heuristics:**
- Idempotent where it can be.
- Pure where it can be.
- Total functions where it can be.
- Loud failures over silent corruption.

---

## I — Idiomatic

**The code feels natural in the language and ecosystem.**

Idiomatic code:
- Uses the language's features as they were intended.
- Matches the conventions of the surrounding codebase.
- Reads as if a native speaker wrote it.
- Doesn't fight the platform.

Idioms vary by language:
- In Python: list comprehensions over manual loops; context managers for resources.
- In C#: `using` for IDisposable; LINQ for collection operations; records for value objects; pattern matching for control flow on types.
- In Rust: ownership and borrowing; `Result` and `?`; iterators over indexed loops.
- In Go: small interfaces, errors as values, channels for concurrency.

**Why this matters:**
- Idiomatic code is faster to read for anyone who knows the language.
- It tends to use well-trodden paths — fewer surprises, fewer bugs.
- It composes well with the ecosystem's libraries (which are themselves idiomatic).

**Smells against idiomaticity:**
- Java-style "AbstractServiceFactoryImpl" naming in idiomatic Go.
- Manual loops in Python where comprehensions would be clearer.
- Reinventing language features (e.g., custom property mechanisms in C# instead of using properties).
- "Translating" code from another language without adapting to local idioms.

**Caveat:** idioms can be local. A team's house style is a valid idiom. New idioms emerge; old idioms fade. Be a native speaker of *this codebase, today*.

---

## D — Domain-based

**The structure of the code matches the structure of the problem.**

Domain-based code:
- Uses the names from the problem domain — for classes, methods, modules.
- Mirrors the domain's structure in the code's structure.
- Models domain concepts as first-class types (not strings, dictionaries, primitives).
- Reads in conversation with a domain expert.

This is **ubiquitous language** (Evans, DDD) reformulated as a CUPID property. The deeper the domain-fit, the easier it is to:
- Understand the code from the requirements.
- Translate new requirements into code changes.
- Verify behavior against expectations.
- Find the right place for a new behavior.

**Smells against domain-based design:**
- Domain logic expressed in framework or technology vocabulary (`OrderRowDTO`, `CustomerRecordEntity`).
- Primitive obsession: `decimal price`, `string status`, `int customer_id` everywhere.
- "Helper" classes whose names refer to no domain concept.
- File / module organization by technology layer rather than by domain.

**Heuristics:**
- Name things as domain experts would.
- Make illegal domain states unrepresentable.
- If a concept appears in conversation, it should appear in code.
- Organize by capability (`Billing`, `Reservations`, `Inventory`) before by technology (`Controllers`, `Repositories`, `Models`).

---

## CUPID vs SOLID

| SOLID | CUPID |
|---|---|
| Five principles (rules) | Five properties (qualities) |
| Class-oriented | Function- and code-oriented |
| Compliance-oriented | Direction-oriented |
| 2002 — designed for OO mainstream | 2022 — incorporates functional, microservices, polyglot |
| Strong on internal class structure | Strong on ergonomics and ecosystem fit |
| SRP — one reason to change | Unix philosophy — one thing well |
| OCP — extend, don't modify | Composable — combine, don't impose |
| LSP — substitutability | Predictable — trustworthy behavior |
| ISP — focused interfaces | Composable + Unix |
| DIP — depend on abstractions | (Implicit: composable code does this naturally) |
| — | Idiomatic — fits the language |
| — | Domain-based — fits the problem |

**Both lenses are useful.** SOLID helps you spot specific structural violations; CUPID helps you evaluate whether the result *feels right*.

---

## CUPID and Other Practices

- **TDD**: tests-first encourages code that is composable (mockable), predictable (verifiable), and domain-based (named for behavior). Joyful code is testable code.
- **DDD**: the *D* in CUPID — domain-based — *is* DDD's ubiquitous language as a code property.
- **Functional core, imperative shell** (Seemann / Bernhardt): the functional core scores high on Predictable; the shell organizes adapters that score high on Composable.
- **Clean Architecture**: an architectural style that supports CUPID (especially Composable and Predictable) at the system level.
- **Tidy First**: tidyings are small moves toward CUPID qualities — improving readability, predictability, idiom.

---

## When to Use CUPID

- **In code review**, as evaluative language alongside SOLID. "This is hard to compose because…" / "The behavior here is unpredictable because…" / "This isn't idiomatic — consider…"
- **When learning a new language**, to internalize what *idiomatic* means there.
- **When designing a library**, to think about what consumers will feel.
- **When SOLID feels like a checklist** — CUPID re-grounds the conversation in *why*.
- **When teaching**, to give juniors qualitative language for design.

---

## Common Mistakes

- **Treating CUPID as a checklist.** It's a set of directions, not a scorecard.
- **Replacing SOLID with CUPID.** Use both; they complement.
- **Confusing "joyful" with "fun".** Joy here means *fits-the-hand* — well-shaped tools that work. Not entertainment.
- **Confusing "idiomatic" with "trendy".** Idioms are stable patterns of usage, not the latest fashion.
- **Using "predictable" to justify rigidity.** Predictability doesn't mean inflexible — it means the flexibility is visible.

---

## Quick Application Checklist

For each module, class, or function:

- [ ] **Composable** — does this play well with others? Is its surface area small? Does it impose its worldview?
- [ ] **Unix-philosophy** — does it do one thing well? Is its purpose clear in its name?
- [ ] **Predictable** — does it behave as its name and types suggest? Is its behavior observable and (where possible) deterministic?
- [ ] **Idiomatic** — does it use the language and ecosystem naturally? Would a native speaker write it this way?
- [ ] **Domain-based** — do its names and structure mirror the problem domain? Could you discuss it with a domain expert?

When something is wrong:
- [ ] Does this code feel joyful or painful to work with? What property is missing?

---

## Reading

- **Dan North**, *CUPID — for joyful coding* (2022 blog post and talk) — the source. dannorth.net/cupid-for-joyful-coding.
- **Dan North**, *Why every element of SOLID is wrong* (2017 talk) — the critique that motivated CUPID.
- **Dan North**, follow-up essays at dannorth.net elaborating each property.
- **Eric Evans**, *Domain-Driven Design* (2003) — the deepest treatment of the *D* in CUPID.
- **Mark Seemann**'s essays on idiomatic C# and functional-style design — practical illustration of Composable and Predictable in practice.
- **The Unix philosophy** — Eric Raymond, *The Art of Unix Programming* (2003) — the *U* in CUPID.
