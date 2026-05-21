---
name: architecture-decision-records
description: Apply Michael Nygard's Architecture Decision Records (ADRs) — lightweight, immutable Markdown documents that capture significant architectural decisions, their context, and their consequences. Covers Nygard's classic format, MADR, when a decision is "architecturally significant", supersession workflow, where to store ADRs, and how to use them as living institutional memory. Use when making a significant technical decision, when joining a project and wondering "why was it built this way", when a past decision starts to bite, or when a team's tribal knowledge is bleeding away through personnel turnover.
---

# Architecture Decision Records (Michael Nygard)

Apply this skill when making a significant architectural or technical decision that future readers — colleagues, your future self, new joiners — will need to understand. ADRs answer the question that's always asked six months later: *"Why did we do it this way?"*

## Core Philosophy

**The why is the hardest thing to recover.** Code captures *what* the system does. Documentation captures *how* to use it. Neither captures *why* a particular path was chosen over alternatives. ADRs fill that gap.

**Decisions, not aspirations.** An ADR records a decision *that was made*, in the moment, with the context available *at that time*. It is a historical record, not a wish list.

**Lightweight.** A few paragraphs of Markdown, in the repository, alongside the code. Not Confluence, not a wiki, not a 40-page document. The cost of writing one must be low or they won't get written.

**Immutable.** Once accepted, an ADR is not edited. If circumstances change, write a new ADR that supersedes the old. The record of changing decisions over time is itself valuable.

**Decentralized institutional memory.** Teams turn over. Companies change. Six months from now, an ADR is the only thing that will tell someone *why* this database was chosen, this pattern adopted, this technology rejected. Without it, the only path to recovering the reasoning is asking the people who made the decision — and they may be gone, or have forgotten.

---

## Nygard's Classic Format

Michael Nygard's 2011 blog post — *Documenting Architecture Decisions* — proposed a minimal template that remains the canonical structure.

```markdown
# 1. Use PostgreSQL as the primary OLTP database

## Status

Accepted

## Context

We need a relational database for transactional workloads. Requirements:
- ACID transactions
- Strong consistency
- JSON column support for semi-structured data
- Active community and good operational tooling
- Compatible with our managed-cloud (AWS) deployment

We considered: PostgreSQL, MySQL, Microsoft SQL Server, Amazon Aurora.

## Decision

We will use PostgreSQL 16 as the primary OLTP database, deployed via
AWS RDS Multi-AZ.

## Consequences

Positive:
- Native JSON/JSONB support reduces need for a separate document store.
- Active OSS community; recent versions ship significant performance work.
- Mature operational tooling (pg_dump, pgbackrest, pgbouncer, etc.).

Negative:
- Team has more MySQL experience than PostgreSQL; some upskilling needed.
- AWS RDS PostgreSQL has occasional minor-version-upgrade incompatibilities.

Neutral:
- Locked into the relational model for OLTP workloads; document-oriented
  data will live in PostgreSQL JSONB unless we explicitly add a document
  store later.
```

### Fields

- **Title** — numbered (`ADR 0001`), descriptive, in imperative or noun phrase form.
- **Status** — Proposed | Accepted | Deprecated | Superseded by ADR-NNNN.
- **Context** — what's the situation, what forces are at play, what constraints exist? Background a reader needs.
- **Decision** — what *we decided*. Active voice. Specific.
- **Consequences** — what becomes easier and what becomes harder as a result. Positive, negative, neutral. *This is the field most often skimped on; it's often the most valuable.*

### Optional fields (use sparingly)

- **Alternatives considered** — explicit list of options weighed, with brief rationale for rejection.
- **Stakeholders** — who was involved in the decision.
- **Related ADRs** — links to ADRs this builds on or interacts with.

---

## Status Lifecycle

```
Proposed ──► Accepted ──┬──► Deprecated
                        │
                        └──► Superseded by ADR-NNNN
```

- **Proposed** — under discussion; not yet binding.
- **Accepted** — the decision is in force. Team is bound by it.
- **Deprecated** — the decision no longer applies but has not been replaced (rare).
- **Superseded by ADR-NNNN** — replaced by a later decision. The original ADR is *not edited*; the status line is updated and (optionally) a brief note points to the successor.

### Why immutability matters

The history is the point. "We chose X in 2024 because Y, then in 2026 we replaced X with Z because Y was no longer true" is a richer story than "we chose Z because Y is no longer true". The first sentence appears only if you preserve the original ADR.

---

## When to Write an ADR

The hard question. Most decisions don't warrant one; some that do don't get written.

Heuristics:

**Worth an ADR:**
- Choice of language, framework, runtime, database, message broker.
- Choice of architectural style (monolith vs microservices, sync vs async, REST vs gRPC).
- Adoption of a major library or pattern with broad consequences.
- Significant interface contract between teams / services.
- Decisions to *not* do something obvious (i.e., explicit no-go on a path others would assume).
- Trade-offs that took more than 30 minutes of team discussion to resolve.
- Anything you would expect to be re-litigated by a new joiner.

**Not worth an ADR:**
- Code-level patterns (those go in the code).
- One-off implementation choices.
- Decisions reversible in minutes.
- Documentation of "how" rather than "why".
- Anything where future readers won't ask "why?"

**Rule of thumb:** if six months from now you'd want a written record to defend or revisit this, write one. If not, don't.

---

## Where ADRs Live

In the repository, alongside the code. Typical paths:

```
docs/adr/0001-use-postgresql.md
docs/adr/0002-domain-events-for-cross-aggregate-coordination.md
docs/adr/0003-strangler-fig-for-legacy-billing-migration.md
docs/adr/0004-superseded-postgresql-version.md
```

Or `adr/` at the root, or `architecture/decisions/`, depending on team taste. The folder name matters less than:
- ADRs are version-controlled with the code.
- They have stable URLs.
- They are discoverable (a `README` index helps).
- They are easy to find from PRs, code comments, and discussions.

Tools that help:
- **adr-tools** (Nat Pryce) — CLI for creating, listing, superseding ADRs.
- **log4brains** — generates a static site of the ADR catalog.
- **MADR template** — Markdown ADR template, slightly more structured than Nygard's.

---

## Variants

### MADR (Markdown ADR)
A more structured version of Nygard's format, with explicit fields for *Decision Drivers*, *Considered Options*, *Decision Outcome*, and *Pros and Cons of the Options*. Better when many alternatives need recording; heavier when only one was seriously considered.

### Y-Statement
A one-line form for trivial decisions:

> In the context of *(use case)*, facing *(concern)*, we decided for *(option)* and against *(alternatives)* to achieve *(benefit)*, accepting *(downside)*.

Useful for inline summaries; not a replacement for a real ADR for significant decisions.

### Lightweight ADRs
Some teams keep ADRs to under 200 words. Tighter discipline, easier to write, easier to read. Worth trying.

---

## Patterns of Good ADRs

- **Specific titles.** "Use PostgreSQL" beats "Database choice". Future readers find specifics faster.
- **One decision per ADR.** Don't bundle. "Use PostgreSQL and standardize on EF Core" is two ADRs.
- **Explicit alternatives.** "We considered X, Y, Z" with one-line reasons for rejecting each. The rejected paths are often what readers want to understand.
- **Honest consequences.** Real downsides, not just upsides. An ADR that lists only benefits looks like marketing, not engineering.
- **Date the decision.** The status line should reflect when it was accepted.
- **Reference real constraints.** "Customer X requires SOC2 compliance" beats "for compliance reasons".
- **Link to evidence.** Benchmarks, RFCs, blog posts, internal docs — anything that supported the call.

---

## Patterns of Bad ADRs

- **ADRs as design specifications.** They are not. ADRs record *the decision*, not the design. Design lives elsewhere.
- **Vague reasoning.** "We chose X for performance reasons" — what reasons? Compared to what?
- **No consequences.** A decision is incomplete without an honest accounting of what it costs.
- **Bundled decisions.** "ADR-7: Architecture v2" containing twelve separate decisions. Split them.
- **Aspirational ADRs.** "We will use TypeScript everywhere by 2026." Not a decision — a goal.
- **Editing accepted ADRs.** Breaks the historical record. Supersede instead.
- **ADRs nobody reads.** A file that exists but is invisible doesn't serve its purpose. Link to it from PR descriptions; mention it in onboarding; refer back during reviews.
- **ADRs as ticket numbers.** "ADR-42: closing JIRA-1234". The ADR exists to document the decision, not the ticket.

---

## ADRs in Practice

A typical workflow:

1. **A significant decision is on the table.** Discussion begins (PR, design meeting, async thread).
2. **Someone drafts a Proposed ADR.** Short — context, decision, consequences. Pushed to the repo as part of the discussion.
3. **The team comments, refines.** The ADR moves through revisions.
4. **A decision is reached.** Status changes to Accepted; ADR is merged.
5. **Months later, circumstances change.** New ADR is drafted that supersedes the original. Original's status is updated to "Superseded by ADR-NNNN".

ADRs *during* the discussion serve as a focal point — they keep everyone arguing about the same options.

ADRs *after* the discussion serve as institutional memory.

---

## Common Mistakes

- **Writing ADRs only for big-bang decisions.** The cumulative value comes from many small ones, not a few epics.
- **Not writing ADRs because "everyone knows".** They won't, six months from now.
- **Writing ADRs in confluence/wiki/email.** Not version-controlled, not discoverable, not durable.
- **Treating ADRs as policy documents.** They are records, not laws. Decisions change; ADRs supersede; the trail is the record.
- **Skipping the consequences section.** "Decision: X." OK, but at what cost? The cost is what people will want to know.
- **Long-winded ADRs.** Two pages max. If it needs more, link to a design doc.
- **No index.** A folder of 50 ADRs is a haystack. Maintain a README listing them with one-line summaries.

---

## ADRs and Other Practices

- **With DDD:** record the bounded-context boundaries, integration patterns (ACL, OHS), and aggregate decisions in ADRs.
- **With Hexagonal Architecture:** record port-and-adapter boundaries and major integration choices.
- **With Continuous Delivery:** record deployment-strategy choices, pipeline structure, environment topology.
- **With Refactoring:** record major refactoring campaigns (Strangler Fig over the legacy system, etc.).
- **With code review:** when a PR introduces a significant architectural shift, the ADR is the right venue for the discussion; the PR cites it.

---

## Quick Application Checklist

When considering an ADR:
- [ ] Is this decision architecturally significant?
- [ ] Will future readers ask "why did we do this"?
- [ ] Are there alternatives worth recording?
- [ ] Are the consequences non-trivial?

When writing an ADR:
- [ ] Is the title specific enough to find by search?
- [ ] Is the context clear to someone with no project memory?
- [ ] Are the alternatives considered explicit?
- [ ] Are the consequences honest (positive *and* negative)?
- [ ] Is it short (one to two pages)?
- [ ] Is it in the repo, alongside the code?

When superseding:
- [ ] Did I leave the old ADR intact?
- [ ] Did I update the old ADR's status to "Superseded by ADR-NNNN"?
- [ ] Does the new ADR link back to the old?
- [ ] Did I record what changed to make the new decision the right one?

---

## Reading

- **Michael Nygard**, *Documenting Architecture Decisions* (2011 blog post) — the original. cognitect.com / thinkrelevance archives.
- **Michael Nygard**, *Release It!* (2nd ed., 2018) — broader operations / architecture book; ADRs are one chapter.
- **adr.github.io** — community resource with the MADR template, links to tools, and many real-world examples.
- **Nat Pryce**, *adr-tools* — github.com/npryce/adr-tools, the original CLI helper.
- **Olaf Zimmermann et al.**, *Sustainable Architectural Decisions* (IEEE Software, 2013) — academic framing.
- **ThoughtWorks Technology Radar** — though not ADRs, the same ethos at organization scale.
- **Pat Kua**, *An appropriate use of metrics* — adjacent essay on capturing technical context that fades.
