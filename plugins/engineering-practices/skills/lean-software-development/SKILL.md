---
name: lean-software-development
description: Apply Mary & Tom Poppendieck's seven principles of Lean Software Development from "Lean Software Development: An Agile Toolkit" (2003) and "Implementing Lean Software Development" (2006). Covers the seven principles (eliminate waste, amplify learning, decide as late as possible, deliver as fast as possible, empower the team, build integrity in, see the whole), the seven wastes of software (partially-done work, extra features, relearning, handoffs, task switching, delays, defects), value-stream mapping, set-based design, Real Options thinking, and the leadership mindset shift required for lean to take root. Use when articulating lean for software teams at a principle level, when distinguishing lean (the broader operational philosophy) from lean tools (Kanban etc.), when an organization is asking "what does lean mean for us?", when assessing where waste lives in a workflow, when arguing for delayed commitment (Real Options), or when planning a lean transformation beyond just adopting Kanban.
---

# Lean Software Development (Poppendieck)

Apply this skill when a team or organization needs the broader operational philosophy of lean — not just the tools (Kanban, value-stream maps, Kaizen events) but the *mindset* behind them. The Poppendiecks translated Taiichi Ohno's Toyota Production System into seven principles for software, with concrete tools and a leadership perspective.

## Core Philosophy

**Lean is a way of thinking, not a set of practices.** The principles are the substance; the tools are downstream. Teams that adopt the tools without the mindset get cargo-cult lean.

**Customer value is the measure.** Every activity is judged by whether it produces value for the customer. Activities that don't — even ones that feel productive — are waste.

**Optimize the whole, not the parts.** Local optimization (a single department working faster) often degrades global performance. Lean thinking is systemic.

**Defer commitment until the last responsible moment.** Decisions made too early lock in assumptions that turn out to be wrong. Decisions made too late miss windows. Find the last responsible moment.

**Build quality in.** Quality is a property of the *process*, not an inspection step at the end. Test-driven development, refactoring, pairing, and short cycles are quality-building mechanisms.

---

## The Seven Principles

The book's spine. Each principle has a chapter; each has associated tools.

### 1. Eliminate Waste
**Waste is anything that doesn't add value to the customer.** Lean's first principle is to learn to see waste.

The Poppendiecks identify **seven wastes of software development** (translating Toyota's seven manufacturing wastes):

| Software waste | Manufacturing equivalent | What it looks like |
|---|---|---|
| **Partially-done work** | Inventory | Unmerged branches, undeployed features, half-finished refactors, untested code |
| **Extra features** | Overproduction | Gold-plating, "we might need this", speculative generality |
| **Relearning** | Reprocessing | Re-deriving knowledge that someone already had; tribal-knowledge loss |
| **Handoffs** | Transportation | Specifications passed between people; each handoff loses information |
| **Task switching** | Motion | Multitasking; context-switch overhead; interrupt-driven work |
| **Delays** | Waiting | Waiting for review, for environments, for decisions, for stakeholders |
| **Defects** | Defects | Bugs, escaped issues, late-found regressions |

**The exercise:** in a team's value stream, identify which of the seven dominate. Most teams have one or two main wastes that, if removed, would transform throughput.

### 2. Amplify Learning
**Software development is a knowledge-creation process.** The plan is wrong; we discover the right design through implementation and feedback. The goal is to maximize learning rate.

Tools:
- **Short iterations** with working software at the end of each.
- **Feedback from real users** as early and often as possible.
- **Set-based design** — keep multiple options alive until information arrives that narrows the choice (rather than committing early to one path).
- **TDD and short test cycles** — every test run is a learning event.
- **Pair programming and code review** — two people learn each thing.
- **Synchronization meetings** — surface assumptions for testing.

The mistake: treating software development as *executing a known plan*. It isn't. It's *creating new knowledge*. Plans serve learning, not the other way around.

### 3. Decide as Late as Possible
**Make decisions at the last responsible moment.** Premature commitment locks in assumptions that haven't been validated.

Tools / patterns:
- **Real Options thinking** (Chris Matts, Olav Maassen) — treat commitments as options to be exercised when conditions are right; preserve flexibility.
- **Set-based design** — keep multiple alternatives in parallel until you have the information to discard.
- **Last responsible moment** — the moment beyond which deferring would forfeit a valuable option.
- **Avoiding feature flags as permanent architecture** — flags should be temporary deferrers, not the design.

What "decide late" doesn't mean:
- *Procrastinate.* The point is to wait for information, not to avoid the decision.
- *Never plan.* You still plan; you avoid premature *commitment* in the plan.
- *Always wait.* Some decisions are irreversible — decide them carefully, but don't pretend they're reversible.

The skill: distinguishing reversible (1-way doors → decide fast) from irreversible (2-way doors → decide carefully and late).

### 4. Deliver as Fast as Possible
**Speed of delivery is itself a quality of the system.** Faster delivery → faster feedback → less waste → higher quality → faster delivery.

Tools:
- **Pull systems** — work moves through the system when capacity allows, not when the previous stage pushes it.
- **Queueing theory awareness** — visible queues; managed WIP.
- **Small batches** — small features, small PRs, small releases.
- **Continuous flow** instead of batch handoffs.
- **Self-determining teams** — teams decide their own work order within constraints.

This is essentially the operational frame that Kanban, Continuous Delivery, and Lean Startup all rest on.

### 5. Empower the Team
**The people doing the work know best how to do it.** Leadership's job is to give them direction and remove obstacles, not to direct the work.

The leadership shift:
- **From manager to leader.** Managers tell people what to do; leaders set direction and let people choose how.
- **From command to mission.** Specify intent and constraints; let the team choose the means (Auftragstaktik).
- **From individual incentives to team incentives.** Software development is collaborative; individual KPIs sabotage it.
- **From specialists in silos to T-shaped contributors.** Depth in one area, breadth across the system. Reduces handoffs.

Daniel Pink's three drivers of motivation (used by the Poppendiecks): **autonomy, mastery, purpose**. Empowerment provides all three; command-and-control destroys all three.

### 6. Build Integrity In
Two kinds of integrity:

**Perceived integrity** — the system's wholeness as the *customer* experiences it. Does it solve their problem? Do its parts fit together coherently from the outside? Did we build the right thing?

**Conceptual integrity** — the system's wholeness as the *developers* understand it. Are the abstractions consistent? Does the architecture hang together? Did we build it right?

Tools for both:
- **Refactoring** continuously, not in big-bang campaigns.
- **TDD** — the only practical way to refactor safely.
- **Pairing and code review** — preserve conceptual integrity through shared understanding.
- **Direct customer access** — perceived integrity requires understanding the customer's actual experience.
- **Working software at frequent intervals** — both integrities surface only by exercising the real system.

Integrity is not a quality assurance phase. It is **built in** by the cycles of development.

### 7. See the Whole
**Optimize the system, not the parts.** Local optimization is often a net negative globally.

Tools:
- **Value Stream Mapping** — diagram the end-to-end flow from customer request to value delivered; measure cycle time and quality at each step.
- **System metrics over local metrics** — measure throughput, lead time, customer satisfaction; not individual or team utilization.
- **Cross-functional teams** — fewer handoffs between specialties.
- **Shared responsibility for outcomes** — no "we shipped, ops failed".

The mistake: making one part of the value stream faster by pushing problems downstream (the QA team falling behind, the support team drowning in incidents). Lean asks: is the *whole* faster?

---

## The Seven Wastes — Detailed

Worth dwelling on; this is where teams find the most actionable insight.

### Partially-done Work (Inventory)
Code in branches that won't merge for weeks. Features built but not deployed. Refactors started but not finished. Each is *inventory* — it has value tied up in it that hasn't been realized, and it's subject to obsolescence.

**Counter:** finish-before-start. Limit WIP. Trunk-based development. Small PRs.

### Extra Features (Overproduction)
"We thought users might want this." "Let's add an option for that." "What if we make it configurable?"

About **45-65% of features shipped are rarely or never used** (Standish Group, also cited by the Poppendiecks). Building them is pure waste.

**Counter:** build the smallest thing that delivers value. Validate before extending. Cut features when in doubt.

### Relearning (Reprocessing)
Someone figured out how the auth flow works two years ago. They wrote nothing down. They left. Now the team is figuring it out again.

**Counter:** ADRs. Documentation of decisions and rationale. Pairing to spread knowledge. Onboarding documentation.

### Handoffs (Transportation)
Designer hands off to developer. Developer hands off to tester. Tester hands off to ops. Each handoff loses information; each gap is a queue.

**Counter:** cross-functional teams. Reduce specialization where possible. When handoffs are unavoidable, shorten the gap and make it bidirectional (pairing across functions).

### Task Switching (Motion)
Working on three things badly is slower than working on one well. Context-switching has measurable cost (5-20 minutes per switch to fully re-engage).

**Counter:** WIP limits. Block time. Single-tasking by default. Protect from interruption.

### Delays (Waiting)
Code waits for review. PRs wait for CI. Features wait for deployment. Decisions wait for stakeholders. Each delay is value not yet delivered.

**Counter:** reduce queue lengths (WIP limits). Reduce queue handling time (faster CI, smaller reviews, automated approvals where safe).

### Defects (Defects)
Bugs in production. Issues that escape testing. Regressions in old features.

**Counter:** test-driven development. CI. Code review. Refactoring. Observability. The shift from "test for quality" to "build for quality".

---

## Value Stream Mapping

The diagnostic tool. Draw the path of a single piece of work from "request received" to "value delivered". For each step:
- **Process time** — time actually spent doing work
- **Wait time** — time the work sits between processes

Add it all up. The ratio of process time to total time is the team's **flow efficiency** (cf. the `flow-efficiency` skill). For most software teams, it's 5-20%.

The map exposes the biggest queues. Those are the leverage points.

**A simple software VSM:**
```
Story ready → Pick up → Dev (3d) → PR wait (2d) → Review (1d) →
  Test queue (1d) → Test (1d) → Deploy queue (3d) → Deploy (½d) →
  Live ↓
Total: 11.5 days. Process time: 5.5 days. Flow efficiency: 48%.
```

(For most real teams, this is *optimistic*. The actual ratio is often worse.)

---

## Set-Based Design

A pattern less known than it should be. Borrowed from Toyota's product design.

**Conventional approach (point-based design):**
1. Pick the "best" design early.
2. Detail it.
3. If it doesn't work, iterate.

**Set-based approach:**
1. Identify multiple possible designs.
2. Develop them in parallel to some depth.
3. As information arrives, eliminate the ones that don't work.
4. Converge on the surviving design.

This is more expensive *per option* but cheaper *per outcome* because it avoids the cost of starting over when the chosen design fails.

In software: feature flags + A/B tests are a degenerate form of set-based design. Genuine set-based design keeps architectural options open through the design phase.

When to use:
- High uncertainty about the right solution.
- Cost of being wrong is high.
- Multiple options can be cheaply explored in parallel.

---

## Real Options Thinking

A frame the Poppendieks promote (citing Chris Matts and Olav Maassen). Borrowed from financial options.

**Every decision is an option.** Until you commit, you can change your mind. Each option has:
- A **value if exercised** at a particular time.
- An **expiration** — beyond which it's no longer available.
- A **cost** of preserving the option.

The discipline:
1. **Identify your real options** in a decision.
2. **Determine each option's expiration** ("when must we choose?").
3. **Defer commitment to the last responsible moment** — exercising the option at the right time.

This is the rigorous form of "decide as late as possible". It avoids paralysis ("we'll decide later") by making the deadline explicit.

---

## The Leadership Mindset Shift

A theme that runs throughout the book. Lean requires a shift in how leadership thinks:

| From | To |
|---|---|
| Managing tasks | Setting direction |
| Telling how | Specifying what and why |
| Individual KPIs | Team outcomes |
| Status reports | Walking the work (gemba) |
| Top-down planning | Pull from the team |
| Punishing variance | Investigating system causes (Deming's 95/5) |
| Hiring for skills | Hiring for learning |
| Inspecting for quality | Building for quality |
| Local optimization | System optimization |

Without this shift, all the tools become bureaucracy. With it, the tools amplify.

---

## How This Skill Pairs with Others

- **`flow-efficiency`** — the strategic frame. Lean Software Development is the principle-level implementation of "choose flow over utilization".
- **`product-development-flow`** — Reinertsen's quantitative version. The Poppendiecks give principles and stories; Reinertsen gives numbers and equations. Different audiences, same direction.
- **`kanban`** — the practical operationalization of principles 1, 4, and 7.
- **`continuous-delivery`** — the deployment side of "deliver as fast as possible" and "build integrity in".
- **`test-driven-development`** — the practice for "build integrity in" and "amplify learning".
- **`splitting-user-stories`** — small batches; eliminates "extra features" waste.
- **`refactoring`** — the continuous practice for "build integrity in".
- **`toyota-kata`** — the improvement discipline that operationalizes "amplify learning" continuously.
- **`pragmatic-programmer`** — overlapping mindset principles at the individual level.
- **`fractal-architecture`** — Seemann's emphasis on sustainable design overlaps heavily with "build integrity in".

---

## Common Pitfalls

- **Cargo-cult lean.** Adopting the tools (Kanban, retros) without the mindset (eliminate waste, empower teams). The tools feel like overhead; nothing improves.
- **"Lean = cost cutting".** Misreading. Lean is about increasing value flow, often by *spending* on test automation, CI, and slack capacity.
- **"Decide late = decide never".** The discipline is to defer to the last *responsible* moment, not avoid decisions.
- **Eliminating "waste" without seeing the system.** Sometimes what looks like waste (a queue, a review step) is buffering against variability. Diagnose before excising.
- **Empowering teams while still measuring individual utilization.** Sends contradictory signals; the metric wins.
- **Building integrity in only at the end.** "Integrity-in" means continuous, not a final phase.
- **Local value-stream optimization.** Speeding up one stage while pushing more work to the next. Lean asks: did the *whole* speed up?
- **Pursuing perfection over flow.** Lean prefers continuous improvement over big-bang transformation.

---

## A Lean Diagnosis: A Worked Example

A software team complains that "we keep working hard but features take forever to ship." Applying Lean Software Development:

**1. Value stream map.** Sketch the flow. Total time: 15 days from story-ready to deployed. Process time: 4 days. Flow efficiency: 27%.

**2. Identify the dominant wastes.** From the map:
- Partially-done work: high (8 PRs open at any time across 5 developers).
- Delays: high (PRs wait 3 days for review on average).
- Handoffs: moderate (separate test team adds 2 days).
- Task switching: high (each developer carries 3 in-flight items).
- Defects: moderate (post-deploy bug rate ~15%).

**3. Pick the leverage point.** Biggest waste = delays in review + task switching = both pointing to high WIP. Diagnosis: WIP is too high; pulling work doesn't bring it in fast enough through review.

**4. Counter-measure.** Lower WIP limit. Each developer holds at most 1 in-flight item. PR queue cap of 3. When the cap is hit, the team swarms on review.

**5. Set-based experiment.** Try the new WIP limits for 2 sprints. If cycle time drops without throughput collapsing, keep. Otherwise revert and try a different lever (faster CI, automated tests instead of separate QA, etc.).

**6. See the whole.** Don't just measure dev cycle time; measure end-to-end including ops + customer support. Are bugs decreasing? Is customer satisfaction rising?

**7. Empower.** Let the team adjust their own WIP limits based on what they see. Leadership specifies the goal (cycle time < 7 days for standard stories at p85), not the means.

This is what the principle-level lean diagnosis looks like in practice.

---

## Quick Application Checklist

When adopting or assessing lean:

- [ ] Have I identified the seven wastes in our specific context?
- [ ] Have I value-stream-mapped at least one full path from request to delivery?
- [ ] Where is the dominant waste? What's the leverage point?
- [ ] Are we treating software development as knowledge creation or as plan execution?
- [ ] Are decisions being deferred to the last responsible moment, or rushed?
- [ ] Are quality practices continuous (TDD, refactoring) or end-of-cycle (QA phase)?
- [ ] Does the team have the autonomy needed to act on what they learn?
- [ ] Are we measuring system outcomes (cycle time, customer value) or local proxies (utilization)?
- [ ] Have I shifted my own management approach to mission-and-intent, or am I still directing tasks?

---

## Reading

- **Mary & Tom Poppendieck**, *Lean Software Development: An Agile Toolkit* (Addison-Wesley, 2003) — the first book. Compact, principle-focused.
- **Mary & Tom Poppendieck**, *Implementing Lean Software Development: From Concept to Cash* (Addison-Wesley, 2006) — the practical follow-up; expands tools and case studies.
- **Mary & Tom Poppendieck**, *Leading Lean Software Development: Results Are Not the Point* (2009) — the leadership-focused third book.
- **Niklas Modig & Pär Åhlström**, *This is Lean* (Rheologica, 2012) — the strategic frame.
- **Don Reinertsen**, *The Principles of Product Development Flow* (Celeritas, 2009) — the quantitative companion.
- **Taiichi Ohno**, *Toyota Production System* (1988) — the source. Read for grounding.
- **Mike Rother**, *Toyota Kata* (2009) — the continuous-improvement engine.
- **Chris Matts & Olav Maassen**, *Commitment* (Hathaway te Brake, 2013) — the Real Options book, in graphic-novel form.
- **Daniel H. Pink**, *Drive* (2009) — the autonomy/mastery/purpose framing the Poppendiecks cite.
- **Eric Ries**, *The Lean Startup* (2011) — adjacent; lean for the business / product side.
