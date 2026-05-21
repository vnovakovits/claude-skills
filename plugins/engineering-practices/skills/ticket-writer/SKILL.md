---
name: ticket-writer
description: Draft, write, structure, or improve engineering tickets — user stories, bug reports, spikes, feature requests — for any tracker (Jira, Linear, GitHub Issues, Shortcut, Asana). Enforces a problem-first structure (outcome → context → constraints → acceptance criteria → dependencies → open questions) drawn from Daniel Starling's "Anatomy of a Software Ticket", Bill Wake's INVEST and SMART, and Marty Cagan / SVPG's "Empowered Product Teams". Actively rejects the standard anti-patterns: prescribed solutions / "files to change", missing outcome, untestable acceptance criteria, PM-supplied estimates, hidden blockers, vague AC. Use when drafting a new ticket, turning a problem into a Jira/Linear/GitHub issue, filing a bug report, scoping a spike, reviewing or rewriting an existing ticket, or improving a story before it enters Ready.
---

# Ticket Writer

Apply this skill when writing or reviewing any engineering ticket — story, bug, spike, or feature request — for any tracker. The goal is a ticket that gives an *empowered team* a problem worth solving and the constraints that bound it, then trusts the team to find the solution.

## Core Philosophy

**Problems, not features.** Empowered teams are "given problems to solve rather than features to build" (Marty Cagan, SVPG). A good ticket describes the outcome and the constraints — not the implementation.

**Outcome before instructions.** Every ticket leads with one sentence a non-engineer can read: the business result we'll know we achieved. If you can't write the outcome, the work isn't ready to be a ticket.

**Acceptance criteria are testable, or they're not criteria.** "Works correctly" / "is fast" / "looks good" are opinions. Replace with concrete thresholds, examples, and yes/no checks.

**A ticket is a placeholder for a conversation, not a contract.** Negotiable. Refined together. The detail belongs on the *problem and examples*, not on which files to edit (Bill Wake — INVEST: Negotiable).

**The team owns the estimate.** Estimates supplied by the requester anchor the team and erode trust. If an estimate exists at *Ready* time, the team wrote it.

**Hidden dependencies kill flow.** A ticket with unresolved blockers should not be *Ready* — it will stall mid-sprint. Surface them early, name them, schedule them.

## When to use this skill

Trigger when the user:
- Asks to draft, write, or "turn into a ticket" anything that smells like work — features, bugs, spikes, support requests.
- Pastes an existing ticket and asks for review, feedback, or a rewrite.
- Mentions Jira, Linear, GitHub Issues, Shortcut, Asana, or any other tracker by name.
- Says "let's file this" / "let's track this" / "how should I word this story" / "draft a Jira for X".

Do not trigger for:
- ADRs — use `architecture-decision-records`.
- Story splitting itself — use `splitting-user-stories` (the two pair well).
- BDD scenario writing — use `behavior-driven-development`.

## Two Ticket Shapes (plus a Spike)

The template below has two top-level shapes — **Story** (new feature / change) and **Bug** — plus an optional **Spike** shape for time-boxed investigation. Pick the shape that fits the work; do not force a bug into a story shape or vice versa.

---

## A. User Story / Feature Change

```markdown
### [Title — outcome-shaped, not implementation-shaped]

**Outcome** (1 sentence, non-engineer-readable)
The business result we will know we achieved.

**Problem / Context — why now**
What currently happens. What is missing or broken. Why it matters now.
Quote real data: customer reports, metrics, support volume, lost revenue.

**Constraints — Do Not** (keep this section even when empty)
- Hard limits the team must respect: contracts to honour, schemas not to break,
  flows not to regress, regulatory boundaries.

**Acceptance Criteria** (testable yes/no)
- [ ] Concrete, checkable condition.
- [ ] Another concrete, checkable condition.
- [ ] Include examples / sample data where ambiguity is possible.

**Dependencies & Blockers**
- External tickets, services, or decisions that must land first. Name them.
- The ticket does not enter Ready until these are resolved.

**Open Questions** (each with a named owner)
- Question? — *owner: @name, due: YYYY-MM-DD*

**(Optional) Engineering Pre-Investigation**
- Things engineering should scout before estimating.
- NOT a list of files to edit.
```

### Title rules

- Names the **outcome** or the **user behaviour**, not the implementation.
- *Good:* "3PL can resend onboarding email without contacting support"
- *Bad:* "Add resend button to admin panel"

### Outcome rules

- One sentence. Readable by a non-engineer.
- States the *result*, not the activity. ("Customers unblock themselves" — not "We build a resend feature".)
- If you find yourself describing *how*, you have drifted. Re-anchor on *what* and *why*.

### Problem / Context rules

- Quote real data when you can: support ticket counts, metric deltas, customer names, dates.
- No hypotheticals. "Some customers might…" is a hypothesis, not a problem — convert it into a spike instead.
- Link to incidents, dashboards, or recorded conversations.

### Constraints rules

- This is the "Do Not" section. Always include it — even when empty (write "None known.").
- Examples: API contracts, schema stability, security boundaries, backwards-compatibility requirements, regulatory limits.
- Constraints belong here, not buried inside AC.

### Acceptance Criteria rules

The AC define **done**. They are the most-misused section of any ticket — usually written as system clicks or test scripts instead of behavioural rules. The principles below are the ones that matter most. (For deeper Gherkin / scenario craft, defer to `behavior-driven-development`.)

#### Rule vs example (Example Mapping)

An AC is a **rule** — an invariant statement of behaviour. A *scenario* is a concrete example that illustrates a rule. Most teams collapse the two and end up with neither.

Matt Wynne's Example Mapping makes the distinction concrete:

- 🟡 **Story** — the outcome.
- 🔵 **Rules** — the actual acceptance criteria (3–7 per story).
- 🟢 **Examples** — Given/When/Then cases nested under each rule (1–3 per rule).
- 🔴 **Open questions** — blockers; must be resolved before *Ready*.

> *Rule:* Customs identifiers swap with the parties; IOSS does not carry forward.
>
> *Example:* Given a Manchester → Berlin shipment with sender EORI `GB123`, receiver EORI `DE456`, and IOSS `IM7700`, when reversed, the new shipment has sender EORI `DE456`, receiver EORI `GB123`, and no IOSS.

A ticket usually wants 3–7 rules, each illustrated by one realistic example. If the ticket has 20 AC, it probably has 5 rules and 15 examples — group them.

#### Declarative, not imperative

Express *intent*, not *mechanics*. UI clicks couple the AC to today's interface and obscure the actual behaviour.

> *Imperative (bad):* "When the user clicks the Reverse Shipment button in the ellipsis menu, the side drawer opens with addresses swapped."
>
> *Declarative (good):* "When a customer chooses to return a delivered shipment, they receive a pre-populated return shipment from their delivery address back to their collection address."

#### From the user / business perspective, not the system's

> *System-shaped (bad):* "System copies shipment-definition fields and increments the source counter."
>
> *User-shaped (good):* "Reversing a shipment never affects the source — its status, tracking, billing, and audit log remain unchanged."

#### Ubiquitous language

Use words domain experts use in conversation and words the code already uses. *"shipment", "manifestation", "3PL", "EORI"* — not *"entity", "record", "ID"*.

#### Real, concrete examples

> *Bad:* "Customer ships parcel from A to B."
>
> *Good:* "Alice ships 2.4 kg from Manchester M1 3HZ to Berlin 10115."

Concrete values flush out edge cases that placeholders hide (postcode shapes, locale formatting, weight rounding, etc.).

#### Each rule yes/no checkable

Each rule is one statement that is testable without judgement. Concrete numbers, ranges, status codes, payload shapes — not adjectives.

> *Bad:* "Resend should not be abusable."
>
> *Good:* "Resend is rate-limited to 3/hour per `accountOnboardingId`; the 4th attempt returns `429` with body `{ \"reason\": \"rate_limited\" }`."

#### One *When* per scenario

A scenario captures one behaviour. Multiple `When` clauses = multiple behaviours badly merged — split into multiple scenarios.

#### AC are not test cases

AC define **done**; test cases are the detailed verifications that prove it. A few good AC support many test cases. Conflating them produces 47-step "AC" that nobody reads. Mike Cohn's framing: *"think of the acceptance criteria as the table of contents into a test plan containing all the test cases."*

#### Cover the happy path AND the unhappy paths

For every rule, ask: what happens when the precondition fails? What is the error case? What is the edge case? Missing unhappy-path AC is the most common source of post-*Ready* surprises.

#### Negotiable until *Ready*

AC are written collaboratively (Three Amigos: PO + dev + tester), refined together, and only frozen when the story enters the sprint. AC handed down from one role to another silently lose information.

#### Stakeholders still read them

If the business stops reviewing AC, AC have collapsed into expensive integration tests. The readability is the point.

### Open Questions rules

- Every question has a **named owner** and ideally a due date.
- Anonymous questions are blockers in disguise — assign someone.
- Resolved questions move into the *Context* or *Constraints* section before the ticket goes *Ready*.

---

## B. Bug Report

```markdown
### [Title — names the bug, not the fix]

**Impact / Outcome we want**
Who is affected, how often, and what "fixed" looks like.

**Steps to Reproduce** (deterministic, numbered)
1. ...
2. ...
3. ...

**Expected vs Actual**
- Expected: ...
- Actual: ...

**Environment**
- Service version / git SHA:
- Environment: prod / staging / local
- Tenant / customer / account ID:
- Affected entity IDs (stream IDs, aggregate IDs, correlation IDs):
- Time window of occurrence (UTC):

**Evidence**
- Logs, screenshots, trace IDs, event store excerpts, Grafana links.

**Acceptance Criteria**
- [ ] Reproduction steps no longer trigger the bug.
- [ ] Regression test added — name it.
- [ ] Existing related tests still pass.

**Open Questions** (each with a named owner)
- Question? — *owner: @name*
```

### Bug-specific rules

- **Title names the bug, not the fix.** *Good:* "Resend returns 500 for paused 3PLs". *Bad:* "Add null-check to resend handler".
- **Steps to reproduce must be deterministic.** "Sometimes happens" = a different ticket (a *spike* to find the repro).
- **Environment is mandatory** for production bugs. No "I think it was last Tuesday" — capture the actual SHA and UTC timestamp.
- **Regression test in AC.** A bug without a regression test is a bug waiting to come back.

---

## C. Spike (Optional)

A spike is a **time-boxed investigation** whose output is *knowledge*, not code.

```markdown
### [Title — names the question]

**Question we are answering**
The decision this spike unblocks.

**Time-box**
Hard cap (hours or days). When you hit it, stop and write what you found.

**What "done" looks like**
- [ ] A document / Slack thread / ADR with a recommendation.
- [ ] Open questions reduced to a known list.
- [ ] Enough information to size or split the follow-up ticket.

**Out of scope**
- Production code changes.
- Final implementation.
```

Spikes have a different shape because their output is a *decision*, not a behaviour change.

---

## Anti-patterns (reject in review)

| Anti-pattern | Why it is bad | How to fix |
|---|---|---|
| **Prescribes the solution / "files to change"** | Strips the team's autonomy and skips the design conversation. | Move to AC or delete. The ticket is *what & why*, not *how*. |
| **No outcome / no "why"** | Team cannot tell if the work matters or when it is done. | Add one sentence on the business result. |
| **Vague AC** ("works correctly", "is fast", "looks good") | Not testable. Done-ness becomes opinion. | Replace with thresholds, examples, status codes, payload shapes. |
| **PM-supplied estimate** | Anchors the team; erodes trust. Estimates belong to the team doing the work. | Leave estimate blank until the team weighs in. |
| **Hidden blockers / dependencies** | Ticket enters *Ready* falsely; stalls mid-sprint. | Surface every dependency by name. Do not mark *Ready* until resolved. |
| **Solutioning in the title** | Pre-decides the answer. | Title names the outcome or the bug, not the fix. |
| **Anonymous open questions** | Nobody owns them; they linger. | Assign each question to a named person with a due date. |
| **No reproduction steps (bugs)** | The fix is guesswork. | Either get deterministic steps, or convert to a spike. |
| **Single AC for a multi-behaviour feature** | Hides scope; makes splitting impossible. | One AC per checkable behaviour. |
| **Imperative / UI-mechanic AC** ("When the user clicks the X button…") | Couples done-ness to today's UI; AC become brittle and stop being readable as behaviour. | Express the rule, not the click sequence. *"When the customer chooses to return a shipment…"* |
| **System-shaped AC** ("System copies fields and increments counter") | Strips the user's perspective; AC describe internals not value. | Reframe as "Customer can X" or "System rejects Y when Z" — from the outside, not from the inside. |
| **Rule and examples merged into one bullet** | Hides what is invariant (the rule) vs what is illustrative (the example); makes it hard to see whether coverage is real or just dense. | Lead with the rule; nest one realistic example beneath it. Use Example Mapping if there are many. |
| **Wall of text with no structure** | Reviewers cannot find what is missing. | Use the template headings even when sections are short. |

## Definition of Ready

A ticket is *Ready* when every box below is checked.

- [ ] Outcome is one sentence and non-engineer-readable.
- [ ] Problem section quotes real data, customers, or metrics.
- [ ] At least one acceptance criterion; all are testable.
- [ ] Constraints section is filled (even if "None known").
- [ ] All dependencies are linked and resolved (or scheduled).
- [ ] Every open question has a named owner.
- [ ] No "files to change" / no prescribed solution.
- [ ] No estimate supplied by the requester.
- [ ] For bugs: reproduction steps are deterministic AND environment is captured.

A ticket that fails any of these is *not Ready*. Send it back.

## INVEST mapping

This template operationalises **INVEST** (Bill Wake, 2003):

- **I — Independent.** Dependencies section flushes out coupling early.
- **N — Negotiable.** The ticket is a placeholder for the conversation, not a contract.
- **V — Valuable.** Outcome section is the test.
- **E — Estimable.** Pre-investigation surfaces unknowns before the team estimates.
- **S — Small.** If outcome + AC do not fit on one screen, split it (see `splitting-user-stories`).
- **T — Testable.** AC are yes/no checks with examples.

## How to behave when this skill is invoked

1. **Identify the shape first** — story, bug, or spike. If unclear from the request, ask before drafting.
2. **Ask for the outcome first.** If the user cannot articulate one sentence of business result, surface this as the gap — do not paper over it with prose.
3. **Refuse to write a "files to change" section.** If the user insists, explain why and offer a *pre-investigation* item instead.
4. **Refuse to add an estimate** unless the team has supplied one. Flag the request explicitly.
5. **Output in Markdown** by default. If the user names a tracker (Jira, Linear, GitHub), adapt syntax (e.g. GitHub's `- [ ]` checkboxes vs Jira's `*` lists) but keep the structure identical.
6. **Walk through the Definition of Ready at the end** and call out anything missing — do not silently produce an incomplete ticket.
7. **When reviewing an existing ticket**, run it against the Definition of Ready and the anti-pattern table. Be specific — quote the offending line and suggest a rewrite.

## References

- Daniel Starling — *Anatomy of a Good Software Ticket & Workflow* — daniel-starling.com/blog/2018/05/05/anatomy-of-a-software-ticket/
- Bill Wake — *INVEST in Good Stories, and SMART Tasks* — xp123.com/invest-in-good-stories-and-smart-tasks/
- Marty Cagan / SVPG — *Empowered Product Teams* — svpg.com/empowered-product-teams/

### Further reading on acceptance criteria

- **Atlassian — "What is Acceptance Criteria? Definition, Examples, & Tips"** — [atlassian.com/work-management/project-management/acceptance-criteria](https://www.atlassian.com/work-management/project-management/acceptance-criteria) — the most direct definitional article; PM-readable.
- **Mike Cohn — "Acceptance Criteria, So-That-Clauses, and Requirements"** — [mountaingoatsoftware.com/blog/short-answers-to-your-big-questions-about-user-stories](https://www.mountaingoatsoftware.com/blog/short-answers-to-your-big-questions-about-user-stories) — the practitioner-canonical source; AC as the "table of contents into a test plan".
- **Mike Cohn — "Clarifying Definition of Done and Conditions of Satisfaction"** — [mountaingoatsoftware.com/blog/clarifying-the-relationship-between-definition-of-done-and-conditions-of-sa](https://www.mountaingoatsoftware.com/blog/clarifying-the-relationship-between-definition-of-done-and-conditions-of-sa) — clarifies AC vs Definition of Done, the most common confusion.
- **Agile Alliance — "What is 'Given - When - Then'?"** — [agilealliance.org/glossary/given-when-then/](https://agilealliance.org/glossary/given-when-then/) — formal definition of the AC structural format.
- **Agile Alliance — "What is Acceptance Testing?"** — [agilealliance.org/glossary/acceptance-testing/](https://agilealliance.org/glossary/acceptance-testing/) — the testing-side counterpart definition.
- **Matt Wynne — Example Mapping** — search [cucumber.io/blog](https://cucumber.io/blog) for "Example Mapping". The four-card discovery technique that underpins the *Rule vs example* section above.

## Related skills

- `splitting-user-stories` — when a story is too big to fit in one cycle.
- `behavior-driven-development` — when AC want to be Gherkin scenarios.
- `architecture-decision-records` — when the ticket is really an architectural decision.
