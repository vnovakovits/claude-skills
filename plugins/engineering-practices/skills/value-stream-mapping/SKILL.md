---
name: value-stream-mapping
description: Map how a request flows from ask to value — Mike Rother & John Shook's "Learning to See" (1999) and Karen Martin & Mike Osterling's "Value Stream Mapping" (2013), adapted to software and knowledge work. Covers scoping one value stream, the map grammar (process boxes with lead time, process time and %C&A, queue triangles, push and pull arrows, information flow, the timeline ladder, kaizen bursts), collecting real numbers from tracker state history instead of opinions, the summary metrics (total lead time, process time, flow efficiency or activity ratio, rolled %C&A), the future-state questions, and the transformation plan. Includes a renderer that turns a JSON description into a current- or future-state map as SVG for documents, pages and PDFs. Use when work feels slow but everyone is busy, when reviewing a delivery process, ways of working or governance document, when asked where a request waits, when comparing a proposed process with today's, or when someone asks for a value stream map.
---

# Value Stream Mapping

A value stream is every step, value-adding or not, that one request goes through from the moment someone asks to the moment they get value. Mapping it makes the waiting visible. In knowledge work most of a request's life is waiting, and nobody sees it, because every person is busy with their own step.

Rother and Shook wrote the method for manufacturing (*Learning to See*, 1999). Martin and Osterling generalised it to office, service and knowledge work (*Value Stream Mapping*, 2013) and added the metric that matters most there: percent complete and accurate. Use their version for software.

Companion skills: `flow-efficiency` (why waiting dominates, Little's law, Kingman), `kanban` (managing the flow the map reveals), `toyota-way`, `make-work-visible`.

## When a map is worth drawing

- A request takes weeks or months, and nobody can say where the time goes.
- A process or ways-of-working document is being reviewed or redesigned: map today, then map the proposal.
- Teams are fully busy, yet delivery is slow (the efficiency paradox).
- Handoffs between roles or departments are frequent and painful.

Skip it for a process with one step and one person, or when the question is about a single team's internal practice (use a Kanban board instead).

## 1. Scope one stream

- **One kind of request**, named concretely: "a feature initiative from intake form to outcome review", not "how we work".
- **A start trigger and an end point** that a customer would recognise. End at value received (enabled for users, outcome reviewed), not at "code merged".
- **The customer** of the stream and what they actually need from it.
- Pick the family of work by its route: requests that share most steps share a stream. Bugs, initiatives and BAU usually need separate maps.

## 2. Map the current state

Walk the stream with the people who do the work. Never map from the process document alone: documents describe intent, maps describe reality. When reviewing a document before it is in use, say plainly that the map is the document's intent.

### The grammar

| Element | Meaning | Data it carries |
|---|---|---|
| **Process box** | A step where work is done, by one role or team | who, lead time (LT), process time (PT), %C&A, cadence |
| **Queue triangle** | Work waiting between steps | wait time, number of items waiting |
| **Push arrow** (striped) | The upstream step sends work regardless of downstream capacity | |
| **Pull** (supermarket, FIFO lane with a limit) | Downstream takes work when it has capacity | the limit |
| **Information flow** (thin, dashed) | Trackers, meetings, reports that schedule or signal the work | cadence |
| **Timeline ladder** | Under the map: lead time on the upper line, process time on the lower | per step |
| **Kaizen burst** | An improvement idea placed where it acts | |
| **Summary box** | Total LT, total PT, flow efficiency, rolled %C&A | |

### The three numbers per step (Martin & Osterling)

- **Process time (PT)**: hands-on time to do the work if uninterrupted. Also called touch time or work time.
- **Lead time (LT)**: from the moment the work is available to the step to the moment it is passed on. Includes waiting inside the step.
- **%C&A**: the share of work the *next* step receives complete and accurate, needing no rework, clarification or correction. Ask the downstream step, not the upstream one.

Summary metrics:

- **Total lead time** = sum of LT, including queues.
- **Flow efficiency** (Martin & Osterling's activity ratio) = total PT ÷ total LT. Knowledge work commonly sits at 5-20%.
- **Rolled %C&A** = product of every step's %C&A: the share of requests that go through without any rework. It is often shockingly low.

### Getting real numbers

- **Tracker state history** is the best source in software: Linear, Jira and GitHub all record when an item entered each state. Sum time per state for the last 10-20 comparable items. Use medians and the 85th percentile, not averages alone.
- **Waits hide inside states.** "In progress" includes waiting for review, environments and answers. Split states where waiting hides, or sample a few items by hand.
- **Cadences set minimum waits.** A weekly meeting adds 2.5 working days on average to every item that needs it. A fortnightly release adds 5.
- **Little's law** estimates an unmeasured queue: wait = items ahead ÷ throughput. Five initiatives ahead at one per four weeks is twenty weeks.
- **Mark every estimate as an estimate**, on the map itself. A map that presents guesses as data destroys trust the first time someone checks.

## 3. Read it

Look for, in this order:

1. **Where the lead time goes.** Usually one or two queues hold most of it, and they are rarely where people argued about.
2. **Waits before the work starts.** Gates, approvals and backlogs upstream of development are invisible to delivery metrics that start at "in progress".
3. **Low %C&A steps.** Rework loops multiply lead time and hide as "busy".
4. **Push between steps.** Each push point builds a queue; each handoff loses context.
5. **Batching.** Work released all at once, one big release at the end, weekly decisions: batch size drives queue size.
6. **Shared specialists without WIP limits.** They are the likely bottleneck (Kingman: waits explode near full utilisation).

## 4. Design the future state

Rother and Shook's future-state questions, translated to software:

1. **What does the customer actually need, and how often?** (Demand rate. Is the stream sized for it?)
2. **Where can work flow continuously,** one small item at a time, without a queue between steps?
3. **Where must there be a queue, and how is it limited?** Replace unlimited backlogs with capped, pulled queues.
4. **Which single point schedules the stream?** One decision point, not several gates.
5. **How is the work levelled?** Small, similar-sized increments instead of one big release.
6. **What is the smallest increment that can reach users and produce learning?**
7. **What improvements are needed** to make all of the above work: tooling, skills, authority, measures.

Draw the future state as a second map with the same notation and the same estimating basis, so the two can be compared honestly. Then write the **transformation plan**: the kaizen bursts as owned, sequenced actions, each with the metric that will show it worked.

## 5. Draw it

`scripts/vsm.py` renders a map from JSON (format in `references/vsm-json.md`) to SVG:

```bash
python scripts/vsm.py current.json current.svg
```

- It draws process boxes, queue triangles, push arrows, information flow, kaizen bursts, the timeline ladder and the summary box. Long streams wrap into labelled rows ("Getting to start", "Delivering").
- Colours come from CSS variables with fallbacks (`--surface`, `--fg`, `--muted`, `--accent`, `--warn`, `--warn-bg`, `--sky`, `--kaizen`, `--kaizen-bg`), so inlined into an HTML page it follows that page's theme, including dark mode.
- For a PDF, inline the SVG in HTML and print with headless Chrome. Put each map on a named landscape page (`@page landscape { size: A4 landscape }` and `page: landscape` on the section), cap the SVG with `max-height` so it fits on one page, and rasterise the PDF (PyMuPDF) to check every page before handing it over.
- Leave `title` out of the JSON when the page already has a heading.

## Anti-patterns

- **Mapping the process document** instead of the work, and presenting it as reality.
- **Starting the clock at "in progress"**: it hides everything upstream, which is usually most of the lead time.
- **Averages only**: a median and an 85th percentile tell you about predictability; an average hides it.
- **Mapping everything at once**: one stream, one map. A wall of every process teaches nothing.
- **Utilisation as the goal**: the map exists to cut waiting, not to keep people busy.
- **A future state with no plan**: kaizen bursts without owners are decoration.
- **Blaming steps**: the queues come from how the system is designed, not from the people in it (Deming).

## Checklist

- [ ] One named stream, a customer, a start trigger and an end at value received?
- [ ] Mapped with the people who do the work, or labelled as the document's intent?
- [ ] LT and PT for every step, %C&A where it can be asked, every estimate labelled?
- [ ] Queues shown as triangles with wait times, including those before development?
- [ ] Summary: total LT, PT, flow efficiency, rolled %C&A?
- [ ] Future state drawn on the same basis, with a transformation plan of owned actions?

## Reading

- Mike Rother & John Shook, *Learning to See* (Lean Enterprise Institute, 1999).
- Karen Martin & Mike Osterling, *Value Stream Mapping: How to Visualize Work and Align Leadership for Organizational Transformation* (McGraw-Hill, 2013).
- Niklas Modig & Pär Åhlström, *This is Lean* (2012): flow efficiency.
- Mary & Tom Poppendieck, *Implementing Lean Software Development* (2006): value stream maps for software.
- Steve Pereira & Andrew Davis, *Flow Engineering* (IT Revolution, 2024): value stream mapping as a team practice in software organisations.
