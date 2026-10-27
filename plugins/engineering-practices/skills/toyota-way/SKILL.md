---
name: toyota-way
description: Apply Jeffrey Liker's "The Toyota Way: 14 Management Principles from the World's Greatest Manufacturer" (2004; 2nd ed. 2021), the management system behind the Toyota Production System. Covers the 4P model (philosophy, process, people and partners, problem solving) and the 14 principles, the TPS house (just-in-time and jidoka on heijunka, standardised work and kaizen), the wastes (muda, mura, muri, unused creativity) mapped to software, and Toyota product development (chief engineer, set-based design, front-loading). Includes a review mode that scores a process, ways-of-working or governance document principle by principle as Strong, Partial or Gap with evidence. Use when reviewing how a team or organisation works, when lean has become a toolbox without a philosophy, when deciding who owns a process standard and how it improves, or when explaining jidoka, andon, heijunka, pull, genchi genbutsu, nemawashi, hansei or kaizen in a software setting.
---

# The Toyota Way (Jeffrey Liker)

Apply this skill when someone is designing or reviewing *how work is managed*: a delivery process, a ways-of-working document, an improvement programme, a governance model. It is the management-system lens behind the tools. `kanban`, `flow-efficiency` and `toyota-kata` cover specific mechanisms; this skill asks whether the system around them is built to surface problems, develop people and keep improving.

## Core Philosophy

**The tools are not the system.** Many companies copied kanban cards, andon cords and 5S, and few got Toyota's results. Liker's argument is that the tools work only inside a management philosophy: long-term thinking, flow that exposes problems, people who are developed to solve them, and leaders who go and see. Adopting the tools without the philosophy produces *lean as a toolbox*, which fades once the consultants leave.

**Two pillars (the internal "Toyota Way 2001").** *Continuous improvement*: challenge, kaizen and genchi genbutsu. *Respect for people*: respect and teamwork. Respect here means expecting people to think, and giving them the means to improve their own work. It does not mean being nice.

**Make problems visible, then solve them at the root.** Flow, pull and stopping to fix problems are designed to surface problems quickly. A system that hides problems in inventory, buffers or status reports can't improve. Lowering the water reveals the rocks.

**Standards exist to be improved.** Standardised work is the current best-known method, written down by the people who do the work so that they can improve it. A standard imposed from above and policed by reporting breaches is the opposite.

**Leaders are teachers.** Toyota grows leaders who understand the work in detail, live the philosophy and teach it. Management by results reports is replaced by going to see and coaching problem solving.

---

## The 4P Model and the 14 Principles

Liker groups the principles into four layers, from foundation to top: **Philosophy, Process, People and partners, Problem solving**. Most organisations work only in the Process layer. Toyota's advantage lies in the other three.

The numbering and wording below follow the first edition (2004). The second edition (2021) keeps fourteen principles in the same four groups. It adds scientific thinking, Toyota Kata and hoshin kanri, and rewords some principles.

### I. Philosophy — long-term thinking

**1. Base your management decisions on a long-term philosophy, even at the expense of short-term financial goals.**
A sense of purpose beyond the next quarter: generate value for the customer, society and the economy, and take responsibility for your own fate.
*Software:* invest in capability, tech debt and people even when the roadmap is full. Don't trade quality or learning for this quarter's date.

### II. Process — the right process produces the right results

**2. Create continuous process flow to bring problems to the surface.**
Move work in small batches without stopping, so that delays and defects become visible right away.
*Software:* small batches, trunk-based development, continuous delivery, WIP limits. Long queues and big releases hide problems.

**3. Use pull systems to avoid overproduction.**
Produce only what the next step needs, when it needs it. Overproduction is the worst waste because it creates and hides all the others.
*Software:* start work when capacity frees up. Don't analyse, specify or design far ahead of demand: specifications written months early go stale and get thrown away.

**4. Level out the workload (heijunka).**
Smooth volume and mix so that people and systems are neither idle nor overloaded. Work like the tortoise, not the hare.
*Software:* allocate capacity explicitly across kinds of work (features, run, debt). Avoid end-of-sprint, end-of-quarter and release-day peaks. Smooth demand on specialists.

**5. Build a culture of stopping to fix problems, to get quality right the first time (jidoka).**
Machines and people stop the line when something is wrong (andon). Quality is built in at the source, not inspected in at the end.
*Software:* a broken build stops merges. Alerts summon people who swarm the problem. Tests are written by the people who write the code. Defects go back to the team that created them, so the system learns.

**6. Standardised tasks are the foundation for continuous improvement and employee empowerment.**
Capture today's best practice so it can be repeated, taught and improved by the people doing the work.
*Software:* Definition of Done, the pipeline, runbooks and team working agreements, all owned and changed by the team. There is no kaizen without a standard to improve from.

**7. Use visual control so no problems are hidden.**
Simple visual indicators show at a glance whether work is normal or abnormal.
*Software:* boards with named queue states and WIP limits, aging work, dashboards everyone can see. Problems are radiated, not reported upward on request.

**8. Use only reliable, thoroughly tested technology that serves your people and processes.**
Adopt technology to support a proven process and the people in it, not to replace thinking.
*Software:* don't buy a tool to fix a process problem. Prove a practice manually, then automate it.

### III. People and partners — add value by developing them

**9. Grow leaders who thoroughly understand the work, live the philosophy and teach it to others.**
*Software:* engineering managers and architects who can do and explain the work. They coach rather than assign, and they grow successors rather than being a single point of failure.

**10. Develop exceptional people and teams who follow your company's philosophy.**
Stable work groups, multi-skilling, team leaders who support the work.
*Software:* long-lived teams that own their product and its outcomes. Reshuffle deliberately, not for every project.

**11. Respect your extended network of partners and suppliers by challenging them and helping them improve.**
*Software:* treat vendors, suppliers, platform teams and other departments as long-term partners. Share problems and data, and improve the interface together.

### IV. Problem solving — continuous learning

**12. Go and see for yourself to thoroughly understand the situation (genchi genbutsu).**
Decide from first-hand observation, not reports.
*Software:* read the code, watch production telemetry and real user sessions, sit with support, look at the board. Leaders who decide only from slide decks are deciding from someone else's filter.

**13. Make decisions slowly by consensus, thoroughly considering all options; implement decisions rapidly (nemawashi).**
Lay the groundwork with everyone affected, explore alternatives, then move fast once agreed.
*Software:* explore options before committing (ADRs, design reviews, example mapping, pre-mortems). Once decided, execute without re-litigating.

**14. Become a learning organisation through relentless reflection (hansei) and continuous improvement (kaizen).**
Reflect honestly on what went wrong, find the root cause (five whys), fix the standard, and spread what was learned.
*Software:* retrospectives on a regular cadence that change the standard, blameless post-incident reviews, the improvement kata. Improvement is daily work owned by the team, not an event or an escalation.

---

## The TPS House

Fujio Cho's house diagram shows how the pieces support each other:

- **Roof (goals):** best quality, lowest cost, shortest lead time, through shortening the flow by eliminating waste.
- **Pillar 1, just-in-time:** takt time, continuous flow, pull. In software: small batches, WIP limits, pull.
- **Pillar 2, jidoka:** stop on abnormality, separate people from machines. In software: CI that stops the line, built-in quality, andon and swarming.
- **Foundation:** heijunka, standardised work, kaizen, stability, and the Toyota Way philosophy.

One pillar without the other fails. Just-in-time without jidoka pushes defects downstream faster. Jidoka without just-in-time finds problems late, because inventory hides them.

---

## The Wastes, in Software Terms

**Muda** (non-value-adding activity). Taiichi Ohno named seven; Liker adds an eighth. The software mapping follows Mary and Tom Poppendieck.

| Toyota waste | Software equivalent | Typical sightings |
|---|---|---|
| Overproduction | Extra features; specs written ahead of demand | Analysis for work that is later rejected or goes stale; fixed scope delivered regardless of outcome data |
| Inventory | Partially done work | Approved-but-unstarted queues, long-lived branches, dark code behind flags for weeks, a "deferred" backlog nobody pulls from |
| Waiting | Delays | Approval gates, weekly decision meetings, waiting for test or review, shared specialists |
| Transportation | Handoffs | Analyst to developer to tester to operations; each handoff loses knowledge |
| Over-processing | Extra process | The same heavyweight route for small and large work; reports nobody acts on |
| Motion | Task switching | Many items in flight per person; interrupts landing on feature developers |
| Defects | Defects | Quality inspected in at the end; bugs fixed by people who didn't create them |
| Unused creativity (Liker's eighth) | Ideas that go nowhere | Improvement ideas that need a committee's approval; teams that may not change their own process |

**Mura** (unevenness: peaks and troughs in demand) and **muri** (overburden: people or systems pushed past capacity) cause muda. Leveling (principle 4) and slack reduce both.

---

## Toyota Product Development

From Morgan and Liker, *The Toyota Product Development System* (2006), and Sobek, Ward and Liker on set-based concurrent engineering (1999).

- **Chief engineer (shusa).** One leader owns a product from concept to launch: the vision, the customer and the trade-offs. They have authority through expertise, not reporting lines. A "champion" who tracks progress but can't trade scope against date is not a chief engineer.
- **Front-load and explore alternatives.** Toyota spends heavily early, exploring options while change is cheap. Up-front analysis is not the problem in itself.
- **Set-based design.** Keep a *set* of options open and narrow it as evidence arrives, rather than locking one point design at the start. Approving one fixed scope at the gate is point-based design.
- **Obeya.** A big room where the product's status, problems and decisions are visible to everyone involved.

---

## Reviewing a Process Through This Lens

Score the document principle by principle. For each principle, say whether it is **Strong**, **Partial** or a **Gap**, and cite the clause that shows it.

| # | Question |
|---|---|
| 1 | Does the process protect long-term capability (quality, debt, people) when short-term demand is high? |
| 2 | Does work flow in small batches, so problems show up early rather than at the end? |
| 3 | Is work pulled when capacity frees, or is analysis and design pushed ahead of demand? |
| 4 | Is load levelled across kinds of work and across specialists, or are there predictable peaks? |
| 5 | Can anyone stop the line on a problem, and is quality built in by the builders rather than inspected in? |
| 6 | Is there a written standard, and do the people doing the work own it and change it? |
| 7 | Can everyone see queues, WIP and problems at a glance, including leadership? |
| 8 | Is tooling chosen to serve a proven process, rather than to fix one? |
| 9 | Do leaders understand the work, coach and grow successors, or are they the bottleneck? |
| 10 | Are teams stable enough to grow capability and own outcomes? |
| 11 | Are partners, suppliers and other departments treated as long-term collaborators? |
| 12 | Do decision makers go and see (production data, demos, the board), or decide from reports? |
| 13 | Are alternatives explored before deciding, and is execution fast once decided? |
| 14 | Is there a regular reflection and improvement cadence with the authority to change the standard? |

Then:

1. **Map the wastes** with the table above, citing where each shows up.
2. **Pick the three to five findings with the most leverage.** Problem solving (principles 6 and 14) and people (principles 9 and 10) usually matter more than another process tweak.
3. **For each finding, state the change.**
4. **Credit what is strong before listing gaps.**

### Output template

```markdown
## Toyota Way review: <document>

| Principle | Verdict | Evidence |
|---|---|---|
| **Philosophy** | | |
| 1. Long-term philosophy | Strong / Partial / Gap | <clause, quote> |
| **Process** | | |
| 2. Continuous flow | ... | ... |
| ... | | |
| **Problem solving** | | |
| 14. Hansei and kaizen | ... | ... |

### The wastes
| Waste | Where it shows |
|---|---|

### Findings
1. **<title>** — <what and where>. **Change:** <the move>.
```

---

## Anti-patterns

- **Lean as a toolbox.** Kanban boards, stand-ups and value-stream maps inside a management system that still rewards utilisation and punishes bad news.
- **Kaizen as an event.** A quarterly improvement workshop instead of daily improvement owned by the team.
- **Andon with no response.** Alerts or escalations that nobody swarms. People stop pulling the cord.
- **Standards from above.** Process documents written by management and policed by reporting breaches. The team can't improve what it doesn't own.
- **Five whys that end at a person.** Root-cause analysis that stops at "someone made a mistake" instead of at the system that allowed it.
- **Gemba walks as inspections.** Leaders visit to check compliance instead of to understand and help.
- **Lean as headcount reduction.** Using waste removal to cut people destroys the trust that improvement depends on. Toyota's promise is that improvement won't cost anyone their job.
- **Quality by inspection.** A test or approval gate at the end standing in for building quality in.
- **Point-based commitment presented as front-loading.** Thorough analysis that ends by locking a single scope, then treating every learning as a change request.

---

## How This Skill Pairs with Others

- **`toyota-kata`** — Rother's improvement and coaching katas, the daily routine behind principle 14.
- **`flow-efficiency`** — Modig and Åhlström's quantitative case for principles 2 to 4: flow over utilisation, Little's law, Kingman.
- **`lean-software-development`** — the Poppendiecks' translation of TPS to software. The waste table above comes from it.
- **`kanban`** — the pull and visual-control mechanics (principles 3 and 7).
- **`continuous-delivery`** — small batches and built-in quality in the pipeline (principles 2 and 5).
- **`product-development-flow`** — Reinertsen's economics of queues, batch size and cost of delay.
- **`accidental-cio`** — the operating-model lens. Liker covers how work is managed; Millett covers how IT is funded, governed and organised.
- **`systems-thinking-iceberg`** — explains why a missing principle produces the behaviour you see.

---

## Quick Application Checklist

- [ ] Have I scored all fourteen principles, with evidence for each verdict?
- [ ] Have I checked whether the tools sit inside the philosophy, or stand alone?
- [ ] Does the team own its standard and have a regular cadence to improve it?
- [ ] Can anyone stop the line, and does anyone respond when they do?
- [ ] Is work pulled, and is analysis done just in time rather than ahead of demand?
- [ ] Is quality built in by the builders?
- [ ] Do leaders go and see, and teach?
- [ ] Have I mapped the eight wastes, including unused creativity?
- [ ] Have I credited what is strong before listing the gaps?

---

## Reading

- **Jeffrey K. Liker**, *The Toyota Way: 14 Management Principles from the World's Greatest Manufacturer* (McGraw-Hill, 2004; 2nd ed. 2021) — the source.
- **Jeffrey K. Liker & David Meier**, *The Toyota Way Fieldbook* (2006) — how to apply the principles.
- **Taiichi Ohno**, *Toyota Production System: Beyond Large-Scale Production* (1988) — the seven wastes and just-in-time, from the system's architect.
- **James M. Morgan & Jeffrey K. Liker**, *The Toyota Product Development System* (2006) — chief engineer, front-loading, set-based design.
- **Durward K. Sobek, Allen C. Ward & Jeffrey K. Liker**, "Toyota's Principles of Set-Based Concurrent Engineering", *MIT Sloan Management Review* (1999).
- **Mike Rother**, *Toyota Kata* (2009) — see `toyota-kata`.
- **Mary & Tom Poppendieck**, *Lean Software Development* (2003) — see `lean-software-development`.
- **Steven Spear & H. Kent Bowen**, "Decoding the DNA of the Toyota Production System", *Harvard Business Review* (1999) — the four rules underneath the tools.
