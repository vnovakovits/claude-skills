---
name: grilling
description: Run a relentless, structured interview that sharpens a plan, design, feature idea or piece of writing until every decision in it is made and written down. Questions come in short rounds, each with a recommended answer; the interviewer looks up facts in the code and docs itself and only asks the human for decisions. In a repository it also keeps the domain language in a GLOSSARY.md and records hard-to-reverse decisions as ADRs as they land. Draws on Socratic questioning (Paul & Elder), Evans's ubiquitous language, Klein's premortem, Example Mapping and Matt Pocock's grilling skills. Use when the user says "grill me", "poke holes in this", "interview me", "help me think this through", or brings a fuzzy idea, a plan with gaps, a design with untested assumptions, or overloaded terms, before writing a spec or tickets.
---

# Grilling

Apply this skill when an idea needs sharpening before anyone builds it: a feature request, a design, a migration plan, an architecture choice, a document. The aim is a set of **decisions**, each made by the person who owns it, with the reasoning written down. The interviewer's job is to find every open question, settle the ones facts can settle, and put the rest to the human one round at a time.

It has two modes:

- **With docs** — in a repository. Terms go into `GLOSSARY.md` and hard-to-reverse decisions into ADRs as they are settled, so the thinking outlives the conversation.
- **Stateless** — anywhere else, or when the user asks for no files. Same interview; the summary at the end is the only record.

## Core Philosophy

**Facts are the interviewer's job; decisions are the human's.** Never ask something you can look up. Before each round, read the code, docs, tickets and data that bear on the open questions, and settle what they settle. Ask the human only for choices: priorities, trade-offs, scope, risk appetite, intent.

**Every question carries a recommendation.** "Should we X or Y? I'd pick X because Z" is answerable in a word. A bare open question costs the human the thinking you were meant to do.

**Rounds, not walls.** Three to five questions per round, most important first. A wall of twenty questions gets skimmed and half-answered.

**Walk the decision tree.** Decisions depend on each other. Keep a **frontier** — the open questions whose prerequisites are settled — and ask only from it. Answering one question often opens two and closes three.

**Concrete beats abstract.** Stress-test every rule with a specific example and an edge case. "What happens to a half-paid order when the customer changes country?" exposes more than "how should payments work?".

**Language is part of the design.** Fuzzy or overloaded terms ("account" meaning three things) hide disagreements. Pin each term down as it comes up.

---

## The Procedure

### 1. Frame

- State in one or two sentences what is being grilled and what "done" looks like: a spec-ready design, a go/no-go, a decided migration path.
- Read what exists: the code in the area, `GLOSSARY.md`, ADRs, related tickets, earlier documents. Note decisions already recorded; they are not reopened without new evidence.
- Build the first frontier: list every open question you can see, grouped by dependency.

### 2. Run rounds

Each round:

1. **Settle facts first.** For every frontier question a fact can answer, look it up and state the answer with its source.
2. **Ask three to five decisions**, highest impact first. Each one names the options, gives your recommendation, and says why.
3. **Record the answers** as soon as they arrive (see below), then update the frontier: close what was answered, add what the answers opened.

Question types that find the gaps (Socratic questioning, adapted):

| Type | Example |
| --- | --- |
| Clarify | "When you say *customer*, do you mean the person who pays or the person who receives the goods?" |
| Probe an assumption | "This assumes payment always succeeds before fulfilment. What if the bank declines after we have reserved the stock?" |
| Ask for evidence | "Do we know how often that happens? The logs show 3% of last month's orders." |
| Explore consequences | "If we allow this, every report that sums totals now has to handle negative amounts." |
| Offer an alternative | "Could the same goal be met by restricting the input instead of handling the edge case?" |
| Premortem (Klein) | "It is six months from now and this failed. What is the most likely reason?" |

Use concrete scenarios to test boundaries, Example Mapping style: one rule, two or three examples that pass, one that should not, and the question the examples raise.

### 3. Keep the paper trail (with-docs mode)

**`GLOSSARY.md`** — update it the moment a term is settled, not at the end. One entry per term:

```markdown
### Order
A customer's commitment to buy a set of items at agreed prices, from checkout until it is fulfilled or cancelled.
*Avoid:* basket (not yet committed), invoice (the request for payment that follows).
*Related:* Basket, Invoice
```

The glossary holds language only: no implementation details, no decisions, no to-dos. If the repository has several bounded contexts with separate glossaries, update the one the term belongs to. Create the file lazily, when the first term is settled.

**ADRs** — offer one only when a decision passes the three-condition test in `architecture-decision-records`: hard to reverse, surprising without context, and the result of a real trade-off. Write it in that skill's format while the reasoning is fresh.

**Challenge against what is written.** When the human uses a term in a way that conflicts with the glossary, or proposes something an ADR rejected, say so immediately: "The glossary defines cancellation as before dispatch, but you seem to include returns. Which is it?"

### 4. Stop

Stop when the frontier is empty, or when the remaining questions are explicitly deferred. Do not stop because a round went quiet; ask whether the human wants to defer the rest.

Close with a summary:

```markdown
## Grilling summary: <topic>

**Goal:** <what was being decided>

### Decisions
1. <decision> — <one-line reason> (ADR-NNNN if recorded)

### Facts established
- <fact> — <source>

### Deferred
- <question> — <why deferred, who decides, by when>

### Terms settled
- <term>: <one-line definition> (in GLOSSARY.md)
```

The summary is the input for `to-tickets` or a spec.

---

## Anti-patterns

- **Asking what you could look up.** The single biggest waste of the human's attention.
- **Questions without recommendations.** It pushes the thinking back onto the person who asked for help.
- **The question wall.** Twenty questions at once; half get answered, and the order of dependence is lost.
- **Answering your own questions.** The interviewer settles facts, never decisions. Filling in the human's choice for them defeats the exercise.
- **Abstract questions only.** "How should errors work?" invites a vague answer. A specific failing scenario does not.
- **Reopening settled decisions** without new evidence, or ignoring ones already recorded in ADRs.
- **A glossary that becomes a spec.** Implementation notes and to-dos belong elsewhere.
- **Grilling a decided, small change.** If there is nothing open, say so and stop.

---

## How This Skill Pairs with Others

- **domain-driven-design** — the glossary is the ubiquitous language made concrete; a term with two meanings may mark a bounded-context boundary.
- **example-mapping** — the concrete-scenario technique used inside a round; for a story with many rules, run a full example map.
- **architecture-decision-records** — where hard-to-reverse decisions go, and the test for when one is worth writing.
- **to-tickets** — turns the grilling summary into dependency-ordered tickets.
- **event-storming** and **process-level-event-storming** — when the open questions are about a whole process, a modelling session surfaces them faster than an interview.
- **ticket-writer** — when the outcome is a single ticket rather than a plan.

---

## Quick Application Checklist

- [ ] Did I read the code, docs, glossary and ADRs before asking anything?
- [ ] Is every question in this round a decision, not a fact?
- [ ] Does each question offer options and my recommendation?
- [ ] Are there at most five questions, most important first, all on the frontier?
- [ ] Did I test the rules with concrete examples and an edge case?
- [ ] Did I update `GLOSSARY.md` as terms were settled, and offer ADRs only where the three conditions hold?
- [ ] Is the frontier empty or explicitly deferred before I stop?
- [ ] Does the summary list decisions, facts, deferrals and terms?

---

## Reading

- **Richard Paul & Linda Elder**, *The Thinker's Guide to the Art of Socratic Questioning* (Foundation for Critical Thinking, 2006) — the question types used in each round.
- **Eric Evans**, *Domain-Driven Design* (2003), chapter 2 "Communication and the Use of Language" — ubiquitous language, the reason for the glossary.
- **Gary Klein**, "Performing a Project Premortem" (*Harvard Business Review*, September 2007) — imagining the failure to find the risk.
- **Matt Wynne**, "Introducing Example Mapping" (Cucumber blog, 2015) — rules, examples and questions.
- **Michael Nygard**, "Documenting Architecture Decisions" (2011) — the ADR format.
- **Matt Pocock**, `grilling`, `grill-with-docs` and `domain-modeling` skills (github.com/mattpocock/skills) — the round-based interview, "facts are the agent's job, decisions are yours", and the glossary kept inline.
