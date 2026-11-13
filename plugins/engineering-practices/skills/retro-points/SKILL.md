---
name: retro-points
description: Turn a discussion into retrospective points for a team's daily retro. Called on the current conversation, a pasted thread, a file, or a ticket or PR, it finds what slowed the team down, traces each item from event to pattern to the structure and belief behind it, names the system archetype, proposes one structural experiment per pattern, scores it for impact, and recommends what the retro should open with. Built on Kerth's Prime Directive, Derby & Larsen's phases, Toyota Kata's daily improvement cycle, a multi-branch 5 Whys repaired with Allspaw's "how" questions and stopping rules, the systems-thinking iceberg, archetypes and causal loops, Meadows' leverage points, and Leopold's blocker clustering. Also covers running the 12-minute daily retro, the impact scorecard, the experiment card and the weekly review. Use when the user runs /retro-points, says "retro points", "what should we bring to the retro", "5 whys this", "what slowed us down", "why does this keep happening", or when retro actions never land. For improving a coding agent's own environment after a session, use agent-retro instead.
---

# Retro Points

## When invoked

**Input.** Use what follows the command:
- nothing: the current conversation, from its start;
- pasted text: that discussion (a Slack thread, meeting notes, an incident timeline);
- a file path: read it;
- a ticket or PR link: read it and its comments, using the connected tools.

Read the whole discussion before writing. Gather evidence: ticket and PR numbers, commits, timestamps, error names, quoted decisions.

**Output, in this order:**

1. **Retro points table**, at most eight rows, highest score first:

   | # | What happened | The pattern underneath | Structure or archetype | Candidate experiment | Score |
   |---|---|---|---|---|---|

   - *What happened:* concrete events with a pointer (ticket, PR, time). Several events per row when they share a pattern.
   - *Pattern:* what keeps happening, in one sentence.
   - *Structure or archetype:* the rule, pipeline, ownership or information gap that produces it, the archetype in bold, and the belief that keeps it in place when the discussion shows one.
   - *Candidate experiment:* one structural change, phrased so it can be tested.
   - *Score:* the impact scorecard total, out of 16.
2. **Suggested order:** which point the retro should open with and why (highest score on the binding flow), the cheapest high scorer next, and which points need another team, so they go to the weekly review.
3. **Experiment card** for the top point, filled in as far as the discussion allows.

**Rules for the points:**
- Friction counts whatever its kind: waits, rework, wrong assumptions, late review findings, environment and tooling gaps, handoffs, unclear tickets, cross-team dependencies.
- Three similar events beat one dramatic one. Cluster before writing.
- Keep people out of the cause column. Write "the review queue had no age signal", not "the reviewer was slow".
- Never invent an event. If the discussion lacks the evidence for a column, say so in the cell.
- Mark a structure you inferred, rather than saw stated, as a hypothesis for the retro to check.
- Write plainly: one idea per sentence, no jargon a teammate outside the thread wouldn't know.

The rest of this skill is the method behind the points, and the playbook for running the retro itself.

## The method

A daily retro works when it behaves like a small improvement cycle, not a mini sprint retro: **one target condition, one obstacle chosen from data, one experiment with a stated expectation, and a check of yesterday's experiment.** Most days end after the check. That is success, not failure.

The aim is not to explain one bad day. It is to find the **structure** that keeps producing bad days and change that. Deming estimated that 94% of troubles belong to the system, not the people in it. Treat a person-shaped cause as a sign you stopped too early.

### What a retro is for

Each layer below depends on the one before. A retro that skips one degrades in a predictable way.

| Layer | Source | Without it, the retro becomes |
|---|---|---|
| Safety: "everyone did the best job they could, given what they knew at the time" | Kerth's Prime Directive | A status meeting, or blame |
| Data: how work actually moved, not how people feel | Kanban service delivery review | Whatever annoyed the loudest person |
| Insight: causes below the symptom | Derby & Larsen, "generate insights" | Corry's "Wheel of Fortune": symptoms fixed, issues return |
| One change, tested | Scrum Guide: "the most impactful improvements are addressed as soon as possible"; Toyota Kata | Venting |

### Set-up, once

1. **Target condition.** One team-level goal with a flow metric. Examples: "no PR waits more than 4 working hours for first review", "a fix is verified before it reaches production", "no booking stays blocked more than one day".
2. **Friction triggers.** Agree thresholds that put an item on the list automatically, the way Google defines postmortem triggers in advance: blocked more than N hours, waited in review more than X hours, reopened, bounced between people or teams, blocked on an environment, found by a customer before us.
3. **Blocker log.** Item, start, end, hours lost, internal or external, cluster. It feeds selection and the weekly review.
4. **Words.** Banned: "should have", "failed to", "human error", "root cause" (singular). Use "contributing conditions" instead.
5. **Run the format as an experiment** for four weeks, then keep it, change it or drop it.

### The daily retro: 12 minutes, straight after stand-up

| Step | Time | Questions |
|---|---|---|
| 1. Check the last experiment | 2 min | What did we expect? What happened? What did we learn? Keep, adapt or drop? Does the obstacle list change? |
| 2. Pick one item | 1 min | Which friction tripped a trigger since yesterday? Which cost the most hours against the target, or hit our bottleneck? Can we change it, influence it, or is it "soup"? Soup is logged, not discussed. |
| 3. Walk the timeline | 3 min | Take one concrete ticket, PR or incident. Where did it wait? At each wait: what were people seeing, expecting and juggling? How did it make sense at the time? What did a fast item have that this one lacked? |
| 4. Dig down several branches | 3 min | Ask 2–3 whys down each of 2–3 branches: people, process, tooling, information. If a branch names a person, reframe: "assume everyone did everything right, how did this still happen?" |
| 5. Go below the waterline | 2 min | Is this a pattern? How often is it in the log? Which structure (rule, pipeline, ownership, information) makes it likely? Does it match an archetype? "If we had done this on purpose, what would we have been thinking?" |
| 6. Choose one experiment, or none | 1 min | Score the candidates, pick the top one, write the card, put it on the board. |

#### Digging: 5 Whys, repaired

5 Whys builds one chain, and the root cause is wherever the team stops. It tends to stop at a person ("the reviewer should have looked sooner"), which produces "be more careful" actions that change nothing (Allspaw, Cook, Card, Dekker). Keep asking, but change the shape:

- **Several branches, not one chain.** A fishbone-lite: people, process, tooling, information.
- **"How" before "why"** at each wait: what were you seeing, expecting, juggling? (Allspaw's Infinite Hows.)
- **Compare a slow item with a fast one.** It breaks the single-cause illusion quickly.
- **A fix at every level, in proportion to the cost** (Ries). The proportion is the stopping rule that protects the timebox.

**Stop a branch when** it reaches a condition the team controls and can test this week, when it leaves the team's sphere (log it and escalate with the hours attached), or when the timebox runs out. **Never stop** at a person or a "should have"; reframe and continue.

#### Below the waterline

Use the `systems-thinking-iceberg` skill for the full method. In a retro, one question per level is enough:

| Level | Question | Action mode |
|---|---|---|
| Event | What happened? | React: fix this instance |
| Pattern | How often, since when? | Adapt: work around it |
| Structure | What rule, pipeline, ownership or information produces it? | Create: change what produces it |
| Mental model | What belief makes this structure seem reasonable? | Reflect: name and test the belief |

Archetypes you will hear in a software team:

| Archetype | What it sounds like | Structural lever |
|---|---|---|
| Fixes that fail | "Same issue again", hotfix then regression | Fix the class of failure; review over 3–4× the delay |
| Shifting the burden | "Ask X, she knows", "QA will catch it", "we'll check it in prod" | Fund the fundamental fix; make the workaround's cost visible |
| Tragedy of the commons | Broken shared staging, flaky CI nobody owns | A named owner or rotation; environments as code |
| Limits to growth | Review queue grows with headcount | Remove the constraint instead of pushing harder |
| Eroding goals | "Done" quietly means "merged"; "flaky is normal" | Anchor the standard in a gate or a definition of done |

When a cluster keeps returning, draw a causal loop in the weekly review: 3–5 variables, arrows marked *s* (same direction) or *o* (opposite), and `||` for a delay. An even number of *o*'s makes the loop reinforcing; an odd number makes it balancing.

#### Choosing the action

Most retro actions sit on Meadows' weakest rung, changing a number, which "RARELY CHANGE[S] BEHAVIOR". A team can reach higher rungs: shorter delays, stronger feedback loops, new information flows, rules and goals.

**Impact scorecard.** Score each candidate 0–2 per row, take the highest total, and break ties by the cheaper option.

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Iceberg level | Event: fixes this instance | Pattern: works around it | Structure or belief: changes what produces it |
| Meadows rung | A number (timeout, limit, headcount) | A buffer or one-off step | A delay, feedback loop, information flow, rule or goal |
| Class removed | This ticket only | Part of this cluster | Every future instance |
| Constraint | Off the bottleneck | Near it | On the binding flow (review, environment, verification, deploy) |
| Burden | Shifts work to a hero or another team | Neutral | Builds capability, removes a handoff |
| Durability | Needs reminders | Needs a habit | Self-enforcing (gate, default, owner) |
| Measurable | No signal | Anecdotal | A metric from the log or pipeline |
| Cost, inverted | More than a week | Days | Today or tomorrow |

**Experiment card.** *Obstacle:* … *If we* ⟨change⟩, *then* ⟨metric⟩ *moves from* ⟨baseline⟩ *to* ⟨expected⟩ *by* ⟨date⟩. *Data source:* … *Owner:* one name. *Review:* when the effect should show, allowing 3–4× the expected delay. *Learned:* …

#### Making actions stick

- At most one action a day, and none is fine. Derby & Larsen allow one or two per iteration.
- Put the card on the same board as delivery work.
- Open every session by checking it.
- Drop actions nobody adopts instead of carrying them forward.
- Obstacles are not action items. The obstacle list is the team's current understanding, and it shrinks and changes as experiments teach.
- Prefer self-enforcing changes: a CI gate, a default, an owner. They outlast reminders.
- Track the retro itself: open actions and their age, the share closed by the next check, recurrence per cluster.

### The weekly review: 30 minutes

1. Total blocked hours per cluster from the blocker log (Leopold's blocker clustering). Put clusters on a cost-to-fix against impact grid.
2. Draw one causal loop for the cluster that keeps returning.
3. Check the target condition, and reset it if the team has reached it.
4. Prune stale cards.
5. Escalate structural items outside the team's control, with their hour totals attached.

### Anti-patterns

| Anti-pattern | Sign | Remedy |
|---|---|---|
| Wheel of fortune | Jumping from complaint to action | Walk the timeline and dig before deciding |
| In the soup | Re-venting about what the team can't change | Sort: change, influence, soup |
| Dot-vote drift | The team votes away its worst problem | Pick from triggers and blocked hours, not popularity |
| Number tweaks | Every action is a timeout, limit or reminder | Score on Meadows' rungs; aim for information, rules, feedback |
| Action pile | Open actions grow; the same items return reworded | One action at most; drop what nobody adopts |
| Status creep | The slot becomes task tracking | Ban status talk; end early when nothing tripped |
| Blame | "Should have", a name in the cause column | Reframe with the Prime Directive and "how" questions |

## How solid the evidence is

No controlled study compares daily with sprint retros, iceberg retros with ordinary ones, or 5 Whys with its alternatives in software teams. The principles come from lean (Toyota Kata, A3), safety science (Cook, Allspaw, Dekker, Leveson) and system dynamics (Meadows, Senge, Kim). The playbook and scorecard are a synthesis, so run them as an experiment the team is free to change.

## Related skills

- `systems-thinking-iceberg`: the full iceberg method, archetypes and leverage points.
- `toyota-kata`: the improvement and coaching kata the daily cycle borrows from.
- `agent-retro`: a retrospective on a coding-agent session instead of a team's work.
- `elements-of-style`: for writing the cards and the summary plainly.

## Sources

- Norm Kerth, *Project Retrospectives* (2001), the Prime Directive.
- Esther Derby & Diana Larsen, *Agile Retrospectives* (2006; 2nd ed. 2024).
- Scrum Guide (2020); Agile Manifesto principles.
- Mike Rother, *Toyota Kata* (2009) and *The Toyota Kata Practice Guide* (2017).
- Eric Ries, "Five Whys" (2008).
- John Allspaw, "The Infinite Hows" (2014); Richard Cook, "How Complex Systems Fail" (1998); Alan Card, *BMJ Quality & Safety* (2017); Sidney Dekker, *The Field Guide to Understanding 'Human Error'*.
- Google SRE book, "Postmortem Culture" (2017).
- Donella Meadows, "Leverage Points: Places to Intervene in a System"; Peter Senge, *The Fifth Discipline*; Daniel Kim, *The Systems Thinker* archetype articles.
- Klaus Leopold and Troy Magennis on blocker clustering (InfoQ, 2014); Aino Vonge Corry, retrospective antipatterns.
- W. Edwards Deming on the system; Will Larson, "Systems thinking" (2018).
- DORA, learning culture capability.
