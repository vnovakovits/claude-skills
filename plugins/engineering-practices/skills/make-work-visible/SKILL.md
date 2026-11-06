---
name: make-work-visible
description: Apply Dominica DeGrandis's "Making Work Visible — Exposing Time Theft to Optimize Work & Flow" (IT Revolution, 2017; 2nd ed. 2022). Covers the five thieves of time (too much WIP, unknown dependencies, unplanned work, conflicting priorities, neglected work), how to expose and counter each, the book's own exercises (demand analysis, work item types, card design, workflow mapping, the five reasons we take on more WIP, the "Oh, By the Way" dependency matrix, the interruption reduction experiment, visualise priorities, the aging report), board design, line of commitment, flow metrics, the Time Thief O'Gram and operations review. Includes an audit mode that checks a board, tool setup or process against each thief, and notes on doing it in a digital tracker. Use when a team is busy but not shipping, WIP feels out of control, work goes stale or gets lost, interruptions or dependencies keep derailing plans, everything is top priority, or a team is designing or redesigning a board.
---

# Making Work Visible (Dominica DeGrandis)

Use this skill when work is invisible, too much is in progress, or a team is busy but not finishing.
The first move is always to show the work that exists, all of it, and the problems around it. Then
manage what you can see.

Source: **Dominica DeGrandis, *Making Work Visible: Exposing Time Theft to Optimize Work & Flow***
(IT Revolution, 2017; second edition 2022). Structure, exercise names and figure titles below are
checked against IT Revolution's companion PDF for the first edition. Material from DeGrandis's later
talks is marked as such. Exercise steps are paraphrased.

## Core ideas

1. **Five thieves steal time.** Too much WIP, unknown dependencies, unplanned work, conflicting
   priorities and neglected work. Naming the thief tells you which countermeasure to reach for.
2. **Too much WIP is the ringleader.** DeGrandis defines it as demand exceeding capacity and treats it
   as the thief that feeds the others. Conflicting priorities and unplanned work also push WIP up, so
   it is a hub, not the only root cause.
3. **Visibility comes before improvement.** A board shows the work, its state, and the problems
   delaying it. The team designs that board together through short exercises.
4. **Measure flow, not busyness.** Part 3 of the book is about metrics and feedback: flow time, lead
   and cycle time, WIP, aging, flow efficiency and batch size, reviewed in an operations review.
5. **Change dips before it improves.** The book closes on calibration and the J curve: things often get
   worse before they get better, so judge an experiment over weeks, not days.

## Structure of the book (first edition)

| Part | Chapters |
|---|---|
| Introduction | Work and Flow |
| 1. The Five Thieves of Time | 1.1–1.5, one per thief |
| 2. How to Expose Time Theft to Optimize Workflow | 2.1 Make Work Visible · 2.2 Ambush the Ringleader · 2.3 Expose Dependencies · 2.4 Committing the Perfect Crime: Unplanned Work · 2.5 Prioritize, Prioritize, Prioritize · 2.6 Preventing Negligence · 2.7 Useful Board Design Examples |
| 3. Metrics, Feedback, and Circumstances | 3.1 Your Metrics or Your Money · 3.2 The Time Thief O'Gram · 3.3 Operations Review · 3.4 The Art of the Meeting · 3.5 Beastly Practices |
| Conclusion | Calibration |

The second edition (2022) adds a preface, an afterword on what the author learned in the five years
since, more exercises and a glossary. The publisher doesn't list which exercises were added.

---

## The five thieves and their countermeasures

| Thief | How it shows | Expose it with | Counter it with |
|---|---|---|---|
| **Too much WIP** | Many things started, few finished; long waits; people say yes beyond capacity | The board with WIP made explicit (figure "Expose WIP"); a WIP report | WIP limits; the "five reasons why we take on more WIP" conversation; finishing before starting |
| **Unknown dependencies** | "Oh, by the way, we also need…"; work waits on other teams or components | The "Oh, By the Way" dependency matrix; dependency tags on cards; a dependency swimlane | Make dependencies visible early, synchronise across teams, remove dependencies where possible |
| **Unplanned work** | Plans dissolve; interruptions arrive during the work; nobody logs them | Tagging unplanned work on the board (the book's "pink dots"); a monthly trend of unplanned work | The interruption reduction experiment: a goalie, office hours, do-not-disturb time, focused sessions |
| **Conflicting priorities** | Many "top" priorities; arbitrary due dates; the loudest request wins | Visualise priorities; show where conflicting requests come from | An explicit prioritisation policy, a line of commitment, cost of delay |
| **Neglected work** | Items stuck for weeks; work waiting on validation that never comes | An aging report; "expose neglected work" on the board | Decide per stale item: finish, re-prioritise or drop; lower WIP |

DeGrandis's heuristic on dependencies, from her talks and the book's framing: each dependency roughly
doubles the chance of being late. It is a coin-flip illustration, not a measured statistic.

---

## The book's exercises

All are short, team-based and physical-first (sticky notes, a whiteboard). Run them with the people who
do the work.

### Chapter 2.1: Make Work Visible (the board-design set)

1. **Demand Analysis** (30–60 min). List the kinds of work the team does and where it comes from. Then
   list what stops the team finishing (team pain) and what customers and the business suffer (business
   pain). These become inputs to the board.
2. **Identify Work Item Types/Categories** (20–30 min). Choose the types of work that will flow across
   the board, roughly **three to seven**, each with its own colour and a legend. If the team wants more,
   use one catch-all type for work with the same workflow and tell items apart with tags or icons.
3. **Card Design** (20–30 min). Decide what each card must show so the thieves are visible: type,
   owner, blockers, dependencies, dates. A digital tool supplies most fields; on a physical board you
   design them.
4. **Workflow Mapping** (40–60 min). Start with three columns, **Options (backlog), Doing, Done**, with
   Doing drawn wide so it can be split into the states the team needs to see. Put the real work on the
   board and discuss which states matter, which type causes the most trouble, and why.

### Chapter 2.2: Explore the Five Reasons Why We Take on More WIP (15–30 min)

People pair up and ask each other why they take on more work than they have capacity for, noting one
answer per sticky. The group clusters the answers and discusses countermeasures, especially for
requests from someone they like or from their boss.

### Chapter 2.3: The "Oh, By the Way" Dependency Matrix (60–90 min)

Draw a grid with the same team names on rows and columns. **Rows are the teams impacted; columns are
the teams that impact them.** For an upcoming feature or project, mark each cell where one team's
output creates work for another and capture the dependency itself. Then discuss how to reduce the risk
of breaking or delaying another team. Variations add upcoming risks, or use software components in
place of teams.

### Chapter 2.4: The Interruption Reduction Experiment (45–60 min)

The team lists ways to reduce the cost of interruptions, such as **a goalie** (one person who fields
interruptions), office hours, do-not-disturb hours, or focused sessions. It picks one, states a
hypothesis, runs it for a week, then regroups to compare what happened.

### Chapter 2.5: Visualize Priorities (60 min)

With everyone affected in the room and each person time-boxed, answer three questions on the current
board. What is the prioritisation policy, and how is it shown? Where is the **line of commitment**:
how do people know an item is prioritised and ready to pull? How is higher-priority work visually
distinguished from lower?

### Chapter 2.6: Create an Aging Report (40–60 min)

Query the tracker for high-priority, partly done work that hasn't moved or been updated in 30 days
(widen to 60 or 90 if the list is short). Take a random sample of seven to eleven items. For each,
note how long it has been stale, the average cycle time for its type, and how long it has been in
progress compared with similar items. Ask what happens if it waits another week. Consider lowering the
WIP limit, re-prioritising, and pushing the single most valuable stale item through.

---

## Board design

The book's figures show the range: a basic To Do / Doing / Done board, the same board coloured by work
type, an expanded Doing column, dependency swimlanes and tags, a line of commitment, multi-level boards
(a team board feeding a higher-level one), "Done vs. Done Done", a Plan-Do-Check-Act board, and "teams
within teams". Principles that follow from them:

- **Columns are states the team needs to see,** not a copy of an approval process. Split Doing only
  where work waits or hands over.
- **Colour or lanes by work type,** so the mix of work is visible at a glance.
- **Show blockers and dependencies on the card,** and give cross-team dependencies their own lane when
  they dominate.
- **Draw the line of commitment.** Left of it are options; right of it the team has committed.
- **Make "done" mean done.** If work sits waiting for validation, release or a customer check, show
  that state. The book calls the place where work rots awaiting validation "the validate pit".
- **Lanes are for types of work, not for people.** "Individually named swimlanes" appear in the
  book's chapter on beastly practices: they hide shared work and encourage everyone to be busy on their
  own thing.

---

## Metrics and feedback (Part 3)

| Measure | What it shows |
|---|---|
| **Flow time; lead time and cycle time** | How long work takes end to end, and once started |
| **WIP report** | How much is in progress, by state and type |
| **Aging report** | Which items have gone stale |
| **Flow efficiency** | Active time as a share of total time; most time is usually waiting |
| **Queueing and batch size** | Why high utilisation and large batches lengthen waits |
| **Cumulative flow diagram** | Arrivals, WIP and completions over time, used in the operations review |

- **The Time Thief O'Gram** (3.2) is a simple chart the team uses to record which thieves are hurting
  them and how that changes over time. Individual charts can be combined into a team view.
- **Operations review** (3.3) is a regular, data-led review of flow across teams, using measures such
  as the cumulative flow diagram, not a status meeting.
- **The Art of the Meeting** (3.4) covers making meetings serve flow, including a Lean Coffee format.
- **Beastly Practices** (3.5) covers anti-patterns, including individually named swimlanes and
  specialisation, set against T-shaped skills.

**In later talks** (2018 onward, from her Flow Framework work), DeGrandis uses five flow metrics: flow
time, flow velocity, flow efficiency, flow load and flow distribution. She tracks **flow distribution**
across four work types (features, defects, technical debt, risk), compares the actual mix with the
target, and asks what to do less of. These names come from the Flow Framework, not the first edition.

---

## Audit mode: checking a board, tool or process

For each thief, say whether the setup **exposes** it, **counters** it, or **misses** it, and cite what
shows it.

| Thief | Questions |
|---|---|
| Too much WIP | Can anyone see how much is in progress right now, per state and per person? Is there an agreed limit, and what happens when it is hit? Has the team discussed why it takes on more? |
| Unknown dependencies | Are dependencies on other teams, components or approvals shown on cards or in a lane? Has anyone mapped which teams impact which? |
| Unplanned work | Is unplanned work tagged so its share and trend are visible? Are interruptions that never become tickets captured? Is there an agreed way to absorb them (a goalie, office hours)? |
| Conflicting priorities | Is the prioritisation policy written where the work is? Is there a line of commitment? Who can reorder, and who can't? |
| Neglected work | Is there an aging view or report? Is there a state where finished work waits for validation, and does anyone watch it? |

Then check board design (types 3–7, lanes by type not person, done means done), and whether there is a
feedback loop (Time Thief O'Gram, operations review). Close with the three changes that expose the
worst thief first.

### Output template

```markdown
## Making Work Visible audit: <board or process>

| Thief | Verdict | Evidence |
|---|---|---|
| Too much WIP | Exposes / Counters / Misses | ... |
| Unknown dependencies | ... | ... |
| Unplanned work | ... | ... |
| Conflicting priorities | ... | ... |
| Neglected work | ... | ... |

### Board design and feedback
- ...

### Changes, in order
1. **<change>**: exposes or counters <thief> because ...
```

---

## In a digital tracker

The book is physical-first but expects electronic tools. When mapping it to one:

- **Run the exercises first,** on a whiteboard with the team, then configure the tool to match. A board
  designed for the team by someone else skips the conversation that makes it stick.
- **Work item types:** one label group or issue type with three to seven values, coloured.
- **Line of commitment:** a status that means "committed and ready to pull".
- **WIP:** most trackers show column counts but don't enforce limits. Write the limits into the view or
  board description and check them in the daily meeting.
- **Unplanned work:** a tag applied when work arrives unplanned, plus a quick way to log interruptions
  that never become tickets.
- **Dependencies:** "blocked by" relations shown on cards, and a view of items waiting on another team.
- **Aging:** a saved filter for in-progress items not updated in 30 days.
- **Flow metrics:** the tool's cycle-time, lead-time and cumulative flow charts, sliced by work type.

---

## Anti-patterns

- **A board without limits.** It shows the overload without reducing it.
- **Tracking only planned work.** Unplanned work and interruptions still consume the time; leaving them
  off makes the team look underloaded.
- **Too many card types.** Past seven, people stop telling them apart. Use tags within a catch-all type.
- **Lanes per person.** Optimises individual busyness and hides the shared work.
- **Arbitrary due dates.** Dates with no real consequence drive conflicting priorities; keep fixed
  dates for real deadlines.
- **Done that isn't done.** Work parked awaiting validation, release or sign-off, counted as finished.
- **Stale work left alone.** Items that haven't moved in a month still occupy attention and WIP.
- **Status meetings in place of flow reviews.** Walk the board by work item and blocker, and review
  flow measures, not individual activity.

---

## Limits

- **The evidence is practitioner experience.** The book is a practical guide built on kanban and lean
  practice, with few studies behind its heuristics (the dependency "doubling" is an illustration).
- **It is team-centric.** Cross-team flow is covered through the dependency matrix, multi-level boards
  and operations review, but portfolio-level questions belong to other sources.
- **Metric names changed after the first edition.** Her later Flow Framework vocabulary (flow load,
  distribution and so on) isn't the book's own.

---

## How this skill pairs with others

- **`kanban`**: the Kanban Method in depth (classes of service, cadences, Little's law, CFDs).
- **`product-development-flow`**: Reinertsen's economics for WIP, queues, cost of delay and sequencing.
- **`flow-efficiency`**: the resource-versus-flow-efficiency argument for leadership.
- **`value-stream-mapping`**: where work waits end to end, before redesigning the board.
- **`toyota-kata`**: running the interruption experiment and other changes as improvement experiments.

## Reading

- **Dominica DeGrandis**, *Making Work Visible: Exposing Time Theft to Optimize Work & Flow* (IT
  Revolution, 2017; 2nd ed. 2022).
- IT Revolution, *Making Work Visible* companion PDF (list of figures and exercises) and the video
  course *Making Work Visible: Core Concepts*.
- DeGrandis talks and interviews: *Making Work Visible* (Speaker Deck, 2019); Tech Lead Journal
  episode 156; InfoQ podcast (2018).
- **David J. Anderson**, *Kanban* (2010), and **Mik Kersten**, *Project to Product* (2018), for the
  method and the Flow Framework behind her later metrics.
