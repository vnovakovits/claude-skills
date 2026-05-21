---
name: kanban
description: Apply Kanban as a method for managing knowledge work, based on Marcus Hammarberg & Joakim Sundén's "Kanban in Action" (Manning, 2014) with David J. Anderson's foundational Kanban Method ("Kanban", 2010) and Klaus Leopold's "Practical Kanban" (2017). Covers the four foundational principles, six core practices (visualize, limit WIP, manage flow, make policies explicit, implement feedback loops, improve collaboratively), Kanban-board design, WIP limits and how to set them, flow metrics (lead time, cycle time, throughput, CFD), Little's Law, classes of service, cadences (daily standup, replenishment, delivery planning, service delivery / operations review), Definition of Done, and the contrast with Scrum. Use when setting up a Kanban board, choosing WIP limits, diagnosing flow problems (bottlenecks, blocked work, unstable cycle time), designing classes of service, picking improvement experiments, running improvement cadences, or deciding whether Kanban (vs Scrum, vs Scrumban) fits the team's situation.
---

# Kanban (Hammarberg & Sundén)

Apply this skill when designing or improving a team's workflow, when an existing process is producing erratic delivery or visible bottlenecks, when work-in-progress is undefined or unbounded, when choosing between Kanban / Scrum / Scrumban, or when running a Kanban-style improvement cadence.

## Core Philosophy

**Kanban is a method for managing and improving service delivery, evolutionarily.** It is not a software development lifecycle. It is not a replacement for Scrum. It is a system of principles and practices applied on top of whatever process you already have.

**Start with what you do now.** The first Kanban act is not to redesign the process; it is to **visualize the existing one** and start measuring it. Change comes from the team observing reality, not from imposing a new methodology.

**Stop starting; start finishing.** The most common dysfunction in knowledge work is having too many things in flight. Kanban's mechanism — WIP limits — physically prevents this by making "start another item" impossible until existing items finish.

**Flow over utilization.** Maximizing individual utilization (everyone busy 100% of the time) is the enemy of system throughput. Some slack is required for work to flow without queuing.

**Pull, not push.** Work moves through the system because the next stage pulls it when it has capacity, not because the prior stage pushes it. This is the inversion that makes WIP limits work.

---

## The Four Foundational Principles

(David J. Anderson; cited in Hammarberg & Sundén Ch. 1)

### 1. Start with what you do now
Don't redesign the process. Map the current workflow as it actually exists. Improvement comes after observation.

### 2. Agree to pursue incremental, evolutionary change
No "big bang" transformation. Small, hypothesis-driven changes; keep what works; revert what doesn't.

### 3. Respect the current process, roles, responsibilities, and job titles
Kanban doesn't require role changes. Job titles, reporting lines, and existing ceremonies stay intact at the start. This is why Kanban can be adopted by teams that resist Scrum's role changes.

### 4. Encourage acts of leadership at all levels
The team improves the system. Anyone can propose a change; the board makes problems visible to everyone.

These four are the reason Kanban "feels lighter" than other methods at adoption — it doesn't ask you to change anything except how you see the work.

---

## The Six Core Practices

### 1. Visualize the work
Make the invisible visible. A physical or digital board shows every work item, where it is in the workflow, who is working on it, and how it is moving (or not).

### 2. Limit work in progress (WIP)
Cap the number of items allowed in each column. The cap is *the policy*; when it's full, you can't start another item until one leaves.

### 3. Manage flow
Track how work moves through the system. Watch for queueing, blocking, and variability. The goal is *smooth, predictable flow*, not maximum speed.

### 4. Make policies explicit
Definition of "Ready", "Done", how items are selected, how to handle expedites, who pulls what — all written on the board, all visible. Implicit policies are fertile ground for disagreement.

### 5. Implement feedback loops
Cadences (see below) — short, frequent meetings that look at the work and the system, not at people.

### 6. Improve collaboratively, evolve experimentally
Use models (Theory of Constraints, Lean, queuing theory) and the scientific method to test changes. Hypothesis → experiment → measure → keep or revert.

---

## The Kanban Board

The single most important Kanban artifact.

### Anatomy

```
┌────────────┬─────────────────┬──────────────┬──────────────┬──────────┐
│   Backlog  │  Ready / Pull   │ In Progress  │  Done (col)  │ Released │
│            │       (5)       │     (3)      │     (3)      │          │
├────────────┼─────────────────┼──────────────┼──────────────┼──────────┤
│  📄 📄 📄  │   📄 📄 📄      │   📄 📄      │   📄         │  📄 📄    │
│  📄 📄 📄  │                 │   📄         │              │          │
└────────────┴─────────────────┴──────────────┴──────────────┴──────────┘
                  ^^^ WIP limit            ^^^ WIP limit
```

### What to put on a card
- A short, intent-revealing title
- The work item type (feature / bug / task / spike)
- The class of service (see below)
- Date entered the system (for lead-time tracking)
- Date entered each column (for cycle-time per stage)
- Blocked? — bright sticker / flag
- Who's working on it (avatar)
- Linked external reference (ticket, doc)

### How to design the columns
- **Start by mirroring the actual workflow.** Don't invent new columns to match a methodology.
- Common shape for software: Backlog → Ready → In Progress (often split into Dev / Review / Test) → Done → Released.
- **Each column should represent a distinct *handoff* or *queue*.** If two columns have the same handoff, merge them.
- **Split "In Progress" into Doing / Done sub-columns** when handoffs cause queuing. The "Done" half is the queue waiting to be pulled by the next stage. This is often where the biggest bottleneck lives.

### Where to put the board
- Physical board > digital board for co-located teams. The radiated information density is irreplaceable.
- Digital board (Trello, Jira, Linear, GitHub Projects) for distributed teams.
- Hybrid: digital source-of-truth + always-on monitor showing it.

**The single most common mistake**: putting up a digital board (often imposed by management) without the team treating it as their source of truth. The board must reflect reality continuously — if it lags behind, it's worse than no board.

---

## WIP Limits — the Heart of Kanban

The mechanism that converts a board into a *system*. Without WIP limits, you have a visualization tool but not a Kanban method.

### What a WIP limit is
A maximum number of work items allowed in a column (or set of columns, or per-person). When the limit is reached, **no new item enters** until one leaves.

### Why WIP limits work
1. **They surface bottlenecks.** When the WIP limit on "Code Review" is hit, everyone sees the queue. The bottleneck is now a team problem, not a hidden one.
2. **They force focus.** Engineers can't context-switch when they can't pull a new item.
3. **They reduce cycle time.** Little's Law (below) tells us cycle time = WIP / throughput. Reducing WIP reduces cycle time at constant throughput.
4. **They encourage swarming.** When a downstream column is blocked, the upstream team has nothing to start — they help unblock the downstream work.

### How to set initial WIP limits

There's no universal formula. Heuristics:
- **Per-column:** typically 1.5× to 2× the number of people who work in that column. Team of 4 developers → "In Progress" limit of 6-8.
- **Total board WIP:** start with `N people × 1.5` and reduce.
- **Per-person:** at most 2 items per person, ever. Often 1.

### How to adjust
- Watch the board for a week. Where does work accumulate?
- Where it accumulates → reduce that column's WIP limit *if* the accumulation is the team holding things, or expand capacity *if* it's a downstream constraint.
- Where work flies through → consider tightening to expose hidden queueing.
- Lower beats higher. Painfully low WIP limits expose dysfunction; comfortably high ones hide it.

### Common WIP-limit failure modes
- **No WIP limits.** "Kanban with a board but no limits" — not Kanban.
- **Limits set so high they never bite.** Comfort over learning. No real signal.
- **Limits per individual but not per column.** Misses the system view.
- **Cheating: starting work without putting it on the board.** Defeats the purpose. Cultural fix, not process fix.
- **Expedite items count against the limit (or don't, deliberately).** Decide and write it as policy.

---

## Flow, Bottlenecks, and the Theory of Constraints

Borrowed from Eli Goldratt's *The Goal*; Hammarberg & Sundén apply it to knowledge work.

### Find the bottleneck
The bottleneck is the slowest stage in the workflow. It is the **only** stage whose speed determines the total throughput of the system. Speed up anything else, and you simply move work to the bottleneck faster (and the bottleneck queue grows).

How to spot it:
- WIP accumulates upstream of it.
- Work waits in its "ready / in queue" position.
- The bottleneck is constantly utilized; everywhere else has slack.

### The Five Focusing Steps (TOC)
1. **Identify** the bottleneck.
2. **Exploit** it — get the absolute most out of the current bottleneck (no idle time, no rework feeding it).
3. **Subordinate** everything else to the bottleneck (other stages run at the bottleneck's pace; reducing their queues; helping them).
4. **Elevate** the bottleneck (add capacity if exploiting isn't enough).
5. **Repeat** — once you fix one, another becomes the bottleneck.

In software teams, the bottleneck is often **code review**, **test environments**, or **deployment**. Sometimes it's a single specialist (DBA, security review). Each case has its own fix.

---

## Flow Metrics

Kanban's quantitative half. Without metrics, you can visualize the work but you can't see the system.

### Lead time
Time from when a customer **requests** something to when they **receive** it. The customer-experienced time.

### Cycle time
Time from when work **starts** to when it **completes** in the team's workflow. The team-experienced time.

These differ by the time work spends in the backlog (the "request → start" gap).

**Cycle time is the more actionable metric.** It is also the metric that responds to WIP-limit changes.

### Throughput
Number of items completed per unit time. "Stories per week", "features per month".

### Little's Law
$$ \text{Cycle time} = \frac{\text{Work in progress}}{\text{Throughput}} $$

The mathematical foundation of Kanban. It tells you: at constant throughput, **reducing WIP linearly reduces cycle time**. This is why WIP limits matter.

### Cumulative Flow Diagram (CFD)
A stacked area chart showing the count of items in each column over time. The single most informative Kanban chart.

```
items
  |  ┌── released
  |  ├── done
  |  ├── in progress
  |  ├── ready
  |  └── backlog
  └─────────────────────── time
```

What it reveals:
- **Widening bands** = WIP growing in that column = bottleneck or scope creep
- **Flat bands** = stage producing no output
- **Horizontal distance between two lines** = cycle time of items between those stages
- **Slope of the top line** = throughput
- **A widening gap between input and output** = WIP growing; cycle time will rise

A CFD is *the* dashboard. If you can have only one chart, have this one.

### Other useful charts
- **Cycle-time scatter plot** — every completed item plotted by completion date vs cycle time. Reveals variability and outliers. Lets you state SLEs as percentiles.
- **Run charts of throughput** — items completed per week.
- **Aging-WIP chart** — for each in-flight item, how long has it been in progress? Surfaces stale work.

### Service Level Expectation (SLE)
Cycle-time stated as a percentile: "We complete 85% of standard items within 8 days." Set from historical data, used as a forecast (not a deadline).

---

## Classes of Service

Different work types deserve different policies. Kanban makes the categories explicit.

### Standard
The default. Pull in FIFO order. Standard SLE applies (e.g., "85% done in 8 days").

### Fixed delivery date
Has a specific deadline that matters (regulatory deadline, contract milestone). Tracked separately; pulled earlier than its SLE would normally require, so it lands on time with margin.

### Expedite
Urgent. **Reserved lane** on the board. Bypasses normal pull order. Often counts against WIP limits as 1 expedite item (some teams reserve 1 expedite slot outside the main WIP limit). **Limit one in flight at a time.**

### Intangible
No clear cost-of-delay yet, but important. Technical debt cleanup, learning, experiments. Reserved capacity (often a quota) to ensure these happen.

### How to use classes of service
- **Make them visible** on the card (color, sticker, icon).
- **Make the policies explicit** for each class.
- **Track them separately** in metrics.
- **Don't over-classify.** Three classes is usually plenty; some teams use only Standard + Expedite.

The point is to handle different work types differently *on purpose*, not to abandon flow.

---

## Cadences — the Rhythms of Kanban

Kanban replaces Scrum's sprint with continuous flow plus a set of recurring meetings. Hammarberg & Sundén list seven (Anderson's full set); most teams adopt 3-4.

### Daily Standup (daily, 5–15 min)
Around the board. Walk right-to-left (start from "Done" — closest to delivery — and work back). For each item:
- Is it blocked?
- Does it need help?
- Who's picking up the next item?

**Talk about the work, not the worker.** Not "what did I do yesterday" — that's status reporting. The board IS the status.

### Replenishment Meeting (weekly or per-pull-event, 30 min)
Refill the "Ready" column from the backlog. Stakeholders + team. Decide:
- Which items move from backlog to ready (in priority/cost-of-delay order).
- What classes of service apply.

### Delivery Planning Meeting (per release event)
What's about to be delivered? Confirm scope, communicate to stakeholders.

### Service Delivery Review (weekly or biweekly, 30–60 min)
Look at metrics. CFD, cycle-time chart, throughput. **Are we meeting our SLE?** Are bottlenecks shifting?

### Operations Review (monthly)
Cross-service. Look at multiple teams' boards and metrics together; coordinate priorities and dependencies.

### Risk Review (monthly or quarterly)
Look at blocked items, aging items, recurring problems. Risk register.

### Strategy Review (quarterly or as needed)
Are we serving the right customers? Should the system itself change?

**Most teams start with: Daily Standup + Replenishment + Service Delivery Review.** Add others when the team has bandwidth and a real reason.

---

## Definition of Done (and "Done" for each column)

Each column has its own Definition of Done. The card cannot move out of a column until *that* column's DoD is met.

Examples:
- **"In Dev — Done":** code committed; unit tests pass; PR opened; self-review complete.
- **"In Review — Done":** at least one approving review; CI green; no open feedback.
- **"In Test — Done":** test cases executed; defects either fixed or accepted as known issues.
- **"Released — Done":** in production; verified working; user notified if applicable.

### Why this matters
Without per-column DoD, "Done" becomes whatever feels finished — which leads to items oscillating between columns, partial work, and rework.

DoD per column is one of the most underused Kanban tools.

---

## Improvement (Kaizen)

Improvement is not a separate activity from Kanban; it IS Kanban. The board makes problems visible; the team experiments with fixes.

### The improvement loop
1. **Observe** — look at the board, the metrics, the cadences. What is the system doing?
2. **Hypothesize** — what would change if we did X?
3. **Experiment** — try X for a defined period (a week, two weeks).
4. **Measure** — did the metric change in the expected direction?
5. **Keep or revert** — based on evidence, not preference.

### Sources of improvement signals
- A column's WIP limit is constantly hit → bottleneck candidate.
- Items spend long stretches "in review" or "in test" → handoff/queue problem.
- A class-of-service category routinely misses its SLE → policy or capacity mismatch.
- Same blocked items recurring → systemic problem worth investigating.
- Throughput declining → something is wrong somewhere.

### A3 problem solving
A one-page structure for solving a recurring problem:
- Background — why does this matter?
- Current condition — what's actually happening (with data)?
- Goal — what would good look like?
- Root-cause analysis — 5 Whys / Ishikawa.
- Countermeasures — what to try.
- Plan — when and by whom.
- Follow-up — did it work?

Borrowed from Toyota. Useful for problems that the daily standup can't fix.

---

## Common Pitfalls

- **"We have a board, so we're doing Kanban."** No. Without WIP limits, explicit policies, and cadences, you have a visualization tool.
- **WIP limits exist but are too high to bite.** No improvement signal; the system runs as it would without them.
- **No flow metrics.** Without measurement, you can't tell whether changes help.
- **Pushing work into "In Progress" because the assignee "has time"**, ignoring downstream capacity. Defeats pull. Items pile up in the next stage.
- **No class of service distinction; everything urgent.** When everything is "expedite", nothing is.
- **Daily standup as status reporting.** Walk the board; talk about items, not people; surface blockers.
- **Treating the backlog as in-flight work.** Backlog is options; items in flight are commitments.
- **Confusing Kanban with "no planning".** Kanban replaces sprint planning with continuous prioritization (replenishment) and explicit cadences. Less episodic, not less planned.
- **Cargo-culting boards from other teams.** Mirror your workflow, not theirs.
- **Stopping at "visualize" and never reaching "limit WIP" or "manage flow".** The most common arrested-adoption pattern. The board becomes wallpaper.

---

## Kanban vs Scrum vs Scrumban

| | Scrum | Kanban | Scrumban |
|---|---|---|---|
| Time-boxed iterations | Yes (sprints) | No (continuous flow) | Optional |
| Roles | PO, SM, Devs | None mandated | Optional |
| Commitment | Sprint goal | None — pull as capacity allows | Mixed |
| Planning cadence | Sprint planning | Replenishment | Replenishment + lighter planning |
| WIP control | Implicit (sprint scope) | Explicit limits | Explicit limits |
| Metrics | Velocity | Cycle time, throughput, CFD | Mix |
| Change resistance | "We can't change job titles" → painful | Low (start with what you have) | Low |
| Best for | Product teams with predictable scope, batched release | Support, ops, maintenance, support-heavy workflows, mixed work types | Teams transitioning from Scrum to flow |

**When to choose Kanban:**
- Work arrives unpredictably (support, ops).
- Mixed work types (features + bugs + spikes + emergencies).
- Scrum's role changes / sprint structure don't fit the team.
- Continuous delivery (each item ships when done).
- Existing process you want to *evolve* without redesigning.

**When to choose Scrum:**
- Predictable, batch-style work where sprint cadence helps focus.
- Need for time-boxed commitments (often for organizational reasons).
- Team needs the structure to learn agile basics.

**Scrumban** combines: Scrum's cadence and roles + Kanban's WIP limits and flow metrics. Often a good middle ground for teams transitioning.

---

## When Kanban Is Not the Right Fit

Be honest. Kanban won't help when:
- Work items are huge and can't be sliced. (See the `splitting-user-stories` skill.)
- Team isn't allowed to limit WIP (e.g., a manager keeps "assigning" work). Kanban requires team authority over its WIP.
- The bottleneck is outside the team's control and won't be addressed (e.g., a single shared specialist that nobody will reorganize). Kanban will surface it but can't fix it alone.
- There's no commitment to make policies explicit and write them down.

---

## How Kanban Pairs with Other Skills

- **`splitting-user-stories`** — small items flow; large items clog the board. Kanban's metrics expose oversized items quickly. Skill is the right partner.
- **`continuous-delivery`** — natural fit. Each item completes and ships independently; CD provides the deployment side.
- **`behavior-driven-development`** — BDD scenarios drive the work items; Kanban manages their flow.
- **`test-driven-development`** — the inner loop. Kanban governs the outer cycle of work; TDD governs the inside of each item.
- **`observability`** — service-delivery review uses operational metrics alongside flow metrics. Cycle time is to delivery what latency is to production.
- **`architecture-decision-records`** — significant decisions made during improvement cycles deserve ADRs.

---

## A Worked Kanban Adoption Sketch

A team of 6 engineers, mixed work (features + bugs + support tickets), no formal method today. The adoption arc:

**Week 1 — Visualize.**
- Map the actual workflow: Backlog → Ready → In Dev → In Review → In Test → Done.
- Put cards on a board for every in-flight item. Be honest about how many.
- Daily standup walking the board.

**Week 2-3 — Limit WIP.**
- Count current WIP. Probably surprising (e.g., 15 items in flight across 6 people).
- Set initial WIP limits: In Dev = 6, In Review = 3, In Test = 3.
- Decide what to do when a limit is hit (typically: swarm the bottleneck).
- Replenishment meeting weekly.

**Week 4-6 — Make policies explicit.**
- Definition of Done per column.
- How to handle expedites (one expedite at a time, separate lane).
- Class of service stickers (Standard / Expedite / Intangible).

**Week 6 onward — Measure & improve.**
- CFD on the wall, updated daily.
- Service delivery review weekly: how's our SLE? Are bottlenecks moving?
- Pick one improvement experiment per cycle. Hypothesis → try → measure → keep or revert.

By month three, the team has data, an evolving process, and visible reasons for each decision.

---

## Quick Application Checklist

For a new Kanban adoption:
- [ ] Have we visualized the *actual* workflow (not an idealized one)?
- [ ] Does every in-flight item appear on the board?
- [ ] Are columns set per *handoff or queue*, not per role?
- [ ] Have WIP limits been set per column?
- [ ] Have we written down per-column Definition of Done?
- [ ] Have we agreed on at least daily standup + replenishment cadence?
- [ ] Are we capturing cycle time / throughput data, even informally?

For an existing Kanban system:
- [ ] Are WIP limits low enough to bite?
- [ ] Do we routinely look at the CFD?
- [ ] Is the bottleneck identifiable? Are we exploiting / subordinating / elevating it?
- [ ] Are classes of service explicit, or has "everything is urgent" set in?
- [ ] Have we run an improvement experiment recently? Did we measure its outcome?
- [ ] Has the daily standup become status reporting? (Refocus on the work.)
- [ ] Are aging items being addressed, or has the board accumulated stale cards?

When something feels wrong:
- [ ] Has cycle time risen? → look for WIP increase.
- [ ] Has throughput dropped? → look for bottleneck shift.
- [ ] Is the board out of sync with reality? → cultural / discipline issue, not process.

---

## Reading

- **Marcus Hammarberg & Joakim Sundén**, *Kanban in Action* (Manning, 2014) — the canonical practical text. Story-driven, hands-on, accessible.
- **David J. Anderson**, *Kanban: Successful Evolutionary Change for Your Technology Business* (2010) — the foundational text; defines the Kanban Method, the four principles, the six practices.
- **Klaus Leopold**, *Practical Kanban: From Team Focus to Creating Value* (2017) — complements Hammarberg & Sundén with deeper Flight Levels (team / service / portfolio scaling) thinking.
- **Klaus Leopold**, *Rethinking Agile: Why Agile Teams Have Nothing To Do With Business Agility* (2018) — adjacent, on why team-level agile fails to scale without flow at the service level.
- **Daniel Vacanti**, *Actionable Agile Metrics for Predictability* (2015) — deep dive on cycle-time distributions, throughput, and forecasting. The serious metrics companion.
- **Daniel Vacanti**, *When Will It Be Done?* (2020) — forecasting from flow metrics; replacing story-point estimation.
- **Eli Goldratt**, *The Goal* (1984) — the novel that introduced the Theory of Constraints. Reads in an evening; transformative.
- **Don Reinertsen**, *The Principles of Product Development Flow* (2009) — the rigorous theoretical foundation (queuing theory, cost of delay, economic decision frameworks).
- **Taiichi Ohno**, *Toyota Production System* (1988) — Kanban's origin in lean manufacturing.
- **Henrik Kniberg**, *Kanban and Scrum: Making the Most of Both* (2010, free) — the canonical Kanban-vs-Scrum and Scrumban comparison.
