# claude-skills

A curated collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills covering software engineering practices and methodology, distilled from canonical software-craftsmanship books.

Thirty-one skills bundled as a single Claude Code plugin (`engineering-practices`), plus the raw skill folders for teams who prefer to copy them in manually.

## What's in here

| Area | Skills |
| --- | --- |
| Design | `clean-code`, `solid-principles`, `cupid-properties`, `fractal-architecture`, `hexagonal-clean-architecture`, `domain-driven-design`, `domain-modeling-made-functional`, `responsibility-driven-design`, `event-storming`, `api-design`, `observability`, `architecture-decision-records` |
| Testing | `test-driven-development`, `behavior-driven-development`, `unit-testing-principles` |
| Refactoring & legacy | `refactoring`, `refactoring-to-patterns`, `tidy-first`, `working-effectively-with-legacy-code`, `pragmatic-programmer` |
| Delivery & flow | `continuous-delivery`, `kanban`, `lean-software-development`, `flow-efficiency`, `product-development-flow`, `make-work-visible`, `toyota-kata` |
| Product | `running-lean`, `splitting-user-stories`, `ticket-writer` |
| Language-specific | `language-ext-csharp` |

Each skill lives in `plugins/engineering-practices/skills/<name>/SKILL.md` with YAML frontmatter that tells Claude when to apply it.

## Install — option A: Claude Code plugin marketplace (recommended)

This is the idiomatic way. Claude Code manages installation and updates for you.

```
/plugin marketplace add vnovakovits/claude-skills
/plugin install engineering-practices@claude-skills
```

To update later:

```
/plugin marketplace update claude-skills
```

## Install — option B: clone and copy

If you'd rather drop the skills directly into your user-level skills folder:

```bash
git clone https://github.com/vnovakovits/claude-skills.git
```

Then copy the skill folders into your Claude Code skills directory:

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

You can also symlink individual skills instead of copying, so `git pull` keeps them up to date.

## Picking a subset

Don't want all 31? Both install methods support cherry-picking:

- **Plugin route**: install the plugin, then disable specific skills from Claude Code's skill settings.
- **Copy route**: only copy the folders you want.

## Skill index

- [`api-design`](plugins/engineering-practices/skills/api-design/SKILL.md)
- [`architecture-decision-records`](plugins/engineering-practices/skills/architecture-decision-records/SKILL.md)
- [`behavior-driven-development`](plugins/engineering-practices/skills/behavior-driven-development/SKILL.md)
- [`clean-code`](plugins/engineering-practices/skills/clean-code/SKILL.md)
- [`continuous-delivery`](plugins/engineering-practices/skills/continuous-delivery/SKILL.md)
- [`cupid-properties`](plugins/engineering-practices/skills/cupid-properties/SKILL.md)
- [`domain-driven-design`](plugins/engineering-practices/skills/domain-driven-design/SKILL.md)
- [`domain-modeling-made-functional`](plugins/engineering-practices/skills/domain-modeling-made-functional/SKILL.md)
- [`event-storming`](plugins/engineering-practices/skills/event-storming/SKILL.md)
- [`flow-efficiency`](plugins/engineering-practices/skills/flow-efficiency/SKILL.md)
- [`fractal-architecture`](plugins/engineering-practices/skills/fractal-architecture/SKILL.md)
- [`hexagonal-clean-architecture`](plugins/engineering-practices/skills/hexagonal-clean-architecture/SKILL.md)
- [`kanban`](plugins/engineering-practices/skills/kanban/SKILL.md)
- [`language-ext-csharp`](plugins/engineering-practices/skills/language-ext-csharp/SKILL.md)
- [`lean-software-development`](plugins/engineering-practices/skills/lean-software-development/SKILL.md)
- [`make-work-visible`](plugins/engineering-practices/skills/make-work-visible/SKILL.md)
- [`observability`](plugins/engineering-practices/skills/observability/SKILL.md)
- [`pragmatic-programmer`](plugins/engineering-practices/skills/pragmatic-programmer/SKILL.md)
- [`product-development-flow`](plugins/engineering-practices/skills/product-development-flow/SKILL.md)
- [`refactoring`](plugins/engineering-practices/skills/refactoring/SKILL.md)
- [`refactoring-to-patterns`](plugins/engineering-practices/skills/refactoring-to-patterns/SKILL.md)
- [`responsibility-driven-design`](plugins/engineering-practices/skills/responsibility-driven-design/SKILL.md)
- [`running-lean`](plugins/engineering-practices/skills/running-lean/SKILL.md)
- [`solid-principles`](plugins/engineering-practices/skills/solid-principles/SKILL.md)
- [`splitting-user-stories`](plugins/engineering-practices/skills/splitting-user-stories/SKILL.md)
- [`test-driven-development`](plugins/engineering-practices/skills/test-driven-development/SKILL.md)
- [`ticket-writer`](plugins/engineering-practices/skills/ticket-writer/SKILL.md)
- [`tidy-first`](plugins/engineering-practices/skills/tidy-first/SKILL.md)
- [`toyota-kata`](plugins/engineering-practices/skills/toyota-kata/SKILL.md)
- [`unit-testing-principles`](plugins/engineering-practices/skills/unit-testing-principles/SKILL.md)
- [`working-effectively-with-legacy-code`](plugins/engineering-practices/skills/working-effectively-with-legacy-code/SKILL.md)

## Contributing

To add or edit a skill:

1. Edit (or add) a folder under `plugins/engineering-practices/skills/`.
2. Each skill needs a `SKILL.md` with YAML frontmatter (`name`, `description`).
3. Update the index in this README.
4. Open a PR.

## License

MIT — see [LICENSE](LICENSE).
