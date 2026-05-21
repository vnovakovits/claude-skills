---
name: splitting-user-stories
description: Split user stories into small, valuable, independently-shippable slices using INVEST (Bill Wake), Richard Lawrence's 9-pattern flowchart, Mike Cohn's SPIDR, Gojko Adzic's hamburger method, Jeff Patton's story mapping, and Henrik Kniberg's MVP analogies. Use when a story is too big to ship in one sprint, when "we'll do it all at once" feels risky, when carving an MVP, when planning incremental delivery, or when a story has hidden complexity that needs to be exposed in slices.
---

# Splitting User Stories

Apply this skill whenever a story feels too large to deliver confidently in a short cycle, when scope is uncertain, when you need to ship value sooner than the full feature, or when a "big bang" delivery would carry too much risk. The goal is **small, vertical, valuable slices** — each one shippable, each one teaching you something about the next.

## Core Philosophy

**Smaller is better.** Small stories ship faster, get feedback sooner, carry less risk, and reveal misunderstandings earlier. The cost of splitting is almost always less than the cost of working with a big story.

**Slice vertically, not horizontally.** A vertical slice goes through every layer (UI → API → domain → DB) for one narrow behavior. A horizontal slice ("build the database first") delivers no value until everything is done.

**Each slice must deliver value.** Not necessarily user-facing value on day one — but feedback, learning, or progress toward a verifiable outcome. "Set up the database" is not a slice; "users can register with an email" is.

**Splitting is a design activity, not a bookkeeping one.** Done well, it surfaces requirements, exposes risk, and shapes architecture. Done badly, it becomes ceremony.

**You can always go smaller.** When in doubt, split again. The smallest valuable slice is almost always smaller than your first instinct suggests.

---

## INVEST: Criteria for a Good Story (Bill Wake, 2003)

Every story should be:

- **I — Independent.** Can be delivered without depending on other un-delivered stories. (Some dependencies are unavoidable, but minimize them.)
- **N — Negotiable.** A story is a placeholder for a conversation, not a contract. Details are refined collaboratively.
- **V — Valuable.** Delivers value to someone — user, business, the team's learning. Pure technical tasks are not stories.
- **E — Estimable.** The team can estimate the work. If they can't, it's too vague or too big — split or spike.
- **S — Small.** Small enough to deliver in a short cycle (days, not weeks). When in doubt, smaller.
- **T — Testable.** Acceptance criteria can be expressed concretely. If you can't define "done", you can't define "the story".

A story that fails INVEST is a candidate to split, refine, or rewrite.

---

## Vertical vs Horizontal Slicing

```
HORIZONTAL (DON'T)              VERTICAL (DO)
┌──────────────┐                ┌─┬─┬─┬─┬─┐
│      UI      │                │ │ │ │ │ │
├──────────────┤                │U│U│U│U│U│
│  Application │                │I│I│I│I│I│
├──────────────┤                ├─┼─┼─┼─┼─┤
│    Domain    │                │A│A│A│A│A│
├──────────────┤                ├─┼─┼─┼─┼─┤
│   Database   │                │D│D│D│D│D│
└──────────────┘                ├─┼─┼─┼─┼─┤
                                │ │ │ │ │ │
                                └─┴─┴─┴─┴─┘
   build a layer at a time,         each slice is shippable,
   nothing ships until done         delivers value end-to-end
```

**Vertical slices** are the foundation of agile delivery, continuous deployment, and outside-in development. **Always prefer vertical.**

Henrik Kniberg's analogy: a skateboard, a scooter, a bike, a motorcycle, a car — each is a *complete* transport solution. Building a wheel, then a chassis, then an engine, then a body produces no value until the end.

---

## Richard Lawrence's 9 Splitting Patterns (Humanizing Work)

The most widely-used field reference. When a story is too big, work through these patterns in roughly this order; usually one or two of them fit your situation.

### 1. Workflow Steps
The story covers a multi-step process; deliver one step at a time, the simplest path first.

> *Place an order* → *Add to cart*, *Check out*, *Pay*, *Confirm*

### 2. Business Rule Variations
The story has many business rules or special cases; pick one rule first, add the others as separate stories.

> *Calculate shipping cost* → *Domestic standard*, *International*, *Express*, *Free over £50*, *Hazardous materials*

### 3. Happy / Unhappy Paths
Implement the happy path first; defer error handling, edge cases, validation to follow-on stories.

> *User pays with credit card* → *Successful payment*, *Card declined*, *Network failure*, *Fraud check failure*

### 4. Input Options / Platform
Support one input type / platform first; add others as separate stories.

> *Customer signs up* → *Email signup*, *Google sign-in*, *Apple sign-in*, *Mobile app signup*

### 5. Data Types or Parameters
The story handles several data types; do one type per story.

> *Import customer records* → *Import CSV*, *Import Excel*, *Import JSON*, *Import via API*

### 6. Operations (CRUD)
The story is "manage X"; split by operation.

> *Manage users* → *Create user*, *View user*, *Edit user*, *Deactivate user*

### 7. Test Scenarios / Use Cases
The story implies many test scenarios; pick the most important first.

> *Search products* → *Search by exact name*, *Search by partial name*, *Filter by category*, *Sort by price*

### 8. Break Out a Spike
The story is unestimable because of unknowns. Replace it with a time-boxed research story (a *spike*) to remove the unknowns; then split the real story afterward.

> *Integrate with new payment provider* → **Spike**: explore provider API, then split the implementation.

### 9. Simple / Complex
Build the simplest "tracer bullet" first — the trivial implementation that proves the path works. Then add the complexity as separate stories.

> *Recommend products* → *Show 3 random products*, *Show recently-viewed products*, *Show ML-based recommendations*

**Use Lawrence's flowchart** (free PDF from Humanizing Work — see Reading). It walks you through these patterns as a decision tree.

---

## Mike Cohn's SPIDR

A simpler mnemonic, with overlap to Lawrence's patterns but easier to remember in conversation:

- **S — Spike.** Time-box a research story to remove unknowns.
- **P — Paths.** Split by execution paths (happy path first, alternates and errors later).
- **I — Interfaces.** Split by UI / device / channel (web first, mobile later; API first, UI later).
- **D — Data.** Split by data types, data variations, or by *deferring* perfect data handling.
- **R — Rules.** Split by business rule (simplest rule first; exceptions and edge rules later).

SPIDR is what to reach for in standup or refinement when you can't load the full flowchart in your head.

---

## Gojko Adzic's Hamburger Method

For stories that resist the patterns above, Adzic's method works in two passes:

**1. List the steps (workflow layers).** Each step is a "bun" or "filling" — a horizontal layer of the work.

**2. For each step, list options from cheapest/dumbest to most sophisticated.** Each option is a level of sophistication for that step.

**3. Build the thinnest slice** — the simplest option for every step. That's your first hamburger. Subsequent stories upgrade individual steps to richer options.

Example: "Customer searches for products"

| Step | Cheap | Medium | Rich |
|---|---|---|---|
| Search input | Single textbox | + filters | + autocomplete |
| Search logic | Exact name match | Partial match | Fuzzy + synonyms |
| Results display | Plain list | + thumbnails | + previews |
| Ranking | Alphabetical | Relevance | ML-personalized |
| Performance | Synchronous DB query | + cache | + search index |

First slice: textbox + exact match + plain list + alphabetical + synchronous. Ships in a day. Each follow-up story upgrades one column.

The method is especially powerful when the team disagrees on scope — laying out the options visually exposes the disagreement.

---

## Jeff Patton's Story Mapping (slicing at scale)

For a whole product or release, not just one story. A **story map** organizes stories into a 2D grid:

- **Horizontal axis** — the user's journey, left to right (the *backbone*).
- **Vertical axis** — depth / sophistication / priority within each step.

```
USER JOURNEY ──►  Browse  → Add to cart → Checkout → Pay → Receive
                  ──────────────────────────────────────────────────
Slice 1 (MVP)     basic   | single item | one form  | card | email
                  ──────────────────────────────────────────────────
Slice 2           filters | multi-item  | saved addr| +PP  | tracking
                  ──────────────────────────────────────────────────
Slice 3           search  | wishlist    | guest co  | wallet| returns
```

Each **horizontal slice** is a coherent release: every step of the journey works, at the chosen sophistication level. Slice 1 is the MVP — the thinnest end-to-end version that proves the journey.

Story mapping is the antidote to "build everything for one step before moving to the next".

---

## MVP, Cupcake, Walking Skeleton, Steel Thread

Different vocabularies for the same idea: **the smallest end-to-end working version**.

- **MVP (Eric Ries)** — Minimum Viable Product. The smallest version that allows you to learn from real users. Not the smallest version you're proud of.
- **Walking skeleton (Cockburn / Freeman & Pryce)** — an end-to-end implementation, however trivial, that exercises every layer of the architecture. Used to prove the pipeline before adding features.
- **Steel thread (Booch et al.)** — one path through the system, fully implemented and integrated. Other threads added later.
- **Cupcake (Henrik Kniberg)** — a tiny, complete, edible version of the cake. The icing matters too — UX/value are part of the cupcake, not deferred.

**Common pitfall:** confusing "MVP" with "the slow first version we're embarrassed by". A good MVP is the smallest version that is genuinely useful or genuinely informative — usually smaller than the team's first instinct.

---

## Spikes: When You Can't Estimate

A **spike** is a time-boxed investigation, not a delivery story. Use one when:
- You can't estimate the story because of unknowns (technology, library behavior, integration, performance).
- A short investigation would dramatically reduce uncertainty.

A spike has:
- A **specific question** to answer ("Can we hit 100ms response time with this DB?").
- A **time box** ("4 hours", "1 day").
- A **deliverable** that closes the question — usually a short writeup, prototype, or decision, not production code.

After the spike, write the real story (or stories) with confidence and split them properly.

---

## Acceptance Criteria as a Splitting Tool

If a story has 8 acceptance criteria, it's usually 2–4 stories.

Read each criterion aloud and ask:
- Is this criterion essential for the story to be valuable, or is it nice-to-have?
- Can the story ship without this criterion and still deliver something?

If yes: split the criterion into its own story.

Acceptance criteria written as Given/When/Then (BDD scenarios) make splitting easy: each scenario is a candidate story.

---

## Common Anti-patterns

- **Technical-task stories.** "Set up the database schema", "build the API layer". These deliver no user-facing value; they are tasks, not stories. Fold them into vertical slices.
- **Horizontal slicing.** "Sprint 1: backend; sprint 2: frontend; sprint 3: integration." Nothing ships until sprint 3, and integration risk is concentrated at the end.
- **"It can't be split."** Almost everything can be split. The actual question is whether the team can see how. Apply the patterns above; the answer almost always appears.
- **Splitting that loses value.** "Login (without password validation)" is not valuable. Verify each slice still delivers something real.
- **Splitting by component, not behavior.** "Story 1: payment service; Story 2: order service." Each is half a behavior. Slice by user behavior, then let architecture follow.
- **Mega-stories that defy estimation.** "Implement the reporting module." Spike, then map, then split.
- **Spikes that become production code.** A spike is a learning artifact; throw it away. Code born of a spike has no tests, no design, no review.
- **Splits with hidden coupling.** Two "independent" stories that share infrastructure changes that haven't been pulled out. Make the shared work visible.
- **Story bloat through "and".** "User can register **and** log in **and** reset password." Three stories with "and"s pretending to be one.
- **Splitting for the sake of metrics.** Splits should improve flow and reduce risk. Splitting to make the burndown look better is theatre.

---

## When NOT to Split Further

Diminishing returns set in eventually. Stop splitting when:
- The story is already small enough to deliver in a day or two.
- Further splits would leave individual stories with no observable value.
- The split would require building and tearing down too much scaffolding.
- The team is confident in the design and the integration.

The goal is *small enough*, not *as small as theoretically possible*.

---

## A Worked Example

Original story: **"As a customer, I can manage my subscription so I can change my plan or cancel."**

This story fails INVEST: too big (S), unclear (T), probably depends on billing changes (I). Split:

Apply **CRUD pattern**:
1. *Customer can view current subscription*
2. *Customer can upgrade plan*
3. *Customer can downgrade plan*
4. *Customer can cancel subscription*

Now apply **Happy/Unhappy paths** to #2:
- 2a. Customer upgrades from monthly to annual *(happy path: simple proration, success)*
- 2b. Customer's payment fails during upgrade *(error path)*
- 2c. Customer upgrades during a promotional period *(business rule variation)*

Now apply **Interfaces** to 2a:
- 2a-i. Upgrade via account settings page
- 2a-ii. Upgrade via mobile app
- 2a-iii. Upgrade via support agent dashboard

You started with one fuzzy story and finished with seven shippable slices, each INVEST-compliant and each delivering observable value. The first slice (2a-i) ships in days.

---

## Quick Application Checklist

When deciding whether to split:
- [ ] Can the team deliver this story in 1–3 days?
- [ ] Can the team estimate this story confidently?
- [ ] Does the story pass INVEST?
- [ ] Are there more than 3–4 acceptance criteria?
- [ ] Does the story contain "and"?
- [ ] Are there unknowns the team can't size?

If any answer suggests splitting, try in this order:
- [ ] **Workflow steps** — is this a multi-step process?
- [ ] **Happy / unhappy paths** — can we ship the happy path first?
- [ ] **Business rule variations** — are there multiple rules or cases?
- [ ] **CRUD** — is this "manage X"?
- [ ] **Data variations** — are there multiple data types or sources?
- [ ] **Interfaces** — multiple channels, devices, platforms?
- [ ] **Spike** — are the unknowns blocking estimation?
- [ ] **Simple / complex** — can we build a tracer bullet first?
- [ ] **Hamburger method** — list steps, list options, ship the thinnest row?

For every resulting slice:
- [ ] Is it a vertical slice (touches every layer it needs to)?
- [ ] Does it deliver observable value or learning?
- [ ] Is it independent of other un-delivered slices?
- [ ] Is it testable with concrete acceptance criteria?
- [ ] Is it estimable?
- [ ] Have I avoided technical-task framing ("set up X")?

---

## Reading and Resources

- **Bill Wake**, *INVEST in Good Stories, and SMART Tasks* (2003) — the original short essay defining INVEST. Available at xp123.com.
- **Richard Lawrence & Peter Green**, *The Humanizing Work Guide to Splitting User Stories* — the canonical 9-pattern flowchart, free PDF at humanizingwork.com.
- **Mike Cohn**, *User Stories Applied: For Agile Software Development* (2004) — foundational text on user stories.
- **Mike Cohn**, *Agile Estimating and Planning* (2005) — sizing, splitting, release planning.
- **Mike Cohn**, *Better User Stories* online course and articles on SPIDR.
- **Jeff Patton**, *User Story Mapping: Discover the Whole Story, Build the Right Product* (2014) — story maps, slicing for releases.
- **Gojko Adzic**, *Fifty Quick Ideas to Improve Your User Stories* (2014) — practical patterns including the hamburger method.
- **Gojko Adzic**, *Impact Mapping* (2012) — driving stories from business outcomes rather than features.
- **Henrik Kniberg**, *Making Sense of MVP* (essay / sketch, 2016) — the skateboard / car analogy.
- **Eric Ries**, *The Lean Startup* (2011) — MVP as a learning instrument.
- **Christiaan Verwijs**, *Splitting User Stories: The 8 Hands-On Patterns* (2017 essay, agilistic.nl).
- **Alistair Cockburn**, *Walking Skeleton* — Wiki / essay.
- **Martin Fowler**, *YAGNI* and *MinimumViableProduct* — short essays at martinfowler.com.
