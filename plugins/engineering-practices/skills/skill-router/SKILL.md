---
name: skill-router
description: Pick the right engineering-practices skill, or sequence of skills, for the situation at hand. Maps common situations — a fuzzy idea, a feature to plan, code to write or test, a bug, legacy code, a design or architecture question, an event-sourced model, a review, a pull request, a slow team or process, product discovery, writing, an agent session that went wrong — to the skills in this plugin, and lays out the main flows through them (idea to shipped change, bug to fix, legacy change, design review, improving how a team works). Use when unsure which skill applies, when the user asks "which skill should I use", "what's the process for", or "where do I start", when a task spans several skills and needs an order, or when two skills seem to overlap.
---

# Skill Router

Apply this skill when it is not obvious which practice fits, or when a piece of work will pass through several. It is a map, not a substitute: once a skill is picked, load it and follow it. Before telling someone what a skill says, read that skill — the one-line summaries here are for orientation only.

## Main flows

### Idea to shipped change

1. **Sharpen the idea** — `grilling` (an interview that settles decisions and keeps a glossary and ADRs). For a story with many rules, add `example-mapping`; for a whole process, `event-storming` or `process-level-event-storming`.
2. **Decide what to build first** — `user-story-mapping` for release slices, `splitting-user-stories` to cut stories thinner.
3. **Plan the work** — `to-tickets` for a dependency graph of thin end-to-end tickets; `ticket-writer` for each ticket's content. A single small change can skip straight to step 4.
4. **Build it test-first** — `test-driven-development`, with `unit-testing-principles` for what makes a test worth keeping, `test-data-patterns` for arranging test data, and `art-of-unit-testing` or `xunit-test-patterns` for naming, doubles and test smells.
5. **Keep the design clean as you go** — `tidy-first` for small structural changes ahead of behaviour changes, `refactoring` for named moves.
6. **Review** — `two-axis-code-review`: standards and spec, reported separately.
7. **Ship** — `pr-writer` for the pull request, `continuous-delivery` for the pipeline and release practices, `observability` so you can tell it works in production.
8. **Learn** — `agent-retro` after an agent session that went sideways; `architecture-decision-records` for any hard-to-reverse decision made along the way.

### Bug to fix

`debugging` (build a failing feedback loop first, then narrow it down) → a regression test via `test-driven-development` → `two-axis-code-review` → `pr-writer`. If the same kind of bug keeps coming back, `systems-thinking-iceberg` for the structure that produces it, and `agent-retro` if an agent introduced it.

### Changing code nobody understands

`working-effectively-with-legacy-code` (characterization tests, seams, dependency-breaking) → `tidy-first` and `refactoring` under that safety net → the normal build flow. To survey a whole service first, `service-atlas`.

### Design and architecture

| Question | Skill |
| --- | --- |
| Is this module's interface worth its cost? Deep or shallow? | `philosophy-of-software-design` |
| Does this fit in a reader's head? How big should units be? | `fractal-architecture` |
| Naming, functions, comments, error handling, smells | `clean-code` |
| Which object should own this behaviour? | `responsibility-driven-design` |
| Class and interface structure, dependency direction | `solid-principles` |
| A lighter, property-based lens on code quality | `cupid-properties` |
| Ports, adapters, layers, keeping the domain independent | `hexagonal-clean-architecture` |
| Bounded contexts, aggregates, ubiquitous language | `domain-driven-design` |
| Making illegal states unrepresentable in a typed language | `domain-modeling-made-functional` |
| Commands, events, appliers, projections, event versioning | `event-sourcing-cqrs` |
| Arriving at a design pattern from a smell | `refactoring-to-patterns` |
| An HTTP, GraphQL or gRPC interface | `api-design` |
| Recording a decision so it is not re-litigated | `architecture-decision-records` |
| General heuristics: DRY, orthogonality, tracer bullets | `pragmatic-programmer` |
| C# with `Option`, `Either`, `Aff` | `language-ext-csharp` |

### Improving how a team works

| Symptom | Skill |
| --- | --- |
| Busy but not shipping; pressure to keep everyone utilised | `flow-efficiency` |
| Work waits a long time between steps; nobody sees the whole path | `value-stream-mapping` |
| Need a board, WIP limits and flow metrics | `kanban` |
| Prioritising by value and urgency; batch sizes; queues | `product-development-flow` |
| Hidden work and interruptions eat the week | `make-work-visible` |
| Waste and learning across the whole process | `lean-software-development` |
| Running improvement experiments as a habit | `toyota-kata` |
| Reviewing a process or governance model against lean principles | `toyota-way` |
| A problem keeps recurring; where to intervene | `systems-thinking-iceberg` |
| Intake, funding, decision rights, team structure, IT strategy | `accidental-cio` |

### Product discovery

`running-lean` to test whether the problem and solution are worth pursuing → `user-story-mapping` for the journey and first release → `example-mapping` and `behavior-driven-development` for the rules and scenarios → `splitting-user-stories` and `to-tickets` to plan the build.

### Writing

`elements-of-style` for any prose: PR descriptions, ADRs, tickets, docs, messages. `pr-writer`, `ticket-writer` and `architecture-decision-records` for the structure of those specific documents.

### Learning

`teaching` to learn a concept, library, technique or codebase over one or many sessions. Any book-based skill here can be its syllabus; for a new codebase, `service-atlas` or `event-storming` makes a good first map.

---

## Telling overlapping skills apart

| These two | Use the first when… | Use the second when… |
| --- | --- | --- |
| `test-driven-development` / `unit-testing-principles` | deciding what test to write next and driving the design | judging whether a test is good, or what to mock |
| `art-of-unit-testing` / `xunit-test-patterns` | naming, structuring and choosing a stub or mock | diagnosing a test smell or choosing a fixture strategy |
| `tidy-first` / `refactoring` | deciding whether and when to tidy, and keeping it separate from behaviour | performing a specific named refactoring |
| `refactoring` / `refactoring-to-patterns` | removing a smell | the smell points toward a design pattern |
| `event-storming` / `process-level-event-storming` | exploring a whole domain or finding context boundaries | modelling one process end to end |
| `example-mapping` / `behavior-driven-development` | discovering rules and examples for one story | writing and maintaining the scenarios as living documentation |
| `splitting-user-stories` / `to-tickets` | cutting one story thinner | planning a whole piece of work as a dependency graph |
| `ticket-writer` / `to-tickets` | writing one ticket well | breaking work into many tickets with blockers |
| `grilling` / `example-mapping` | open decisions across a plan or design | the rules of one story |
| `grilling` / `teaching` | sharpening the user's own decisions | building the user's understanding of something |
| `two-axis-code-review` / `pr-writer` | reviewing someone's change | presenting your own |
| `debugging` / `working-effectively-with-legacy-code` | something is broken and you need the cause | the code works but must change and has no tests |
| `philosophy-of-software-design` / `fractal-architecture` | the cost of an interface relative to what it hides | whether a unit fits in working memory |
| `kanban` / `flow-efficiency` | setting up and running the system | explaining why utilisation is the wrong goal |
| `toyota-kata` / `toyota-way` | running improvement experiments | the management philosophy around them |
| `agent-retro` / `systems-thinking-iceberg` | improving an agent's setup after a session | a recurring organisational problem |

---

## When no skill fits

Say so rather than stretching one. Work from first principles, and if the situation recurs, it may be worth a new skill.
