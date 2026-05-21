---
name: event-storming
description: Apply Alberto Brandolini's Event Storming — a collaborative modeling technique using domain events on sticky notes to discover business processes, identify bounded contexts, and design software collaboratively. Covers Big Picture, Process Modeling, and Software Design levels, the color-coded sticky-note grammar, the workshop flow, and how Event Storming pairs with DDD. Use when starting a new project, exploring a complex domain, finding bounded-context seams, designing aggregates, or surfacing hidden assumptions across business and tech.
---

# Event Storming (Alberto Brandolini)

Apply this skill when starting a new system, exploring an unfamiliar domain, finding bounded-context seams, designing aggregates, onboarding a team into a complex domain, or surfacing tacit knowledge that lives only in people's heads. Event Storming is a workshop format — collaborative, visual, fast — that produces a shared model from a roomful of stakeholders in hours rather than weeks.

## Core Philosophy

**Domain events are the unit of discovery.** Not entities, not data models, not class diagrams. Events — past-tense facts about what happened — anchor every business process and reveal where complexity actually lives.

**Knowledge lives in many heads, not one.** The domain expert knows the rules, the developer knows the constraints, the salesperson knows the edge cases, the support engineer knows the failures. Event Storming brings them all to one wall and lets the model emerge from their collective drawing.

**Big sheets of paper beat slide decks.** A 10-meter roll of paper gives space for the model to sprawl and reshape. Sticky notes encode information cheaply and move freely. The medium is part of the method.

**Find the chaos before resolving it.** The first half of a workshop is deliberately chaotic — everyone adds events without coordination. The chaos surfaces disagreements, gaps, and edge cases that would never appear in a tidy diagram drawn by one person.

---

## The Three Levels

Event Storming has three "flavors", increasing in detail.

### 1. Big Picture Event Storming
**Audience:** broad — business, product, engineering, support.
**Goal:** see the whole domain in one room. Identify the major flows, the bounded contexts, the hot spots.
**Output:** a high-level map of business processes; candidate bounded contexts; a list of open questions.
**Duration:** half-day to two days.

This is the discovery workshop you run before deciding what to build, what to split, what to integrate.

### 2. Process Modeling Event Storming
**Audience:** narrower — people involved in one specific process.
**Goal:** model a single business process in detail. Add commands, actors, policies, read models.
**Output:** a richer model with the full sticky-note grammar; refined business rules.
**Duration:** half-day to a day per process.

This is the workshop you run when designing a specific feature or service.

### 3. Software Design Event Storming
**Audience:** developers + a domain expert.
**Goal:** translate the process model into a tactical software design — aggregates, commands, events as code-level concepts.
**Output:** aggregate sketches, bounded-context candidates, integration patterns.
**Duration:** a few hours.

This is the design session that bridges from understanding to implementation.

---

## The Sticky-Note Grammar

The colors are conventions; the meaning is what matters.

### Domain Event — orange
A past-tense fact. **"Reservation Confirmed"**, **"Payment Received"**, **"Order Shipped"**.
- Named in domain language.
- Past tense, always.
- Something a domain expert would care to know happened.
- The atom of Event Storming — events come first, everything else follows.

### Command — blue
An intent to make something happen. **"Confirm Reservation"**, **"Receive Payment"**, **"Ship Order"**.
- Imperative form.
- Issued by an actor or a policy.
- Triggers (one or more) domain events.

### Actor / User — small yellow
The person or role issuing a command. **"Customer"**, **"Cashier"**, **"Operations Manager"**.

### External System — pink
A system the domain interacts with but doesn't own. **"Payment Gateway"**, **"Shipping Carrier"**, **"Email Service"**.
- Things you can't control; their failures and constraints matter.

### Read Model / View — green
The information shown to a user that informs a decision. **"Available Slots"**, **"Order History"**, **"Stock Levels"**.
- What does the actor *see* before issuing the command?

### Policy — lilac / purple
The "whenever X happens, do Y" rule. Reactive logic. **"Whenever Payment Received, Confirm Reservation"**.
- Connects events to commands automatically (rather than via human decisions).
- Often becomes a saga, process manager, or event handler in code.

### Aggregate — large yellow (vertical)
A cluster of behavior; a consistency boundary. **"Reservation"**, **"Order"**, **"Inventory"**.
- Receives commands; emits events.
- Identified late in the workshop, after events and commands are stable.

### Hot Spot — pink/red (often handwritten or angled)
A point of disagreement, missing knowledge, or risk. **"What if the customer cancels mid-payment?"**, **"We're not sure how returns work"**.
- Capture, do not resolve in the moment. Leave them visible.

### Bounded Context — drawn boundary
A region of the wall where one model applies. Drawn after the events stabilize. Each context has its own language and its own model.

---

## The Workshop Flow

A typical Big Picture session runs roughly:

### 1. Chaotic Exploration (45–90 min)
Everyone gets a stack of orange stickies and a marker. Without coordination, they write domain events and slap them on the paper.
- Past tense.
- One event per sticky.
- Don't worry about order yet.
- Don't worry about duplicates.
- Don't worry about being wrong.

The room fills with stickies. The chaos is the point.

### 2. Enforce the Timeline (30–60 min)
Now arrange the events in temporal order, left to right. Duplicates merge or get clarified. Causal flows emerge.

This is when the room starts arguing constructively — "no, that happens *before* the other thing" — which surfaces understanding.

### 3. Identify Hot Spots (continuous)
Whenever a disagreement, uncertainty, or risk surfaces, plant a pink/red sticky on it. **Don't try to resolve.** Just mark.

### 4. Add People and Systems (30 min)
Yellow stickies for actors who trigger events. Pink stickies for external systems involved.

### 5. Walk Through the Model (30 min)
A facilitator walks the timeline from left to right, narrating what happens. The room interrupts to correct. Each pass improves the model.

### 6. Add Commands and Aggregates (Process Modeling level) (60+ min)
Now add blue stickies (commands) before each orange event. Yellow vertical stickies (aggregates) cluster the commands and events that belong together.

### 7. Add Policies and Read Models (60+ min)
Lilac stickies for "whenever X, then Y" reactive logic. Green stickies for the views actors consult before issuing commands.

### 8. Identify Bounded Contexts (final step)
Draw boundaries around clusters of events that share language and lifecycle. Different boundaries → different bounded contexts (and likely different services / teams).

---

## Tactical Outputs

By the end of a successful workshop, you have:

- **A shared model** in a single visual artifact — every participant points at the same wall.
- **A list of bounded contexts** with candidate names.
- **An event catalog** in domain language — directly usable as event names in code.
- **Aggregate candidates** — sized by how many events they receive.
- **A list of hot spots** — known unknowns, captured rather than glossed over.
- **A roadmap** — sequences of events that have to work for the business to work.

Many of these map directly to DDD tactical building blocks. **Event Storming is the discovery method DDD always implied but didn't specify.**

---

## Logistics: What You Actually Need

- **Wall space.** 8–15 meters of horizontal wall, ideally smooth and floor-to-ceiling.
- **Roll of butcher paper.** Cover the wall.
- **Sticky notes** in the canonical colors (orange, blue, yellow, pink, lilac, green) — *thousands*, more than you think.
- **Markers** in dark colors (Sharpies work; ballpoint won't read at distance).
- **People.** 4–20. Domain experts, developers, product, sometimes operations and support. One facilitator.
- **Time.** Half-day minimum; full day common.
- **Standing space** — chairs work against the energy.

**Remote/virtual variant:** Miro, Mural, FigJam. Lower energy, lower bandwidth, but viable when in-person isn't possible. Use breakout rooms for chaotic exploration; bring everyone back for the walkthrough.

---

## Facilitation Notes

The facilitator is critical. Their job:

- **Hold the space** — keep the room moving, prevent any one person dominating.
- **Enforce past tense on events** — every drift to "the system processes the order" is corrected to "Order Processed".
- **Use domain language** — quietly correct technical jargon when domain words exist.
- **Capture hot spots without resolving** — "great question, let's pink-sticky it and move on".
- **Walk the timeline often** — frequent narrations catch errors quickly.
- **Notice silence** — if a domain expert hasn't spoken, draw them in.
- **Notice volume** — if a developer is dominating, gently quiet them.

Bad facilitation kills the workshop. Practice on smaller domains before facilitating a high-stakes session.

---

## Event Storming and DDD

The two are deeply complementary. Event Storming is the *discovery* technique that produces DDD's *artifacts*:

| Event Storming output | DDD concept |
|---|---|
| Bounded boundary on the wall | Bounded Context |
| Cluster of events around an aggregate sticky | Aggregate |
| Domain event in orange | Domain Event |
| Blue command sticky | Command (often on an aggregate root) |
| Lilac policy | Process manager / saga / event handler |
| Pink external system | Anticorruption Layer candidate |
| Common terms appearing repeatedly | Ubiquitous Language |
| Disagreements about terms (hot spots) | Language reconciliation needed |

**If you do DDD without Event Storming, you usually invent your model in isolation and miss insights.**
**If you do Event Storming without then translating into DDD, you have a beautiful wall but no software.**

---

## Common Mistakes

- **Treating it as documentation.** The wall is a thinking tool; its real output is the *understanding* in the room. Photograph it, then expect to redo it as understanding deepens.
- **Skipping chaotic exploration.** Letting one person draw a "clean" timeline first. The chaos surfaces disagreement; without it, you smooth over the friction that matters.
- **Resolving hot spots in the moment.** Tempting, but kills momentum. Capture and continue.
- **Letting the room go silent.** Energy is the substrate. Stand-up rooms; visible artifacts; frequent narration.
- **Adding technology too soon.** Events and commands are in domain language. "User clicks button" is not a domain event.
- **Doing it alone.** Solo Event Storming on a piece of paper at your desk produces a personal mind-map, not shared understanding. The collaboration is the method.
- **Stopping at the first level.** Big Picture is great; without Process Modeling and Software Design, the workshop produces inspiration but not design.
- **Translating to UML afterward.** Don't. The sticky-note model *is* the artifact. Translate directly to code, with the wall as reference.

---

## When NOT to Use Event Storming

- **Trivial CRUD systems.** No emergent complexity to discover.
- **One-person teams.** The collaboration premium is the value; alone, it's overhead.
- **Domain experts unavailable.** Without them, you're guessing on paper.
- **Strict time constraints with a well-known domain.** If you already know the model, you don't need to discover it again.

For everything else with non-trivial domain complexity — give it a try.

---

## Quick Application Checklist

Before the workshop:
- [ ] Wall space booked, materials acquired, attendees confirmed?
- [ ] At least one domain expert in the room?
- [ ] A facilitator who's done this before (or read up extensively)?
- [ ] A clear scope ("we'll explore the whole reservation flow" — not "we'll model everything")?

During the workshop:
- [ ] Are events past tense?
- [ ] Are events in domain language?
- [ ] Are hot spots being captured (not resolved)?
- [ ] Is the room standing and moving?
- [ ] Has the facilitator walked the timeline at least 2–3 times?
- [ ] Have all attendees contributed?

After the workshop:
- [ ] Photographs of the wall preserved?
- [ ] Hot spots tracked for follow-up?
- [ ] Bounded contexts named and sketched?
- [ ] Next steps agreed (process modeling for highest-value flow, etc.)?
- [ ] Plan to translate to code (or further design sessions) in place?

---

## Reading

- **Alberto Brandolini**, *Introducing EventStorming* (Leanpub, ongoing) — the canonical text. Read whichever version is current.
- **Alberto Brandolini**'s talks (search "Event Storming Brandolini") — short videos worth watching before facilitating.
- **Vaughn Vernon**, *Implementing Domain-Driven Design* (2013) — pairs Event Storming inputs with DDD tactical outputs.
- **Mariusz Gil & Krisztina Hirth** — case studies and blog posts on EventStorming in the wild.
- **Paul Rayner**, *EventStorming Glossary* — sticky-note colors and definitions reference.
- **Avanscoperta**'s training materials — the firm behind much of the Event Storming dissemination.
