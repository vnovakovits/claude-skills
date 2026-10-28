---
name: two-axis-code-review
description: Review a branch or pull request on two separate axes, reported side by side and never merged into one ranking. Standards — does the diff follow this repository's written rules (CLAUDE.md, AGENTS.md, CONTRIBUTING, coding standards) plus a baseline of Fowler's code smells? Spec — does it do what the ticket, spec or plan asked, with nothing missing, nothing extra and nothing done wrongly? Draws on Boehm's verification vs validation ("building the product right" vs "building the right product"), Google's code-review practice and Matt Pocock's two-axis review. Covers pinning the diff to a merge base, finding the spec and the standards sources, running each axis as its own reviewer (in parallel where subagents exist), verifying every finding against the code before reporting it, and the report format. Use when asked to review a branch, PR or work-in-progress change, to check a change against its ticket, or to "review since X".
---

# Two-Axis Code Review

Apply this skill when reviewing a change: a branch, a pull request, uncommitted work. It answers two questions separately, because a change can pass one and fail the other:

- **Standards** — is it built right? Does the code follow the rules this repository writes down, and is it free of the classic smells?
- **Spec** — is it the right thing? Does it do what the ticket, spec or plan asked: all of it, only it, correctly?

Code that follows every convention but implements the wrong behaviour passes Standards and fails Spec. Code that does exactly what was asked in a way the codebase forbids passes Spec and fails Standards. Reporting them as one list lets one axis hide the other, so they stay apart from start to finish.

## Core Philosophy

**Verification and validation are different questions** (Boehm): "Are we building the product right?" and "Are we building the right product?" Each needs its own source of truth — the standards for the first, the spec for the second.

**Scope is the diff.** Review what the change touches, against a fixed point (usually the merge base with the main branch). Problems that were already there are not findings for this change.

**A finding is a claim until checked.** Before reporting anything, confirm it against the code: read the lines, run the build, run the relevant tests. Say what the evidence was. An unverified finding wastes the author's time and the reviewer's credibility.

**Written rules first, judgement second.** A documented standard is a hard finding when broken. A smell from the baseline is always a judgement call, labelled as such, and a documented standard that endorses something overrides the baseline.

**Separate reviewers keep separate heads.** Run each axis as its own pass, by a separate subagent where that is possible, so the spec reviewer is not anchored by style issues and the standards reviewer is not drawn into product questions.

---

## The Procedure

### 1. Pin the diff

- Take the fixed point the user names (a branch, tag, commit, `HEAD~5`). If none is named, use the merge base with the main branch: `git diff $(git merge-base origin/main HEAD)..HEAD`.
- Check the fixed point resolves and the diff is not empty before going further.
- List the commits (`git log <base>..HEAD --oneline`) and the files touched.

### 2. Find the spec

Look in this order:

1. Ticket or issue references in the branch name, commit messages and PR description; fetch them with the tracker's tool.
2. The PR description itself.
3. A plan or spec document in the repository that matches the branch or ticket.
4. Ask the user. If there is no spec, the Spec axis is skipped and the report says so.

### 3. Find the standards

Collect every file that says how code should be written: `CLAUDE.md` and `AGENTS.md` (repository and directory level), `CONTRIBUTING`, `CODING_STANDARDS`, style guides, `.editorconfig`, analyzer and linter configuration. Note which rules tooling already enforces; those are not review findings unless the tooling was bypassed.

Add the **smell baseline** (Fowler, *Refactoring*, chapter 3), applied as judgement calls:

| Smell | What it looks like in a diff | Direction |
| --- | --- | --- |
| Mysterious Name | A name that does not say what it is or does | Rename; if no honest name comes, the design is unclear |
| Duplicated Code | The same logic shape in two hunks or files | Extract the shared shape |
| Feature Envy | A method using another object's data more than its own | Move it to the data |
| Data Clumps | The same few values always passed together | Give them a type |
| Primitive Obsession | A string or number standing in for a domain concept | Give the concept a small type |
| Repeated Switches | The same `switch` on the same type in several places | One map, or polymorphism |
| Shotgun Surgery | One logical change scattered across many files | Gather what changes together |
| Divergent Change | One module edited for unrelated reasons | Split by reason to change |
| Speculative Generality | Parameters, hooks or abstractions the spec does not need | Inline until a real need appears |
| Message Chains | `a.b().c().d()` navigation | Hide the walk behind one method |
| Middle Man | A class that mostly forwards | Call the target directly |
| Refused Bequest | A subtype ignoring most of what it inherits | Composition instead |

### 4. Review each axis

**Standards reviewer** — given the diff, the commit list, the standards files and the smell baseline. For each finding: the file and line, the rule broken (file and quote) or the smell named, why it matters here, and a suggested direction. Mark each as *hard* (a documented rule) or *judgement* (a smell or style preference).

**Spec reviewer** — given the diff, the commit list and the spec. Report three kinds of finding, each quoting the spec line it rests on:

- **Missing or partial** — something the spec asks for that the diff does not do, or does only in part.
- **Unasked for** — behaviour in the diff the spec did not ask for (scope creep, or an undocumented decision).
- **Implemented wrongly** — something that looks done but behaves differently from what the spec says, including edge cases and failure paths the spec names.

Give each reviewer the material in its brief; a subagent sees nothing else. Run both at once where possible.

### 5. Verify

For every finding, check it before it goes in the report: read the code around the cited line, run the build, run the tests that cover it, or reproduce the behaviour. Drop what does not hold. Keep the evidence (command and result, or the lines read) with each finding that survives.

### 6. Report

Two sections, in that order, never interleaved and never re-ranked across axes:

```markdown
## Standards
| Severity | Kind | Where | Finding | Rule or smell | Evidence |
| -------- | ---- | ----- | ------- | ------------- | -------- |
| High | hard | src/Orders/Pricing.cs:42 | ... | CLAUDE.md: "..." | build output / lines read |

## Spec
| Kind | Where | Finding | Spec line | Evidence |
| ---- | ----- | ------- | --------- | -------- |
| Missing | — | Refunds over the limit are not rejected | "Refunds above £500 need approval" | no branch for it; test X absent |

**Summary:** Standards: 3 findings (worst: ...). Spec: 2 findings (worst: ...).
```

End with one line per axis: how many findings, and the worst within that axis. Do not pick a single worst finding across both. If the repository's own review protocol asks for findings in a particular place (in the conversation, a file, a tool), follow it.

---

## Anti-patterns

- **One merged list.** Style nits push a missing requirement off the first screen.
- **Reviewing the whole file.** Pre-existing problems outside the diff are noise for this change.
- **Unverified findings.** "This might throw" without reading the call site or running the test.
- **Smells as rules.** A baseline smell reported as a hard violation, or against a pattern the repository's standards endorse.
- **Re-litigating tooling.** Formatting and lint rules the build already enforces.
- **Spec review without a spec.** Guessing intent from the code; if there is no spec, say so and skip the axis.
- **Leaking one axis into the other.** "This is badly named and also wrong" — two findings, two sections.

---

## How This Skill Pairs with Others

- **pr-writer** — the author's side: a description that states the spec, the contracts crossed and the evidence makes both axes faster.
- **refactoring** — the source of the smell baseline and the moves that fix each smell.
- **clean-code**, **solid-principles** and **philosophy-of-software-design** — deeper design lenses when a Standards finding needs more than a smell name.
- **example-mapping** — turns a spec's rules into concrete examples the Spec reviewer can check one by one.
- **unit-testing-principles** — when the change's tests are part of the review.

---

## Quick Application Checklist

- [ ] Is the diff pinned to a fixed point and non-empty?
- [ ] Did I find the spec, or record that there is none?
- [ ] Did I collect every standards file and note what tooling already enforces?
- [ ] Did each axis run as its own pass, with only its own sources?
- [ ] Does every Standards finding cite a rule or name a smell, marked hard or judgement?
- [ ] Does every Spec finding quote the spec line it rests on?
- [ ] Is every reported finding verified, with its evidence?
- [ ] Are the two sections reported separately, with a worst finding per axis?

---

## Reading

- **Barry Boehm**, *Software Engineering Economics* (Prentice Hall, 1981) — verification ("building the product right") vs validation ("building the right product").
- **Google**, *Engineering Practices: How to do a code review* (google.github.io/eng-practices) — what to look for, and the standard for approving.
- **Martin Fowler**, *Refactoring* (2nd ed., 2018), chapter 3 "Bad Smells in Code".
- **Matt Pocock**, `code-review` skill (github.com/mattpocock/skills) — the Standards and Spec axes run as parallel reviewers and kept apart in the report.
