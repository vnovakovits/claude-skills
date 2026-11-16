---
name: peer-review
description: Review a change the way a respected colleague would — design and craft lenses applied to the diff, every finding verified in the code, and the result written as kind, specific comments anchored to lines. Loads clean-code, fractal-architecture, responsibility-driven-design and domain-driven-design for the production code; unit-testing-principles (Khorikov's four pillars, managed vs unmanaged dependencies), art-of-unit-testing, xunit-test-patterns and test-data-patterns for the tests, including a map of every promised scenario to the test that pins it and a check that no guard can be removed with every test still green; and elements-of-style for the comments. Applies the repository's own CLAUDE.md / AGENTS.md as a further lens. Comments carry an honest severity (blocking, worth changing, question, nit, praise) and follow observation → consequence → suggestion. Local only — prints the review and never posts it. Use when asked to review a PR, a branch or uncommitted work as a peer, to "review this like a colleague", or when the user wants line comments they can paste into a review.
---

# Peer Review

Review the change the user names — a pull request number, a branch, or nothing for the current branch against its base — and write the review they would want to receive from a colleague they respect.

**Local only.** Print the review. Never post, edit, approve or request changes on the hosting service unless the user asks for that in so many words; they paste what they agree with.

## 1. Get the change

- A number → `gh pr view <n>` for title and description, `gh pr diff <n>` for the diff.
- A branch or nothing → `git merge-base` with `master` (or `main`), then `git diff <base>...HEAD`.
- Read the surrounding code, not just the hunks. A finding that depends on context must be checked in the file.
- Skip `CLAUDE.md`, `AGENTS.md`, lockfiles and generated files.

## 2. Load the lenses

Load these skills before reading the diff:

- `clean-code` — names, function size, one level of abstraction, comments only for a why.
- `fractal-architecture` — does each unit fit in a head: ≤ ~7 chunks, cyclomatic complexity ≤ 7, no partial functions, invariants enforced.
- `responsibility-driven-design` — who knows, who does, who decides; Tell, Don't Ask; information expert; no god objects or middle men.
- `domain-driven-design` — ubiquitous language in names, value objects over primitives, aggregate boundaries, domain events as facts, layering.
- The unit-testing lenses, all four, for every test file in the diff:
  - `unit-testing-principles` (Khorikov) — score the suite on the four pillars (protection against regressions, resistance to refactoring, fast feedback, maintainability) and name the trade-off it makes; which style each test is (output, state, communication), preferring the strongest that fits; observable behaviour, not internals; mocks only for unmanaged dependencies (external services, a shared bus), real or faked managed ones (the service's own store); no verification on stubs; is the code under test worth a test (domain significance × complexity).
  - `art-of-unit-testing` (Osherove) — `UnitOfWork_StateUnderTest_ExpectedBehavior` names, one Act, one concept, at most one mock per test, no logic in tests, a test that has never failed proves nothing.
  - `xunit-test-patterns` (Meszaros) — four phases visible, the right double for the role, fresh and minimal fixtures, and the smells: Mystery Guest, Eager Test, General Fixture, Irrelevant Information, Hard-Coded Test Data, Assertion Roulette, Fragile Test, Test Code Duplication, overlap between tests.
  - `test-data-patterns` — builders, object mothers, creation methods and arrangements; setup that states only what the scenario varies.
- `elements-of-style` — for the comments themselves.

Also read the repository's `CLAUDE.md` / `AGENTS.md` and apply its conventions as a lens of their own.

## 3. Review

Go through the diff once per lens, then merge. Keep a finding only if all of these hold:

- It's **in the change** (or the change made it worse). Pre-existing code is out of scope unless the change touches it.
- It's **verified** in the code, not inferred from the diff alone.
- A senior engineer **would say it out loud** in a review. Linters, formatters and tooling catch the rest.
- You can state the **consequence**: what gets harder, slower, riskier or wrong.

Also note, deliberately, one to three things the author did well. Only if true; empty praise is noise.

### 3a. The tests get their own pass

Review the test files as production code, with the four unit-testing lenses above, and ask of the change as a whole:

- **Does a test exist for the risk the change introduces?** Name the missing scenario as a test name. A change that moves a rule, a gate or an order of evaluation needs a test on the path that reaches it, not only on the function that implements it.
- **Is every promised scenario pinned?** List the behaviours the description, ticket or example map promises — including the "nothing happens when…" cases and the edge cases — and map each to the test that pins it: ✅ pinned, ⚠️ only indirectly, ❌ missing. A promise with no test is a finding.
- **Can a guard be broken with nothing going red?** For each condition in the change — each `&&` operand, each early return, each skip reason — ask which test fails if it is removed. When none does, name the test that would. Where it is cheap, break the guard, run the tests to prove it, and restore the code.
- **Is the persisted or published outcome asserted, not only the call that produced it?** An event written to a stream, a row stored, a message sent: if the description relies on it for observability, a test should check it.
- **Does each test fail for the right reason?** A fixture built by hand that the real path no longer produces, a stub verified as if it were a mock, a test pinning an optimisation rather than an outcome: each passes while the behaviour is wrong.
- **Does each test earn its place?** Two tests that exercise the same inputs and assert the same outcome are one test; a test on a trivial mapping is noise.
- **Can the next reader tell what it specifies?** From the name alone, and from the setup, which should show only what this scenario varies.

Report test findings with the same severities and in the same per-file comment shape as everything else, in diff order. A missing test anchors on the production line it would protect.

## 4. Write the comments

**One comment per line (or short range), in diff order, grouped by file.** Shape:

```
**path/File.cs:42** · <severity>
> `the line, or its first ~80 chars`

<the comment>
```

Severity, honestly chosen: **blocking** (wrong, unsafe, or breaks a convention the team agreed), **worth changing** (the code works; this makes it clearer or safer), **question** (the reviewer may be missing context), **nit** (take it or leave it, at most three per review), **praise**.

**Voice: one human to another.** Elements of Style, applied to kindness:

- Address the code, never the author. "This method does two things" — not "you did two things here".
- Lead with the observation, then the consequence, then a concrete suggestion. One topic per comment.
- Own opinions with "I" ("I'd find this easier to follow as…"); use "we" for shared conventions ("we keep comments for the why").
- Ask when unsure, and mean it: a question is a question, not a softened order.
- Active voice, specific words, no needless ones. No "just", "simply", "obviously", "should have".
- No sarcasm, no rhetorical questions, no exclamation marks, no emoji.
- Assume the author had a reason; name the trade-off before suggesting the other side of it.
- A suggestion fits in a sentence or a tiny code block. Anything bigger is a conversation, so say that.

Before each comment, read it as the author would on a bad day. If it stings and the sting isn't the point, rewrite it.

## 5. Output

1. **Summary, three lines at most:** the verdict (looks good / a few things worth changing / needs another pass), then the one to three findings that matter most.
2. **The flow**, if the change alters runtime behaviour: load the `pr-flow` skill and print its flow diff here, for the user only.
3. **The tests**, if the change has any: the four-pillar scores in a few lines, then the scenario-to-test map from 3a.
4. **The comments**, grouped by file in diff order.
5. **What I liked**, if anything was.
6. If nothing survived step 3: say so plainly, name the lenses applied, and stop.

## Related skills

- **two-axis-code-review** — checks a change against the repository's written standards and against its ticket, as two separate reports. Use it to answer "is this built right, and is it the right thing?"; use peer-review for craft and design feedback written as line comments to a colleague.
- **pr-writer** — the other side of the table: presenting your own change for review.
