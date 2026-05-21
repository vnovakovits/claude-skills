---
name: clean-code
description: Apply Clean Code principles by Robert C. Martin (Uncle Bob) when writing new code, refactoring existing code, or reviewing changes in any language. Covers meaningful names, small functions, comments, formatting, objects vs data structures, error handling, boundaries, unit tests, classes, systems, emergent design, concurrency, and code smells.
---

# Clean Code (Robert C. Martin)

Apply these principles whenever writing, refactoring, or reviewing code. Code is read far more often than it is written — optimize for the reader, not the writer.

## Core Philosophy

- **The Boy Scout Rule**: Leave the code cleaner than you found it.
- **Bad code rots**: small disciplines compound; small messes compound faster.
- **Clean code does one thing well**, reads like prose, contains no duplication, and minimizes the number of moving parts.
- **Care is the missing ingredient**. Clean code is a result of attention, not talent.

---

## Chapter 2: Meaningful Names

**Use intention-revealing names.** The name must answer: why it exists, what it does, how it is used. If you need a comment to explain a name, the name has failed.

```csharp
// Bad
int d; // elapsed time in days

// Good
int elapsedTimeInDays;
```

**Avoid disinformation.** Don't call something a `List` if it isn't one. Don't use `l` and `O` as variable names (they look like `1` and `0`).

**Make meaningful distinctions.** `a1`, `a2`, `Info`, `Data`, `Object`, `Variable`, `theMessage` vs `message` — these are noise. If two names exist, they must mean different things.

**Use pronounceable names.** `genymdhms` is unspeakable in code review; `generationTimestamp` is.

**Use searchable names.** Single letters only inside short loop bodies. `MAX_CLASSES_PER_STUDENT` is grep-able; the literal `7` is not.

**Avoid encodings.** No Hungarian notation (`strName`, `iCount`). Do not encode type or scope in the name. (Exception: follow language convention — C# uses `I` prefix for interfaces.)

**Avoid mental mapping.** The reader should not have to translate `r` to "lowercased URL with host and scheme removed".

**Class names are nouns.** `Customer`, `WikiPage`, `Account`, `AddressParser`. Avoid `Manager`, `Processor`, `Data`, `Info`.

**Method names are verbs.** `postPayment`, `deletePage`, `save`. Boolean methods read as predicates: `isPosted`, `hasPermission`.

**Use static factory methods with descriptive names** when constructors overload:
```csharp
// Bad
var fulcrumPoint = new Complex(23.0);

// Good
var fulcrumPoint = Complex.FromRealNumber(23.0);
```

**Don't be cute.** `HolyHandGrenade()` instead of `DeleteItems()` is a maintenance liability.

**Pick one word per concept.** Choose `fetch`, `retrieve`, OR `get` — not all three.

**Don't pun.** Don't use `add` for both list-append and arithmetic sum.

**Use solution-domain names** for technical concepts the team knows (`AccountVisitor`, `Queue`).

**Use problem-domain names** when no technical term applies. Reach for the domain expert's vocabulary.

**Add meaningful context.** `firstName`, `lastName`, `street`, `city` are ambiguous alone; group them into `Address`.

**Don't add gratuitous context.** Prefixing every class in a mail app with `MAC` is noise.

---

## Chapter 3: Functions

**Small.** Twenty lines is a ceiling, not a target. Two to four lines is normal.

**Do one thing.** A function does one thing if you cannot extract another meaningful function from it. "One thing" is defined at a single level of abstraction.

**One level of abstraction per function.** Don't mix high-level policy with low-level details in the same function.

**The Stepdown Rule.** Code should read top-down. Each function is followed by functions at the next-lower level of abstraction.

**Switch statements** are unavoidable but should be buried in a low-level factory and never repeated. Prefer polymorphism for behavior selection.

**Descriptive names.** Long descriptive beats short cryptic. `IncludeSetupAndTeardownPages` over `Include`. Be consistent.

**Function arguments.** Ideal count is zero, then one, then two. Three is a smell; four needs strong justification.
- **Monadic** functions: ask a question (`fileExists(path)`), operate on input (`fileOpen(path)`), or handle an event.
- **Flag arguments are ugly** — `render(true)` is incomprehensible. Split into two functions: `renderForSuite()` and `renderForSingleTest()`.
- **Argument objects** when you have many related args:
```csharp
// Bad
Circle MakeCircle(double x, double y, double radius);

// Good
Circle MakeCircle(Point center, double radius);
```

**Have no side effects.** `checkPassword` should not also initialize a session. Don't lie about what you do.

**Output arguments are bad.** Prefer return values. `appendFooter(s)` is ambiguous — modified in place or returned?

**Command-Query Separation.** A function either does something or answers something, never both.

**Prefer exceptions to returning error codes.** Error codes force inline checking and break the normal flow.

**Extract try-catch blocks.** The body of try and catch should each be a single function call.

**Don't Repeat Yourself (DRY).** Duplication is the root of nearly all software evil.

**Structured programming.** Each function has one entry and one exit. Small functions usually only need one return — multiple returns are fine if they clarify intent.

**Write code, then refactor.** First draft is ugly. Keep the tests green and clean it.

---

## Chapter 4: Comments

**Comments are at best a necessary evil.** They exist because we have failed to express intent in code. The proper use of comments is to compensate for our failure to express ourselves in code.

**Don't comment bad code — rewrite it.**

### Good comments
- **Legal comments** required by company or license
- **Informative comments** — regex meaning, format of a returned value
- **Explanation of intent** — why the chosen approach
- **Clarification** — when you can't rename the API you're calling
- **Warning of consequences** — "this test takes hours; don't run it casually"
- **TODO comments** — with real intent to follow up
- **Amplification** — highlighting why an apparently-trivial line matters
- **Public API documentation** — XML doc / Javadoc on public interfaces

### Bad comments
- **Mumbling** — notes to self
- **Redundant comments** — restating the code
- **Misleading comments** — outdated or imprecise
- **Mandated comments** — forced Javadoc on every variable
- **Journal/changelog comments** — git already has this
- **Noise** — `// Default constructor`
- **Position markers** — `////// Actions //////`
- **Closing brace comments** — `} // while`
- **Attributions** — `/* Added by Rick */`, use git blame
- **Commented-out code** — delete it; git remembers
- **HTML in comments**
- **Non-local information**
- **Too much information**
- **Inobvious connection** between comment and code
- **Function headers** — a well-named short function needs none

---

## Chapter 5: Formatting

**The newspaper metaphor.** Headline at top, summary below, details further down. High-level concepts first; details below.

**Vertical openness between concepts.** Blank lines separate logical groupings.

**Vertical density.** Closely related lines should be tightly grouped — no blank lines in the middle of a tight algorithm.

**Vertical distance.** Concepts that are conceptually close should stay close. Don't force readers to hop between files.
- **Variable declarations** near their use. Loop counters inside the `for`. Instance variables at the top of the class.
- **Dependent functions**: caller above callee when possible.
- **Conceptual affinity**: similar functions near each other.

**Horizontal formatting.** Aim for 80–120 chars per line.
- **Horizontal openness**: spaces around operators (`a = b + c`); no space between function name and `(`.
- **Indentation** follows scope. Don't collapse short blocks (`if (x) return;`) for the sake of brevity unless your team agrees.

**Team rules trump personal preference.** Consistency within a codebase is more important than which style you prefer.

---

## Chapter 6: Objects and Data Structures

**Data abstraction.** Hide implementation; expose abstract operations. A class is not just a bag of getters and setters.

**Objects vs Data Structures — opposites:**
- **Objects** hide their data behind abstractions and expose behavior.
- **Data structures** expose their data and have no meaningful behavior.

**The procedural/OO trade-off:**
- Procedural code (using data structures) makes it easy to add new functions without changing data structures. Hard to add new data structures.
- OO code makes it easy to add new classes without changing existing functions. Hard to add new functions.

**The Law of Demeter.** A method `f` of class `C` should only call methods on:
1. `C` itself
2. Objects created by `f`
3. Arguments passed to `f`
4. Instance variables of `C`

It should NOT call methods on objects returned by any of these (no train wrecks):
```csharp
// Bad — train wreck
var outputDir = ctxt.GetOptions().GetScratchDir().GetAbsolutePath();

// Better — tell don't ask
var outputDir = ctxt.GetScratchDirAbsolutePath();
```

**Data Transfer Objects (DTOs).** Pure data, no behavior. Acceptable at system boundaries (DB, API).

---

## Chapter 7: Error Handling

**Use exceptions, not return codes.** Return codes pollute every caller with conditional checks.

**Write your try-catch-finally first.** It defines a transaction scope and clarifies the contract before you write the body.

**Use unchecked exceptions.** Checked exceptions break the Open/Closed Principle by forcing signature changes up the call stack.

**Provide context with exceptions.** Include the operation, intent, and relevant identifiers in the message.

**Define exception classes by caller's needs.** Group exception types by how callers will handle them — not by source.

**Wrap third-party exceptions.** Translate them into your own domain exceptions at the boundary.

**Define normal flow with the Special Case Pattern.** Instead of throwing for "no result", return a special-case object that exhibits the right default behavior.

**Don't return null.** Return empty collections, `Optional<T>` / `Maybe<T>`, or throw. Null forces every caller to defend.

**Don't pass null.** Fail fast at boundaries, then trust internal code.

---

## Chapter 8: Boundaries

**Wrap third-party APIs.** Keep their interfaces out of your domain code. Your code should depend on an interface you own.

**Use the Adapter pattern** at boundaries to translate between your domain and the third-party shape.

**Use learning tests.** Write tests against a third-party library to verify your understanding of its behavior. These tests also catch breaking changes when you upgrade.

**Code at boundaries needs clear separation and tests that define our expectations.** Avoid letting too much of our code know about third-party particulars.

---

## Chapter 9: Unit Tests

**The Three Laws of TDD:**
1. You may not write production code until you have a failing unit test.
2. You may not write more of a unit test than is sufficient to fail (and not compiling is failing).
3. You may not write more production code than is sufficient to pass the currently failing test.

**Keep tests clean.** Test code is first-class. Dirty tests are worse than no tests because they rot and lie. Tests must change as easily as production code, or they will be abandoned.

**Tests enable change.** Without them, every change is risk. With them, every change is verifiable.

**F.I.R.S.T:**
- **Fast** — slow tests don't get run.
- **Independent** — tests don't depend on each other or order.
- **Repeatable** — works in any environment, no flakes.
- **Self-validating** — boolean result, no manual interpretation.
- **Timely** — written just before the production code that makes them pass.

**One concept per test.** "One assert per test" is a useful approximation, but the real rule is one concept.

**Build-Operate-Check (Arrange-Act-Assert).** Split each test visually into three sections.

**Domain-specific testing language.** Extract test utilities that express domain intent — tests should read at the same abstraction level as the requirement they encode.

---

## Chapter 10: Classes

**Classes should be small.** Measured in responsibilities, not lines.

**Single Responsibility Principle (SRP).** A class should have one and only one reason to change. Getting software to work and making it clean are two different activities; both matter.

**Cohesion.** Methods and instance variables are interdependent. A class is cohesive when its methods manipulate most of its variables. Low cohesion is a signal to split.

**Maintain cohesion → many small classes.** When a class loses cohesion, extract the cohesive subset into its own class.

**Organize for change.** Open/Closed Principle: open for extension, closed for modification. Use abstractions to isolate change.

**Isolating from change.** Depend on abstractions, not concretions (Dependency Inversion Principle). This makes testing and substitution trivial.

---

## Chapter 11: Systems

**Separate construction from use.** Wiring belongs in `main` (or composition root); business logic in domain code.

**Dependency Injection.** Let containers or factories assemble the graph; objects do not construct their own dependencies.

**Scale up incrementally.** Emergent architecture beats big up-front design. Start with the simplest thing; let architecture grow with proven need.

**Cross-cutting concerns** (logging, transactions, security, caching) should be handled via AOP, decorators, middleware, or aspects — not scattered through domain code.

**Use POJOs / POCOs.** Domain objects should be free of framework concerns. Frameworks plug into your domain, not the reverse.

**Test-drive the system architecture.** It should be possible to evolve architecture from optimal-for-today to optimal-for-tomorrow without invasive rewrites.

---

## Chapter 12: Emergence — Kent Beck's Rules of Simple Design

In strict priority order:

1. **Runs all the tests.** Testable code is decoupled, focused code. A system that cannot be verified should not be deployed.
2. **Contains no duplication.** DRY at every level — code, logic, data, tests. Duplication is the prime enemy of clean design.
3. **Expresses the intent of the programmer.** Through good names, small functions, standard patterns, and tests that read like specifications.
4. **Minimizes the number of classes and methods.** Don't proliferate beyond what's needed. Dogmatic application of rules can multiply useless classes.

---

## Chapter 13: Concurrency

**Concurrency is a decoupling strategy.** It separates what gets done from when.

**Concurrency myths to discard:**
- Concurrency always improves performance.
- Design doesn't change with concurrency.
- Concurrency in containers is "handled for you".

**SRP for concurrency.** Keep concurrency code separate from non-concurrency code. Concurrency has its own reasons to change.

**Limit access to shared data.** Use synchronized regions / locks minimally. Prefer copies, prefer immutable data, prefer message passing.

**Use thread-safe collections.** `ConcurrentDictionary`, `Channel<T>`, `BlockingCollection<T>` in .NET; equivalents in every modern stack.

**Know your execution models:**
- Producer-Consumer
- Readers-Writers
- Dining Philosophers

**Beware dependencies between synchronized methods.** They invite deadlock.

**Keep synchronized sections small.** Hold locks for the minimum time needed.

**Test threaded code with instrumentation.** Force interleavings using random sleeps/yields in test mode to surface race conditions.

**Get your non-threaded code working first.** Don't try to debug concurrency and logic at the same time.

---

## Chapter 14, 15, 16: Successive Refinement (Case Studies)

The book devotes three chapters to case studies (command-line argument parser, JUnit internals, SerialDate refactoring). The takeaway from all three:

- **Write it ugly first; then clean it.** First make it work; then make it right.
- **Don't be afraid to refactor.** Drop bad designs that you've worked on for hours when a better one emerges.
- **Tests give you the freedom** to refactor aggressively.
- **Continual improvement is the discipline.** Every read is an opportunity to improve.

---

## Chapter 17: Smells and Heuristics (Reference Catalog)

### Comments
- **C1** Inappropriate Information (non-technical, changelog)
- **C2** Obsolete Comment
- **C3** Redundant Comment
- **C4** Poorly Written Comment
- **C5** Commented-Out Code

### Environment
- **E1** Build requires more than one step
- **E2** Tests require more than one step

### Functions
- **F1** Too many arguments
- **F2** Output arguments
- **F3** Flag arguments
- **F4** Dead function

### General
- **G1** Multiple languages in one source file
- **G2** Obvious behavior is unimplemented
- **G3** Incorrect behavior at boundaries
- **G4** Overridden safeties
- **G5** Duplication
- **G6** Code at wrong level of abstraction
- **G7** Base classes depending on derivatives
- **G8** Too much information (bloated interfaces)
- **G9** Dead code
- **G10** Vertical separation (variables and functions far from use)
- **G11** Inconsistency
- **G12** Clutter
- **G13** Artificial coupling
- **G14** Feature envy (a method manipulates another class's data more than its own)
- **G15** Selector arguments (boolean / enum that picks behavior)
- **G16** Obscured intent
- **G17** Misplaced responsibility
- **G18** Inappropriate static
- **G19** Use explanatory variables
- **G20** Function names should say what they do
- **G21** Understand the algorithm
- **G22** Make logical dependencies physical
- **G23** Prefer polymorphism to if/else or switch/case
- **G24** Follow standard conventions
- **G25** Replace magic numbers with named constants
- **G26** Be precise (don't guess; verify)
- **G27** Structure over convention
- **G28** Encapsulate conditionals
- **G29** Avoid negative conditionals
- **G30** Functions should do one thing
- **G31** Hidden temporal couplings
- **G32** Don't be arbitrary
- **G33** Encapsulate boundary conditions
- **G34** Functions should descend only one level of abstraction
- **G35** Keep configurable data at high levels
- **G36** Avoid transitive navigation (Law of Demeter)

### Java / Language
- **J1** Avoid long import lists by using wildcards (language-dependent)
- **J2** Don't inherit constants
- **J3** Constants vs Enums (prefer enums)

### Names
- **N1** Choose descriptive names
- **N2** Choose names at the appropriate level of abstraction
- **N3** Use standard nomenclature where possible
- **N4** Unambiguous names
- **N5** Use long names for long scopes
- **N6** Avoid encodings
- **N7** Names should describe side effects

### Tests
- **T1** Insufficient tests
- **T2** Use a coverage tool
- **T3** Don't skip trivial tests
- **T4** An ignored test is a question about ambiguity
- **T5** Test boundary conditions
- **T6** Exhaustively test near bugs
- **T7** Patterns of failure are revealing
- **T8** Test coverage patterns can be revealing
- **T9** Tests should be fast

---

## SOLID (Referenced Throughout)

- **S — Single Responsibility**: one reason to change per class.
- **O — Open/Closed**: open for extension, closed for modification.
- **L — Liskov Substitution**: subtypes must be substitutable for their base types without surprising the caller.
- **I — Interface Segregation**: many small client-specific interfaces beat one fat interface.
- **D — Dependency Inversion**: depend on abstractions, not concretions.

---

## Quick Application Checklist

When writing or reviewing code, ask:

- [ ] Do names reveal intent without needing comments?
- [ ] Is each function small and doing one thing at one level of abstraction?
- [ ] Are arguments ≤ 3, with no flag arguments?
- [ ] Are there no hidden side effects?
- [ ] Is duplication removed?
- [ ] Does each class have one reason to change (SRP)?
- [ ] Are tests F.I.R.S.T and readable as specifications?
- [ ] Have I deleted dead code, commented-out code, and noise comments?
- [ ] Does the code read top-to-bottom like a narrative (Stepdown Rule)?
- [ ] Have I left this file cleaner than I found it?
