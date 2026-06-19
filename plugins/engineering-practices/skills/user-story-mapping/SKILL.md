---
name: user-story-mapping
description: Apply Jeff Patton's User Story Mapping (O'Reilly, 2014) — arranging user stories into a two-dimensional map that preserves the user's narrative journey, which a flat backlog destroys. Covers the map's anatomy (backbone/spine and ribs; activities → tasks → details; user tasks as short verb phrases), the two axes (narrative flow left-to-right, priority/necessity top-to-bottom), the core philosophy (shared understanding over documents; minimize output, maximize outcome and impact), running a mapping workshop (frame, map breadth-first, explore alternatives/exceptions, distill a backbone, slice), slicing releases into a walking-skeleton MVP and a release roadmap anchored on target outcomes, and Patton's five common mistakes. Use when planning a product, release, or feature; when a flat backlog has lost the big picture; when carving an MVP or first release that still tells a complete story; when running a discovery or release-planning workshop; or when framing work by user journey and outcome rather than a feature list.
---

# User Story Mapping (Jeff Patton)

Apply this skill when planning a product, a release, or a sizeable feature; when a flat
backlog has turned into a pile of disconnected stories nobody can see the shape of; when you
need to carve a genuine MVP that still tells a complete story end-to-end; when running a
discovery or release-planning workshop; or whenever you want to reason about work by the
**user's journey and the outcome you're after** rather than a feature checklist.

A story map is a simple idea: lay the user's story out left-to-right in the order it happens,
break each step down top-to-bottom, and you get a two-dimensional picture that a one-dimensional
backlog throws away. The map is a tool for *building shared understanding*, not a document to
hand off.

## Core Philosophy

**The goal is shared understanding, not documents.** Patton's central claim: *"Shared documents
are not shared understanding."* Good design documents are *"like vacation photos"* — they help the
people who were in the room relive and recall the conversation, but they fail to give the same
information to anyone who wasn't there. The book's section titles say it plainly: *"Building
Shared Understanding Is Disruptively Simple,"* *"Stop Trying to Write Perfect Documents,"* *"Good
Documents Are Like Vacation Photos."* Kent Beck's line, quoted in the book, is the slogan:
*"Stop exchanging documents. Tell me your story."* (Patton is **not** anti-document — he advocates
"talk and doc": write to externalize and capture the thinking *during* the conversation. The
target is the static document mailed between absent parties.)

**Minimize output; maximize outcome and impact.** Distinguish the three:
- **Output** — what you build (features, releases). Easy to measure, easy to over-produce.
- **Outcome** — what users can now *do*, or do better/faster, because of what you built.
- **Impact** — the business result that follows from that outcome.

The job is to *build less* — the least output that produces the outcome you want. A story map
makes "build less" concrete by letting you slice off the smallest thing that still achieves a
real outcome.

**The map preserves the story a flat backlog destroys.** A prioritized list is one-dimensional:
it tells you order but loses the *whole* — who the user is, what they're trying to accomplish, and
how the pieces fit into one journey. The map keeps the journey intact and uses the second
dimension for priority.

**A story is a token for a conversation.** Building on Ron Jeffries's *Three C's* — **Card,
Conversation, Confirmation** — the card is a placeholder, not a spec. The real value is the
shared understanding the conversation creates. The map is a backdrop that keeps those
conversations anchored in the user's whole story.

---

## The Problem: a Flat Backlog Is "a Bag of Context-Free Mulch"

Agile teaches us to split big requirements into small, story-sized chunks. The unintended side
effect, in Martin Fowler's words (from his foreword), is that you end up with *"a jumble of
pieces that don't fit into a coherent whole"* — you lose the big picture. Patton is blunter: a
flattened backlog is *"a bag of context-free mulch."*

His tree metaphor makes the loss vivid. Think of the work as a tree:

```
        goals        ← the trunk
          │
       users         ← the branches
          │
   capabilities      ← the twigs
          │
      stories        ← the leaves
```

Flatten that into a single prioritized list and you've **ripped the leaves off and cut down the
tree** — the structure that gave each story its meaning is gone. Fowler's one-sentence summary of
the whole book: *"Story mapping is a technique that provides the big picture that a pile of
stories so often misses."*

The cure is to stop flattening. Keep the structure visible as a map.

---

## Anatomy of a Story Map

A story map is built from one kind of thing, arranged in two dimensions.

**The building block is the user task** — *"short verb phrases that are the basic building block
of a map."* A task is something a person *does* to reach a goal: "search for a flight," "read
message," "pay for order." If every card on your wall is a **noun** (a thing, a feature, a
screen) rather than a **verb phrase** (a step someone takes), you've drawn a *feature
decomposition*, not a story map. The noun-vs-verb tell is the quickest way to check you're
actually mapping a story.

Tasks aggregate upward into **activities** (higher-goal-level groupings — "manage email") and
break downward into **sub-tasks, details, alternatives, and exceptions**.

**The spine-and-ribs structure.** In Patton's words: *"Activities and tasks at a higher goal
level give the story map its structure. The backbone is arranged in a narrative flow. Smaller
sub-tasks, details and variations hang down to form the ribs connected to the backbone."* The big
items across the top are the *"essential capabilities the system needs to have"* — Patton calls
them the **backbone** (they look a little like **vertebrae**); the cards hanging below are the
**ribs**.

```
narrative flow  ──────────────────────────────────────────────────────────────►
(the order you'd tell the user's story)

ACTIVITIES /   Check mail        Compose          Organize         Search
BACKBONE       ──────────        ─────────        ──────────       ────────
(top = the
 vertebrae)
                  │  │  │           │  │  │          │  │  │          │  │  │
TASKS          open inbox        write msg        file in folder   by sender
(verb-phrase   read message      attach file      flag / star      by date
 ribs)         mark as spam      send message     delete message   filter unread
               ▲
               │  the same activity ("manage email") breaks into tasks:
               │  "send message", "read message", "delete message", "mark as spam"
priority /
necessity
   ▼   high on the map = must-have; lower = can wait
```

A concrete instance Patton uses: the activity **"manage my email"** decomposes into the tasks
**"send message," "read message," "delete message," "mark message as spam."**

---

## The Two Axes

The power of the map is that the two directions mean different things, and they're independent.

**Horizontal — narrative flow (left → right).** Order the backbone *"in the order you'd tell the
story about your user to someone else"*: earlier actions on the left, later ones on the right.
The test Patton gives — *"the order you'd explain the behavior of the system in is the correct
order."* This is **telling order**, roughly time, **not** a precise workflow. He's explicit:
*"if you're looking for the precision of a workflow model, flow chart, or UML model, then a story
map isn't your best choice."* Don't agonize over every branch and loop; tell the main story.
(Left-to-right follows Western reading direction — flip as needed.)

**Vertical — priority / necessity (top → bottom).** Within each step, stack the tasks by how
essential they are: *"Place them high to indicate they're absolutely necessary, lower to indicate
they're less necessary."* Lower can also mean richer/more sophisticated versions of the same step.
This axis is what you slice for releases.

---

## Build the Map: the Workshop Flow

Patton's chapter on building a map is titled *"You Already Know How"* — the technique is
deliberately low-ceremony. The flow:

### 1. Frame the work
Agree who the user is and what outcome you're after *before* you write cards. Know the
**beginning and the end** of the story you're about to tell.

### 2. Map the big picture — breadth first
Write the backbone of activities/tasks left-to-right across the whole journey, **beginning to
end, before dropping into detail.** Patton's heuristic: ***"mile wide, inch deep"*** to start.
*"Make sure you know the beginning and end to your story before you start. Then, get from
beginning to end before dropping down into detail."* Resist the urge to perfect step one before
you reach step two.

### 3. Explore — go deep where it matters
Now break the high-level tasks down into **sub-tasks, alternative tasks, exceptions, and
details**. The book's section titles for this are *"Organize Your Story"* and *"Explore
Alternative Stories."* This is where variations, edge cases, and "what about…" live — as ribs
hanging under the relevant step, not as a new spine.

### 4. Distill the backbone
*"Distill Your Map to Make a Backbone"* — pull the high-level activities back up into a clean top
row so anyone can read the whole story at a glance. Detail stays below; the spine stays legible.

### 5. Slice into releases
Draw horizontal lines across the map to carve out releases (next section).

A finished first-pass map is wide (the whole journey) and only as deep as it needs to be to make
decisions. Photograph it; expect to redraw it as understanding deepens. The artifact is
disposable — the **shared understanding is the product.**

---

## Slice Releases: the Walking Skeleton and the MVP

Release planning *is* slicing the map horizontally. Patton: *"I take a long strip of masking tape
and line off the story map — creating horizontal swim lanes for each release."*

**The top slice is the walking skeleton.** *"All the stories placed high on the story map
describe the smallest possible system you could build that would give you end-to-end
functionality"* — Alistair Cockburn's *walking skeleton*. It's thin but **complete**: it runs the
whole journey, however minimally. The rule of thumb: *"The smallest number of tasks that allow
your specific target users to reach their goal compose a viable product release."* The book's
sections are *"Slice Out a Minimum Viable Product Release"* and *"Slice Out a Release Roadmap."*

**Every slice must still tell a whole story.** A release slice goes *across* the journey, picking
one task per step — never down one step to completion while others have nothing. Patton's image:
***"that way we never release a car without brakes."*** The failure mode is building half a
product per step (a *"half-built product"*) instead of a complete-but-minimal product.

```
              Step A        Step B        Step C        Step D
            ┌───────────────────────────────────────────────────┐
 SLICE 1    │  thinnest A    thinnest B   thinnest C   thinnest D │  ← walking skeleton:
 (MVP)      │                                                     │     a whole journey, minimal
            ├───────────────────────────────────────────────────┤
 SLICE 2    │  richer A      richer B     (—)          richer D   │  ← next outcome
            ├───────────────────────────────────────────────────┤
 SLICE 3    │  …             …            …            …          │  ← later outcome
            └───────────────────────────────────────────────────┘
   DO:   slice across (a complete thin journey)
   DON'T: finish Step A top-to-bottom before starting Step B (a car with no brakes)
```

This is the same idea the [`splitting-user-stories`](../splitting-user-stories/SKILL.md) skill
calls *vertical slicing* and *MVP / walking skeleton / steel thread / cupcake*. Reach for that
skill for the splitting-pattern catalog (INVEST, Lawrence's nine patterns, SPIDR, the hamburger
method); reach for this one to lay out the **whole** journey those slices cut across.

---

## Prioritize Outcomes, Not Features

A story map tempts you to ship "everything in step one, then everything in step two." Resist it.
The book's instruction is a chapter heading: ***"Don't Prioritize Features — Prioritize
Outcomes."***

Anchor each release slice on a **target outcome**, not a bundle of features:

1. Pick the **specific target users** for this release.
2. Describe **how they'll do things better** — *"What will they be faster at? Better at?"*
3. Name **a few metrics** that would move if you succeeded. *"These are your outcomes."*
4. Slice the map to the smallest set of tasks that delivers that outcome.

Patton's promised payoff: *"When you anchor each release on a target outcome, you'll find each
release is smaller and more successful than you ever thought possible."* (Aspirational rhetoric —
but the mechanism is real: an outcome is a sharper knife than a feature list.)

For driving the *choice* of outcome from business goals, pair this with Gojko Adzic's **impact
mapping** (goal → actors → impacts → deliverables) — it answers "which outcome?"; story mapping
answers "what's the smallest journey that delivers it?"

---

## Mapping a Single Feature

A common objection: *"I hate story maps because I need to map the whole product when I'm just
trying to add a single feature."* Patton's answer: **no, you don't.**

*"Just map that feature. Just map the story of the new feature. Start the story when users first
touch it. End the story with them successfully using it and getting value."* You get a
right-sized map that tells the story of that one feature. (Optionally keep a high-level
whole-product backbone alongside, just to see where the feature plugs into the larger journey.)

---

## Five Common Mistakes

Patton's own list of the five most common story-mapping mistakes:

1. **Losing the story.** Cards drift into a feature list (all nouns). Keep them verb phrases;
   keep them in narrative order. If you can't read the wall as a story, it isn't a story map.
2. **Getting lost in the details.** Breaking every step down too early yields *"potentially
   hundreds of cards — way too much detail to make sense of."* Map *mile wide, inch deep* first;
   go deep only where a decision needs it.
3. **Worrying too much about flow, branches, and what-abouts.** A map is telling order, not a
   flowchart. Capture the main story; park exceptions as ribs; don't model every branch.
4. **Mapping the whole product when you only want to add a feature.** Map just the feature's
   story (see above).
5. **Not anchoring releases on an outcome.** Slices that are feature bundles, not outcomes, grow
   without bound. Anchor each slice on a measurable change for specific users.

---

## Facilitation Tips

- **Get from end to end before going deep.** The first complete left-to-right pass is worth more
  than any one perfectly-detailed step.
- **Keep cards as verb phrases.** Quietly rewrite nouns into the action the user takes.
- **Let exceptions hang as ribs.** "What if payment fails?" is a card under the step, not a new
  spine and not a debate to resolve mid-flow.
- **Map with the people who'll build it.** The map is a conversation; the best estimates and the
  best edge cases come from the people who'll do the work. (See the *three amigos* practice in
  [`behavior-driven-development`](../behavior-driven-development/SKILL.md) for who to have in the
  room.)
- **Slice across, never down.** Every release lane is a complete thin journey.
- **Treat the wall as disposable.** Photograph it; redraw it as you learn. The understanding is
  the deliverable.

---

## Story Mapping in the Wider Toolbox

| Tool | What it's for | Relationship |
|---|---|---|
| **Flat product backlog** | Ordered list of work | Story mapping is the **structure**; the map *generates* a sensibly-ordered backlog without losing the big picture. Keep the map; treat the list as a projection of it. |
| **MVP thinking** | Smallest releasable thing that's still useful/learnable | The top slice of the map **is** an MVP / walking skeleton. The map keeps the MVP honest — a *whole* journey, not a half-built product. |
| **Impact mapping** (Adzic) | Choosing *which* outcome to pursue | Complementary. Impact mapping picks the outcome; story mapping finds the thinnest journey to deliver it. |
| **Scrum / Kanban** | Cadence and flow of delivery | Story mapping is upstream of both — it produces the outcome-anchored, sliced backlog that sprints pull from or that flows across a board. |
| **Event Storming** (Brandolini) | Discovering the domain's events & boundaries | A sibling workshop. Event storming explores *the system's* behavior; story mapping explores *the user's* journey. See [`event-storming`](../event-storming/SKILL.md). |

---

## When NOT to Reach for a Story Map

- **You need workflow precision.** Branch-heavy logic, state machines, exact sequencing — use a
  flow chart, BPMN, or UML. Patton says so directly.
- **There is no user journey.** Pure infrastructure or a batch job with no human narrative has no
  story to map (though even "ops" work often has an operator journey worth mapping).
- **A single tiny, well-understood change.** Mapping it is overhead; just write the story.
- **You're alone and only need to think, not align.** Solo mapping can clarify *your* thinking,
  but the method's real value is the **shared** understanding among people. Without others in the
  conversation, you have a personal sketch, not alignment.

---

## Quick Application Checklist

Framing:
- [ ] Do we know **who** the user is and **what outcome** we're after?
- [ ] Do we know the **beginning and end** of the story before we start?

The map:
- [ ] Is every card a **verb phrase** (a step someone takes), not a noun (a thing)?
- [ ] Does the backbone read **left-to-right as a story** ("…and then they…")?
- [ ] Did we get **end-to-end first** (mile wide, inch deep) before going deep?
- [ ] Do details, alternatives, and exceptions **hang as ribs** under the right step?
- [ ] Is the top row a clean, legible **backbone**?

Slicing:
- [ ] Is the **top slice a walking skeleton** — thin but a *complete* journey?
- [ ] Does each slice go **across** the journey (no car without brakes)?
- [ ] Is each release **anchored on a target outcome + metric**, not a feature bundle?
- [ ] Have we sliced for the **smallest** set of tasks that reaches the user's goal?

Hygiene:
- [ ] Did the **people who'll build it** help map it?
- [ ] Did we **photograph** the map and treat it as disposable?
- [ ] Are we using the map to drive **conversations**, not as a document to hand off?

---

## Heritage and Reading

- **Jeff Patton**, *User Story Mapping: Discover the Whole Story, Build the Right Product*
  (O'Reilly, 2014; ISBN 9781491904893) — the canonical text. Forewords by **Martin Fowler**,
  **Alan Cooper**, and **Marty Cagan**.
- **Jeff Patton**, *"It's All in How You Slice It"* (*Better Software* magazine, 2005) — the
  origin of release slicing ("design your project in working layers to avoid half-baked
  incremental releases"; the *"system span"* = "the smallest set of features necessary to be
  minimally useful in a business context"). **Terminology caveat:** this early article draws
  release slices as *horizontal* layers with *vertical* business-process lanes — the **opposite**
  axis labels from the 2014 book and modern usage, where release slices are *horizontal swim
  lanes* across the map. The concept (thin, end-to-end-usable slices) is identical; only the
  drawing convention flipped.
- **Jeff Patton**, jpattonassociates.com essays — *"The New User Story Backlog Is a Map"* (the
  mulch / tree / backbone-and-ribs framing), *"Why Documents Fail and What You Can Do About It"*
  (vacation photos), *"Five Common Story Mapping Mistakes,"* and the *"Story Map Concepts"* PDF
  (the one-page vocabulary reference).
- **Ron Jeffries**, *"Essential XP: Card, Conversation, Confirmation"* (2001) — the **Three C's**
  that ground "a story is a token for a conversation."
- **Alistair Cockburn** — the **walking skeleton**: a thin end-to-end implementation that
  exercises the whole system.
- **Gojko Adzic**, *Impact Mapping* (2012) — choosing the outcome a map should deliver.
- **Eric Ries**, *The Lean Startup* (2011) — MVP as a learning instrument.

### Related skills in this repo
- [`splitting-user-stories`](../splitting-user-stories/SKILL.md) — the splitting-pattern catalog
  (INVEST, Lawrence's 9 patterns, SPIDR, hamburger, MVP analogies) for the slices a map cuts.
- [`event-storming`](../event-storming/SKILL.md) — the sibling discovery workshop for the domain.
- [`ticket-writer`](../ticket-writer/SKILL.md) — turning mapped tasks into well-formed tickets.
- [`behavior-driven-development`](../behavior-driven-development/SKILL.md) — the three-amigos
  conversation and Gherkin confirmation for each story.
- [`running-lean`](../running-lean/SKILL.md) — outcome-driven, experiment-first product discovery.
