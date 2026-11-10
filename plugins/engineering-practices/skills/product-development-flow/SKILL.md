---
name: product-development-flow
description: Apply Don Reinertsen's "The Principles of Product Development Flow" (Celeritas, 2009), the quantitative case for flow in product work. Covers its 175 principles across eight areas (economics, queues, variability, batch size, WIP constraints, flow control under uncertainty, fast feedback, decentralised control) with verified codes; cost of delay and the SJF, HDCF and WSJF (CD3) sequencing rules; utilisation, Little's formula and why you control queue size rather than cycle time; the batch-size U-curve; congestion collapse; cadence; pooled versus dedicated capacity; and how to handle interrupt, bug and fixed-date work alongside planned features. Includes a review mode that scores a process document area by area. Use when prioritising a backlog, sizing batches, setting WIP limits, arguing against high utilisation, deciding whether to split a team into feature and support streams, deciding what to centralise or decentralise, or reviewing a ways-of-working document.
---

# Principles of Product Development Flow (Don Reinertsen)

Use this skill when a product-development decision needs economic and queueing reasoning: what to do
next, how big a batch should be, how much work to allow in progress, how busy people should be, how to
handle interruptions, and who should decide.

The book has nine chapters. Chapter 1 sets out the problem; chapters 2–9 hold **175 numbered
principles** in eight areas. The full index, with codes, names and a paraphrased gist of each, is in
[references/principle-index.md](references/principle-index.md). Codes in this skill follow that index.
They come from a study transcription whose counts match the book, so check the book before quoting a
code formally.

## Core ideas

1. **Decide in money.** Most process decisions are made on proxies such as utilisation, conformance or
   "busy". Reinertsen wants them made on economics, and says that if you quantify only one thing, it
   should be cost of delay (E1, E3).
2. **Queues are the main waste, and they are invisible.** Development inventory is information, so it
   doesn't show on a shop floor or a balance sheet (Q1, Q2). Queues lengthen cycle time and add risk,
   variability, overhead and quality problems, and they sap motivation.
3. **High utilisation creates queues.** As utilisation approaches 100%, queues grow sharply, and past a
   point output collapses (Q3, F1). Spare capacity is an economic choice, not idleness.
4. **Batch size is the cheapest lever.** Smaller batches cut cycle time, variability and risk, and speed
   up feedback (B1–B4). The best size is a U-curve set by transaction cost, so cut transaction cost
   first (B11, B12).
5. **Variability is not always bad.** Product development creates value through uncertain experiments.
   Reduce the *cost* of variability rather than the variability itself (V1, V3, V12).
6. **Decentralise with intent.** Push decisions about problems that age quickly to the people nearest
   the information, aligned by a stated mission and decision rules (D1, D8, E13).

---

## The eight areas

| Ch. | Area | Codes | Central question |
|---|---|---|---|
| 2 | The economic view | E1–E21 | What is this worth, and what does a delay cost? |
| 3 | Managing queues | Q1–Q16 | Where is work waiting, and how much does it cost? |
| 4 | Exploiting variability | V1–V16 | Where does uncertainty create value, and where does it only cost? |
| 5 | Reducing batch size | B1–B22 | How much work moves together, and why that much? |
| 6 | Applying WIP constraints | W1–W23 | How much is in progress, and what happens at the limit? |
| 7 | Controlling flow under uncertainty | F1–F30 | How do we sequence, route and pace work we can't predict? |
| 8 | Using fast feedback | FF1–FF24 | How quickly do we learn that something is off? |
| 9 | Achieving decentralized control | D1–D23 | Who decides, with what information and intent? |

### 2. The economic view

- **E3 Quantified Cost of Delay.** If you quantify one thing, quantify this.
- **E6 U-Curve.** Important trade-offs have an optimum in the middle. Pushing one variable to its
  extreme is usually wrong.
- **E7 Imperfection.** A rough estimate of cost of delay beats none. Teams that wait for precision never
  start.
- **E10 First Perishability.** Many choices lose value if made slowly.
- **E13 First Decision Rule.** Decision rules (for example, "one week of delay costs about X") let
  people far from the centre make economic trade-offs.
- **E17 Sunk Cost** and **E16 Marginal Economics.** Judge the next increment on its own cost and value.

### 3. Managing queues

- **Q3 Queueing Capacity Utilization.** Queues rise sharply with utilisation. For a single queue with
  random arrivals and service times (M/M/1), the wait relative to the work time is u ÷ (1 − u):

  | Utilisation | 50% | 70% | 80% | 90% | 95% |
  |---|---|---|---|---|---|
  | Wait ÷ work time | 1× | 2.3× | 4× | 9× | 19× |

  Kingman's approximation generalises this: waiting grows with utilisation and with the variability of
  both arrivals and work.
- **Q4 High-Queue States.** Most of the damage comes from the occasional very long queue.
- **Q7 Queueing Structure.** Serve pooled demand with reliable, high-capacity servers.
- **Q12 Little's Formula.** Wait time = queue size ÷ processing rate.
- **Q13 and Q14 Queue Size Control.** Control queue size, not utilisation (Q13) or cycle time (Q14).
  Queue size is a leading indicator; cycle time reports a problem after it has happened.
- **Q15 Diffusion and Q16 Intervention.** Random queues drift far out of control and stay there. Act;
  don't wait for them to correct themselves.

Where queues hide in software teams: review, testing, deployment, design, decisions, environments,
triage, and the backlog itself. The decision queue is often the most expensive and the least visible.

### 4. Exploiting variability

- **V1 Beneficial Variability** and **V2 Asymmetric Payoffs.** An experiment with a cheap downside and a
  large upside is worth running even if it usually fails (see also E20 Newsboy).
- **V5 Variability Pooling.** Combining uncorrelated work reduces total variation. This is the argument
  for pooled capacity.
- **V6 Short-Term Forecasting.** Forecasts get much easier over short horizons, so plan short.
- **V7 Small Experiments.** Many small experiments vary less than one big one.
- **V12 Variability Consequence.** Reducing the consequence (feature flags, fast rollback, canaries) is
  usually cheaper than reducing variability.
- **V15 Iteration Speed.** Improving iteration speed usually beats lowering the defect rate.

### 5. Reducing batch size

- **B1–B4.** Smaller batches cut cycle time and variability, speed up feedback and reduce risk.
- **B8 Slippage and B9 Death Spiral.** Large batches slip disproportionately and grow into larger ones.
- **B11 Batch Size Economics and B12 Low Transaction Cost.** The optimum balances holding cost against
  transaction cost. Automating test and deployment moves the optimum smaller; this is why continuous
  delivery is a flow investment.
- **B16 Transport Batches.** The handoff batch matters most: how much one step passes to the next.
- **B21 Batch Size First.** Reduce batch size before attacking bottlenecks.

Batches in software include: pull requests, releases, quarterly plans, approval packs, requirement
documents handed over whole, questions saved for a weekly meeting, and the funding decision itself.

### 6. Applying WIP constraints

- **W1 WIP Constraints.** Limit WIP to control cycle time and flow.
- **W6 Demand Blocking**, **W7 WIP Purging** and **W8 Flexible Requirements.** At the limit, stop
  admitting work, drop low-value work, or shed requirements.
- **W9 Resource Pulling**, **W11 Big Gun**, **W12 T-Shaped Resources** and **W13 Skill Overlap.** React to
  an emerging queue by moving capable people to it quickly, which needs cross-trained people.
- **W10 Part-Time Resources.** Use part-time people for high-variability tasks.
- **W15 Aging** and **W16 Escalation.** Watch the oldest items, and plan in advance how outliers escalate.
- **W18 Differential Service.** Give different workstreams different service levels inside one
  WIP-limited system.
- **W21 Critical Queue.** Limit WIP where the queue is most expensive.

### 7. Controlling flow under uncertainty

- **F1 Congestion Collapse** and **F2 Peak Throughput.** Overload causes a sudden drop in output.
  Limit occupancy to keep throughput at its peak, as ramp meters do on a motorway.
- **F5–F9 Cadence.** A regular cadence stops variance accumulating, makes waiting times predictable,
  enables small batches, and needs spare capacity (F6).
- **F15–F17 Sequencing.** See the sequencing section below.
- **F18 Local Priority.** Priorities are local to a queue; a global ranked list hides that.
- **F19 Round-Robin.** When durations are unknown, time-share capacity.
- **F20 Preemption.** Preempt work in progress only when switching costs are low.
- **F25 Flexible Resources**, **F26 Late Binding**, **F28 Preplanned Flexibility** and **F29 Resource
  Centralization.** Absorb variation with flexible capacity bound to work as late as possible. Plan and
  invest in that flexibility ahead of time.

### 8. Using fast feedback

- **FF3 Leading Indicators.** Control on variables that predict the future, such as queue size, not
  ones that report the past.
- **FF7** and **FF11.** Fast feedback allows smaller queues, and small batches give fast feedback.
- **FF9 Useless Measurement.** Measuring something does not get it done.
- **FF10 First Agility.** A short turning radius beats a long planning horizon.
- **FF15 Relief Valve.** Agree in advance what gives when the system is overloaded.
- **FF16 Multiple Control Loops.** Nest fast loops (daily) inside slow ones (quarterly).

### 9. Achieving decentralized control

- **D1 Second Perishability** and **D2 Scale.** Decentralise problems that age badly. Centralise those
  that are rare, large, or have economies of scale.
- **D5 Virtual Centralization.** Be able to pool decentralised people quickly when needed.
- **D7 Alignment**, **D8 Mission** and **D10 Main Effort.** State the end state, its purpose and the fewest
  constraints. Name a main effort; everything else supports it, and it can shift (D11).
- **D15 Tactical Reserves.** Keep some reserve capacity at the local level.
- **D19 Quality of Service.** If response time matters, measure response time.

---

## Cost of delay and sequencing

**Cost of delay** is the value lost per unit of time that a piece of work is not done, in money per
week. It is the weighting in every rational sequencing rule. Estimate it roughly (E7) with a few
inputs: the value once delivered, how that value changes with time, and any date after which it
collapses.

Delay costs have different shapes over time. Kanban's class-of-service archetypes describe four:

| Shape | Delay cost | Typical work | Policy |
|---|---|---|---|
| Expedite | High and immediate | Outage, data loss, security breach | Pre-empts other work; allow one at a time |
| Fixed date | Jumps at a known date | Regulatory or partner change | Start from the latest safe start, not "when free" |
| Standard | Rises steadily | Most features and improvements | Sequence by CD3 |
| Intangible | Unknown now, real later | Tech debt, platform work | Guaranteed share of capacity |

**Sequencing rules (F15–F17):**

- If delay costs are similar, do the **shortest job first** (SJF).
- If durations are similar, do the **highest cost of delay first** (HDCF).
- If neither is similar, use **weighted shortest job first** (WSJF): sort by
  **CD3 = cost of delay ÷ duration**, highest first.

Worked example, all in £k per week of delay:

| Job | Cost of delay | Duration (weeks) | CD3 | Order |
|---|---|---|---|---|
| A | 10 | 5 | 2 | 3rd |
| B | 6 | 1 | 6 | 1st |
| C | 15 | 4 | 3.75 | 2nd |

Doing B, C, A delays less value than doing the "most valuable" job C first.

**Cautions:**

- WSJF's benefit comes from using a common unit, money per week. Relative scoring schemes such as
  SAFe's WSJF, which add up 1–20 scores for value, urgency and risk, lose that unit. They are still
  better than gut feel, but the arithmetic means less.
- **F18 Local Priority:** the ranking applies to one queue. Don't impose one global list on queues with
  different economics.
- **F20 Preemption:** breaking into work in progress costs switching time. Only expedite items should do
  it, and only when switching is cheap.

---

## Interrupts, BAU and mixed work

Product teams usually face two kinds of demand: planned work (features, initiatives) and unplanned work
(bugs, incidents, support, fixed-date partner changes). A common response is to split them into a
"feature stream" and a separate "BAU" or "support" stream. Reinertsen doesn't prescribe a team structure
for this, but several of his principles bear directly on it.

**What the principles favour:**

- **Pooling.** Pooled demand served by shared capacity queues less (Q7, V5, F29). Two dedicated groups,
  each serving its own stream, will see one group's queue grow while the other has slack.
- **Flexible capacity bound late.** Flexible, cross-trained people assigned to work as late as possible
  absorb variation (F25, F26, W12, W13). Preplanned flexibility (F28) and resource pulling (W9) move
  people to an emerging queue quickly.
- **Differential service, not separate systems.** Give urgent work a faster service level inside one
  WIP-limited system (W18).
- **Part-time and reserved capacity.** Use part-time resources for high-variability tasks (W10), keep
  tactical reserves (D15), and leave capacity margin so cadence works (F6).
- **Cadence bounds waiting.** In his talks, Reinertsen replaces a vague share of someone's time (say,
  "10% for project support") with a fixed daily slot where that support is top priority. A regular slot
  puts an upper bound on how long a request waits (F7).
- **FIFO and hard admission rules don't fit urgent work.** His satirical "TPS emergency room" shows that
  copying manufacturing rules literally (first in, first out; turn arrivals away at the WIP limit) is
  wrong when urgency varies. Urgent work needs its own queueing discipline.

**What practitioners add:**

- **Google SRE** found that spreading tickets round-robin across a team failed. Engineers couldn't do
  project work and ticket duty at once, so tickets were centralised on a rotating person. The rotation
  sits inside the team that owns the service, and that person is written off for project work that
  week.
- **Kenny Rubin** recommends that one team reserve capacity for interrupts when their volume is
  predictable from history. If volume is wildly scattered, he suggests routing it to a separate team.
- **LeSS (Craig Larman, Bas Vodde)** argues that each additional backlog reduces an organisation's
  ability to adapt toward the highest value. One product means one priority order.

**A decision guide:**

| Option | What it is | Fits when | Costs |
|---|---|---|---|
| One pool, differential service | One backlog, classes of service, everyone can take any item | Interrupts are modest and predictable | Interrupts fragment focus unless contained |
| One pool with a rotating interrupt role | One backlog; a rota person per team takes interrupts first and helps finish the top item when quiet | Most product teams | A weekly handover; someone is out of feature work |
| Separate support team | Its own people and backlog | Interrupt volume is high, unpredictable and needs different skills | Two queues, no pooling, defects don't return to their makers, a priority boundary to argue over |

The middle option fits most of these principles at once: pooling and one priority order (Q7, V5, F18
within one system), part-time reserved capacity (W10, D15), and differential service (W18). The SRE
evidence supports containing interrupts on one person. Signs that a split is hurting flow:

- The support group is fixed in size whatever the demand.
- Help flows one way: support can pull feature people in, but not the reverse.
- Each side has its own priority rules, and nobody trades one stream against the other.
- Defects from new work land on people who didn't build it.
- Fixed-date work is treated as an interruption, although its date was known weeks ahead.
- Measures are kept per stream, so no one sees total WIP or the share of capacity going to failure
  demand (work caused by not getting something right the first time).

---

## Reviewing a process through this lens

Score the document area by area as **Strong**, **Partial** or a **Gap**, citing the clause that shows it.

| Area | Questions |
|---|---|
| Economics (E) | Is cost of delay estimated, even roughly? Are decisions framed in money or in proxies? Are there decision rules people can apply locally? |
| Queues (Q) | Are queues visible, including decisions and approvals? Is queue size measured and acted on, or only cycle time after the fact? Is utilisation a target? |
| Variability (V) | Is variability treated as something to remove at all costs, or are consequences reduced (flags, rollback)? Are experiments small and cheap? |
| Batch size (B) | What is the largest batch: approval, requirements, release, handover? Is transaction cost being driven down? |
| WIP (W) | Are there explicit WIP limits? What happens at the limit: block, purge or shed scope? Can people move to an emerging queue? |
| Flow control (F) | How is work sequenced: CD3, HDCF, FIFO, loudest voice? When may work be preempted? Is capacity flexible and bound late? Is there a cadence with margin? |
| Feedback (FF) | Are the measures leading indicators? How long from a question to an answer, or from a release to a signal? Is there an agreed relief valve? |
| Decentralised control (D) | Which decisions are centralised, and do they age well? Is intent stated so teams can decide? Is there a main effort? |

Then pick the three to five findings with the most economic leverage, state the change for each, and
credit what is strong before listing gaps.

### Output template

```markdown
## Flow review: <document>

| Area | Verdict | Evidence |
|---|---|---|
| Economics (E) | Strong / Partial / Gap | <clause, quote> |
| Queues (Q) | ... | ... |
| Variability (V) | ... | ... |
| Batch size (B) | ... | ... |
| WIP (W) | ... | ... |
| Flow control (F) | ... | ... |
| Feedback (FF) | ... | ... |
| Decentralised control (D) | ... | ... |

### Findings
1. **<title>** (<principle codes>): <what and where>. **Change:** <the move>.
```

---

## Anti-patterns

- **Utilisation as a target.** "Keep everyone busy" is the setting that creates queues and collapse.
- **Steering by cycle time.** By the time cycle time moves, the queue that caused it has been there for
  weeks.
- **Priority by volume or seniority.** Without cost of delay, the loudest request wins.
- **Value-only ranking.** Ignoring duration; WSJF exists because a short job can be worth doing before a
  more valuable long one.
- **Dedicated queues for every work type.** Each split forfeits pooling and adds a boundary to argue over.
- **Expedite as a habit.** If most items are urgent, nothing is; limit expedite to one at a time.
- **Big-batch approval.** Approving and funding a whole solution at once, then treating every learning
  as a change request.
- **Decision queues.** Questions parked for a weekly meeting or an absent approver. Decisions age badly
  (D1).
- **Zero queues.** Some queue buffers variability; size it deliberately (Q9).

---

## Limits and criticisms

- **Cost of delay is hard to estimate,** and teams that wait for accuracy never use it. Reinertsen's
  answer is E7: rough numbers still beat proxies.
- **The queueing results assume steady arrivals and service.** Real teams have correlated, bursty demand.
  The direction of the effects holds; the exact multipliers don't.
- **The book is dense and abstract,** with few worked software case studies. Expect to translate.
- **Principle codes circulate mainly through study notes.** Treat them as a convenient index, not
  citations.
- **It says little about people and culture.** Pair it with a management-system lens such as the Toyota
  Way.

---

## How this skill pairs with others

- **`flow-efficiency`**: Modig and Åhlström's strategic frame. Read it for the why; this skill gives the
  how-much.
- **`kanban`**: puts WIP limits, classes of service, cadences and flow metrics into practice.
- **`continuous-delivery`**: lowers transaction cost so small batches become economic (B12, B19).
- **`splitting-user-stories`**: makes the batches smaller.
- **`value-stream-mapping`**: finds where work waits before you price the queue.
- **`toyota-way`** and **`toyota-kata`**: the management system and the improvement routine.
- **`systems-thinking-iceberg`**: when the queue is a symptom of a structure or a mental model.

---

## Quick checklist

- [ ] Can I put a rough cost of delay on the options, in money per week?
- [ ] Which queues does this decision lengthen or shorten, including decision queues?
- [ ] Am I steering by queue size or by cycle time after the fact?
- [ ] How busy are the people involved? Above about 80%, small surprises cause long waits.
- [ ] What batch size does this choose, and can transaction cost come down first?
- [ ] How is the work sequenced, and does duration count?
- [ ] Are urgent and planned work in one priority order, with differential service?
- [ ] Who decides, how quickly, and does the decision age badly if it waits?

---

## Reading

- **Donald G. Reinertsen**, *The Principles of Product Development Flow: Second Generation Lean Product
  Development* (Celeritas, 2009). The source.
- **Donald G. Reinertsen**, *Managing the Design Factory* (Free Press, 1997). The precursor.
- **Reinertsen**, "Understanding the Magic of Lean Product Development", QCon San Francisco 2011
  slides. Cadence bounding waiting time, queueing disciplines and the "TPS emergency room".
- **Betsy Beyer et al.**, *Site Reliability Engineering* (O'Reilly, 2016), chapter 29, "Dealing with
  Interrupts", and the ;login: article on ticket rotations (winter 2016).
- **Kenneth S. Rubin**, "Can a Scrum Team Handle Both Plan-Driven and Interrupt-Driven Work?"
  (innolution.com).
- **Craig Larman and Bas Vodde**, LeSS, on the number of backlogs (less.works).
- **Kanban University**, *The Official Kanban Guide* glossary: class-of-service archetypes.
- **Daniel Vacanti**, *Actionable Agile Metrics for Predictability* (2015): Little's law and forecasting
  in practice.
- **Joshua Arnold and Özlem Yüce**, Black Swan Farming: cost of delay case studies.
