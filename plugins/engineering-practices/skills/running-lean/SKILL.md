---
name: running-lean
description: Apply Ash Maurya's "Running Lean: Iterate from Plan A to a Plan That Works" (3rd edition, O'Reilly, 2022). Covers the Continuous Innovation Framework (Vision → Strategy → Continuous Innovation), the three stages of a product (Problem/Solution Fit → Product/Market Fit → Scale), the Lean Canvas (Maurya's 9-box adaptation of the Business Model Canvas), the Customer Factory model (acquisition, activation, retention, revenue, referral), the Traction Roadmap (working back from a minimum success criteria), the 90-day cycle as the unit of execution, the three types of customer interviews (problem, solution, MVP), the Mafia Offer pattern, MVP types and how to choose, the eight pivot types, and the discipline of testing demand before building. Use when starting a new product or feature without product/market fit, when deciding what to build (or whether to build at all), when designing customer-discovery interviews, when filling in or refining a Lean Canvas, when building an MVP, when evaluating whether to pivot or persevere, or when running a 90-day product cycle.
---

# Running Lean (Ash Maurya, 3rd edition)

Apply this skill when you have an idea but not yet a working product — or a product but not yet repeatable customer acquisition — or you are about to invest serious engineering effort in something whose customer value hasn't been validated. *Running Lean* is the operational manual for de-risking a new product *before* the engineering investment becomes a sunk cost.

## Core Philosophy

**Most products fail not because they can't be built, but because nobody wants them.** Engineering effort is the largest single risk to a startup or new-product initiative. The discipline of Running Lean is to **test demand before testing implementation** — and only invest engineering after the demand is real.

**Idea ≠ Product.** A working product is just one execution of an idea. There are infinite possible products that could embody an idea. The job of a founder / intrapreneur is to find the *one product* that works — not to faithfully build the *first product* they imagined.

**Plan A is wrong.** Maurya's central tenet (and the book's subtitle: "Iterate from Plan A to a Plan That Works"). Your first written plan won't survive contact with customers. The discipline is to iterate it deliberately rather than randomly.

**Customers don't want your product. They want their problem solved.** The right product is the cheapest, simplest thing that solves the customer's problem better than the current alternatives — not the technologically most impressive thing you can build.

**Continuous innovation is the loop:** Sense → Decide → Act. Sense the market (interviews, metrics, signal); Decide based on what you sensed (persevere or pivot); Act on the decision (build a tiny thing); repeat.

---

## The Continuous Innovation Framework

The 3rd edition's central organizing structure:

```
       ┌─────────────────┐
       │     VISION      │  Where you want to take this in 3-10 years
       │  (north star)   │
       └────────┬────────┘
                │
       ┌────────▼────────┐
       │    STRATEGY     │  How you'll get there (lean canvas, traction roadmap)
       │  (the bet)      │
       └────────┬────────┘
                │
       ┌────────▼────────┐
       │  CONTINUOUS     │  Sense → Decide → Act
       │  INNOVATION     │  (90-day cycles)
       └─────────────────┘
```

- **Vision** changes rarely (years).
- **Strategy** is revised quarterly or when major learnings occur.
- **Continuous innovation** is the daily/weekly/90-day cadence of testing and learning.

The three levels must be aligned. A 90-day cycle that doesn't serve the strategy, or a strategy that doesn't serve the vision, wastes effort.

---

## The Three Stages of a Product

Different stages require different tactics. Confusing which stage you're in is one of the most common errors.

### Stage 1: Problem/Solution Fit
**Question being answered:** is there a problem worth solving?

You don't yet know if customers care enough about the problem to pay for / adopt a solution. **No code is needed here.** Your work is:
- Lean Canvas
- Problem interviews
- Initial solution interviews
- Mafia Offer prototype

**Exit criterion:** customers say "yes" to a defined problem they have, *with their own money or commitment*.

### Stage 2: Product/Market Fit
**Question being answered:** can a product be built that customers will use / pay for repeatedly?

You're building the MVP — but only the smallest version that proves the value proposition.
- Solution interviews to refine
- MVP interviews to validate
- Build a usable MVP
- Get to first paying customers
- Iterate on the customer factory until activation and retention are stable

**Exit criterion:** Sean Ellis test (40% of users would be "very disappointed" if your product disappeared), AND repeatable customer acquisition.

### Stage 3: Scale
**Question being answered:** can growth be made repeatable and profitable?

Now (and only now) is the right time to invest in marketing, automation, growth engineering. Earlier investment in scale is wasted because the customer factory wasn't yet stable.

**Each stage requires different focus, different metrics, different team structure.** Trying to "scale" before product/market fit produces expensive flameouts. Doing "customer discovery" interviews when you're already at scale is a misallocation.

---

## The Lean Canvas

Maurya's adaptation of Alex Osterwalder's Business Model Canvas — replacing four boxes to make it more useful for startups. **One page, nine boxes, 20 minutes to draft.**

```
┌─────────────┬─────────────┬───────────────────┬──────────┬──────────────────┐
│  PROBLEM    │  SOLUTION   │ UNIQUE VALUE      │ UNFAIR   │  CUSTOMER        │
│             │             │ PROPOSITION       │ ADVANTAGE│  SEGMENTS        │
│ Top 3       │ Top 3       │                   │          │                  │
│ problems    │ features    │ Single, clear,    │ Cannot   │ Target users     │
│             │             │ compelling msg    │ be copied│ Early adopters   │
│             │             │ that turns        │ or       │                  │
│             ├─────────────┤ visitor into      │ bought   ├──────────────────┤
│             │ KEY METRICS │ prospect          │          │  CHANNELS        │
│             │             │                   │          │                  │
│ Existing    │ Key numbers │                   │          │ Path to          │
│ alternatives│ that tell   │                   │          │ customers        │
│             │ you how the │                   │          │                  │
│             │ business is │                   │          │                  │
│             │ doing       │                   │          │                  │
├─────────────┴─────────────┴───────────────────┴──────────┴──────────────────┤
│  COST STRUCTURE                                │  REVENUE STREAMS           │
│                                                │                            │
│  Customer acquisition cost, distribution,       │  Revenue model, lifetime  │
│  hosting, salaries, etc.                       │  value, gross margin,     │
│                                                │  break-even               │
└────────────────────────────────────────────────┴────────────────────────────┘
```

### How to use it
- **Draft fast.** First pass in 20 minutes. Don't research first; capture your current assumptions, then test.
- **One canvas per customer segment.** Different segments = different canvases.
- **Iterate ruthlessly.** Every customer interview, every experiment, every learning prompts canvas updates.
- **Make it visible.** The canvas is a strategic tool; treat it like one.

### The order Maurya recommends filling it in
1. Customer Segments + Problem (start with the customer's pain)
2. Unique Value Proposition (the message)
3. Solution
4. Channels
5. Revenue Streams
6. Cost Structure
7. Key Metrics
8. Unfair Advantage (last because most founders don't have one yet)

### The Lean Canvas vs Business Model Canvas
Maurya replaced:
- Key Partners → **Problem**
- Key Activities → **Solution**
- Key Resources → **Key Metrics**
- Customer Relationships → **Unfair Advantage**

The replacement reflects what's actually risky for a startup (problem definition, key metrics, defensibility) vs what's risky for an established business (partnerships, relationships).

---

## The Customer Factory

A systems view of the business: it's a *factory* that turns leads into happy, paying, referring customers. Five steps (Dave McClure's "AARRR" / Pirate Metrics):

| Stage | Question | Metric |
|---|---|---|
| **Acquisition** | How do leads find us? | Visitors, leads, sign-ups |
| **Activation** | Do they experience the value? | Activated users (defined by you) |
| **Retention** | Do they come back? | DAU, WAU, MAU, retention curves |
| **Revenue** | Do they pay? | MRR, ARPU, gross margin |
| **Referral** | Do they tell others? | Referral rate, NPS, organic growth |

**The Customer Factory is the thing you're really building.** The product is just the machinery inside one or two of these stages. The whole factory must function for the business to work.

### How to use it
1. Draw your customer factory end-to-end.
2. Define each step with explicit definitions (what does "activated" mean for *your* product?).
3. Measure the flow through each step.
4. Find the bottleneck — the step where the largest percentage of users drop off.
5. Focus next 90-day cycle's experiments on the bottleneck.

This is **Theory of Constraints applied to the customer journey**. (Compare with the `kanban` skill's bottleneck thinking.)

---

## The Traction Roadmap

Working *backward* from a future success state to figure out what to do next.

### Steps
1. **Define minimum success criteria** — what is the smallest outcome that makes this initiative "successful"? (e.g., £10M ARR in 5 years.)
2. **Work backward** to year 3, year 1, this quarter — what would have to be true at each point?
3. **Identify the first 90-day milestone** — what's the next concrete thing to test that moves toward the success criteria?

### Why it matters
Most product plans drift forward (each step seems plausible, but the trajectory doesn't add up). The traction roadmap pulls planning backward from a defined outcome — exposing implausibility early.

Also makes it visible *whether you're on track*. If the year-1 milestone said £500k ARR and you're at £20k, the strategy needs to change — not the execution.

---

## The 90-Day Cycle

The unit of execution. Long enough to learn something real; short enough to avoid sunk-cost paralysis.

```
┌────────── 90-DAY CYCLE ──────────┐
│                                  │
│  Week 1-2:  Plan (Sense → Decide)│
│             - Review last cycle  │
│             - Update canvas       │
│             - Pick experiments    │
│                                  │
│  Week 3-12: Act                  │
│             - Run experiments    │
│             - Weekly check-ins   │
│             - Adjust as you learn│
│                                  │
│  Week 13:   Review               │
│             - Did we hit metrics?│
│             - What did we learn? │
│             - Pivot or persevere?│
└──────────────────────────────────┘
```

**Pick 1-3 experiments per cycle, not 10.** Focus.

**Weekly check-ins** keep the cycle alive — if you only review at week 12, you've lost 12 weeks if the direction is wrong.

---

## Customer Interviews

The most important skill in Running Lean. Three types, sequenced:

### 1. Problem Interview
**Purpose:** confirm a problem worth solving exists.
**Talk to:** people who *might* be in your target segment.
**Don't:** pitch your solution. Don't even mention you're building anything.
**Do:** ask about their last experience with the problem.

Script outline (Maurya's "Mom Test"–style):
- "Tell me about the last time you [activity]."
- "What was hardest about that?"
- "Why was that hard?"
- "How did you solve it?"
- "What didn't you like about your current solution?"

**Past behavior > future intentions.** People lie about what they would do; they tell the truth about what they did.

**Exit criterion:** 10-20 interviews where you can predict the next interviewee's answer about the problem. That's the signal you understand the problem.

### 2. Solution Interview
**Purpose:** validate that your proposed solution would solve the problem.
**Talk to:** people from the same segment.
**Show:** mockups, a demo, a prototype — not a product.
**Ask:** "Does this address what you described? What would have to be true for you to pay for / adopt this?"

**Watch for:** verbal agreement vs *committed action*. The acid test is: would they put a small payment / time commitment / signed letter of intent down to be in the early access?

### 3. MVP Interview
**Purpose:** validate the actual MVP delivers on the solution promise.
**Talk to:** users of the MVP.
**Ask:** "What's working? What's not? What's missing? Would you be very disappointed if this went away?"

Sean Ellis's "very disappointed" question is the canonical product/market fit signal.

### Interview best practices (Rob Fitzpatrick / "The Mom Test"; cited heavily by Maurya)
- **Don't pitch.** Listen.
- **Ask about specifics**, not generics ("the last time you" vs "in general").
- **Past behavior**, not future intentions.
- **Commitments and currencies** (time, money, social capital, reputation), not compliments.
- **Talk to ~10-20 per stage**, then re-plan.

---

## The Mafia Offer

The 3rd edition's signature concept. Adapted from "The Godfather" — *an offer they can't refuse*.

### Definition
A Mafia Offer combines:
- **A clear value proposition** that addresses the documented problem.
- **A specific solution** delivered at a specific moment.
- **A price** (or commitment) that makes them say yes.
- **Risk reversal** that lowers their downside (money-back, time-limited, pilot scope).

### Why it matters
Asking "would you use this?" generates polite "yes". Presenting a Mafia Offer requires the customer to put real currency (money, time, identity) on the table. *That* is the signal.

### When to use it
- At the end of Problem/Solution Fit, before building the MVP.
- To pre-sell — get money before you build.
- To filter — separate genuine demand from politeness.

### What a Mafia Offer is NOT
- A pitch.
- A free pilot (no friction = no signal).
- "Would you pay $X someday?" (committed currency only).

Mafia Offers are how you avoid building the most common kind of failed product: the one that everyone said they wanted but nobody actually paid for.

---

## MVPs — Choosing the Right Kind

The MVP's purpose is to **maximize validated learning per unit of effort**. Different questions call for different MVPs.

### Demo MVP
A video / mockup / clickable prototype. No backend.
- **Validates:** desirability. Do people want this enough to sign up for early access / pre-pay?
- **Famous example:** Dropbox's demo video that drove 75,000 sign-ups overnight.

### Landing Page MVP
A page describing the product, with sign-up or pre-order CTA.
- **Validates:** initial demand and conversion at the messaging level.
- **What to measure:** visitor → sign-up conversion.

### Concierge MVP
You manually deliver the service to a small number of customers — no software, just labor.
- **Validates:** the value proposition genuinely delivered.
- **What to measure:** do they keep using it? Refer it?

### Wizard of Oz MVP
The customer sees software; behind the scenes, humans do the work.
- **Validates:** the workflow makes sense and produces the outcome — before building the automation.

### Single-Feature MVP
A minimal version of the actual product, with one feature working.
- **Validates:** the core use case can be served by software.
- **Trap:** "minimum" easily becomes "first version of the full thing".

### How to choose
Match the MVP to the riskiest assumption:
- **"Is there demand?"** → Landing page, demo video.
- **"Will users do the workflow?"** → Concierge or Wizard of Oz.
- **"Can software actually deliver?"** → Single-feature MVP.

Build the cheapest MVP that addresses the *current* riskiest assumption. Don't skip to "real software" because it feels more legitimate. Maurya is unambiguous: software is the most expensive MVP type. Use it last.

---

## Pivots

Maurya enumerates several specific pivot types (drawing on Eric Ries):

| Pivot | What changes |
|---|---|
| **Customer Segment** | Same problem, different customers |
| **Customer Need** | Same customers, different problem |
| **Solution** | Same problem and customer, different solution |
| **Revenue Model** | Same product, different way to charge |
| **Channel** | Same product, different distribution |
| **Technology** | Same value proposition, different tech under it |
| **Engine of Growth** | Different acquisition mechanism |
| **Business Architecture** | High-margin/low-volume vs low-margin/high-volume |

### When to pivot
- 90-day cycle didn't move the metric.
- Customer interviews keep contradicting a canvas assumption.
- The canvas's riskiest assumption has been falsified.

### When NOT to pivot
- The 90-day result is unclear (run another cycle).
- The metric moved but slower than expected (timeline issue, not direction).
- The team is bored (boredom isn't a strategic signal).

**Persevere is the default; pivot is the deliberate exception.** Cumulative learning compounds; constant pivoting loses it.

---

## Common Pitfalls

- **Building before validating.** The most common and most expensive mistake. Customers say nice things to your face; only currency tells the truth.
- **Asking "would you buy this?"** Future intention is not a signal. The Mafia Offer is the antidote.
- **Treating MVP as "first version of the real product".** MVPs are *experiments*. Often the right MVP is a video or a landing page, not code.
- **Skipping the customer factory diagnosis.** Investing engineering effort on the wrong stage (e.g., new features when the bottleneck is activation).
- **Pivoting too soon** — abandoning a thread before the data is in.
- **Pivoting too late** — sunk cost ("we already built it") preventing honest re-evaluation.
- **Using the Lean Canvas as a one-time exercise.** It's a living document. Out of date by week three of any real product.
- **Confusing the three stages.** Doing scale-stage tactics (paid acquisition, growth hacking) before product/market fit. Doing problem-discovery interviews after you have paying customers.
- **Founder/team falls in love with the solution.** The customer cares about their problem. Stay attached to the problem, not the solution.
- **Hiding the metrics.** If the customer factory metrics aren't visible to the team weekly, you're flying blind.

---

## How This Skill Pairs with Others

- **`splitting-user-stories`** — once you know what to build (Running Lean), splitting tells you how to slice it. They sit at different layers of the same problem: what to build vs how to ship it incrementally.
- **`behavior-driven-development`** — once Running Lean validates *what* to build, BDD's three amigos translate it into acceptance criteria.
- **`continuous-delivery`** — fast delivery is what makes 90-day cycles credible. Without CD, "iterate" becomes "quarterly release".
- **`lean-software-development`** — Poppendieck's "decide as late as possible" and "amplify learning" are the engineering-side complement of Running Lean's product-side discipline.
- **`flow-efficiency`** — the customer factory has the same flow dynamics as any other process; Modig's laws apply.
- **`product-development-flow`** — Reinertsen's Cost of Delay applies directly to product decisions (delaying a launch when the market window matters).
- **`toyota-kata`** — the 90-day cycle is a long-cycle kata; the experiments within it are PDCA cycles.
- **`kanban`** — the operational tool for managing the experiment flow.
- **`event-storming`** — once you have product/market fit, event storming maps the system you're building.

---

## A Worked Example

A team has the idea: "we'll build a SaaS tool that automates expense reports for small businesses."

**Naïve plan:** spec the product, hire devs, build in 6 months, launch, sell.

**Running Lean plan:**

*Week 1-2 (Plan):*
- Lean canvas drafted. Customer segment: bookkeepers at companies with 10-50 employees. Problem: monthly expense reconciliation is manual.
- Riskiest assumption: bookkeepers don't actually find this painful enough to pay for. (Could be tolerable.)

*Week 3-6 (Act — problem interviews):*
- 15 bookkeeper interviews. Of those, 11 describe the same pattern: 4-6 hours per month chasing receipts; current solution is spreadsheets + email; one bookkeeper said "I'd pay £200/month for an hour of my life back."
- Problem confirmed.

*Week 7-10 (Act — solution + Mafia Offer):*
- Mockup of a simple receipt-upload + auto-categorization UI.
- Mafia Offer: £49/month, 30-day free trial, set-up call included, money back if not satisfied within 60 days, only 10 founding-customer slots.
- 7 of the 11 follow-up calls take the Mafia Offer.
- Strong signal — and 7 paying pilots before any code is written.

*Week 11-12 (Plan next 90-day cycle):*
- Build the actual MVP. Riskiest next assumption: can the receipt-categorization be accurate enough that the bookkeeper actually saves time?

*Cycle 2 (Build MVP):*
- Concierge MVP for first month: humans do the categorization manually behind the scenes. 7 pilots fully served.
- Cycle ends with: yes, the categorization saves them 4-5 hours/month, AND they're willing to extend. Time to build automation.

*Cycle 3 onward:*
- Now the team builds real software, with paying customers already in place, with concrete data about what to automate, and with the customer factory model defined.

Compare to the naïve plan: the team would have built 6 months of speculative software before discovering that, say, receipts photo'd by phone are too low-quality for OCR to categorize — at which point the entire architecture would need rework. The lean version exposed the right risks first.

---

## Quick Application Checklist

For a new product / feature with uncertain demand:
- [ ] Have I drafted a Lean Canvas, even rough?
- [ ] What is the single riskiest assumption right now?
- [ ] Which stage am I in: Problem/Solution Fit, Product/Market Fit, or Scale?
- [ ] What's the Customer Factory bottleneck?
- [ ] What's the minimum success criteria? Have I worked backward from it?
- [ ] What's the 90-day cycle's goal? Is it focused (≤ 3 experiments)?
- [ ] Am I planning to test demand before building software?

For customer interviews:
- [ ] Am I asking about past behavior, not future intentions?
- [ ] Am I avoiding pitching?
- [ ] Am I seeking currency / commitments, not compliments?
- [ ] Do I have ≥ 10 interviews per segment per stage?

For the Mafia Offer:
- [ ] Does it require real currency (money, signed commitment, time)?
- [ ] Does it have risk reversal?
- [ ] Is it specific (not "would you someday")?

For deciding to pivot or persevere:
- [ ] Has a 90-day cycle's data come in?
- [ ] Did the cycle move the target metric?
- [ ] If not, has the canvas's riskiest assumption been falsified, or is it just slow?
- [ ] Am I attached to the problem (good) or the solution (bad)?

For tracking:
- [ ] Are customer-factory metrics visible weekly?
- [ ] Are we on the Traction Roadmap, or has reality drifted?

---

## Reading

- **Ash Maurya**, *Running Lean: Iterate from Plan A to a Plan That Works*, 3rd edition (O'Reilly, 2022) — the source. The 3rd edition is substantially restructured from the 2nd — buy the new one.
- **Ash Maurya**, *Scaling Lean: Mastering the Key Metrics for Startup Growth* (Portfolio, 2016) — the scale-stage companion.
- **Eric Ries**, *The Lean Startup* (Crown, 2011) — the philosophical foundation (Build-Measure-Learn, validated learning, vanity metrics).
- **Steve Blank**, *The Four Steps to the Epiphany* (Cafepress, 2005) — the customer-development origin Maurya builds on.
- **Steve Blank & Bob Dorf**, *The Startup Owner's Manual* (K&S Ranch, 2012) — encyclopedic customer-development reference.
- **Alex Osterwalder & Yves Pigneur**, *Business Model Generation* (Wiley, 2010) — the original Business Model Canvas Maurya adapted.
- **Rob Fitzpatrick**, *The Mom Test* (2013) — the canonical interview technique book; Maurya quotes it extensively.
- **Dan Olsen**, *The Lean Product Playbook* (Wiley, 2015) — overlapping practical guide.
- **Clayton Christensen et al.**, *Competing Against Luck* (HarperBusiness, 2016) — Jobs to be Done; complements Running Lean's problem definition.
- **Marty Cagan**, *Inspired* (SVPG / Wiley, 2017) — the product-management-org companion; how to organize a company around continuous discovery.
- **Teresa Torres**, *Continuous Discovery Habits* (Product Talk, 2021) — modern customer-interview practice in product organizations.
- **leanstack.com** — Maurya's company; templates, courses, software for Lean Canvas, Customer Factory tracking.
