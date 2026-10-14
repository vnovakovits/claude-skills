---
name: accidental-cio
description: Apply Scott Millett's "The Accidental CIO — A Lean and Agile Playbook for IT Leaders" (Wiley, 2024) when designing or reviewing how a technology organisation decides, funds, governs and delivers work. Covers the five components of an adaptive IT operating model (organised, work, govern, talent, lead) and its four themes (outcomes over output, intrinsic motivation, being not doing agile, manage flow not people); matching method and governance to context via Cynefin and Wardley evolution; governance as demand management + funding + measurement + decision rights, shifting from project funding to product teams funded against outcomes (Beyond Budgeting); teams bounded by Conway's law and cognitive load; and the strategy-to-execution chain (capability heat map → target architecture → initiatives → roadmap). Use when reviewing a change-request, intake, prioritisation or portfolio-governance process, an IT strategy, a funding model, decision rights or team structure.
---

# The Accidental CIO (Scott Millett)

Apply this skill when someone is designing or reviewing *how a technology organisation works* — its intake and prioritisation process, funding model, governance, team structure, decision rights, strategy or roadmap — rather than the code itself. It is the operating-model lens: the layer above `kanban`, `flow-efficiency` and `continuous-delivery`, and the layer below business strategy.

## Core Philosophy

**The problem is the system, not the people.** Most IT dysfunction — order-taking, missed dates, "the business vs IT", busy teams that deliver little — is produced by the operating model: how work is requested, funded, governed, staffed and led. Changing practices (standups, boards, sprints) without changing the system changes nothing. Millett leans on Deming, Ackoff and systems thinking: *a system is the product of the interactions of its parts, not the sum of them.*

**Service provider vs disruptor is a false choice.** The old mental model lets a CIO be either the efficient utility (keep the lights on, cut cost) or the innovator. Millett's position: IT must do both, and the operating model must be *ambidextrous* — different sub-models for different kinds of problem, held together by shared strategic intent.

**Context determines method.** There is no one right way of working. Match the approach to the problem domain (Cynefin) and to the evolutionary stage of the component (Wardley). Uncharted problems want design thinking, discovery and governance that reduces uncertainty; known problems want lean/agile and governance that measures operational outcomes; industrialised components want planning, conformance and cost control. *Being* agile means choosing; *doing* agile means copying.

**Outcomes over output.** Fund, prioritise, measure and review *impacts on the business* (revenue, cost, risk, customer behaviour), never features delivered or scope conformance. A plan delivered to spec that moved no needle is a failure the system should be able to see.

**Structure follows strategy.** (Chandler.) The operating model exists only to deliver the strategy. Copying another company's structure — Spotify squads, SAFe trains — without the strategy and the other four components that made it work has little effect.

**Lead the people, manage the flow of work.** Command-and-control management of people (utilisation, task assignment, status reporting) is replaced by designing the system, setting intent, and managing the flow of work through it. People get purpose, mastery and autonomy (Pink); the system gets transparency, WIP limits and feedback.

---

## Part I — A New System of Work

### Chapter 1 — Why we need to change the system
Digital disruption, rising customer expectations, new business models and a VUCA environment mean IT can no longer be a back-office function executing a fixed plan. **Cynefin** is the decision-making frame:

| Domain | Nature | Response | Governance emphasis |
|---|---|---|---|
| Clear | Known knowns, best practice | Sense → categorise → respond; standardise, automate, buy | Cost, conformance, SLAs |
| Complicated | Known unknowns, expertise | Sense → analyse → respond; experts, good practice, plans | Business case, plan adherence |
| Complex | Unknown unknowns, emergent | Probe → sense → respond; safe-to-fail experiments, discovery | Reduce uncertainty, learn fast, limit bet size |
| Chaotic | No cause/effect visible | Act → sense → respond; stabilise | Stop the bleeding, then move to another domain |

IT operates in **both** the ordered (clear/complicated) and unordered (complex) spaces at once. A single process that treats a rate-table change, a payment-provider migration and a new marketplace channel the same way is already wrong.

### Chapter 2 — Philosophies for a new system
Philosophies, not methodologies. Four that matter:
- **Design thinking** — discover value by understanding the customer's problem before specifying a solution.
- **Lean** (TPS, Toyota Way, Lean Enterprise) — eliminate waste, respect people, continuous improvement, flow; and **Theory of Constraints** — the bottleneck governs throughput.
- **Agile** — manage complexity through short feedback loops, working software, and collaboration over contract negotiation.
- **Wardley mapping** — situational awareness: plot components by visibility to the user (y) and evolution (x: genesis → custom → product → commodity). **Doctrine** is the set of universally good practices (know your users, use appropriate methods, focus on outcomes, remove bias and duplication, think small teams, bias towards action, be transparent).

### Chapter 3 — How to change the system
- Adopting practices ≠ being agile. Behaviour is a product of the system; change the system (structure, incentives, information flow, decision rights) and behaviour follows.
- **Systems thinking** tools: causal loop diagrams, iceberg model, leverage points, mental models. Linear thinking (plan → execute → conform) fails in complex domains.
- **Command-and-control** (annual budgets, fixed targets, detailed plans, status reporting) is replaced by **Beyond Budgeting**: relative targets, rolling forecasts, resources allocated as needed, transparency, decisions pushed to the front line, coordination through intent rather than plans.
- **Intrinsic motivation**: purpose, mastery, autonomy. Leadership principles that instil it: clarity of intent, trust, information radiated not hoarded, failure as learning.
- Emergent, adaptive management processes — not a transformation programme with an end date.

---

## Part II — Designing an Adaptive Operating Model

### Chapter 4 — The anatomy of an operating model
Strategy says **what**; the operating model says **how we work around here**. Five interlocking components — change one and the others must change with it:

1. **How we are organised** — teams, boundaries, reporting lines, accountability.
2. **How we work** — discovery and delivery methods.
3. **How we govern** — demand management, funding, measurement, performance review, decision rights.
4. **How we source and manage talent** — hire, develop, retain; explorers / villagers / town planners.
5. **How we lead** — the roles leaders and managers actually play.

Four **themes** run through all five:
- **Impacts and outcomes over output.**
- **Structured for intrinsic motivation.**
- **Being agile, not just doing agile** (context-specific ways of working).
- **Manage the flow of work; lead the people.**

**Sub-models per context.** The same organisation runs an exploratory sub-model (design thinking + agile; governance = reduce uncertainty, small bets, learning metrics), an efficiency sub-model (lean + agile; governance = growth/profit/operational metrics), and an industrialised sub-model (planning + vendor management; governance = business case + conformance). One governance process for all three is the most common operating-model defect.

### Chapter 5 — How we are organised
- **Hierarchy vs holacracy** — neither alone; a *balanced* design: hierarchy for accountability and alignment, self-managing circles for autonomy and speed.
- **Conway's law** — team boundaries become system boundaries; design teams for the architecture you want (inverse Conway). **Cognitive load** (Team Topologies) caps what a team can own well.
- **Product-centric development teams**, not project teams: long-lived, cross-functional, owning a product (a thing with users and an outcome, not a deliverable), with defined boundaries of responsibility, clarity of purpose, autonomy and self-sufficiency, appropriately sized (two-pizza / Dunbar ~7±2 at the core).
- **Product taxonomy** to organise the portfolio: value streams → products → capabilities; boundaries drawn from business capabilities and domain (DDD bounded contexts), not from technology layers or departments.
- Team types: stream-aligned, platform, enabling, complicated-subsystem; interaction modes: collaboration, X-as-a-service, facilitating.

### Chapter 6 — How we work
- **Discovery and delivery are both the team's job.** Dual-track: continuous discovery (problem framing, user research, experiments, impact mapping) feeding continuous delivery. The people who analyse should be the people who build; a separate analysis function that hands over a specification is a project-era handoff.
- Match the method to the component's evolution: genesis/custom → explore (Lean Startup, prototypes, MVPs); product → exploit (lean/agile, incremental delivery, continuous improvement); commodity → buy/outsource/automate (ITIL-style operations, SLAs).
- Continuous delivery, DevOps, small batches, feature flags; measure with flow metrics and DORA.
- Slice work by outcome and by thin end-to-end increments; **release early to learn**, not when "complete".

### Chapter 7 — How we govern
The chapter most relevant to intake, prioritisation and change-request processes. Governance = **demand management + funding + measurement + performance review + decision rights.**

**Demand management**
- Capture *problems and opportunities framed as desired outcomes*, not requests for features. A request form that asks "what do you need" produces order-taking; ask "what change in the business do you want, how will we know, what is it worth".
- **Triage by context** (Cynefin / Wardley stage) and by class — run (BAU/keep-the-lights-on), grow, transform — then route to the right sub-model. Don't push an exploratory bet and a regulatory deadline through the same gate.
- Prioritise economically: **cost of delay**, value vs effort, alignment to strategic intent — not seniority of the requester.

**Funding**
- **Fund capacity (long-lived teams / value streams), not projects.** Projects fund a scope and a date and then disband the team; products fund a team against outcomes and let scope flex. Project funding is the root of fixed-scope thinking, big-batch delivery, and "IT as cost centre".
- Beyond Budgeting: rolling, incremental allocation; **small bets with stage gates based on learning**, not big business cases approved once.
- Explicitly allocate capacity across run / grow / transform and across the exploratory / efficiency / industrialised sub-models; otherwise run work silently eats everything.

**Measurement and performance review**
- Measure **outcomes and impacts** (leading and lagging business metrics) plus **flow** (lead time, throughput, WIP, aging) plus **health** (DORA, reliability, engagement). Not utilisation, not velocity, not scope delivered.
- Review *bets*, not status: did the outcome move? pivot, persevere or stop. A review "for information only" that cannot stop or redirect funding is reporting, not governance.
- Transparency: everyone sees the portfolio, the metrics and the decisions.

**Decision rights**
- Push decisions to the lowest level with the information and the accountability. Leadership sets **intent and guardrails** (outcomes, constraints, budget envelope, non-negotiables); teams decide **how**, including scope trade-offs inside the intent.
- Centralised approval of every change is appropriate only for the industrialised/commodity sub-model (and for the few decisions with irreversible, enterprise-wide consequences). Applied everywhere it becomes the organisation's bottleneck and teaches teams not to think.
- Make decision rights explicit: who decides, who is consulted, who is informed, and at what threshold a decision escalates.

### Chapter 8 — How we source and manage talent
- **Explorers / villagers / town planners** (Wardley's pioneers / settlers / town planners): different people thrive at different evolution stages; staff the sub-models accordingly, and let people move.
- T-shaped people, hiring for attitude and learning, growing generalists for stream-aligned teams and deep specialists for complicated subsystems/platforms.
- Mastery pathways, feedback and coaching over annual appraisal; retention through purpose and autonomy.

### Chapter 9 — How we lead
- From manager-of-people to **designer of the system and setter of intent** (Marquet's intent-based leadership, mission command / commander's intent).
- Servant leadership, psychological safety, generative culture (Westrum), transparency, modelling learning from failure.
- Leaders remove impediments, protect focus, and resolve cross-team conflicts of priority; they do not assign tasks or demand utilisation.
- Senior leadership's job is to make the strategy and the constraints *legible* so that decentralised decisions are coherent.

---

## Part III — Strategy to Execution

The playbook for turning business strategy into an IT contribution and a plan, then executing without reverting to command-and-control.

1. **Understand the business** — business model, value proposition, revenue model, competitive position, and a **business capability model** heat-mapped by strategic importance and current performance. This is where IT stops being an order taker: it reasons from the business's goals, not from the request queue.
2. **Define IT's strategic contribution** — which capabilities IT must create, improve or industrialise; **target architecture** (what moves along the evolution axis, build vs buy vs retire) and **operating vision** (how each area will be organised and governed). Wardley maps show strategy, architecture, team topology and way-of-working on one picture.
3. **Review the current landscape** — technology estate and IT capability; review the operating model: what needs changing.
4. **Define initiatives** — the tactical bridge from strategy to work: each initiative names the outcome, the capability gap it closes, the architecture change *and* the operating-model change, and the measures of success. Prioritise and sequence; communicate as a **tactical investment roadmap** (themes and outcomes over time, not a Gantt of features).
5. **Operational planning and execution** — quarterly cadence: translate initiatives into team-level objectives and measures, allocate capacity, run, review outcomes, re-plan. Strategy deployment, not strategy announcement.

---

## Reviewing a process or governance document through this lens

Walk the document against these questions. Each "no" is a finding.

**Context fit**
1. Does the process distinguish kinds of work (exploratory / efficiency / industrialised; run / grow / transform; Cynefin domain), or does one route handle everything?
2. Is the degree of up-front analysis and approval proportionate to the uncertainty and reversibility of the work?

**Outcomes over output**
3. Is work framed and approved as a desired business impact with a measure, or as a scope?
4. Is "success" at review measured against the outcome or against the delivered scope?
5. Who owns the outcome after delivery — a team, or nobody once the "project" closes?

**Funding and portfolio**
6. Is capacity funded (teams, value streams) or are items funded (projects, requests)?
7. Is capacity explicitly allocated across run / grow / transform, or does one stream silently consume the others?
8. Are bets sized small and gated on learning, or approved once as a full scope?
9. Is there a portfolio WIP limit *and* a limit on the approved-but-unstarted queue?

**Decision rights**
10. Which decisions are reserved for executives, which delegated to the team or champion, and is that written down with thresholds?
11. Can the delivering team change *how* and *how much* within the approved intent without returning to a committee?
12. Who decides scope-vs-date trade-offs? (Lean answer: fix capacity and date, flex scope towards the outcome; the product owner / champion decides within intent.)

**Organisation and ways of working**
13. Are analysis and delivery done by the same long-lived team, or does an analysis function hand a specification over?
14. Is "the technology team" treated as one resource pool, or as product teams with their own flow and ownership?
15. Does the process assume discovery happens before approval (specify then build) or allow discovery during delivery (build to learn)?

**Measurement and feedback**
16. Are flow metrics (lead time end-to-end, cycle time, throughput, aging WIP) and outcome metrics visible to everyone, continuously?
17. Does the review have teeth — can it stop, pivot or re-fund — or is it "for information"?
18. Does the process improve itself through its own data (kaizen), or only through escalation of breaches?

**Leadership posture**
19. Does the executive body set intent and guardrails, or approve items?
20. Does compliance rest on transparency and trust, or on breaches being reported upward?

---

## Common anti-patterns Millett names

- **Order-taker IT** — a request form, a queue, and a committee; IT delivers what it is told and is measured on throughput of requests.
- **Project funding** — fund scope and date, disband the team, lose the knowledge, measure conformance to plan.
- **One governance for everything** — the exploratory bet and the rate-table update go through the same business case and the same gate.
- **"Doing agile"** — standups and boards inside a command-and-control funding and approval model.
- **Analysis as a separate function** — BAs/architects specify, developers build, nobody owns the outcome.
- **Fixed scope as the baseline** — scope signed off and defended; learning during delivery has nowhere to go.
- **Utilisation and status as the management signal** — "are people busy, is the plan on track" instead of "is the outcome moving, is work flowing".
- **Review for information** — outcomes presented after the fact with no ability to redirect funding.
- **Copying structure** — adopting Spotify / SAFe / a competitor's org chart without the strategy and other components.
- **Executive bottleneck** — a single approver (CTO, CIO, steering committee) on every change, so the organisation's lead time is the approver's calendar.

---

## How this skill pairs with others

- **`flow-efficiency`**, **`kanban`**, **`product-development-flow`** — the mechanics of managing flow once the operating model allows it (WIP limits, cost of delay, queues). This skill decides *who may limit WIP and fund capacity*; those decide *how*.
- **`lean-software-development`** — Poppendieck's seven principles are the "how we work" philosophy in Part I.
- **`continuous-delivery`** — the delivery-side prerequisite for small bets and outcome-based review.
- **`domain-driven-design`** / **`event-storming`** — bounded contexts and business capabilities are how product-team boundaries get drawn (Chapter 5).
- **`splitting-user-stories`** / **`user-story-mapping`** — slicing initiatives into outcome-bearing increments so review can happen before "complete".
- **`running-lean`** — the exploratory sub-model's method (Lean Canvas, experiments, pivot/persevere).
- **`ticket-writer`** — the intake artefact: problem-first, outcome-stated, no prescribed solution.
- **`architecture-decision-records`** — recording the target-architecture and operating-model decisions Part III produces.
- **`toyota-kata`** — the improvement engine for the operating model itself.

---

## Quick application checklist

When reviewing or designing an operating-model artefact:
- [ ] Have I identified which of the five components it touches, and which others must change with it?
- [ ] Does it separate kinds of work by context, or force one route?
- [ ] Is work framed as outcomes with measures, and reviewed against them?
- [ ] Is funding attached to teams/capacity rather than to items?
- [ ] Are decision rights explicit, and pushed as low as information allows?
- [ ] Do the delivering teams own discovery as well as delivery?
- [ ] Are flow and outcome metrics visible and used to steer?
- [ ] Does the review loop have authority to stop or pivot?
- [ ] Does leadership set intent and guardrails rather than approve items?
- [ ] Have I said what the document gets *right* against this lens before listing gaps?

---

## Reading

- **Scott Millett**, *The Accidental CIO: A Lean and Agile Playbook for IT Leaders* (Wiley, 2024) — the source. Part I (Ch. 1–3) the case and philosophies; Part II (Ch. 4–9) the five operating-model components; Part III (Ch. 10–13) strategy to execution.
- **Simon Wardley**, *Wardley Maps* (free online book) — maps and doctrine; Wardley wrote the foreword.
- **Dave Snowden & Mary Boone**, "A Leader's Framework for Decision Making" (HBR, 2007) — Cynefin.
- **Matthew Skelton & Manuel Pais**, *Team Topologies* (2019) — team types, interaction modes, cognitive load.
- **Bjarte Bogsnes**, *Implementing Beyond Budgeting* (2nd ed., 2016) — the funding and target-setting alternative to command-and-control.
- **Mik Kersten**, *Project to Product* (2018) — the funding shift and flow metrics at portfolio level.
- **Daniel Pink**, *Drive* (2009) — purpose, mastery, autonomy.
- **L. David Marquet**, *Turn the Ship Around!* (2012) — intent-based leadership.
- **Russell Ackoff**, *Re-Creating the Corporation* (1999) and **Donella Meadows**, *Thinking in Systems* (2008) — systems thinking foundations.
- **Don Reinertsen**, *The Principles of Product Development Flow* (2009) — cost of delay and queues; see `product-development-flow`.
