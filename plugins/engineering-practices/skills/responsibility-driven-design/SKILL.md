---
name: responsibility-driven-design
description: Apply Responsibility-Driven Design (RDD) by Rebecca Wirfs-Brock and Brian Wilkerson when designing classes, distributing behavior across objects, modeling a domain, or refactoring object-oriented code. Covers responsibilities, role stereotypes, CRC cards, collaborations, contracts, object neighborhoods, and the Tell-Don't-Ask principle.
---

# Responsibility-Driven Design (Wirfs-Brock & Wilkerson)

Apply this approach whenever designing or refactoring object-oriented code, modeling a domain, deciding where behavior belongs, or reviewing class designs. RDD asks the central question: **"Who is responsible for what, and who collaborates with whom?"**

## Core Philosophy

**Objects are members of a community of cooperators.** Each object has a role and a set of responsibilities. The system's behavior emerges from objects sending messages to one another to fulfill their obligations.

**Design by responsibilities, not by data.** The classical (data-driven) question is "what data does this class hold?" The RDD question is "what is this object responsible for?" Data follows responsibility; behavior is primary.

**Anthropomorphize.** Talk about objects as if they were people with jobs. "The OrderProcessor accepts an order, asks the InventoryService to reserve stock, and tells the PaymentGateway to charge the customer." If your design doesn't read this way, the responsibilities are misplaced.

**The goal is a well-functioning community.** Each object has a clear job, knows its neighbors, and trusts them to do their jobs. No object hoards work; no object snoops on another's internals.

---

## What Is a Responsibility?

A responsibility is an obligation an object has to other objects. Three kinds:

1. **Knowing responsibilities** — what an object knows.
   - Knows its own data (`Order` knows its line items).
   - Knows related objects (`Order` knows its `Customer`).
   - Knows things it can derive or calculate (`Order` knows its total).

2. **Doing responsibilities** — what an object does.
   - Performs computations (`Calculator` computes a result).
   - Initiates actions in other objects (`OrderProcessor` tells `PaymentGateway` to charge).
   - Controls and coordinates activities (`Workflow` sequences steps).

3. **Deciding responsibilities** — what an object decides.
   - Chooses among options based on rules (`PricingPolicy` decides which discount applies).
   - Validates business rules (`OrderValidator` decides if an order is acceptable).

**Responsibilities are stated at a high level of intent**, not as method signatures. "Calculates the total cost of a shipment" is a responsibility; `CalculateTotal(decimal weight, string carrier)` is the implementation of it.

---

## Role Stereotypes

Every object plays one or more **roles**. Roles are categorized into six **stereotypes** — recurring kinds of behavior. Assigning a stereotype clarifies what an object should and should not do.

### 1. Information Holder
Knows and provides information. Largely passive — answers questions, holds state.
- Examples: `Customer`, `Order`, `Product`, value objects.
- Smell: an information holder that "does" too much is becoming a god object.

### 2. Structurer
Maintains relationships between objects and the rules about those relationships.
- Examples: `OrderLineCollection`, `OrgChart`, `RouteGraph`.
- Often a container or registry. Knows how things fit together.

### 3. Service Provider
Performs computation or work on demand. Typically stateless or near-stateless.
- Examples: `MarkupCalculator`, `PdfRenderer`, `EmailFormatter`.
- The "doer" — invoked, does its job, returns.

### 4. Coordinator
Reacts to events by delegating work to other objects. Glues collaborators together without doing the work itself.
- Examples: `OrderProcessor`, `ShipmentWorkflow`, application-service-style classes.
- Has lots of collaborators; usually short methods that say "ask X, then tell Y, then return".

### 5. Controller
Makes decisions and directs the actions of other objects. Encodes business rules and policy.
- Examples: `AuthorizationController`, `PricingPolicy`, `RoutingStrategy`.
- Different from Coordinator: a Coordinator delegates; a Controller decides *what* to delegate.

### 6. Interfacer
Translates information and requests between parts of the system. Lives at the boundary.
- Examples: `RestController` (HTTP ↔ domain), `SqlRepository` (domain ↔ DB), `PaymentGatewayAdapter` (domain ↔ third-party).
- Three sub-flavors: external interfacer (third-party boundary), internal interfacer (layer boundary), user interfacer (UI).

**A class may combine roles**, but each role should be distinct and named. If one class is "Information Holder + Service Provider + Controller", it is probably three classes.

---

## CRC Cards: The Working Tool of RDD

A **Class-Responsibility-Collaborator (CRC) card** is a physical or virtual index card with three regions:

```
┌─────────────────────────────────────────────┐
│ ClassName                  [stereotype]     │
├──────────────────────────┬──────────────────┤
│ Responsibilities         │ Collaborators    │
│                          │                  │
│ - Knows X                │ - SomeService    │
│ - Calculates Y           │ - SomeRepository │
│ - Validates Z            │                  │
└──────────────────────────┴──────────────────┘
```

**Why cards?** Their small size forces small classes. If responsibilities overflow the card, the class is doing too much.

**How to use them:**
1. Identify candidate classes from the problem domain (nouns and concepts).
2. For each, write its responsibilities (verbs and obligations).
3. For each responsibility, ask: "Does this class have all the information it needs?" If not, who does — that's a collaborator.
4. Walk through scenarios ("What happens when a customer places an order?") moving cards around the table. Mismatches reveal missing classes or misplaced responsibilities.
5. Refactor cards until the conversation flows cleanly.

CRC cards are a thinking tool, not a deliverable. Throw them away after the design crystallizes.

---

## Collaborations and Contracts

A **collaboration** is a request from one object to another to fulfill a responsibility. Collaboration creates dependency.

A **contract** is the set of services one object offers to others. It defines:
- What can be requested
- What inputs are needed
- What outputs / effects to expect
- What invariants hold
- What can go wrong

**Design to contracts, not to implementations.** A collaborator should depend on what an object promises (its public contract), never on how it fulfills the promise.

**Minimize collaborators.** Each new collaborator is a new dependency, a new reason to change, and a new thing to mock in tests. If a class has many collaborators, ask whether some are really doing the same job and could be merged, or whether the class itself is over-coordinating.

**Categorize collaborations:**
- **Peer** — same layer, equivalent stature.
- **Subordinate** — the caller owns the callee's lifetime.
- **External** — across a boundary (third-party, OS, network).

---

## Object Neighborhoods (Layers)

Objects group naturally into **neighborhoods** that share concerns. Common layers:

1. **Presentation** — user interfacers; views, controllers (MVC sense), API endpoints.
2. **Application** — coordinators that orchestrate use cases.
3. **Domain** — information holders, structurers, service providers, controllers that encode business rules.
4. **Infrastructure** — external interfacers; persistence, messaging, third-party adapters.

**Rules of the neighborhood:**
- Dependencies point inward toward the domain (Clean Architecture / Hexagonal alignment).
- Information holders and domain services know nothing about persistence, transport, or framework concerns.
- Coordinators in the application layer compose domain behavior to fulfill use cases.
- Interfacers translate between the inside and the outside.

---

## Key Design Heuristics

### Tell, Don't Ask
Don't pull data out of an object to make a decision; tell the object to make the decision.

```csharp
// Asking — caller knows too much about Account internals
if (account.Balance >= amount) {
    account.Balance -= amount;
}

// Telling — Account is responsible for its own state
account.Withdraw(amount);
```

### The Hollywood Principle
"Don't call us, we'll call you." Higher-level objects coordinate; lower-level objects are called when relevant. Implemented through callbacks, events, and inversion of control.

### Information Expert
Assign a responsibility to the object that has the information needed to fulfill it. If `Order` knows the line items, `Order` should compute the total — not `OrderTotalCalculator` reaching into it.

### Keep related responsibilities together (high cohesion)
A class whose methods all manipulate the same data and serve the same purpose is cohesive. A class whose methods are unrelated is two classes wearing one name.

### Minimize what each object knows (low coupling)
Each object should know as little about other objects as possible. Knowing only an interface (a contract) is better than knowing a concrete class.

### Distribute intelligence horizontally
Don't make one object smart and the rest dumb. Spread decisions and behavior across the community so no one object becomes a god.

### Don't tell others how to do their jobs
Send a message stating *what* you want, not *how* to do it. If the caller specifies the algorithm, the abstraction has leaked.

### Beware of long parameter lists
Many parameters mean the caller is supplying too much knowledge to the callee — either the callee should fetch the info itself, or the parameters should be grouped into a meaningful object.

### Objects know themselves, not the world around them
An object should not know who its callers are. Callers know callees, not vice versa. Use events or callbacks if a callee needs to notify upward.

### Avoid getter/setter explosion
A class composed entirely of getters and setters is a data structure pretending to be an object. Push behavior onto it or accept that it is a DTO and label it as such.

---

## Applying RDD: The Design Process

1. **Read the problem statement.** Underline the nouns — candidate objects. Underline the verbs — candidate responsibilities.

2. **Identify candidate objects.** Domain concepts, actors, things the system knows about, things it does.

3. **Assign a stereotype** to each candidate. Many classes will play multiple roles; explicitly note which.

4. **Distribute responsibilities** using Information Expert and the heuristics above. Use CRC cards to sketch.

5. **Walk through scenarios** end to end. "User clicks Submit" → who handles it? → who does what next? → where does the data live? Look for:
   - Objects with no responsibilities (cut them)
   - Objects with too many responsibilities (split them)
   - Responsibilities with no clear home (a new class is missing)
   - Two-way calls (probable design smell — usually one direction is wrong)

6. **Define contracts** for each collaboration. What does the caller need to know? What does the callee promise?

7. **Group into neighborhoods.** Make layer boundaries explicit. Identify which classes are interfacers.

8. **Refactor based on scenarios** — iterate until conversations flow naturally and each object's purpose is clear in one sentence.

9. **Translate to code** with the responsibilities as the public surface and the collaborations as constructor dependencies.

---

## Smells of Poor Responsibility Distribution

- **God class** — one class with too many responsibilities; everything else is anemic.
- **Anemic domain model** — domain objects are bags of getters/setters; logic lives in services that should be methods on the objects.
- **Feature envy** — a method uses another object's data more than its own → move the method.
- **Data class** — an object that holds data but does nothing → either give it behavior or downgrade to a DTO.
- **Inappropriate intimacy** — two classes know too much about each other's internals → strengthen the contract between them.
- **Shotgun surgery** — one change requires edits in many classes → responsibilities are scattered; consolidate.
- **Divergent change** — one class changes for many unrelated reasons → split by reason for change.
- **Message chains / train wrecks** — `a.B().C().D().E()` → violates Law of Demeter; introduce a method on `A` that performs the goal.
- **Middle man** — a class that only forwards calls to another → remove it.
- **Speculative generality** — abstractions for needs that never materialized → delete.
- **Refused bequest** — a subclass doesn't want what the parent offers → wrong inheritance, prefer composition.

---

## RDD vs Other Approaches

- **vs Data-Driven Design.** Data-driven asks "what data?"; RDD asks "what behavior?". Data-driven tends toward anemic models and procedural services. RDD distributes behavior with the data that supports it.

- **vs Domain-Driven Design (DDD).** Complementary. DDD provides strategic concepts (bounded contexts, aggregates, ubiquitous language). RDD provides the tactical "how do I decide what goes where?" inside a bounded context. Aggregates align with RDD object neighborhoods; aggregate roots are typically Information Holders with strong Controller flavor.

- **vs SOLID.** Compatible. SRP is the principle; RDD is a method to discover what the single responsibility *is*. ISP aligns with role-based contracts; DIP aligns with depending on contracts not implementations.

- **vs Clean Code.** Compatible. Clean Code addresses readability at the line/function level; RDD addresses the structure of objects and conversations between them.

---

## Quick Application Checklist

When designing or reviewing a class, ask:

- [ ] What is this class responsible for, in one sentence?
- [ ] What role stereotype does it play? (Information Holder, Structurer, Service Provider, Coordinator, Controller, Interfacer)
- [ ] If it plays more than one role, should it be split?
- [ ] Does it have all the information needed for its responsibilities, or is it asking others for data?
- [ ] Does it tell collaborators what to do, rather than asking and acting?
- [ ] Are its collaborators reasonable in number (typically ≤ 5)?
- [ ] Does it depend on contracts (interfaces / abstractions), not implementations?
- [ ] Does it know about its callers? (It shouldn't.)
- [ ] Is it in the right neighborhood (layer)?
- [ ] Can you describe a scenario using this class without reaching into another class's internals?
- [ ] Would a CRC card for this class fit on an index card without overflowing?

---

## Reading

- Wirfs-Brock & McKean, *Object Design: Roles, Responsibilities, and Collaborations* (2002) — the canonical reference.
- Wirfs-Brock, Wilkerson & Wiener, *Designing Object-Oriented Software* (1990) — the original.
- Beck & Cunningham, *A Laboratory for Teaching Object-Oriented Thinking* (1989) — the CRC-card paper.
