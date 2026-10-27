---
name: agent-retro
description: Run a retrospective on a coding-agent session and improve the agent's environment, not the code. Combines Derby & Larsen's five-stage retrospective, Shigeo Shingo's poka-yoke (turn a mechanical mistake into a check that makes it impossible), and Matt Pocock's retro categories — navigation, automated checks, coding standards, steering files, tool economy, information access. Covers mining the session transcript for corrections, wrong turns and slow searches; deciding where each fix belongs (analyzer, hook, CI, reviewer standards, CLAUDE.md pointer, skill, doc or memory); the no-op test for steering instructions; and a ranked findings report. Use after a session that went sideways, when the user says "retro", "what went wrong", "why did it keep doing X" or "how do we stop this happening again", when CLAUDE.md or AGENTS.md has grown long, or when the same correction keeps being given.
---

# Agent Retro

Apply this skill after a coding-agent session, especially one that needed many corrections, took a long detour, or shipped a mistake that review caught. The question is not *"what was wrong with the code?"* but *"what about the environment let the agent go wrong, and what is the cheapest durable change that stops it next time?"* The environment is everything the agent works inside: steering files (`CLAUDE.md`, `AGENTS.md`), skills, docs, linters and analyzers, hooks, CI, tool access and memory.

It combines three sources. Esther Derby and Diana Larsen's *Agile Retrospectives* gives the structure. Shigeo Shingo's **poka-yoke** (mistake-proofing) gives the central rule: don't remind people not to make a mechanical mistake, make the mistake impossible or immediately visible. Matt Pocock's `retro` skill gives the categories of agent environment to inspect.

## Core Philosophy

**Fix the environment, not the agent.** Kerth's Prime Directive, applied to an agent: assume it did the best it could with the context, tools and instructions it had. Blame produces louder instructions; analysis produces better context.

**Mechanical mistakes get checks; judgement calls get standards.** A mistake with a fixed, detectable shape — a banned API, a wrong import, a file in the wrong folder, a missing argument — belongs in a deterministic check: an analyzer rule, a test, a hook, a CI job. An instruction that says "never do X" is a reminder, and reminders fail. Reserve written standards for what no check can decide.

**Standards belong where they are enforced.** The implementing agent carries the heaviest context load: exploring, writing, debugging. The reviewing agent receives a diff and has room to apply rules. Put coding standards in a document the reviewer reads, not in the always-loaded steering file the implementer must carry.

**Steering files are expensive.** Every line in `CLAUDE.md` or `AGENTS.md` is in context for every task, relevant or not. Keep them to navigation pointers and the few rules that apply everywhere. Everything else belongs in a doc, a skill, a standards file or a check, reached when needed.

**Every rule earns its place with evidence.** Add or change a rule because the session showed a failure it would have prevented, not because it sounds wise.

---

## The Procedure

Derby and Larsen's five stages, adapted to an agent session.

### 1. Set the stage

- Identify the session(s) under review: the current one by default, or named ones. Claude Code keeps transcripts as JSONL under `~/.claude/projects/<project>/`.
- State the goal of the work and how it ended: shipped, abandoned, corrected in review, still broken.
- Agree the scope: the agent's environment for this repo, the user's global setup, or both.

### 2. Gather data

Read the primary sources, not a summary: the transcript, the diff, review comments, CI results. Mark the moments that matter:

- **Corrections** — the user said "no", "not that", "I told you", or restated an instruction.
- **Wrong turns** — work that was undone, reverted or thrown away.
- **Slow searches** — many tool calls to find a file, a convention or a command.
- **Failed commands** — wrong flags, wrong directory, wrong shell, repeated retries.
- **Review findings** — mistakes caught after the fact by a reviewer, CI or the user.
- **Missing information** — the agent guessed because it couldn't see logs, data, a service or a doc.
- **Expensive calls** — huge outputs, whole-file reads of large files, repeated full test runs.

Quote each moment briefly, with enough context to find it again.

### 3. Generate insights

For each moment, ask why until you reach something in the environment (a short *5 whys*). Then classify it into one category:

| Category | Ask | Typical fix |
| --- | --- | --- |
| **Navigation** | Did the agent struggle to find the right file, type or command? Is there a hidden dependency between files? | A one-line pointer in the steering file or next to the code. |
| **Automated checks** | Could a check have caught the mistake? Does the repo already have one that is unwired, skipped or broken? | An analyzer or linter rule, an architecture test, a pre-commit hook, an agent hook, a CI job. |
| **Coding standards** | Did review miss something, or enforce a rule nobody wrote down? Is an existing standard wrong or unclear? | A rule in the standards doc the reviewer reads, or a rule removed. |
| **Steering files** | Is the steering file long, contradictory or stale? Does it hold rules that belong elsewhere? | Move content to a check, a standards doc, a skill or a doc; delete no-ops. |
| **Skills and procedures** | Did the agent improvise a multi-step procedure that recurs? Did a skill fail to load, or load when it shouldn't? | A new skill or script; a sharper skill description. |
| **Tool economy** | Did a tool call cost far more than its value? Did permission prompts or a slow tool interrupt the flow? | A narrower command, a script that summarises, a permission allowlist, a faster tool. |
| **Information access** | Was a crucial fact unavailable? | Read-only access to logs, a service, or data; a captured fixture; a doc. |
| **Memory** | Was the same correction given again from an earlier session? Did a stale memory mislead? | Turn the repeated correction into a rule or check; fix or delete the memory. |

A first mistake is information; a **repeated** correction is the strongest signal in the transcript. It means a lesson was given and didn't stick, so it needs a more durable home.

### 4. Decide what to do

For each finding, choose the **most durable home that is cheap enough**, in this order of preference:

1. **Make it impossible** — a type, a test, an analyzer rule, a check in CI. (Poka-yoke's control function: the mistake stops the line.)
2. **Make it immediately visible** — a hook that runs a formatter or linter after each edit, a pre-commit hook. (Poka-yoke's warning function.)
3. **Put it where it's needed** — a standards rule read at review, a skill loaded on a matching task, a doc linked from the code.
4. **Point to it** — a one-line navigation pointer in the steering file.
5. **Write it into the steering file** — only for rules that apply to nearly every task and that no check can enforce.

Before proposing a new check, read the repo's own check commands and CI configuration: an existing check that isn't wired in, or that silently fails, is the finding. A repo with no guardrail at all (no CI running lint, type check and tests, no pre-commit hook) is itself a top finding.

Rank findings by **severity × recurrence**: what it cost this session, and how often it will bite again. Keep the action list short — the top three to five. A retro that produces twenty actions produces none.

### 5. Close

Present the ranked findings with evidence and concrete proposed changes. Apply changes only once the user agrees, one finding at a time. Record what changed so the next retro can see whether it worked.

---

## Where Each Kind of Rule Belongs

| What it is | Example | Home |
| --- | --- | --- |
| A fixed, statically detectable pattern | "Don't call `DateTime.Now` in domain code" | Analyzer or linter rule, or an architecture test |
| A structural rule across modules | "The domain project must not reference infrastructure" | Architecture test in the test suite |
| Something to run after every edit | Formatting, import order | Formatter plus an agent hook or pre-commit hook |
| A judgement about consistency | "Match the error-handling style of the surrounding module" | Standards doc read by the reviewer |
| Where something lives | "Migrations are in `db/migrations/`" | One-line pointer in the steering file |
| A recurring multi-step procedure | Releasing, regenerating clients, seeding data | A skill or a script |
| Reference knowledge | The domain glossary, an external API's quirks | A doc, linked from the steering file or the code |
| A personal preference across all repos | Commit message style, review tone | User-level steering file or memory |

---

## The No-op Test

For each instruction in a steering file, ask: **if I deleted this line, would the agent behave differently?** If not, delete it. Common no-ops:

- **Defaults restated** — "write clean, readable code", "follow best practices", "be careful".
- **Unverifiable** — no one could tell whether it was followed.
- **Derivable** — describes code structure the agent finds by reading the code anyway.
- **Stale** — names a file, command, flag or tool that no longer exists. (Check every path and command a steering file names.)
- **Duplicated** — says the same as another rule, a skill or a standards doc.
- **Contradicted** — conflicts with another rule, so the agent must guess which wins.
- **Shouted** — escalating emphasis (`NEVER`, `IMPORTANT`, `MUST`) added after each failure. Emphasis is a sign the rule is in the wrong place; a check doesn't need capital letters.

---

## Output Template

```markdown
## Agent retro: <session or task>

**Outcome:** <shipped / corrected in review / abandoned>, <one line on what went wrong>

### Findings (most severe first)

#### 1. <short title> — <category>
- **Evidence:** <quoted moment(s), with where to find them>
- **Why:** <the gap in the environment, not the agent's fault>
- **Proposed change:** <file + the exact rule, check or pointer to add, move or delete>
- **Why this home:** <why a check / standard / pointer / skill, and not something cheaper>
- **Recurrence:** <one-off / likely again / already repeated>

### Steering-file hygiene
- No-ops to delete: <lines>
- Content to move: <lines → destination>

### Not worth fixing
- <moment> — <why it's a one-off or too costly to prevent>
```

---

## Anti-patterns

- **Adding a line to the steering file by reflex.** The cheapest change to make and the most expensive to carry. Prefer a check.
- **Retro without data.** Working from memory of the session instead of the transcript; the vivid moment crowds out the frequent one.
- **Fixing the instance, not the class.** Correcting the one wrong call instead of the gap that made it likely.
- **Shouting.** Making an ignored rule louder instead of moving it somewhere it is enforced.
- **Rules without evidence.** Adding guidance the session never showed a need for.
- **Too many actions.** Twenty findings with no ranking; nothing gets done.
- **Blaming the model.** "It just ignored the instruction" ends the analysis exactly where it should start: why was the instruction ignorable?
- **Never removing anything.** Steering files only grow unless every retro also deletes.

---

## How This Skill Pairs with Others

- **toyota-way** and **toyota-kata** — jidoka and poka-yoke are the origin of "make the mistake stop the line"; the retro is a small hansei (reflection) followed by one improvement experiment.
- **systems-thinking-iceberg** — a repeated correction is a *pattern*; the steering files, checks and tool access are the *structures* that produce it. Intervene at the structure.
- **debugging** — when the retro follows a hard bug, ask what would have caught it earlier and what made the feedback loop hard to build.
- **elements-of-style** — rules that survive the retro should be short, concrete and positive.
- **architecture-decision-records** — when a finding is a deliberate trade-off (a check you chose not to add), record why so the next retro doesn't re-propose it.

---

## Quick Application Checklist

- [ ] Did I read the transcript and the diff, not a recollection of them?
- [ ] Did I mark corrections, wrong turns, slow searches, failed commands, review findings and missing information?
- [ ] Is each finding traced to a gap in the environment, with quoted evidence?
- [ ] For each mechanical mistake, did I propose a check before a written rule?
- [ ] Did I check for an existing check that is unwired or broken?
- [ ] Are standards headed to the reviewer's doc, not the steering file?
- [ ] Did I run the no-op test on the steering file and name lines to delete?
- [ ] Is the list ranked by severity × recurrence and cut to the top three to five?
- [ ] Am I waiting for the user's agreement before changing anything?

---

## Reading

- **Esther Derby & Diana Larsen**, *Agile Retrospectives: Making Good Teams Great* (Pragmatic Bookshelf, 2006; 2nd ed. 2021) — the five stages: set the stage, gather data, generate insights, decide what to do, close.
- **Norman Kerth**, *Project Retrospectives: A Handbook for Team Reviews* (Dorset House, 2001) — the Prime Directive.
- **Shigeo Shingo**, *Zero Quality Control: Source Inspection and the Poka-Yoke System* (Productivity Press, 1986) — mistake-proofing: control and warning functions that stop defects at the source.
- **Matt Pocock**, `retro` skill (github.com/mattpocock/skills) — the categories of agent environment, the split between implementation and review context, and mechanical-versus-judgement classification.
- **Anthropic**, "Claude Code: Best practices for agentic coding" (anthropic.com/engineering, 2025) — keeping `CLAUDE.md` concise and tuning it like a prompt.
- **Anthropic**, "Effective context engineering for AI agents" (anthropic.com/engineering, 2025) — context as a finite resource: the smallest set of high-signal tokens.
- **Claude Code documentation** — memory (`CLAUDE.md`), hooks, skills, subagents and permission settings: the places a retro's fixes land.
