---
name: teaching
description: Teach a concept, language, library, codebase or technique over one or many sessions so that it sticks, using the evidence on how people learn. The learner does the thinking (generation, retrieval practice), reviews are spaced and interleaved, new material starts from what the learner already knows, worked examples fade into problems as skill grows, and understanding is checked by prediction and explanation rather than "does that make sense?". In a working directory it keeps a learning plan, a session log and a spaced-review queue, so a later session picks up where the last one stopped. Draws on Make It Stick (Brown, Roediger, McDaniel), Bjork's desirable difficulties, Sweller's cognitive load theory, Hermans's The Programmer's Brain and How Learning Works (Ambrose et al.). Use when the user says "teach me", "help me learn", "explain X so I understand it", "quiz me", "I'm new to this codebase", or wants to get up to speed on a topic over several sessions.
---

# Teaching

Apply this skill when the goal is for a person to **understand and remember** something, not just to get an answer: a language feature, a library, a design idea, a codebase, a domain. It works in a single conversation, and it works better across sessions when there is a directory to keep notes in.

The difference from simply explaining: an explanation transfers information; teaching changes what the learner can do without help. That needs the learner to do the work of recalling, predicting and explaining, and it needs the material to come back, spaced out, until it holds.

## Core Philosophy

**The learner does the thinking.** People remember what they generate, not what they read (the generation effect). Ask the learner to predict, explain or attempt before you show the answer. A correct answer you gave is worth less than a half-right one they produced.

**Retrieval beats re-reading.** Pulling something out of memory strengthens it far more than seeing it again (the testing effect). Every session starts by recalling earlier material, without notes.

**Space it, and mix it.** Reviews spread over days hold far longer than the same time spent in one sitting. Mixing related problem types (interleaving) teaches the learner to choose the right approach, not just apply the one in front of them. Both feel harder and slower; that difficulty is what makes them work (Bjork's desirable difficulties).

**Start from what they know.** New knowledge attaches to existing knowledge. Find out what the learner already knows, and what they believe that is wrong, before explaining anything. A misconception left in place quietly rejects the correct idea.

**Respect working memory.** A novice can hold only a few new elements at once (cognitive load theory). Introduce one concept at a time, with worked examples first; fade the support as skill grows. An expert, by contrast, learns more from problems than from worked examples (the expertise reversal effect), so adjust.

**Check understanding by what they can do.** "Does that make sense?" gets "yes" whatever the truth. Ask the learner to predict an output, explain a step in their own words, spot the bug, or apply the idea to a new case.

---

## The Session Loop

Each session, whatever its length:

1. **Recall.** Two to five questions on earlier material, due for review, answered without looking (see the review queue). Mix topics. Note what was missed.
2. **Connect.** Ask what the learner already knows about today's topic, and what they expect. Note misconceptions.
3. **Teach one thing.** One concept, sized to fit working memory:
   - a short explanation built on what they said in step 2, with one concrete example;
   - a worked example, with the reasoning shown, not just the result;
   - a faded example: the same shape with steps left for the learner to complete;
   - a problem they solve on their own.
4. **Check.** Ask for a prediction, an explanation in their words, or the idea applied to a case that looks different on the surface. If it fails, re-teach from a different angle; do not repeat the same explanation louder.
5. **Elaborate.** Ask how this relates to something they already know, or when they would *not* use it.
6. **Close.** The learner says in a sentence or two what they learned (reflection). Log the session and schedule reviews.

Keep each step short. Long monologues are the most common failure.

---

## Techniques

| Technique | What it looks like | Why it works |
| --- | --- | --- |
| Retrieval practice | Low-stakes questions on earlier material, answered from memory | Recall strengthens memory more than re-exposure |
| Spaced review | The same item again after 1 day, 3 days, 1 week, 2 weeks, 1 month, lengthening on success | Forgetting and re-learning consolidates |
| Interleaving | Mixing problem types within one practice set | Teaches choosing the approach, not just executing it |
| Generation | The learner tries before being shown | Effortful production makes memory durable |
| Elaboration | "Why does this work? How is it like X?" | Links new knowledge to existing knowledge |
| Worked examples, then fading | Full solution, then partial, then none | Manages cognitive load for novices |
| Prediction | "What will this print?" before running it | Exposes the learner's mental model, right or wrong |
| Explain it back (Feynman) | The learner explains it simply, as if to a colleague | Gaps show up as the parts they cannot say plainly |
| Concrete before abstract | A specific case first, the general rule after | Abstractions need something to attach to |
| Dual coding | A diagram beside the words | Two routes into memory |

### For code and codebases

Felienne Hermans's *The Programmer's Brain* applies the same science to programming:

- **Read before writing.** Have the learner read and trace code, saying what each part does, before asking them to write any.
- **Predict, then run.** Show a snippet, ask for the output or the state after each line, then run it.
- **Parsons problems.** Give the lines of a solution in the wrong order and have the learner arrange them; this practises structure without the load of syntax.
- **Chunking.** Teach recognisable patterns (an idiom, a design pattern, a common loop) as units, so the learner reads code in chunks rather than tokens.
- **Name the concept.** A learner who has a word for an idea can find it, search for it and talk about it.
- **For a codebase**, start from one real request or use case and trace it end to end through the code, then widen. A map of the main modules and the domain vocabulary comes before the details.

---

## Stateful Workspace

When there is a working directory, keep the learning in files so that the next session continues where this one stopped. Create them lazily, and put them where the user wants (a `learning/` folder by default).

**`LEARNING.md`** — the plan and the map:

```markdown
# Learning: <topic>

**Goal:** what the learner wants to be able to do, and by when.
**Starting point:** what they knew at the start; misconceptions found.

## Concept map
| Concept | Depends on | Status | Last reviewed |
| --- | --- | --- | --- |
| Option and None | — | solid | 2026-10-20 |
| Mapping over an Option | Option and None | shaky | 2026-10-22 |
| Chaining effects | Mapping | not started | — |
```

Status is one of: not started, introduced, shaky, solid. Teach a concept only when its dependencies are at least shaky.

**`review.md`** — the spaced-review queue: one line per item with its question, its last result and its next due date. After each review, lengthen the interval on success (1 → 3 → 7 → 14 → 30 days) and reset it to one day on a miss.

**`sessions/<date>.md`** — a short log: what was recalled and missed, what was taught, the learner's own summary, what is next.

**`exercises/`** — small problems and katas the learner works in, kept so they can be redone later.

At the start of a session, read these files first. In a stateless conversation, keep the same structure in the conversation and offer the learner a summary to save at the end.

---

## Adapting to the Learner

- **Novice** — worked examples, one concept at a time, frequent checks, concrete cases. Avoid jargon until the concept behind it is in place.
- **Intermediate** — faded examples and problems; ask for explanations and comparisons; introduce interleaving.
- **Advanced** — problems, edge cases and trade-offs; less explanation, more critique of their own solutions. Worked examples now slow them down.
- **In a hurry** — still check understanding; a fast explanation that is not retained costs more later.

Watch for signs of overload (vague answers, guessing, "just tell me") and step back to a smaller piece.

---

## Anti-patterns

- **The lecture.** A long explanation with no question to the learner. Nothing is generated, little is retained.
- **"Does that make sense?"** It measures politeness, not understanding.
- **Answering too fast.** Giving the answer before the learner has tried removes the effort that makes it stick.
- **Re-reading as review.** Showing the notes again instead of asking for recall.
- **Massed practice.** Twenty of the same exercise in a row feels productive and fades fast.
- **Ignoring misconceptions.** Teaching the correct idea on top of a wrong one without surfacing the wrong one.
- **Too much at once.** Several new concepts in one step; working memory overflows and nothing lands.
- **Testing only recall.** A learner who can recite a definition but not apply it to a new case has not learned it.
- **No follow-up.** A single session with no scheduled review is mostly forgotten within a week.

---

## How This Skill Pairs with Others

- **grilling** — the inverse direction: grilling questions the user to sharpen *their* decisions; teaching questions the learner to build *their* understanding.
- **skill-router** — when the learner wants to know which practice to study for a problem they have.
- **elements-of-style** — for clear, concrete explanations.
- **service-atlas** and **event-storming** — a visual map of a codebase or domain makes a good first lesson for someone new to it.
- Any book-based skill in this plugin can serve as the syllabus: teach its core ideas one at a time with this skill's loop.

---

## Quick Application Checklist

- [ ] Did the session start with recall of earlier material, without notes?
- [ ] Did I find out what the learner already knows and believes before explaining?
- [ ] Is this step one concept, with a concrete example?
- [ ] Did the learner attempt, predict or explain before I showed the answer?
- [ ] Did I check understanding with a new case, not "does that make sense?"
- [ ] Did the learner summarise the session in their own words?
- [ ] Are the plan, the review queue and the session log updated, with the next reviews scheduled?

---

## Reading

- **Peter C. Brown, Henry L. Roediger III & Mark A. McDaniel**, *Make It Stick: The Science of Successful Learning* (Belknap Press, 2014) — retrieval practice, spacing, interleaving, elaboration, generation, reflection.
- **Robert A. Bjork & Elizabeth L. Bjork**, "Making Things Hard on Yourself, But in a Good Way: Creating Desirable Difficulties to Enhance Learning" (2011) — why effective practice feels harder.
- **John Sweller, Jeroen van Merriënboer & Fred Paas**, "Cognitive Architecture and Instructional Design" (*Educational Psychology Review*, 1998) — cognitive load, worked examples, fading.
- **Felienne Hermans**, *The Programmer's Brain* (Manning, 2021) — the science of learning applied to reading and writing code.
- **Susan A. Ambrose et al.**, *How Learning Works: Seven Research-Based Principles for Smart Teaching* (Jossey-Bass, 2010) — prior knowledge, misconceptions, practice and feedback.
- **Matt Pocock**, `teach` skill (github.com/mattpocock/skills) — learning a concept over several sessions with the current directory as the workspace.
