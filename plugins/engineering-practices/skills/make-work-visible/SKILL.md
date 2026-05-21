---
name: make-work-visible
description: Apply Dominica DeGrandis's "Making Work Visible: Exposing Time Theft to Optimize Work & Flow" (IT Revolution, 2017; 2nd ed 2022) — the practical discipline of surfacing invisible work, managing WIP, and recovering stolen time. Covers the Five Thieves of Time (too much WIP, unknown dependencies, unplanned work, conflicting priorities, neglected work), kanban board design for individuals and teams, demand analysis (business projects vs maintenance vs ad hoc vs intangible work), WIP limit calculation, Personal Kanban, classes of service, the Demand Card, and the operational rituals that keep work visible (daily standup, replenishment, operations review). Use when a team is busy but not shipping, when WIP feels uncontrolled, when work is being lost or forgotten, when setting up a board for the first time, when designing WIP limits, when diagnosing where time is being stolen, when an individual feels overwhelmed and wants Personal Kanban, or when explaining to leadership why "keeping everyone busy" backfires.
---

# Making Work Visible

Apply this skill when work is invisible, WIP is uncontrolled, or a team / individual is busy but not shipping. The goal is to surface the work that exists — *all* of it — and then manage it. You cannot manage what you cannot see.

Based on **Dominica DeGrandis — *Making Work Visible: Exposing Time Theft to Optimize Work & Flow*** (IT Revolution, 2017; 2nd edition 2022).

## Core Philosophy

**Invisible work is unmanageable work.** If it is not on a board, it is not real to the system — but it is still consuming the team's time. The first move is always *make it visible*.

**Time is being stolen — by you, from you.** DeGrandis frames overload not as a personality flaw or a planning failure, but as *theft*. Five distinct thieves are stealing the team's time. Naming them is the first step to catching them.

**WIP is the root cause, not the symptom.** Most "we have too much work" complaints resolve to: *we started too many things*. Cutting WIP is the highest-leverage intervention in almost every team's process.

**Multitasking is a lie.** Humans context-switch; they do not parallelise. Each switch carries a measurable cost. The math says: doing two things sequentially finishes both faster than doing them in parallel.

**Yes, you have time. You are spending it on the wrong things.** The fix is not "work harder" — it is "stop doing the work that does not matter so you can finish the work that does."

**The board is a mirror, not a checklist.** Its job is to show the truth of what the team is doing — including the ugly truth that they are doing nine things and finishing none.

---

## The Five Thieves of Time

DeGrandis's central organising idea. Each thief has distinct symptoms, distinct costs, and distinct countermeasures.

### Thief 1 — Too Much WIP

**Symptom:** every team member has 4+ things in flight; nothing closes; cycle time grows; standups turn into status reporting on stalled work.

**Cost:** context-switching tax (Gerald Weinberg estimates ~20% productivity loss per concurrent project; at 5 projects you have ~25% capacity left). Higher defect rates. Delivery dates slip silently.

**Countermeasure:** WIP limits. Calculate, post them on the board, enforce them. (See "WIP Limits" below.)

### Thief 2 — Unknown Dependencies

**Symptom:** "I was almost done but I had to wait on…" appears in every standup. Work moves forward in fits and starts. Cross-team coordination happens by accident.

**Cost:** waiting time dominates working time. A 2-hour task can take 2 weeks of calendar time. Estimates become fiction.

**Countermeasure:** make dependencies visible on the card and on the board (DeGrandis: red sticky / dependency markers). Surface them at replenishment, not at the moment they bite.

### Thief 3 — Unplanned Work

**Symptom:** the sprint plan disintegrates by Wednesday. Production incidents, urgent customer requests, "quick favors" — none of which were in the plan — eat the week.

**Cost:** planned work slips. The team learns that plans do not matter, which makes future plans worse.

**Countermeasure:** *measure* unplanned work as a percentage of total. If it is over ~25%, you have a capacity problem, not a discipline problem. Reserve capacity for it explicitly — do not pretend it does not exist.

### Thief 4 — Conflicting Priorities

**Symptom:** everything is P1. Two managers ask for opposite things. The team member with the loudest stakeholder wins.

**Cost:** the team optimises for whoever yelled most recently. Strategic work is starved by tactical noise.

**Countermeasure:** *one* ordered list, visible to everyone. Force the priority conversation upstream of the team. If two stakeholders disagree, *they* resolve it before the work enters the board.

### Thief 5 — Neglected Work

**Symptom:** a sticky has been in "Doing" for 14 days and nobody has mentioned it. Tickets without owners. Half-finished initiatives that nobody will admit are dead.

**Cost:** sunk-cost work consumes mental space and sometimes capacity. Old work goes stale and grows expensive to finish.

**Countermeasure:** age tracking on cards (DeGrandis: dot per day in column). Aged cards get a forced decision at replenishment: finish, kill, or escalate. Never silently abandon.

---

## Making Work Visible — Board Design

### Personal Kanban (the minimum viable board)

The simplest useful board, one person, three columns. From Jim Benson & Tonianne DeMaria Barry's *Personal Kanban* (2011), which DeGrandis builds on.

```
┌────────┬──────────┬────────┐
│ To Do  │  Doing   │  Done  │
│        │ (WIP=3)  │        │
├────────┼──────────┼────────┤
│  ...   │   ...    │  ...   │
└────────┴──────────┴────────┘
```

Two rules:
1. **Visualize your work.** Every commitment goes on the board.
2. **Limit your WIP.** Pick a number; do not exceed it.

The discipline is not the board. It is the courage to say "I cannot start this until something finishes."

### Team Board (next step up)

```
┌─────────┬──────────┬──────────┬──────────┬──────────┐
│ Backlog │  Ready   │  Doing   │  Review  │   Done   │
│         │ (WIP=5)  │ (WIP=4)  │ (WIP=2)  │          │
├─────────┼──────────┼──────────┼──────────┼──────────┤
│  ...    │   ...    │   ...    │   ...    │   ...    │
└─────────┴──────────┴──────────┴──────────┴──────────┘
```

Per-column WIP limits. Cards move left-to-right; if Review is full, Doing cannot push — it has to *pull* completed cards through, or stop and help.

### Card Design — what every card shows

DeGrandis's standard card surfaces:
- **What** — a one-line title (outcome, not implementation).
- **Who** — owner (an avatar / initials).
- **Type** — class of service (color or icon: feature / defect / risk / debt).
- **Dependencies** — red markers / linked card IDs.
- **Blockers** — explicit blocker mark with reason and who is unblocking.
- **Age** — a dot per day in current column (or a date sticker).
- **Size** — t-shirt or points, when used.

Cards without owners do not move. Cards without types are invisible to demand analysis. Both are bugs in the system.

---

## Demand Analysis — what kinds of work exist?

DeGrandis's four demand categories. Surface them as **swimlanes** or as card types — the team should be able to *see* the mix at a glance.

| Type | Examples | Predictability |
|---|---|---|
| **Business projects** | New features, strategic initiatives. | High — usually planned. |
| **Maintenance / improvements** | Refactors, debt paydown, dependency upgrades, observability work. | Medium — usually skipped. |
| **Ad hoc / unplanned** | Production incidents, urgent customer requests, "quick favors". | Low by definition. |
| **Intangible work** | Architectural runway, learning, mentoring, knowledge-sharing. | Low — usually invisible. |

### Why this matters

Most teams *only* see business projects. Maintenance gets squeezed; intangible work is treated as "free"; unplanned work appears as drama. The mix shows where time *actually* goes — almost always different from where stakeholders think it goes.

### The Demand Card

DeGrandis: for one or two weeks, *every* piece of work that enters the team gets a card, including ad hoc requests, meetings, and interruptions. At the end, sort by type and count. The picture will surprise people. Use the data to negotiate capacity.

---

## WIP Limits — how to choose them

### Starting heuristics

- **Per person:** `WIP ≤ 2`. One thing in flight + one being unblocked / reviewed.
- **Per team:** `WIP ≤ team_size × 1.5`. A team of 4 → 6 cards in *Doing*.
- **Per column:** lower for slow columns (Review often the tightest), higher for fast ones.

These are starting points. The right answer is empirical: lower until flow improves, raise if the team starves.

### How to enforce

- The limit is **on the column header**, not in the team's head.
- When a column is full, *nobody* pulls a new card into it. Period.
- Hitting a limit is a *signal*, not a failure — usually it surfaces a bottleneck or a missing skill.
- Limits are *team policy*, not management decree. Renegotiate openly.

### When the limit hurts

If the team is starving (people idle, nothing to pull), the limit is too tight *or* the upstream is too slow. Both are visible problems — fix the visible problem, do not paper over by raising the limit.

---

## Classes of Service (when one priority is not enough)

When work has fundamentally different urgency profiles, use classes of service — each with its own swimlane and policies. DeGrandis (after Anderson):

- **Standard** — the default. FIFO-ish.
- **Expedite** — drop everything; one slot, never more than one card.
- **Fixed Date** — has a hard external date. Pull early enough that lead time fits.
- **Intangible** — long-term value (debt, learning). Reserve capacity explicitly; otherwise it never happens.

Each class has explicit policies — when it can be pulled, how it is sequenced, what it preempts. Written on the board.

---

## Operational Rituals

Visibility is wasted without rituals that *use* the board.

### Daily Standup — DeGrandis-style

Walk the board **right to left** (closest to Done first), not by person. Three questions *per card*:
1. What is blocking it?
2. What is needed to move it?
3. Has it aged? (Look at the dots.)

**Skip:** "what I did yesterday / will do today" status round-robin. The board shows that. The standup is for *flow*, not for reporting.

Time-box: 15 minutes, standing.

### Replenishment — pulling new work into Ready

Cadence: usually weekly. Stakeholders + team. The question is "what does the team pull *next*?" — not "what is in the plan?". Look at the data:
- Demand mix (last cycle's actual breakdown).
- Aged cards (force a decision).
- Blocked work (resolve before pulling new).
- Capacity (WIP limits respected).

### Operations Review — broader system health

Cadence: monthly. Look at flow metrics — lead time, cycle time, throughput, % unplanned, % blocked. *Not* individual performance. The board is the team's, not management's scoreboard.

---

## Metrics — measuring what the board shows

DeGrandis is light on the math (the kanban skill covers Little's Law and CFDs in more depth) but emphasises a few:

| Metric | What it tells you | Watch for |
|---|---|---|
| **Cycle time** (days in *Doing* → *Done*) | How fast work clears once started. | Growth = WIP creeping up. |
| **Lead time** (idea → *Done*) | How responsive the team is end-to-end. | Most lead time is usually *queue time*, not *work time*. |
| **Throughput** (cards / week) | How much actually ships. | Flat or declining despite "more work" = WIP problem. |
| **% Unplanned** | How much of the week was firefighting. | > 25% = capacity problem, not discipline problem. |
| **% Blocked** | How much WIP is waiting. | High = dependency problem (Thief 2). |
| **Aged WIP** | Cards over (say) 2× median cycle time. | Each one is Thief 5 in action. |

Pair-up with `flow-efficiency` to talk about resource-vs-flow trade-offs, and `kanban` for the deeper CFD / Little's Law treatment.

---

## Anti-patterns

| Anti-pattern | Why it is bad | How to fix |
|---|---|---|
| **Board with no WIP limits** | Visualises the problem without managing it. Teams feel "agile" while drowning. | Put a number on every active column. Tight first, relax later. |
| **Tickets without types** | Hides the demand mix; maintenance and intangible work disappear. | Force a class on every card. No type = no pull. |
| **Standup as status report** | Wastes 15 min/day per person, surfaces nothing actionable. | Walk the board right-to-left. Flow, blockers, age — not "yesterday I…". |
| **One person = one swimlane** | Optimises for individual utilisation; destroys flow and collaboration. | Lanes are *types of work*, not *people*. People help where the bottleneck is. |
| **Hidden ad hoc work** | "Quick favors" never hit the board → the team looks underloaded. | Every ask gets a card. Even the 10-minute ones. Cap unplanned slots explicitly. |
| **Aged cards left alone** | Sunk-cost work hangs around forever; mental load never drops. | Force a finish/kill/escalate decision when a card crosses the age threshold. |
| **"We will limit WIP next sprint"** | The limit is the intervention. Postponing it is choosing the disease. | Pick a number today. Wrong number > no number. |
| **Board curated by the manager** | Reality gets edited to look good. | The team owns the board. Management reads the board, does not edit it. |
| **Tools before walls** | Jumping to Jira / Trello before the team understands the practice. | Start on a physical wall (or whiteboard / Miro). Tooling encodes whatever practice you already have. |

---

## When this skill applies (vs related skills)

- This skill — **practical, diagnostic, individual + team scale.** Five Thieves of Time, demand analysis, Personal Kanban, ritual design.
- `kanban` — broader Kanban Method (Anderson, Hammarberg & Sundén): foundational principles, CFDs, classes of service in depth, Scrum vs Kanban.
- `flow-efficiency` — Modig & Åhlström's resource-vs-flow framework. Use when explaining *why* the principles work to skeptical leadership.
- `product-development-flow` — Reinertsen's quantitative version. Use when an argument needs hard numbers (cost of delay, queue economics).
- `lean-software-development` — Poppendieck's principle-level lean. Use when the conversation is "what does lean mean for us?", not "how do we run a board next Monday?".

Pick this skill when the answer needs to be **operational by Friday**. Pick the others when the conversation is theoretical.

---

## How to behave when this skill is invoked

1. **Diagnose by Thief.** When a user describes a flow problem ("we keep slipping", "we are drowning", "nothing finishes"), map it to one or more of the Five Thieves before suggesting interventions. Do not jump to solutions.
2. **Make the invisible visible first.** If the user has no board, the first deliverable is a board (even a sketched one) — not a process change.
3. **Ask for the demand mix.** If they have a board but cannot answer "what % of last week was unplanned?", that gap *is* the problem.
4. **Start tight on WIP.** Recommend a starting limit lower than the team's intuition. Lower is almost always right.
5. **Resist tool-first thinking.** If asked "should we use Jira / Linear / Trello?", redirect: the practice precedes the tool. Tooling encodes whichever discipline already exists.
6. **Refuse to optimise for individual utilisation.** If a stakeholder asks "how do I keep everyone 100% busy?", explain why that goal *causes* the slowness they are seeing. Use `flow-efficiency` if a deeper economic argument is needed.

---

## References

- Dominica DeGrandis — *Making Work Visible: Exposing Time Theft to Optimize Work & Flow* (IT Revolution, 1st ed 2017, 2nd ed 2022).
- Jim Benson & Tonianne DeMaria Barry — *Personal Kanban: Mapping Work | Navigating Life* (Modus Cooperandi, 2011) — the Personal Kanban foundation DeGrandis builds on.
- David J. Anderson — *Kanban: Successful Evolutionary Change for Your Technology Business* (Blue Hole Press, 2010) — the Kanban Method DeGrandis operationalises.
- Gerald Weinberg — *Quality Software Management Vol. 1* (1992) — original context-switching cost estimates DeGrandis quotes.

## Related skills

- `kanban` — for deeper Kanban Method foundations and metrics.
- `flow-efficiency` — for the economic argument behind low utilisation.
- `product-development-flow` — for quantitative backing (WSJF, cost of delay, queue math).
- `ticket-writer` — for what *a* card should look like once the board exists.
