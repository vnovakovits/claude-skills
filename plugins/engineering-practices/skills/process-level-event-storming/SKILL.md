---
name: process-level-event-storming
description: Apply Alberto Brandolini's Process Modeling level of Event Storming — modeling ONE business process in full sticky-note grammar (read model → actor → command → aggregate/external system → event → policy → …) on a timeline, with hot spots as first-class output. Covers the picture-that-explains-everything loop, grammar rules, completeness walks (backwards walk, orphan checks, missing failure paths), swimlane/frame layout for remote boards (Miro/Mural/FigJam), and mapping the model onto process managers, sagas, and workflow code. Use when designing or documenting a single process end-to-end, modeling a new feature's flow across services, reviewing a workflow for gaps, or turning a Big Picture cluster into an implementable design.
---

# Process-Level Event Storming (Alberto Brandolini)

Apply this skill when one specific business process needs to be modeled in detail — a new feature's flow, an existing workflow you're changing, a cross-service saga you're reviewing. It assumes the scope is already known (from a Big Picture session or simply from the ticket); for whole-domain discovery, use the companion `event-storming` skill.

The output is a **process model**: a left-to-right timeline in the full sticky-note grammar, precise enough to walk into code, with every unknown marked as a hot spot rather than smoothed over.

---

## The Picture That Explains Everything

Brandolini's process-level grammar is one repeating loop:

```
(green)        (small yellow)   (blue)        (large yellow / pink)   (orange)       (lilac)
Read Model  →  Actor         →  Command    →  Aggregate or         →  Domain      →  Policy  →  next Command …
"what they     "who decides"    "the intent"   External System         Event          "whenever X,
 looked at"                                    "what decides"          "the fact"      then Y"
```

Every complete process is this loop unrolled along a timeline. When a step is missing, that's not a simplification — it's a gap in understanding. The loop closes when a policy (or an actor reading a read model) issues no further command: the process is complete.

## The Grammar

| Sticky | Color | Form | Rule |
|---|---|---|---|
| Domain Event | orange | past tense | The atom. A fact a domain expert cares about. Domain language, never "record saved". |
| Command | blue | imperative | Every command has exactly one issuer: an actor or a policy. |
| Actor | small yellow | role name | Who decides to issue the command. Roles, not names or departments. |
| Aggregate / Process | large yellow | noun | What receives the command and emits the event(s). At process level this is often the process manager / workflow itself. |
| External System | pink | system name | Something the process talks to but doesn't own. Its failures are part of YOUR process. |
| Read Model | green | view name | What the actor looked at to decide. If you can't name it, the actor is deciding blind — hot spot. |
| Policy | lilac | "whenever X → Y" | Reactive automation. Everything that happens without a human. Becomes a saga / process manager / event handler. |
| Hot Spot | dark red / rotated | question or claim | Disagreement, missing knowledge, risk, unresolved decision. Capture, don't resolve. |

### Hard rules

1. **Timeline is sacred.** Strictly left → right in time. Parallel outcomes stack vertically at the same x.
2. **Events are past-tense facts in domain language.** "Cancellation Confirmed", not "handle confirmation".
3. **Every command has an issuer.** No issuer on the board → you don't know who triggers it → hot spot.
4. **Every event has a source.** An orange sticky not attached to an aggregate or external system is folklore.
5. **Policies carry the automation.** The word "automatically" in conversation means a lilac sticky on the board. Policies are where sagas, timeouts, retries, and schedules live — and where they're missing.
6. **Alternative flows are part of the process.** The happy path alone is a brochure, not a model. Rejections, failures, timeouts, and out-of-order arrivals go on the same timeline, stacked below the happy path.

## Completeness Walks

A process model is done when it survives these walks, done aloud, pointing at stickies:

- **Forward walk.** Narrate left to right: "the customer looks at …, decides to …, which makes the workflow …, which emits …, and whenever that happens we …". Any stumble is a missing sticky.
- **Backward walk.** For each event, ask: what command produced this? Who or what issued that command? What did they look at first? Walking backwards catches issuer-less commands and blind decisions that the forward walk glosses over.
- **Orphan check.** Events nothing reacts to — is that intentional (recorded fact) or a missing policy? Commands with no resulting event — what does success even look like?
- **Silence check (external systems).** For every pink system: what happens if it never answers? If the answer is "nothing reacts to that", write it on a dark-red sticky verbatim. Missing failure paths are the single most common finding at this level.
- **First-event check.** For every inbound event: what if it arrives before the process exists, or after it's finished? Out-of-order delivery is the norm in messaging systems.

## Hot Spots Are the Point

At process level, hot spots stop being only "we disagree" and become concrete engineering findings:

- a message routed somewhere nobody could explain
- a failure that no policy reacts to
- a decision recorded as "TODO" in code
- a confirmation that means nothing
- a contract that can't evolve

Write them as a **claim or a question, verbatim and specific** ("if Orchid has no consumer for this, the cancel is silently lost"), place them **on the exact sticky they're about**, and leave them visible. A process model whose hot spots were quietly resolved by the modeler is a fiction. Hot spots are the input to the next tickets.

## Remote Boards (Miro / Mural / FigJam)

- **Frames per phase** of the process ("Request", "Fan-out", "Outcome", "Settlement") keep a long timeline navigable; the frame titles narrate the process on their own.
- **Swimlanes**: happy path along the top; alternative/failure flows stacked below; external systems' stickies aligned in their own horizontal band so each integration reads as a column of ask → answer.
- **Stick to the canonical colors** (map them once in a legend sticky if the tool's palette differs). Color IS the grammar; a wrong-colored sticky is a wrong statement.
- **Connectors sparingly**: the timeline carries most causality; use arrows only where flow jumps (policy → command far away, out-of-order arrivals).
- Keep stickies terse — the phrase on the sticky is the ubiquitous language; put message/type names (`ShipmentCancellationCompleted`) on the sticky when the model documents an existing system.

## From Model to Code

The process model maps mechanically onto a process manager / saga / workflow engine:

| On the board | In code |
|---|---|
| Large-yellow process sticky | Process manager / saga / workflow instance (one stream per subject) |
| Blue command → pink system | Outbound message/call (state the idempotency + retry stance) |
| Orange event from pink system | Inbound subscription / consumer |
| Lilac policy | The decision function: `(state, event) → commands` |
| Ordered orange stickies | The state machine's transitions; stacked alternatives = branches |
| Green read model | Query/projection backing the UI decision |
| Dark-red hot spot | Ticket, ADR, or test to write before trusting the process |

If the code has a decision arm the board doesn't show, the board is wrong. If the board shows a policy the code doesn't have, the code is wrong — or the hot spot was real.

## Quick Checklist

- [ ] One process, named, with a clear start (first command) and end (final event)?
- [ ] Timeline strictly left → right; alternatives stacked, not hidden?
- [ ] Every command has an issuer; every event has a source?
- [ ] Read models named for every human decision?
- [ ] Every external system given the silence check ("what if it never answers?")?
- [ ] Inbound events given the first-event / out-of-order check?
- [ ] Hot spots specific, verbatim, placed on the sticky they're about — and NOT resolved on the board?
- [ ] Forward and backward walks done without stumbling?

## Reading

- **Alberto Brandolini**, *Introducing EventStorming* (Leanpub) — Part "Process Modelling"; the picture-that-explains-everything diagram.
- **Alberto Brandolini**, "50,000 Orange Stickies Later" (talk) — where process level sits between Big Picture and Software Design.
- Companion skills: `event-storming` (the whole method, workshop facilitation), `event-sourcing-cqrs` and `domain-driven-design` (turning the model into aggregates and sagas).
