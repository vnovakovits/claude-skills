---
name: example-mapping
description: Apply Matt Wynne's Example Mapping — the four-colour discovery technique (yellow story, blue rules, green concrete examples, red questions) that breaks a story or spec into rules, hangs concrete examples under each rule, and surfaces open questions. Covers the 25-minute session, card conventions, shape-of-the-map diagnostics (a rule with no examples is under-specified; an example fitting no rule means a missing rule; a red-heavy map is not ready), AUDIT MODE for checking whether a written spec's examples cover its rules, building the map on Miro or as a document, and converting greens into acceptance tests and reds into a review agenda. Use when refining a story before development, preparing or running a three-amigos session, writing or reviewing acceptance criteria, reviewing a requirements doc or algorithm that is "hard to reason about", or whenever an abstract discussion would be sharpened by concrete examples — even if nobody says "example mapping".
---

# Example Mapping (Matt Wynne)

A structured conversation that turns one story or spec into a four-colour map: the story, the rules it must obey, concrete examples proving each rule, and the questions nobody in the room can answer. Invented by Matt Wynne (Cucumber) for pre-development discovery; equally powerful in **audit mode** — mapping a spec that is already written to expose which of its rules are illustrated, which are asserted but never shown, and which questions it silently leaves open.

The output is not the cards — it is the **shape** of the map. A balanced, green-heavy map says "ready"; the imbalances say precisely what is missing and where.

## The Four Cards

| Card | Colour | One per | What it says |
|---|---|---|---|
| Story | yellow | map | The feature or behaviour under discussion. One story per map — a second yellow card means a second map. |
| Rule | blue | constraint | A business rule / acceptance criterion, phrased as behaviour ("nothing selected available → nearest slower band"), never as implementation. The rules become the columns. |
| Example | green | concrete case | One specific situation with real data that proves one rule. Hangs under the rule it proves. |
| Question | red | unknown | Something nobody present can answer, or an inconsistency found while mapping. Capture verbatim, don't resolve — like an Event Storming hot spot. |

### Card-writing rules

1. **Green cards follow one formula:** `context · inputs → outcome — one-line why`. Real values ("DPD £6.20, UPS £5.90 → UPS"), not categories ("a cheaper quote wins"). Terse enough for a sticky (~200 characters). Spoken aloud, Wynne's "the one where…" naming keeps the room concrete.
2. **Hunt the off-stage rules.** Exclusions, defaults, tie-breaks, special-cased entities, and equivalences ("forced mode is the same rule with sets of one") are stated once in prose and never illustrated — those are exactly the rules that hide. Give each its own blue card; an empty column under one is a finding, not a layout accident.
3. **Red cards must be answerable in one sentence.** Phrase each so the product owner or spec author can resolve it on the spot; each answer converts into a doc edit, a new blue card, or a new green card.
4. **Provenance tags in audit mode:** prefix examples taken from the document with their section reference (`§4 Ex1`) and examples you invented with `NEW`. The finished map doubles as a coverage report of the doc.

## Layout

Story card top-left, legend beside it, rules in a row, each rule's examples stacked beneath it — reading the map is reading columns. Red cards sit in the column of the rule they challenge; genuinely general ones park in a final column.

When the subject is an algorithm, add a **one-sentence mental model** as a header — the staged/procedural rule restated as a preference ordering ("prefer your carriers; within them your bands, then nearest slower, then anything faster; price only breaks ties inside the winning bucket"). If you cannot restate it in a sentence or two, that inability is itself a red card.

## The Shape Is the Diagnostic

- **A rule with no green cards** → under-specified. In audit mode: the doc asserts it but never shows it.
- **An example that hangs under no rule** → a missing blue card — or a contradiction in the source, which is a better catch.
- **A red-heavy map** → not ready. Don't start development; don't sign off the spec.
- **More than ~6 rules** → the story is too big; split it (companion: `splitting-user-stories`).
- **One column hoarding most of the examples** → the complexity hotspot. Expect the bugs, the review argument, and the test effort to concentrate there.
- **Mostly green, evenly spread, few reds** → ready.

## Audit Mode: Mapping a Written Spec

1. Extract the rules — including the off-stage ones (rule 2 above) — as blue cards.
2. Place every worked example from the doc under a rule, **verifying it against the rule as you place it**. Placement is verification: a card that won't hang under any rule is a defect in the doc, and an example whose stated outcome disagrees with the rule is a bug in one of them.
3. Derive the missing examples (`NEW`): boundaries, empty sets, ties, the excluded thing being the only option, the equivalence collapses. Prefer examples that a reviewer would construct to attack the spec.
4. The red column is the review agenda. Take it to the author/CTO review; when a question is answered, recolour it green (or add the rule) and move it into place — the map converges on the acceptance-test inventory.

## Running It Live (Discovery Mode)

- Timebox **~25 minutes per story**, three amigos (product, dev, test) — if it can't be mapped in 25 minutes, the story is too big or too vague; that's the result, not a failure.
- Start with the yellow card and whatever acceptance criteria already exist as blues.
- Alternate two questions: *"can you give me an example of that rule?"* and *"what rule does that example illustrate?"* The first fills columns; the second discovers missing blues.
- Anything that stalls the room for more than a minute becomes a red card, and the conversation moves on.
- Close with a thumb vote: *ready to build?* A "no" plus the map beats an hour of unstructured discussion.

## On a Miro Board

- Stickies: `yellow` story, `blue` rules, `light_green` examples, `red` questions. One frame per story.
- Geometry that works with wide stickies (350×228): column pitch 400, rules row beneath the header, example rows at pitch 260, frame width = columns × 400 + margins. Legend as a text block at the top: colour key, abbreviations, and the reminder *"a rule with no green cards is under-specified"*.
- Keep card text inside the sticky budget rather than shrinking the font — cut the why to one clause before cutting the data.
- After the review, recolour answered reds and move them under their rule; the board stays alive as the story's acceptance-test inventory instead of dying as workshop residue.

## As a Document

No board available — same grammar in Markdown: the story as a blockquote, one subsection per rule with its examples as bullets, questions as a final checklist. Keep the colour grammar visible with 🟨🟦🟩🟥. All shape diagnostics still apply; count what a board would show.

## From Map to Work

| Card | Becomes |
|---|---|
| Green | One acceptance test each — formulation into Given/When/Then (`behavior-driven-development`), or the unit-test list for the rule's implementation. |
| Red | The review / three-amigos agenda; then a doc edit, a new rule, or a new example. Unanswerable ones become spikes or tickets (`ticket-writer`). |
| Blue | The spec's rule list. If the map's blues disagree with the doc's structure, restructure the doc — the map is how readers actually reason. |

## Quick Checklist

- [ ] One yellow card, and it fits in a sentence?
- [ ] Off-stage rules (exclusions, defaults, ties, collapses) have their own blue cards?
- [ ] Every green card: concrete data, one rule, outcome + one-line why?
- [ ] Every doc example placed *and verified* against its rule (audit mode)?
- [ ] Derived `NEW` examples for every rule the doc never illustrates?
- [ ] Reds phrased answerable-in-one-sentence, parked not resolved?
- [ ] Shape read out loud: hotspot column, empty columns, red count?
- [ ] Map handed onward — reds as agenda, greens as test inventory?

## Reading

- **Matt Wynne**, "Introducing Example Mapping" — cucumber.io blog (2015); the original write-up.
- **draft.io**, [Example Mapping guide](https://draft.io/example/example-mapping) — the layout conventions this skill follows.
- **Gojko Adzic**, *Specification by Example* — the book-length case for illustrating rules with examples.
- Companion skills: `behavior-driven-development` (discovery → formulation → automation), `splitting-user-stories` (when the map says the story is too big), `ticket-writer` (turning reds into tickets), `process-level-event-storming` (when the gaps are in the process flow, not the rules).
