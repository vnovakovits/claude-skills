---
name: toyota-kata
description: Apply Mike Rother's Toyota Kata from "Toyota Kata: Managing People for Improvement, Adaptiveness and Superior Results" (McGraw-Hill, 2009) — the structured patterns of scientific experimentation that drive Toyota's actual learning capability. Covers the Improvement Kata (4 steps: understand the direction, grasp the current condition, establish the next target condition, iterate experiments toward the target) and the Coaching Kata (5 questions a coach asks the improver), the "threshold of knowledge" idea, PDCA inside the Improvement Kata, storyboards, the improver/coach/2nd-coach hierarchy, and why kata > tools as Toyota's actual competitive advantage. Use when a team has Kanban and metrics in place but improvement has stalled, when "continuous improvement" has become an empty ritual, when leaders want to develop people's improvement capability rather than dictate solutions, when running an improvement cadence (retrospectives that change behavior), or when adopting a scientific approach to process change.
---

# Toyota Kata (Mike Rother)

Apply this skill when continuous improvement has stalled, when retrospectives produce action items that don't change behavior, when a team has Kanban and metrics but no improvement engine, when leadership wants to grow the team's improvement capability instead of dictating solutions, or when applying the scientific method to process change without the overhead of a formal A3.

## Core Philosophy

**Toyota's competitive advantage isn't TPS tools.** It's the *kata* — the daily routines of scientific experimentation and coaching that produce continuous improvement. Other companies copied the tools (kanban, andon, 5S) and got short-term gains; the kata is what produces the long-term adaptive capability.

**Improvement is a skill, not an event.** It's developed by daily practice, not by quarterly initiatives or Kaizen events.

**Two complementary kata.** The **Improvement Kata** is the routine the improver follows. The **Coaching Kata** is the routine the coach uses to develop the improver's capability. They work together: the coach asks structured questions that make the improver think scientifically.

**Embrace the threshold of knowledge.** At any moment, you know some things and don't know others. The boundary is the threshold of knowledge. Improvement happens by designing experiments that push past it.

**Move toward a target condition, not toward "better".** Vague aspirations don't drive learning. Specific, measurable target conditions do.

**Process matters more than outcome.** Toyota Kata is judged by whether teams develop the *capability* to improve, not by any single improvement's result.

---

## The Improvement Kata (4 Steps)

The pattern an improver follows. A continuous cycle, not a one-time event.

### Step 1: Understand the Direction / Challenge
What is the long-term direction we're heading? What's the bigger vision the next year of improvement serves?

This isn't a target — it's a direction. "Become the most reliable team in the company". "Reach zero post-deploy incidents". "Decimate cycle time".

The direction provides context but isn't actionable on its own.

### Step 2: Grasp the Current Condition
**Where are we now, in measurable detail?**

This is the most often-skipped step. Teams want to jump to solutions. The kata insists: characterize the current state precisely before improving it.

For software:
- What is current cycle time at p50, p85, p95?
- What is the distribution of cycle times — does any subset of work behave differently?
- What's the throughput per week, and how variable is it?
- Where in the workflow do items accumulate?
- What are the recurring failure modes (bug categories, escapes, rework triggers)?

The goal is **facts about the system**, not opinions about why it's bad.

### Step 3: Establish the Next Target Condition
**Where do we want to be, by when, in measurable detail?**

A target condition is:
- **Specific** — "p85 cycle time below 5 days" (not "faster")
- **Measurable** — a number, derived from the current condition
- **Time-bounded** — "by 4 weeks from now" (not "eventually")
- **Achievable but uncomfortable** — past the threshold of knowledge; we don't yet know how

Crucially, the target condition is **outside the team's current knowledge** about how to reach it. If you already know how, it's not a target condition; it's just an action item.

### Step 4: Experiment Toward the Target (PDCA)
Iterate Plan-Do-Check-Act experiments toward the target.

Each experiment:
- **Plan** — "We will try X. We expect to see Y."
- **Do** — Run the experiment for a defined period.
- **Check** — What actually happened? Did the expectation hold?
- **Act** — Adopt the change (target advance), adjust (different experiment), or revert.

**Experiments are tiny.** Often a single day or single iteration. The goal is fast learning, not big bets.

**Failed experiments are not failures.** They're information. The kata is the scientific method: hypothesis → experiment → result → new hypothesis.

---

## The Coaching Kata (5 Questions)

The pattern a coach follows. Used in a daily 15-30 minute coaching cycle.

The coach asks the same five questions, in order, every time:

### 1. What is the target condition?
What are we trying to achieve, by when, measurably?

### 2. What is the actual condition now?
What does the current state look like, with data?

### 3. What obstacles do you think are preventing you from reaching the target condition? Which one are you addressing now?
Surface the threshold of knowledge. Which specific obstacle is in play?

### 4. What is your next step? What do you expect?
What's the next experiment? What's the prediction? (The prediction is critical — without it, you can't tell whether you learned anything.)

### 5. When can we go and see what we have learned from taking that step?
Schedule the check-in. Often the next day.

These five questions, asked daily, in this order, produce two effects:
- **The improver thinks more scientifically over time** — internalizing the pattern.
- **The coach learns to coach** — developing their own ability to develop others.

**The coach does not provide answers.** This is the discipline. When the improver is stuck, the coach asks more questions, not provides solutions. Because the goal is developing the improver's capability, not maximizing this week's improvement.

---

## The Storyboard

The physical/digital artifact that supports the kata. A single sheet (or wall area) per improvement, showing:

```
┌────────────────────────────────────────────────────────┐
│ DIRECTION / CHALLENGE                                  │
│ Become the team with the most predictable cycle time   │
├────────────────────────────────────────────────────────┤
│ TARGET CONDITION (by: 4 weeks)                         │
│ - p85 cycle time ≤ 5 days (currently 11)               │
│ - Cycle-time spread (p95-p50) ≤ 4 days                 │
├────────────────────────────────────────────────────────┤
│ CURRENT CONDITION                                      │
│ - p50: 4 days, p85: 11 days, p95: 19 days              │
│ - Spread: 15 days                                      │
│ - Items > 7 days: mostly stories with >3 review cycles │
├────────────────────────────────────────────────────────┤
│ OBSTACLES                                              │
│ ☐ PRs wait avg 2.5 days for first review               │
│ ☑ Test environments shared, causing queueing           │
│ ☐ Tickets carry unclear acceptance criteria            │
├────────────────────────────────────────────────────────┤
│ NEXT EXPERIMENT                                        │
│ Try: Round-robin daily review duty                     │
│ Expect: First-review wait drops below 6 hours          │
│ Check: Friday standup                                  │
└────────────────────────────────────────────────────────┘
```

Updated visibly, daily. Shows what's been learned. Lets coaches see the state without long discussions.

---

## The Improver / Coach / 2nd Coach Hierarchy

Rother documents Toyota's coaching structure:

- **The improver** — the person (or team) doing the work and the experiments. They use the Improvement Kata.
- **The coach** — usually the improver's direct supervisor. They use the Coaching Kata. They develop the improver's capability.
- **The 2nd coach** — the coach's coach. Often two levels up. They develop the coach's capability — observing coaching sessions, debriefing them, asking the coach what they noticed.

This three-level structure is what produces the sustained capability. The coach is themselves being coached. The skill propagates up the hierarchy as a deliberate developmental practice.

In software-team adoption:
- Improver: the team (or an individual on the team).
- Coach: the team lead or engineering manager.
- 2nd coach: the engineering director or VP, periodically.

Many adoptions skip the 2nd-coach role and weaken over time as a result.

---

## Threshold of Knowledge

A central concept. At any moment:
- You **know** some things about how to reach the target.
- You **don't know** some things — they lie beyond the threshold.

Improvement happens by designing experiments that probe the threshold:
- If you already know what will happen, it's not an experiment, it's just doing.
- If you have no idea what will happen, it's not an experiment, it's a guess.
- The sweet spot: you have a prediction, but you're not sure — and the test will tell you.

The discipline is to **identify the threshold for the current obstacle** and design experiments at it. Not too easy (no learning) and not too hard (no signal).

---

## PDCA Inside the Kata

PDCA (Plan-Do-Check-Act) is the workhorse cycle within step 4. Each cycle is small:

- **Plan:** "We'll try X. We predict Y because Z."
- **Do:** Run the experiment for the agreed time.
- **Check:** What happened? Compare to prediction.
- **Act:** Decide — adopt, adjust, or revert. Update what we now know.

**Each cycle is typically a single working day or single iteration.** Not a week, not a sprint. The fast cadence is what creates the learning rate.

**The prediction is non-negotiable.** Without a prediction, you can't tell whether the experiment confirmed or surprised. Most teams skip this and lose the learning value.

---

## Why Kata > Tools

Rother's central argument. After decades of attempted Toyota imitation:
- Companies copied **kanban boards** → got marginal short-term gains.
- Copied **5S** → got tidier workplaces.
- Copied **andon** → built escalation systems that nobody used.
- Copied **value stream mapping** → produced one-time maps that gathered dust.

What didn't transfer was the **kata** — the daily routine. Because kata is invisible (you can't photograph it), foreign visitors didn't bring it home with them.

The implication for software teams: **adopting Kanban + retrospectives is not enough**. Without an improvement discipline practiced daily, the improvements stop.

This is the gap Toyota Kata fills.

---

## Toyota Kata vs Other Improvement Approaches

| Approach | Cadence | Coach role | Output |
|---|---|---|---|
| **Retrospectives (Scrum/Kanban)** | Every iteration (2-4 weeks) | None / facilitator | Action items list |
| **Kaizen events** | Quarterly / annual | Sensei | Process changes |
| **A3 problem solving** | Per problem | A3 owner / sponsor | One-page report |
| **Toyota Kata** | Daily | Coach using 5 questions | Continuously evolving target conditions |

Toyota Kata's distinguishing feature: **daily cadence + structured coaching**. Retrospectives produce action items that often fail to land because nobody coaches the experimentation. A3 is heavier and slower. Kaizen events are too infrequent. Kata fills the daily-coaching gap.

**Best combined:** retrospectives surface obstacles → kata works on them daily → A3 documents major learnings.

---

## How This Skill Pairs with Others

- **`kanban`** — Kanban provides the system to improve. Toyota Kata provides the improvement engine. Hammarberg & Sundén's "improve evolutionarily" practice IS Toyota Kata in spirit; this skill gives it procedural detail.
- **`flow-efficiency`** — Modig & Åhlström's frame helps choose meaningful target conditions (flow efficiency targets).
- **`product-development-flow`** — Reinertsen's quantitative principles help design economically-sensible experiments.
- **`lean-software-development`** — the Poppendiecks' "amplify learning" principle is operationalized by Toyota Kata.
- **`test-driven-development`** — the inner-loop equivalent: red-green-refactor is PDCA at the code level.
- **`continuous-delivery`** — the deployment side; each deployment is potentially a PDCA cycle if you're measuring outcomes.
- **`observability`** — provides the data for "Check"; without measurement, kata degrades into opinion.
- **`architecture-decision-records`** — major target conditions and the learnings from major experiments deserve ADRs.

---

## Common Pitfalls

- **Skipping "grasp the current condition".** Jumping to solutions. The kata insists on facts first.
- **Targets that are inside current knowledge.** "We'll do code review faster" — but how? If you don't know, that's a real target. If you do, just do it.
- **Targets without measurable terms.** "Improve quality" isn't actionable. "Reduce post-deploy bugs to under 2 per release" is.
- **Skipping the prediction.** "Let's try X" without "we expect Y" wastes the learning.
- **Coach providing answers.** The temptation is overwhelming. Resist. The point is to develop the improver, not to maximize improvement speed this week.
- **Weekly or monthly coaching cadence.** Too slow. The kata requires daily or near-daily.
- **Treating kata as one more meeting.** It's a daily 15-minute practice. If it's bloating, it's broken.
- **No 2nd coach.** The coach's coaching degrades over time without feedback. Build the three-level structure or expect drift.
- **Adopting only the artifacts (storyboard, 5 questions) without the discipline.** Cargo-cult kata. The substance is daily practice, not the worksheet.

---

## A Worked Software Kata

A team's situation: cycle time is highly variable (p50=4d, p95=19d). The team has adopted Kanban but hasn't improved on this in 3 months.

**Direction:** become the team with the most predictable cycle time in the org.

**Current condition (week 0):** p85 = 11 days, with most outliers being stories that required multiple review cycles (3+ revisions per PR).

**Target condition (4 weeks):** p85 ≤ 5 days, with no more than 2 review cycles per PR on average.

**Obstacles surfaced by the team:**
1. PRs wait 2.5 days for first review on average.
2. Reviewers leave vague feedback requiring multiple rounds.
3. Test environments are shared and queued for.

**Coach's daily cycle (improver = team lead):**

*Monday:* "What's the target? What's the current condition? Which obstacle are you working on?" — team picks #1 (review wait).
"What's your next step?" — "Daily rotating review duty: one person owns being available for review."
"What do you expect?" — "First-review wait drops below 6 hours."
"When will we go see?" — "Friday."

*Friday:* "What's the target? What's actual now?" — first-review wait is now 5 hours (down from 60). p85 cycle time: 9 days (was 11).
"What did you learn?" — "Faster first review didn't fix all of it. Many PRs go to multiple rounds."
"What obstacle next?" — #2 (vague feedback).
"Next experiment?" — "Reviewer checklist + reviewer responsible for clear acceptance criteria."
"What do you expect?" — "Average rounds per PR drops below 2."
"When go see?" — "Wednesday."

…and so on. Each experiment is small, predicted, and checked. Over weeks, the team accumulates learning. After 4 weeks, p85 is at 5 days. The target was met; a new target condition is set.

This is what continuous improvement looks like when it's actually working.

---

## Quick Application Checklist

For adopting Toyota Kata:

- [ ] Have we picked a direction / challenge that motivates real improvement?
- [ ] Have we grasped the current condition in measurable terms, not opinions?
- [ ] Is the target condition specific, measurable, time-bounded, and outside current knowledge?
- [ ] Do we have a coach using the Coaching Kata?
- [ ] Do we have a 2nd coach for the coach?
- [ ] Are we running PDCA daily, not weekly?
- [ ] Are predictions written down before each experiment?
- [ ] Is the storyboard visibly updated and reflecting reality?

For a given coaching session:

- [ ] Did I ask "what is the target?" first, not "what should we do?"
- [ ] Did I get the actual condition with data, not opinion?
- [ ] Did I surface the specific obstacle we're working on?
- [ ] Did I make the next step specific, with a prediction?
- [ ] Did I resist providing the answer?
- [ ] Did I schedule the next check-in?

When improvement has stalled:

- [ ] Are target conditions outside current knowledge, or just to-do lists?
- [ ] Are we measuring the right things?
- [ ] Are we running fast experiments or slow ones?
- [ ] Is the coach providing answers instead of asking questions?
- [ ] Has the 2nd-coach role atrophied?

---

## Reading

- **Mike Rother**, *Toyota Kata: Managing People for Improvement, Adaptiveness and Superior Results* (McGraw-Hill, 2009) — the source.
- **Mike Rother**, *The Toyota Kata Practice Guide* (McGraw-Hill, 2017) — hands-on companion; checklists, exercises, sample storyboards.
- **Mike Rother & Gerd Aulinger**, *Toyota Kata Culture* (2017) — the leadership-level companion.
- **Mike Rother & John Shook**, *Learning to See* (1999) — value-stream mapping. Useful precursor to identifying current conditions.
- **Mary & Tom Poppendieck**, *Implementing Lean Software Development* (2006) — overlapping material on continuous improvement. See the `lean-software-development` skill.
- **Niklas Modig & Pär Åhlström**, *This is Lean* (2012) — the strategic frame. See the `flow-efficiency` skill.
- **Steven J. Spear**, *The High-Velocity Edge* (2009) — the broader theory of "swift, even flow" through experimentation.
- **Edwards Deming**, *Out of the Crisis* (1982) — the foundation; PDCA is Deming's via Shewhart.
- **Brent Gleeson** and various authors on coaching — the coaching kata draws on broader developmental-coaching practice.
- **mikerother.com** and **toyotakata.com** — practical resources, free downloads of storyboards, etc.
