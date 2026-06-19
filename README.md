# claude-skills

A shared collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills the team can install, so we all code with the same set of design heuristics, refactoring catalogs, and methodology vocabularies in Claude's hands.

> **TL;DR — for teammates installing this:** Run the two `/plugin` commands in [Install](#install), then keep coding. Claude will automatically pull the right skill into context when your task matches one (e.g. "refactor this method" → `refactoring`; "design a new endpoint" → `api-design`). You don't invoke skills manually.

---

## What is a Claude Code skill?

A skill is a Markdown file (`SKILL.md`) with YAML frontmatter — a `name` and a `description`. Claude Code keeps the names and descriptions in mind at all times; when your current task matches a skill's description, Claude silently loads that skill's full body into context and follows its guidance.

So installing a skill doesn't add a button or a slash command. It changes how Claude behaves when the matching situation comes up. Think of it as a shared playbook the whole team agrees on.

---

## Prerequisites

- [Claude Code](https://docs.claude.com/en/docs/claude-code) installed (CLI, IDE extension, or desktop app — any of them works)
- Git (only if you use [Option B](#option-b--clone-and-copy))

---

## Install

### Option A — Plugin marketplace (recommended)

Inside Claude Code, run:

```
/plugin marketplace add vnovakovits/claude-skills
/plugin install engineering-practices@claude-skills
```

That's it. Claude Code manages the install location and updates for you.

### Option B — Clone and copy

If you'd rather drop the skill folders straight into your user folder (no plugin layer):

```bash
git clone https://github.com/vnovakovits/claude-skills.git
```

Then copy them into your Claude Code skills directory:

**macOS / Linux**

```bash
cp -r claude-skills/plugins/engineering-practices/skills/* ~/.claude/skills/
```

**Windows (PowerShell)**

```powershell
Copy-Item -Path .\claude-skills\plugins\engineering-practices\skills\* `
          -Destination $env:USERPROFILE\.claude\skills\ `
          -Recurse
```

Tip: instead of copying, symlink each folder. Then `git pull` is the only step needed to stay current.

---

## Verifying it worked

1. Open Claude Code.
2. Start a new session. Type `/help` (or check the skills list in your settings).
3. You should see the skills from this repo by name — `clean-code`, `refactoring`, `solid-principles`, etc.
4. Try a task that triggers one: e.g. ask Claude to "review this method against SOLID". The `solid-principles` skill should activate.

---

## How and when skills fire

Skills load based on Claude's read of your current task against each skill's `description` field. You won't see a notification — the behaviour just gets sharper.

Examples:

| What you ask | Skill that fires |
| --- | --- |
| "Refactor this method." | `refactoring`, often with `clean-code` |
| "Design a new endpoint for X." | `api-design` |
| "Split this story." | `splitting-user-stories` |
| "Write a bug report ticket." | `ticket-writer` |
| "Why is this test brittle?" | `unit-testing-principles` |
| "Set up a Kanban board." | `kanban`, often with `make-work-visible` |
| "Model this domain." | `domain-driven-design`, sometimes `domain-modeling-made-functional` |

If Claude isn't picking up the skill you want, just mention it by name — *"apply the `refactoring` skill to this method"* — and it will pull it in.

---

## Updating

- **Plugin route:** `/plugin marketplace update claude-skills`
- **Copy route:** `git pull` in your local clone, then re-copy the folders (or rely on the symlinks if you set them up).

---

## Disabling skills you don't want

You don't have to take all 31.

- **Plugin route:** open Claude Code's skill settings and toggle individual skills off.
- **Copy route:** delete the unwanted folder from `~/.claude/skills/`.

---

## Skill catalog

All skills live under [`plugins/engineering-practices/skills/`](plugins/engineering-practices/skills).

### Design & architecture

| Skill | Apply when |
| --- | --- |
| [`clean-code`](plugins/engineering-practices/skills/clean-code/SKILL.md) | Writing, refactoring, or reviewing code (Robert C. Martin — naming, small functions, comments, error handling, smells). |
| [`solid-principles`](plugins/engineering-practices/skills/solid-principles/SKILL.md) | Designing classes, structuring inheritance, defining interfaces, organizing dependencies. |
| [`cupid-properties`](plugins/engineering-practices/skills/cupid-properties/SKILL.md) | Evaluating code quality through Dan North's "joyful code" lens — Composable, Unix philosophy, Predictable, Idiomatic, Domain-based. |
| [`fractal-architecture`](plugins/engineering-practices/skills/fractal-architecture/SKILL.md) | Sizing methods/classes against working-memory limits (Mark Seemann — "Code That Fits in Your Head"). |
| [`hexagonal-clean-architecture`](plugins/engineering-practices/skills/hexagonal-clean-architecture/SKILL.md) | Structuring an application around its domain — Ports & Adapters, Onion, Clean Architecture. |
| [`domain-driven-design`](plugins/engineering-practices/skills/domain-driven-design/SKILL.md) | Modeling complex domains — bounded contexts, aggregates, ubiquitous language (Evans & Vernon). |
| [`domain-modeling-made-functional`](plugins/engineering-practices/skills/domain-modeling-made-functional/SKILL.md) | DDD in a typed functional language — making illegal states unrepresentable (Scott Wlaschin). |
| [`responsibility-driven-design`](plugins/engineering-practices/skills/responsibility-driven-design/SKILL.md) | Distributing behaviour across objects — Wirfs-Brock's CRC cards, role stereotypes, Tell-Don't-Ask. |
| [`event-storming`](plugins/engineering-practices/skills/event-storming/SKILL.md) | Discovering business processes and bounded contexts collaboratively (Alberto Brandolini). |
| [`api-design`](plugins/engineering-practices/skills/api-design/SKILL.md) | Designing REST / GraphQL / gRPC endpoints — versioning, pagination, errors, idempotency. |
| [`observability`](plugins/engineering-practices/skills/observability/SKILL.md) | Instrumenting services — structured logging, RED/USE/golden signals, tracing, SLOs. |
| [`architecture-decision-records`](plugins/engineering-practices/skills/architecture-decision-records/SKILL.md) | Capturing significant architectural decisions in lightweight, immutable ADRs (Michael Nygard). |

### Testing

| Skill | Apply when |
| --- | --- |
| [`test-driven-development`](plugins/engineering-practices/skills/test-driven-development/SKILL.md) | Driving design outside-in in small red/green/refactor steps (GOOS, Mancuso, Beck). |
| [`behavior-driven-development`](plugins/engineering-practices/skills/behavior-driven-development/SKILL.md) | Three-amigos discovery, Gherkin scenarios, living documentation (North, Adzic, Wynne). |
| [`unit-testing-principles`](plugins/engineering-practices/skills/unit-testing-principles/SKILL.md) | Evaluating test quality — Vladimir Khorikov's four pillars, mocks vs stubs, what's worth testing. |

### Refactoring & legacy code

| Skill | Apply when |
| --- | --- |
| [`refactoring`](plugins/engineering-practices/skills/refactoring/SKILL.md) | Improving structure without changing behaviour — Martin Fowler's named refactorings & smells. |
| [`refactoring-to-patterns`](plugins/engineering-practices/skills/refactoring-to-patterns/SKILL.md) | Arriving at GoF patterns through refactoring driven by smells, not upfront design (Joshua Kerievsky). |
| [`tidy-first`](plugins/engineering-practices/skills/tidy-first/SKILL.md) | Separating "tidyings" from behaviour changes — Kent Beck's economic view of software design. |
| [`working-effectively-with-legacy-code`](plugins/engineering-practices/skills/working-effectively-with-legacy-code/SKILL.md) | Changing code that has no tests — characterization tests, seams, dependency-breaking refactorings (Feathers). |
| [`pragmatic-programmer`](plugins/engineering-practices/skills/pragmatic-programmer/SKILL.md) | General heuristics — DRY, orthogonality, tracer bullets, broken windows (Hunt & Thomas). |

### Delivery & flow

| Skill | Apply when |
| --- | --- |
| [`continuous-delivery`](plugins/engineering-practices/skills/continuous-delivery/SKILL.md) | Designing pipelines, branching, deploys, DORA metrics (Humble & Farley). |
| [`pr-writer`](plugins/engineering-practices/skills/pr-writer/SKILL.md) | Writing, scoping, and sizing pull requests that are fast to review — small CLs, Conventional-Commit titles, stand-alone descriptions (Google eng-practices, GitHub, SmartBear). |
| [`kanban`](plugins/engineering-practices/skills/kanban/SKILL.md) | Setting up boards, WIP limits, flow metrics (Hammarberg & Sundén, Anderson, Leopold). |
| [`lean-software-development`](plugins/engineering-practices/skills/lean-software-development/SKILL.md) | Mary & Tom Poppendieck's seven principles — eliminate waste, amplify learning, see the whole. |
| [`flow-efficiency`](plugins/engineering-practices/skills/flow-efficiency/SKILL.md) | Diagnosing why "busy" doesn't equal "shipping" — Modig & Åhlström's flow-efficiency framework. |
| [`product-development-flow`](plugins/engineering-practices/skills/product-development-flow/SKILL.md) | Don Reinertsen — cost of delay, WSJF, batch sizing, queueing theory for product work. |
| [`make-work-visible`](plugins/engineering-practices/skills/make-work-visible/SKILL.md) | Surfacing invisible work, the Five Thieves of Time, Personal Kanban (Dominica DeGrandis). |
| [`toyota-kata`](plugins/engineering-practices/skills/toyota-kata/SKILL.md) | Running improvement experiments via the Improvement Kata + Coaching Kata (Mike Rother). |

### Product

| Skill | Apply when |
| --- | --- |
| [`running-lean`](plugins/engineering-practices/skills/running-lean/SKILL.md) | Finding product/market fit — Lean Canvas, Customer Factory, 90-day cycles (Ash Maurya). |
| [`user-story-mapping`](plugins/engineering-practices/skills/user-story-mapping/SKILL.md) | Mapping the whole user journey to plan releases and carve a walking-skeleton MVP — backbone & ribs, slice by outcome (Jeff Patton). |
| [`splitting-user-stories`](plugins/engineering-practices/skills/splitting-user-stories/SKILL.md) | Slicing big stories into INVEST-compliant pieces (Wake, Lawrence, Cohn, Adzic, Patton). |
| [`ticket-writer`](plugins/engineering-practices/skills/ticket-writer/SKILL.md) | Drafting Jira / Linear / GitHub issues that pass review (problem-first structure, INVEST, SMART). |

### Language-specific

| Skill | Apply when |
| --- | --- |
| [`language-ext-csharp`](plugins/engineering-practices/skills/language-ext-csharp/SKILL.md) | Reading or writing C# that uses the LanguageExt library (`Option<T>`, `Either<L,R>`, `Aff<T>`, etc.). |

---

## Troubleshooting

**A skill isn't activating.** Skills load when their description matches your task. Either be more explicit ("apply clean-code principles") or mention the skill by name ("use the refactoring skill"). Check that the skill appears in your skills list to confirm install.

**`/plugin install` says the plugin isn't found.** Run `/plugin marketplace add vnovakovits/claude-skills` first.

**I installed both ways and now have duplicates.** Pick one. Either uninstall the plugin (`/plugin uninstall engineering-practices@claude-skills`) or delete the manually-copied folders from `~/.claude/skills/`.

**A skill description seems wrong / outdated.** Open a PR (see below).

---

## Contributing

1. Edit (or add) a folder under [`plugins/engineering-practices/skills/`](plugins/engineering-practices/skills).
2. Each skill needs a `SKILL.md` with YAML frontmatter (`name`, `description`). Keep the `description` specific — it's what makes the skill trigger at the right moment.
3. Update the [skill catalog](#skill-catalog) in this README.
4. Open a PR.

If you're adding several related skills, tag a release after merging so plugin users can pull a stable version.

---

## License

[MIT](LICENSE).
