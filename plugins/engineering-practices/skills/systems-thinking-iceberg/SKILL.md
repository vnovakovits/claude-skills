---
name: systems-thinking-iceberg
description: Apply the systems-thinking iceberg — events, patterns, systemic structures, mental models (and Daniel Kim's fifth level, vision) — to explain why a problem keeps happening and where to intervene. Draws on Peter Senge's The Fifth Discipline (levels of explanation, archetypes), Daniel Kim's Vision Deployment Matrix and archetype work, Donella Meadows' Thinking in Systems and twelve leverage points, Peter Stroh's Systems Thinking for Social Change, and Deming/Ackoff on the system producing the behaviour. Covers the questions and response mode at each level, causal loops and delays, the archetypes that most often sit under the waterline, mapping structures to Meadows' leverage points, and reviewing a proposed process, policy or fix by asking which level it acts on. Use for recurring incidents, a "people keep doing X" complaint, a retro or post-incident review, a ways-of-working or governance proposal, or before choosing a fix.
---

# Systems Thinking Iceberg

Apply this skill when someone is about to fix a visible problem — an outage, a missed date, a process breach, a team "not following the process" — or is proposing a process, policy or reorganisation meant to stop one. The iceberg asks *which level the problem lives at* and *which level the proposed fix acts on*. Most fixes act on events; most problems live in structure and mental models.

## Core Philosophy

**The system produces the behaviour.** Senge: "structure influences behaviour". Deming: most variation in outcome comes from the system, not the worker. Put different people into the same structure and you get much the same results (the beer game). Blaming people for a recurring event is a sign the analysis stopped at the waterline.

**Leverage rises with depth.** Responding to an event changes one event. Changing a structure changes every future event it would have produced. Shifting a mental model changes which structures people build in the first place. Depth also costs more and takes longer — so the skill is choosing the right level, not always the deepest.

**Structure means more than the org chart.** In systems thinking, structure is what generates a pattern: feedback loops, delays, stocks and flows, incentives, rules, information flows, physical and digital layout, who decides what. A form, a metric, an approval step, a budget cycle and a dashboard are all structure.

**A fix is a hypothesis about structure.** Every proposed process change predicts that a pattern will change. State the pattern, the structure you believe causes it, and the leading indicator that will show whether you were right.

**The iceberg is a thinking aid, not a diagram to fill in.** The value is in the questions and the conversation, not the drawing. A level with a weak or invented answer is a finding: you don't yet understand the system well enough to act there.

---

## The Five Levels

Senge's *Fifth Discipline* gives three levels of explanation: events, patterns of behaviour, and systemic structure. Systems practitioners (Innovation Associates, the Academy for Systems Change, Stroh) add **mental models** beneath structure. Daniel Kim's Vision Deployment Matrix (*The Systems Thinker*, 1995) adds **vision** at the base.

| Level | What it is | Question to ask | Response mode (Kim) | Typical artefact |
|---|---|---|---|---|
| **Events** | What happened — a single, visible occurrence | What just happened? | **React** — fix, firefight, escalate | Incident, ticket, complaint, breach |
| **Patterns / trends** | What keeps happening — events over time | What has been happening? Is this new or recurring? What changed with it? | **Anticipate / adapt** — plan buffers, forecast | Behaviour-over-time graph, run chart, metric trend |
| **Systemic structures** | What produces the pattern | What loops, delays, incentives, rules, information flows and decision rights make this pattern likely? | **Design** — change the structure | Causal loop diagram, stock-and-flow, value-stream map, RACI |
| **Mental models** | Beliefs and assumptions that keep the structure in place | What must people believe for this structure to make sense? Who holds that belief? | **Reflect / transform** — surface and test assumptions | Ladder of inference, stated vs in-use assumptions |
| **Vision** | The future the system is actually serving | What future are we really optimising for — the espoused one or the one in use? | **Generate** — articulate a shared purpose | Purpose statement, strategy, intent |

Above the waterline: events (and often patterns, if anyone is charting them). Below: structure, mental models, vision.

### Questions per level, in more depth

**Events**
- What exactly happened, when, to whom? Separate observation from interpretation.
- What was the immediate response, and was it reactive by necessity or by habit?

**Patterns**
- Plot it. How often over the last 3–12 months? Is it rising, flat, cyclic, or tied to a calendar (quarter end, release day, budget cycle)?
- What other variables move with it? (Lead time and WIP; incidents and deploy batch size; escalations and unplanned work.)
- Is the pattern the same across teams, or only some? A shared pattern points to shared structure.

**Systemic structures**
- What feedback loops are at work? Name each one **reinforcing (R)** or **balancing (B)**.
- Where are the **delays**? Delays between action and effect cause overshoot and oscillation and make people over-correct.
- What are the **stocks** (things that accumulate: backlog, tech debt, approved-but-unstarted work, trust) and their **flows**?
- Who decides, with what information, on what timetable? Who sees the consequences of the decision — and how late?
- What gets rewarded, measured, reported, and funded? What is invisible?
- Which written rules does this structure include, and which unwritten ones?

**Mental models**
- What would a reasonable person have to believe to design it this way?
- Which beliefs are espoused (in the doc) vs in use (in behaviour)? (Argyris: espoused theory vs theory-in-use.)
- Whose mental model is it — leadership, teams, customers? Does each group hold a different one?
- Is the belief tested by data, or does the structure prevent it from being tested?

**Vision**
- What outcome is the system evidently optimised for, judged by what it actually produces?
- Does that match the stated purpose? If not, the vision-in-use wins.

---

## Method — Building an Iceberg

1. **Name the event precisely.** One sentence, observable, not a diagnosis ("three P1 incidents in October from config changes", not "people are careless").
2. **Find the pattern before the cause.** Get data over time. If nobody can say whether it is recurring, that absence is itself a finding: the system has no pattern-level feedback.
3. **Draw the structure as loops.** Use a causal loop diagram: variables as nouns, arrows with `+` (same direction) or `−` (opposite direction), loops labelled R or B, delays marked `||`. Two to four loops is usually enough; a hairball explains nothing.
4. **Match an archetype** (below). If the structure matches a known archetype, its known high-leverage intervention is a strong starting hypothesis.
5. **Surface the mental models** that make the structure feel reasonable. Phrase each as a belief held by a group ("Leadership believes that more approval steps reduce risk").
6. **State the vision-in-use** the system is serving, and compare with the espoused one.
7. **Locate the leverage.** Map each candidate intervention to its iceberg level and to Meadows' leverage points. Prefer one structural change with a measurable pattern-level prediction over five event-level reactions.
8. **Write the prediction.** "If we change structure S, pattern P should move in direction D within time T, visible in metric M." This turns the fix into a safe-to-fail experiment (see `toyota-kata`).

Run it as a group when you can: people at different positions see different layers. Done alone it reflects one mental model — the author's.

---

## Systems Archetypes Most Often Below the Waterline

From Senge (*Fifth Discipline*, Appendix 2), Kim & Anderson (*Systems Archetype Basics*, 1998) and Braun's archetype summaries. Each is a recurring structure with a recognisable pattern.

| Archetype | Pattern you see | Structure | Leverage |
|---|---|---|---|
| **Fixes that fail** | Problem goes away, then comes back worse | Quick fix (B) has a delayed side effect that feeds the problem (R) | Watch for the side effect; fix the cause, not the symptom |
| **Shifting the burden** | Growing dependence on a workaround; the real capability withers | Symptomatic fix (B) and fundamental fix (B) compete; side effect erodes the fundamental | Invest in the fundamental fix; ration the symptomatic one |
| **Limits to growth** | Early success, then stall despite more effort | Growth engine (R) hits a constraint (B) | Remove the constraint, not push harder on growth (Theory of Constraints) |
| **Eroding goals** | Standards slip quietly ("80% coverage" becomes "tests where we can") | Gap between goal and reality closed by lowering the goal | Hold the goal; invest in the means |
| **Escalation** | Two parties each respond to the other's move with more of the same | Two balancing loops, each reacting to relative position | Find a shared goal; one side de-escalates unilaterally |
| **Success to the successful** | One team or product gets all the resources | Allocation based on past success (R) starves the alternative | Allocate on purpose, not on past winning; separate pools |
| **Tragedy of the commons** | Shared resource (platform, on-call, CI) degrades | Each actor's gain (R) depletes the commons (B), with delay | Make the cost visible; govern the commons; give it an owner |
| **Growth and underinvestment** | Demand outstrips capacity; quality drops; demand drops; "see, we didn't need it" | Limits to growth plus eroding performance standard | Invest ahead of demand; hold the performance standard |
| **Accidental adversaries** | Two teams that should help each other end up blocking each other | Each side's local fix unintentionally harms the other | Make the shared loop visible; joint goals and metrics |

Software-delivery instances worth recognising:
- **More process after an incident** → slower, bigger releases → riskier changes → more incidents (fixes that fail).
- **A central team that "just does it" for others** → others never build the skill → more requests to the central team (shifting the burden; Team Topologies' enabling team is the fundamental fix).
- **Approval gates for every change** → batching to minimise approvals → larger, riskier batches (fixes that fail; see `continuous-delivery`, `product-development-flow`).
- **Hero on-call** → hero becomes the system → nobody else learns (shifting the burden).

---

## Meadows' Leverage Points

Donella Meadows, "Leverage Points: Places to Intervene in a System" (1999; *Thinking in Systems*, 2008). From least to most effective. Map each proposed intervention to a number — the comparison is usually sobering.

| # | Leverage point | Iceberg level | Delivery-org example |
|---|---|---|---|
| 12 | Constants, parameters, numbers | Events / patterns | Change an SLA, a threshold, a sprint length |
| 11 | Buffer sizes relative to flows | Structure | Spare capacity, slack, queue sizes |
| 10 | Stock-and-flow structure | Structure | Team boundaries, deployment topology |
| 9 | Length of delays | Structure | Feedback time from commit to production |
| 8 | Strength of balancing loops | Structure | Monitoring, alerting, review cadences |
| 7 | Gain of reinforcing loops | Structure | Compounding tech debt, skills growth |
| 6 | Structure of information flows | Structure | Who sees what metric, when; radiating vs reporting |
| 5 | Rules (incentives, constraints) | Structure | Approval rules, WIP limits, Definition of Done, funding rules |
| 4 | Power to change the system structure | Structure / mental models | Teams allowed to change their own process |
| 3 | Goals of the system | Vision | Optimise for outcomes vs output vs utilisation |
| 2 | Mindset / paradigm the system arises from | Mental models | "Control reduces risk" vs "small batches reduce risk" |
| 1 | Power to transcend paradigms | Mental models / vision | Holding models lightly; learning organisation |

Meadows' warning: people find leverage points intuitively and then **push them in the wrong direction**. More control when the loop needs faster feedback; a higher target when the goal is the problem.

---

## Reviewing a Process, Policy or Fix Through the Iceberg

When asked to review a ways-of-working doc, a governance process, a post-incident action list or a reorganisation proposal:

1. **List the problems the document says it solves** (or implies, if unstated). For each, build a mini-iceberg: what event, what pattern (with evidence?), what structure, what mental model.
2. **Classify every mechanism in the document by level and leverage point.** A rule that adds a sign-off is #5 acting on events; a metric everyone sees is #6; a change in who may change the process is #4; a statement of purpose is #3.
3. **Check the fit.** A pattern-level problem answered only with event-level mechanisms (report it, escalate it, add a checklist) will recur. Flag it.
4. **Surface the mental models the document encodes.** Read the verbs: *approve, sign off, ensure, must, escalate, report* reveal a control model; *limit, visualise, experiment, learn, decide within* reveal a flow/learning model. Neither is wrong everywhere — say which the context needs (see `accidental-cio`'s Cynefin fit).
5. **Look for the archetypes** the document may create: added gates (fixes that fail), central approvers (shifting the burden, executive bottleneck), targets on proxies (eroding goals, Goodhart), shared resources with no owner (tragedy of the commons).
6. **Check the feedback loop on the process itself.** Does the document say how anyone will know it is working — which pattern should change, measured how, reviewed when, by whom with power to change it (#4)? A process with no loop on itself cannot learn.
7. **Say what it gets right** at each level before listing gaps.

---

## Output Template

```markdown
## Iceberg: <problem in one line>

| Level | Finding | Evidence |
|---|---|---|
| Events | ... | link / quote / data |
| Patterns | ... | trend, frequency, period |
| Structures | loops (R/B), delays, rules, info flows, incentives | ... |
| Mental models | "<group> believes <belief>" | where it shows |
| Vision (in use vs espoused) | ... | ... |

**Archetype:** <name> — <one line on how it fits>

**Causal loop** (text or diagram):
A --(+)--> B --(+)--> C --(−)--> A   [B1: ...]
C --(+)--||--> D --(+)--> A          [R1: ..., delayed]

**Interventions, by leverage**
| Intervention | Iceberg level | Meadows # | Predicted pattern change | Indicator | Review by |
|---|---|---|---|---|---|

**What we still don't know** — levels with weak evidence; how to find out.
```

For a visual, an iceberg sketch (waterline between patterns and structures) or a causal loop diagram works; use the `artifact-diagramming` skill or Miro if available. Keep the text table as the source of truth.

---

## Anti-patterns

- **Stopping at the event** — the action list is all "fix X, add a check for Y". Ask "how often?" before "how to fix".
- **Iceberg as decoration** — five boxes filled with plausible-sounding text and no evidence. Each level should cite something observed.
- **Blame in structure's clothing** — "structure: people don't follow the process". That's an event-level judgement. Ask what makes not following it the reasonable choice.
- **Mental models attributed to "they"** — mental models belong to named groups and include the analyst's own.
- **Always going deepest** — not every problem needs a paradigm shift. An isolated event warrants a reaction. Match depth to how recurring and costly the pattern is.
- **One-loop thinking** — a single reinforcing loop with no balancing loop or delay usually means the analysis missed what limits it.
- **Interventions with no prediction** — a structural change without a stated pattern-level effect cannot be evaluated and becomes permanent by default.
- **Pushing the leverage point the wrong way** — more approvals, more reporting, higher targets, when the loop needs shorter delays and better information.

---

## How this skill pairs with others

- **`accidental-cio`** — the operating-model lens. Its five components are *structures*; its themes (outcomes over output, manage flow not people) are *mental models*. Use the iceberg to explain why an operating-model defect produces the behaviour it does.
- **`flow-efficiency`**, **`product-development-flow`**, **`kanban`** — the queueing and flow structures (utilisation, WIP, batch size, delays) that sit under most delivery patterns.
- **`toyota-kata`** — turns an iceberg's intervention-with-prediction into an improvement experiment.
- **`continuous-delivery`** — the structural fix for the "more gates, bigger batches" loop.
- **`make-work-visible`** — information-flow interventions (leverage #6).
- **`event-storming`** — surfaces the structure of a business process and its hot spots as a group.
- **`architecture-decision-records`** — record the structural change and its predicted effect.

---

## Quick application checklist

- [ ] Is the event stated as an observation, not a diagnosis?
- [ ] Is there evidence of a pattern over time — or is its absence a finding?
- [ ] Are the structures named as loops (R/B), delays, stocks, rules, information flows and incentives?
- [ ] Are mental models phrased as beliefs held by named groups, including mine?
- [ ] Is the vision-in-use compared with the espoused vision?
- [ ] Does a known archetype fit, and what's its usual leverage?
- [ ] Is each intervention tagged with its level and Meadows leverage point?
- [ ] Does each structural intervention carry a pattern-level prediction, an indicator and a review date?
- [ ] Have I said what's already right at each level?

---

## Reading

- **Peter Senge**, *The Fifth Discipline* (1990; rev. 2006) — levels of explanation (events, patterns, structure), the beer game, laws of the fifth discipline, archetypes in Appendix 2.
- **Peter Senge et al.**, *The Fifth Discipline Fieldbook* (1994) — practical tools including the ladder of inference and archetype templates (Michael Goodman, Art Kleiner and others).
- **Daniel H. Kim**, "Vision Deployment Matrix: A Framework for Large-Scale Change", *The Systems Thinker* 6(1), 1995; "From Event Thinking to Systems Thinking", *The Systems Thinker* vol. 7 — the five-level matrix with vision and its response modes.
- **Daniel H. Kim & Virginia Anderson**, *Systems Archetype Basics* (Pegasus, 1998).
- **Donella Meadows**, "Leverage Points: Places to Intervene in a System" (Sustainability Institute, 1999); *Thinking in Systems: A Primer* (2008).
- **David Peter Stroh**, *Systems Thinking for Social Change* (2015) — iceberg, archetypes and the four-stage change process for real organisations.
- **W. Edwards Deming**, *Out of the Crisis* (1982); **Russell Ackoff**, *Re-Creating the Corporation* (1999) — the system, not the worker.
- **Chris Argyris**, *Overcoming Organizational Defenses* (1990) — espoused theory vs theory-in-use, ladder of inference.
- **John Sterman**, *Business Dynamics* (2000) — the rigorous version: stocks, flows, delays, simulation.
