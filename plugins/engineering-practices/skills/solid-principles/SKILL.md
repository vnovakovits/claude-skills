---
name: solid-principles
description: Apply the SOLID principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion) by Robert C. Martin when designing classes, structuring inheritance hierarchies, defining interfaces, organizing dependencies, or reviewing object-oriented code. Includes intent, bad/good examples, common pitfalls, and when to relax each principle.
---

# SOLID Principles (Robert C. Martin)

Apply SOLID when designing classes, choosing between inheritance and composition, defining interfaces, structuring dependencies, or reviewing object-oriented code. SOLID is a set of heuristics for making code easier to change. They are guidelines, not laws — apply them where the design tension they address is real.

## Core Philosophy

**Software gets changed.** SOLID exists to make change cheap and safe.

**The cost of bad design is paid at every change.** A small upfront investment in structure pays back many times over the system's life.

**Apply only when the tension is real.** Premature abstraction in pursuit of SOLID purity creates more pain than it prevents. Wait until a second or third reason to change appears, then refactor.

---

## S — Single Responsibility Principle (SRP)

> *A module should have one, and only one, reason to change.*

The classical short form is "a class should do one thing." Martin's more precise modern formulation: **a module should be responsible to one and only one *actor*** — one source of business decisions that can demand change.

### Why it matters
When a class serves two actors, a change requested by one can break behavior the other relies on. Code that should be independent ends up coupled through a single class.

### Bad
```csharp
public class Employee
{
    public decimal CalculatePay() { /* HR's algorithm */ }
    public string ReportHours() { /* Operations' format */ }
    public void Save() { /* DBA's schema */ }
}
```
Three actors (HR, Operations, DBA) can each demand a change. A change for HR risks breaking what Operations or the DBA depend on.

### Good
```csharp
public class Employee { /* data + invariants */ }

public class PayCalculator { decimal Calculate(Employee e); }
public class HoursReporter { string Report(Employee e); }
public class EmployeeRepository { void Save(Employee e); }
```
Each class has one actor.

### Pitfalls
- **Confusing SRP with "do one thing" at the function level** (Clean Code's function-level principle). SRP is about *reasons to change* at the module/class level.
- **Splitting too aggressively** — a class with five methods that all serve one actor is fine; don't split into five classes.

### When to relax
- Small, stable code where multiple "responsibilities" never actually drift apart.
- Data classes / DTOs where there is no behavioral actor.

---

## O — Open/Closed Principle (OCP)

> *Software entities should be open for extension, but closed for modification.*

Originally Bertrand Meyer (1988); Martin's polymorphic reformulation: extend behavior by adding new code, not by editing existing code.

### Why it matters
Modifying existing, working code introduces risk: regressions, test invalidation, ripple effects through dependents. Extending via new types localizes change.

### Bad
```csharp
public decimal CalculateArea(object shape)
{
    if (shape is Circle c) return Math.PI * c.Radius * c.Radius;
    if (shape is Square s) return s.Side * s.Side;
    if (shape is Triangle t) return 0.5m * t.Base * t.Height;
    throw new ArgumentException();
}
```
Every new shape requires editing this method.

### Good
```csharp
public abstract class Shape { public abstract decimal Area(); }
public class Circle : Shape { public override decimal Area() => ... }
public class Square : Shape { public override decimal Area() => ... }
// Adding a new shape: write a new subclass; no existing code changes.
```

### Pitfalls
- **Speculative abstraction.** Don't introduce hierarchies until you have at least two real implementations and a reason to expect more.
- **OCP is not "never modify code".** Bug fixes and clarifications still require modification. OCP is about *behavioral extension*.
- **Pluggable everything.** Plugin architectures can become impossible to follow. Reserve the indirection for axes of variation that actually vary.

### When to relax
- The variation never materializes — YAGNI beats OCP.
- A single concrete implementation is genuinely all you'll ever have.

---

## L — Liskov Substitution Principle (LSP)

> *Subtypes must be substitutable for their base types.*

Barbara Liskov (1987). A caller using a base type should not need to know which subtype it has; substituting any subtype must not break the caller.

### Why it matters
When LSP is violated, polymorphism lies. Callers must add type-checks (`if subtype is X`), defeating the purpose of inheritance.

### Bad — the classic Rectangle/Square
```csharp
public class Rectangle {
    public virtual int Width { get; set; }
    public virtual int Height { get; set; }
}
public class Square : Rectangle {
    public override int Width { set => base.Width = base.Height = value; }
    public override int Height { set => base.Width = base.Height = value; }
}

void Caller(Rectangle r) {
    r.Width = 5;
    r.Height = 4;
    Debug.Assert(r.Width * r.Height == 20); // Fails when r is a Square.
}
```
`Square` is not a behavioral subtype of `Rectangle` — they have different invariants.

### Good
- Model `Square` and `Rectangle` as separate types (or as immutable value objects with no setters and a common `Shape` abstraction).

### LSP contract requirements (behavioral subtyping)
A subtype may:
- **Weaken preconditions** (accept more inputs than the parent).
- **Strengthen postconditions** (guarantee more about results than the parent).
- **Preserve invariants** of the parent.
- **Preserve history** — operations should not change in surprising ways.

A subtype may NOT:
- Strengthen preconditions (require more than the parent).
- Weaken postconditions.
- Throw new unexpected exceptions.
- Break parent invariants.

### Pitfalls
- **Inheritance for code reuse** when behavior actually differs. Prefer composition.
- **Refused bequest** — a subclass that overrides parent methods to throw `NotSupportedException` is signaling that it isn't really a subtype.

### When to relax
- Almost never. LSP violation is usually a signal that the inheritance is wrong; fix the hierarchy rather than relax LSP.

---

## I — Interface Segregation Principle (ISP)

> *Clients should not be forced to depend on methods they do not use.*

Many small, client-specific (role) interfaces are better than one fat interface.

### Why it matters
Fat interfaces couple unrelated clients. A change for one client's needs triggers recompilation, retesting, and risk for all the others.

### Bad
```csharp
public interface IWorker {
    void Work();
    void Eat();
    void Sleep();
}

public class Robot : IWorker {
    public void Work() { ... }
    public void Eat() => throw new NotSupportedException();   // smell
    public void Sleep() => throw new NotSupportedException(); // smell
}
```

### Good
```csharp
public interface IWorkable { void Work(); }
public interface IFeedable { void Eat(); }
public interface ISleepable { void Sleep(); }

public class Human : IWorkable, IFeedable, ISleepable { ... }
public class Robot : IWorkable { ... }
```

### Role interfaces vs header interfaces
- **Header interface** — extracted from a class by copying its public methods one-for-one. Often too fat.
- **Role interface** — extracted from a *client's* perspective, containing only what the client uses. Smaller, more focused, more stable.

### Pitfalls
- **Interface explosion.** Each role interface has a cost. Group methods that genuinely belong together.
- **One interface per method.** ISP is not a license for ceremony — group cohesive methods.

### When to relax
- Internal code with one client. The "role" and the "header" are the same thing.
- Sealed/internal classes that don't need interfaces at all.

---

## D — Dependency Inversion Principle (DIP)

> *High-level modules should not depend on low-level modules. Both should depend on abstractions.*
> *Abstractions should not depend on details. Details should depend on abstractions.*

Invert the natural compile-time dependency direction so that policy (high level) does not depend on mechanism (low level).

### Why it matters
Without DIP, high-level business logic is welded to specific databases, frameworks, and IO. Testing becomes hard, replacement becomes risky, and frameworks invade the domain.

### Bad
```csharp
public class OrderService
{
    private readonly SqlOrderRepository repo = new SqlOrderRepository(); // concrete dep
    public void Place(Order o) => repo.Save(o);
}
```
`OrderService` (high-level policy) directly depends on `SqlOrderRepository` (low-level mechanism). Swapping the DB or testing without it is hard.

### Good
```csharp
public interface IOrderRepository { void Save(Order o); }

public class OrderService
{
    private readonly IOrderRepository repo;
    public OrderService(IOrderRepository repo) { this.repo = repo; }
    public void Place(Order o) => repo.Save(o);
}

// In infrastructure:
public class SqlOrderRepository : IOrderRepository { void Save(Order o) { ... } }
```
The high-level `OrderService` depends only on the abstraction `IOrderRepository`. The low-level `SqlOrderRepository` depends on the same abstraction (and implements it). The dependency arrow has been *inverted* — both sides point to the abstraction.

### Where the interface lives
A common subtlety: the interface (`IOrderRepository`) should live with the high-level module (the domain), not with the low-level one (infrastructure). This way the domain owns the contract and infrastructure conforms to it.

### DIP vs Dependency Injection (DI)
- **DIP** is a design principle about which way dependencies point.
- **DI** is a technique (constructor injection, setter injection, frameworks) for supplying dependencies.
- You can have DI without DIP (injecting concretes) and DIP without a DI framework (manual wiring).

### Pitfalls
- **Abstracting everything.** Not every class needs an interface. Reserve DIP for axes of substitution that matter (testing seams, swappable infrastructure, polymorphism).
- **One-implementation interfaces forever.** If after a year there is still only one implementation and no test substitute, the abstraction may be premature.

### When to relax
- Pure value objects and data structures.
- Internal helpers that are not test seams and have no substitute.
- Throwaway scripts.

---

## SOLID in Practice — Combined Heuristics

- **Start concrete.** Write the simplest thing. Add abstractions when the second or third reason to vary appears.
- **Listen to the pain.** When changes require shotgun edits, fragile tests, or duplicated logic, SOLID violations are usually present.
- **Refactor toward, not toward perfection.** It is rare for a class to perfectly satisfy all five. Aim for "no glaring violations" rather than "five gold stars".
- **Composition over inheritance** is implicit in LSP and DIP. Inheritance is one tool; usually a smaller one than juniors assume.
- **Tests are an honest judge.** Code that is easy to test usually satisfies SOLID. Code that requires mocks for every dependency, or that resists testing, usually violates DIP or SRP.

---

## SOLID vs Other Principles

- **DRY (Don't Repeat Yourself)** — compatible. Duplication is often a SOLID violation in disguise; eliminating it tends to clarify responsibilities.
- **KISS (Keep It Simple)** — sometimes in tension. SOLID can introduce indirection in service of changeability; KISS resists indirection for its own sake. Apply SOLID where change is actually expected.
- **YAGNI (You Aren't Gonna Need It)** — keeps SOLID honest. Don't introduce abstractions for changes that won't come.
- **GRASP (Information Expert, Creator, etc.)** — complementary; GRASP focuses on responsibility assignment, SOLID on structural quality.

---

## Common Smells That Signal SOLID Violations

- **God class** — SRP and OCP violation.
- **Long if/else or switch on type** — OCP violation; reach for polymorphism.
- **Type-checking inside polymorphic code** — LSP violation.
- **NotSupportedException in overrides** — LSP and/or ISP violation.
- **Wide interfaces with optional methods** — ISP violation.
- **`new` keyword in business logic for infrastructure** — DIP violation.
- **Tests requiring real DB / network / FS** — DIP violation; domain isn't isolated from infrastructure.
- **Changes that cascade across unrelated modules** — SRP and/or DIP violation.

---

## Critiques and Nuance

SOLID is widely taught but not above critique:

- **Dogma is costly.** Indiscriminate application produces ceremony — interfaces with one implementation, classes with one method, factories everywhere — without making change easier.
- **OCP can ossify.** If extension is always preferred over modification, code accumulates dead branches and adapter layers.
- **DIP overuse leads to "configuration as programming".** Wire-up code grows while real logic shrinks.
- **Modern functional and data-oriented styles** address some of the same concerns differently (immutability, pattern matching, sum types).

Treat SOLID as one toolkit among several. Apply it where the design tension it addresses is real, and relax it where it isn't.

---

## Quick Application Checklist

For each class, ask:

- [ ] **S** — How many actors can demand a change to this class? (Ideally one.)
- [ ] **O** — Can I extend this behavior without modifying existing code where extension is plausible?
- [ ] **L** — Can any subtype be substituted for the base type without surprising callers? Are there overrides that throw or ignore?
- [ ] **I** — Does every client use every method of every interface it depends on? Or are some methods dead for some clients?
- [ ] **D** — Does the high-level policy depend on an abstraction, not a concrete low-level implementation? Does the abstraction belong to the high-level module?
- [ ] Is the code I wrote testable in isolation, without spinning up real infrastructure?
- [ ] Have I introduced any abstraction whose second implementation does not exist and is not expected?

---

## Reading

- Robert C. Martin, *Agile Software Development: Principles, Patterns, and Practices* (2002) — original SOLID exposition.
- Robert C. Martin, *Clean Architecture* (2017) — modern restatement, with updated SRP formulation.
- Barbara Liskov, *Data Abstraction and Hierarchy* (1987) — origin of LSP.
- Bertrand Meyer, *Object-Oriented Software Construction* (1988) — origin of OCP.
