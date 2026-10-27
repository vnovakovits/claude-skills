---
name: service-atlas
description: Survey a service's codebase and publish a Miro "atlas" of it — a Pete Hodgson tech debt wall (value × cost cards), SIG-style health scorecard, hotspot treemap (churn × size), change coupling, pay-down roadmap, code quality metrics (cyclomatic complexity risk profile, unit size, parameters, duplication), system context map and coupling matrix (Khononov strength, efferent/afferent), domain logic leaking into the application layer, a Big Picture EventStorming, and one process-level EventStorming frame per pivotal phase. Grounds every claim in the code with parallel read-only agents, measures with lizard and git, renders with bundled scripts, publishes frame by frame and verifies what landed. Use when asked to assess a service's tech debt or maintainability, build a tech debt wall, map a service's coupling, onboard people onto an unfamiliar service, or EventStorm an existing codebase onto a Miro board.
---

# Service Atlas

One run produces a Miro board that answers, for one service: what hurts, where it hurts, why, how it is wired to its neighbours, and how work flows through it. The board is for onboarding and for deciding what to fix next.

Everything on it must be traceable to the code. Agents read; you verify the headline claims before anything is drawn; scripts draw.

## Before you start

- **Miro MCP** connected (`canvas_create_from_svg`, `canvas_update_from_svg`, `canvas_read_as_svg`, `board_create`). Load the Canvas Composer skill (`canvas_get_canvas_composer_skill`, step `design` then `dsl`) once per conversation; the bundled renderer already follows its grammar, but you need it to patch frames.
- **Python 3** and **lizard** (`pip install lizard`, ideally into a venv in the scratchpad) and **git**.
- Work read-only on the service repo. Write outputs to the scratchpad, and offer to copy `atlas.json` plus the SVGs into the repo (for example `docs/service-atlas/`) at the end; Miro URLs rot, a checked-in model survives.

Ask the user once, in a single batched question, only for what you cannot infer: the service name, the scope (for example "the v3 API only": exclude legacy versions everywhere), and whether to create a new board (default) or extend an existing one.

## Workflow

### 1. Measure

```bash
python scripts/measure.py <repo> <src-dir> <scratch>/measurements.json --ext .cs --since <one year ago>
```

`--ext` limits the languages; `--exclude GLOB` adds exclusions (tests, generated code and migrations are excluded by default). It writes the complexity profile, histogram, unit size, parameters, duplication, per-project table, top methods, hotspots (revisions × lines) and change-coupled pairs.

Lizard's limits: it under-counts branching inside lambdas and switch expressions and can truncate expression-bodied members. Say so on the quality frame commentary when the code is functional-style.

### 2. Survey with parallel agents

Launch the four survey agents in one message, read-only, using the briefs in `references/briefs.md` verbatim (fill in the placeholders). Each returns JSON in the shape `references/atlas-schema.md` defines:

| Agent | Produces |
|---|---|
| Debt lenses | `wall.cards` (25-80 cards across 5-6 lenses) |
| Coupling | `coupling.services` + notes (efferent and afferent) |
| Application-layer leaks | `leaks` |
| Big Picture | `big_picture` (5 pivotal phases, about 15 events) |

When the Big Picture is back and verified, launch one **process agent per phase** (same message), again with the brief from `references/briefs.md`.

### 3. Verify before drawing

Agents' reports are claims, not facts. For each agent, check the two or three findings that carry the most weight (every hot spot you will headline, every "never/always/no" claim) against the code with a quick `sed -n`/grep. Fix or drop what does not hold. Typical repairs to process models:

- two events in a row with nothing between them: insert the policy, or merge;
- external systems placed before the aggregate that calls them: order is command → aggregate → system → event, or command → system → aggregate → event when the application layer calls out first;
- an alternative that ends with two outcomes: split the rejection into its own branch;
- branch `from` indices that point at the wrong sticky after you edit the happy path.

### 4. Write `atlas.json`

Combine the agents' JSON with your own writing: scorecard (from the measurements, SIG thresholds in `references/atlas-schema.md`), roadmap (5-10 moves, each naming the wall cards it retires), and the short commentary fields. Keep board copy plain and short (apply `elements-of-style`), business language on EventStorming stickies with the code name only in the `code` field, and no ticket IDs.

### 5. Render

```bash
python scripts/render.py <scratch>/atlas.json <scratch>/measurements.json <scratch>/out --origin 0,0
```

It writes one SVG per frame and `manifest.json` (title, item count, position, size). On an existing board, pick `--origin` below the lowest existing frame plus 400 (read the board's frames first; never draw over content).

### 6. Publish and verify

- New board: `board_create`, then publish each SVG with its own `canvas_create_from_svg` call, in manifest order. One frame per call keeps each response readable and limits a partial failure to one frame.
- After each call, compare `created_count` with the manifest's `items`. If Miro reports unconfirmed items, read that frame back (`canvas_read_as_svg` with the frame id, and a scoped read over the missing area) before retrying: some unconfirmed items do land.
- Re-add only what is missing with `canvas_update_from_svg` into the existing frame (`<g data-miro-id="<frame id>" ...>`). A connector to an item from an earlier call needs that item as a stub carrying its `data-miro-id` and a local `id`.
- Never delete board items without the user's explicit yes, item by item or frame by frame.

### 7. Report

Give the board link and one link per frame (`?moveToWidget=<frame id>`), then the five or six findings worth acting on, each with its evidence. State what was not verified and which parts of the EventStorming are inferences from code rather than a workshop; recommend a domain expert walks the EventStorming frames before they are used for onboarding.

## Rules learned the hard way

- **Big Picture means big.** About 15 events, 5 pivotal events, at most 6 hot spots, two lanes at most. Details belong in the process frames.
- **External systems are pink stickies with name and role only** (for example "Pachira: payments"). No call/message/integration-type labels on EventStorming frames; that belongs on the coupling frames.
- **One scope.** If the user names an API version, model only that version everywhere; legacy paths appear at most as a hot spot.
- **Hot spots are specific, verified claims or questions**, placed on the sticky they are about: missing failure paths, silence checks ("what if X never answers?"), out-of-order messages, rules living in the wrong layer.
- **Process grammar:** read model → actor → command → aggregate or system → event → policy → next command; every command has an issuer, every event a source; conditions are policies, never arrow labels.
- **Escape once.** Sticky and shape `data-content` takes HTML (`<b>`, `<br>`, `<i>`) escaped once as an attribute; the renderer handles it. Hand-written patches must not double-escape apostrophes.

## Frames

| # | Frame | Source |
|---|---|---|
| 1 | Tech debt wall | `wall` |
| 2 | Health scorecard | `scorecard` |
| 3 | Hotspots treemap | measurements + `hotspots.commentary` |
| 4 | Files that change together | measurements + `change_coupling.commentary` |
| 5 | Moves to pay down the debt | `roadmap` |
| 6 | Code quality metrics | measurements + `quality` |
| 7 | System context map | `coupling` |
| 8 | Coupling matrix | `coupling` |
| 9 | Domain logic in the application layer | `leaks` (optional) |
| 10 | Big Picture EventStorming | `big_picture` |
| 11+ | Process: one per pivotal phase | `processes` |

## Related skills

`event-storming` and `process-level-event-storming` (the method behind frames 10+), `domain-driven-design`, `unit-testing-principles`, `fractal-architecture` (complexity ceilings), `elements-of-style` (board copy).
