---
name: to-tickets
description: Break a plan, spec, grilling summary or conversation into a set of tracer-bullet tickets — thin, end-to-end slices that each work and can be demonstrated on their own — with explicit "blocked by" edges, so the work forms a dependency graph and anyone can pick up a ticket whose blockers are done. Covers vertical vs horizontal slicing (Hunt & Thomas's tracer bullets, Cockburn's Elephant Carpaccio, INVEST), prefactoring first ("make the change easy, then make the easy change"), sequencing a wide refactor as expand-migrate-contract (Parallel Change), sizing a ticket to one session and one pull request, confirming the breakdown with the user, and publishing to a tracker with native blocking links. Use when a piece of work is too big for one PR, when asked to split a plan or epic into tickets, to plan the order of work, or to find what can run in parallel.
---

# To Tickets

Apply this skill when a piece of work is decided but too big to build in one go: a spec, an epic, a grilling summary, a design that spans several layers. The output is a set of tickets, each a **tracer bullet** — a narrow slice that runs through every layer it needs and works on its own — and each naming the tickets that **block** it. Together they form a dependency graph; the **frontier** is every ticket whose blockers are done, and that is what can be picked up next, in parallel.

Use `ticket-writer` for the anatomy of a single ticket; this skill is about the set.

## Core Philosophy

**Slice vertically, not horizontally.** A horizontal slice ("all the database changes", then "all the API", then "all the UI") delivers nothing until the last slice lands, and hides integration problems until then. A vertical slice cuts a thin path through schema, logic, API, UI and tests, so each one can be demonstrated and verified on its own.

**Tracer bullets find the target early.** Hunt and Thomas: build a thin version that connects end to end first, then thicken it. The first ticket should prove the path; later tickets widen it.

**Dependencies are edges, not order.** A numbered list implies a sequence that may not exist. Name for each ticket exactly which tickets must finish first. Everything else can run in parallel.

**Make the change easy, then make the easy change** (Beck). If the code resists the change, the first tickets are prefactorings that reshape it without changing behaviour. They block the feature tickets.

**Size to one sitting.** A ticket should fit in one working session and one reviewable pull request. If it cannot be described in a paragraph and a handful of acceptance criteria, split it.

---

## The Procedure

### 1. Gather

Work from what exists: the spec, the grilling summary, the ticket thread, the conversation. Read the code in the area: which modules change, what already exists, where the seams are. Use the project's domain language (its glossary, if there is one) in every title.

### 2. Find the prefactorings

Look for changes that would make the feature easy: an extraction, a renamed concept, a seam a test needs, a dependency to break. Each is its own ticket, with no behaviour change, ahead of the tickets it unblocks (see `tidy-first` and `working-effectively-with-legacy-code`).

### 3. Draft the slices

Start with the thinnest slice that exercises the whole path. Then add slices, each making one more behaviour work end to end. Ways to cut thinner (Lawrence's story-splitting patterns, Cockburn's Elephant Carpaccio):

- one variation of a business rule at a time;
- the happy path first, then each failure path;
- one data type, channel or platform at a time;
- simple input before complex input;
- a manual or hard-coded step first, automated later;
- the read path before the write path, or the reverse.

Check each slice against INVEST: Independent where possible, Negotiable, Valuable on its own, Estimable, Small, Testable.

### 4. Wire the edges

For each ticket, list the tickets that must finish before it can start, and only those. A ticket with no blockers can start now. Check:

- every edge is a real dependency (it needs that code, that data, that decision), not just "it felt earlier";
- there are no cycles;
- the frontier at the start is as wide as the work allows.

### 5. Sequence wide refactors as expand–migrate–contract

Some changes cannot be sliced vertically: renaming a column, retyping a shared type, replacing a library used everywhere. One edit breaks hundreds of call sites at once. Use Parallel Change instead:

1. **Expand** — add the new form beside the old; nothing breaks.
2. **Migrate** — move call sites over in batches sized by blast radius (per module, per directory), each batch its own ticket blocked by the expand; the build stays green because the old form still exists.
3. **Contract** — delete the old form, in a ticket blocked by every migrate batch.

For data, the same shape applies: add the new column, dual-write, backfill, switch reads, stop writing the old, drop it.

### 6. Confirm with the user

Present the breakdown before publishing:

```markdown
| # | Title | Blocked by | What it makes work |
| - | ----- | ---------- | ------------------ |
| 1 | Extract the pricing rules into one module | — | No behaviour change; unblocks 3 and 4 |
| 2 | Customer can see their order history | — | The list, newest first, one page |
| 3 | Discount applies to one item type | 1 | ... |
```

Ask: is the granularity right (too coarse, too fine)? Is every blocking edge real? Should any tickets merge or split? Iterate until the user approves.

### 7. Publish

Write each ticket with `ticket-writer`'s structure: the outcome from the user's perspective, testable acceptance criteria, and the blockers. Avoid file paths and code in the ticket body; they go stale. (An exception is a snippet that encodes a decision more precisely than prose, such as a state machine or a schema from a prototype.)

- **A tracker with native dependencies** (Linear "blocked by", Jira "is blocked by", GitHub sub-issues) — create the tickets in dependency order so blockers have ids first, then add the blocking links in a second pass. Native links show the frontier in the tracker's own views.
- **No tracker** — one Markdown file per ticket, numbered blockers-first, each with a "Blocked by" line.

If the work came from a parent issue, link each ticket to it as a child. Do not close or edit the parent.

---

## Ticket Template

```markdown
# <Title: the behaviour this ticket makes work>

**Outcome:** what a user or caller can do once this is done.

**Blocked by:** <ticket ids>, or "none — can start now".

**Acceptance criteria:**
- [ ] <observable, testable criterion>
- [ ] <the failure path this slice covers, if any>

**Notes:** <decisions it depends on, links to the spec or ADR>
```

---

## Anti-patterns

- **Layer tickets.** "Backend for X", "frontend for X": nothing works until both land, and the integration risk sits at the end.
- **A list pretending to be a graph.** Numbering tickets 1 to 12 with no edges forces a serial order that wastes parallelism and hides the real dependencies.
- **Edges by feel.** Marking a ticket blocked because it "comes later" shrinks the frontier for no reason.
- **The everything ticket.** One ticket that needs several sessions and an unreviewable PR.
- **Prefactoring buried in a feature ticket.** The reviewer cannot tell structure changes from behaviour changes.
- **A wide refactor as one ticket.** It cannot land green; sequence it as expand–migrate–contract.
- **Solution-only tickets.** Steps and file paths instead of an outcome; they rot and constrain the person doing the work.
- **Publishing without confirming.** The user knows dependencies and priorities the code does not show.

---

## How This Skill Pairs with Others

- **grilling** — settles the decisions first; its summary is this skill's input.
- **ticket-writer** — the structure and quality bar for each ticket.
- **splitting-user-stories** — the catalogue of ways to cut a story thinner.
- **user-story-mapping** — when the question is which slices make the first release.
- **example-mapping** — turns a slice's rules into acceptance criteria.
- **tidy-first** and **refactoring** — the prefactoring tickets.
- **pr-writer** — each ticket should become one reviewable pull request.

---

## Quick Application Checklist

- [ ] Does every ticket cut through every layer it needs, and work on its own?
- [ ] Is the first ticket the thinnest end-to-end path?
- [ ] Are prefactorings separate tickets, ahead of what they unblock?
- [ ] Does each ticket name only the blockers it really depends on, with no cycles?
- [ ] Is a wide refactor sequenced as expand, migrate in batches, contract?
- [ ] Does each ticket fit one session and one reviewable PR?
- [ ] Did the user confirm the granularity and the edges before publishing?
- [ ] Are blocking links native in the tracker, created after the tickets exist?

---

## Reading

- **Andrew Hunt & David Thomas**, *The Pragmatic Programmer* (20th anniversary ed., 2019), "Tracer Bullets".
- **Alistair Cockburn**, the Elephant Carpaccio exercise, and **Henrik Kniberg & Alistair Cockburn**, *Elephant Carpaccio Facilitation Guide* (2013) — slicing a feature into very thin, valuable pieces.
- **Bill Wake**, "INVEST in Good Stories, and SMART Tasks" (xp123.com, 2003).
- **Richard Lawrence**, "How to Split a User Story" (Humanizing Work) — the splitting patterns.
- **Kent Beck**, *Tidy First?* (O'Reilly, 2023) — "make the change easy, then make the easy change".
- **Danilo Sato**, "ParallelChange" (martinfowler.com, 2014) — expand, migrate, contract.
- **Matt Pocock**, `to-tickets` skill (github.com/mattpocock/skills) — tracer-bullet tickets with blocking edges and the frontier.
