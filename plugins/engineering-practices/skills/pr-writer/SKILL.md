---
name: pr-writer
description: Write, scope, size, and review pull requests that are fast and safe to review and merge. Grounded in Google's Engineering Practices (small CLs, CL descriptions, the reviewer standard & speed), GitHub's PR guidance, the SmartBear/Cisco code-review study (defect detection vs PR size), Conventional Commits, and modern delivery practice (expand/contract migrations, feature flags, observability gates, breaking-change discipline). Covers PR scope & splitting, the size band, Conventional-Commit titles, a stand-alone description template (what/why · changes · contracts crossed · testing · observability · risk & rollback · review focus · deferred), the author self-review checklist, CI/safety gates, anti-patterns, and how to handle review comments. Use when opening or describing a PR, deciding whether a change is one PR or several, sizing or splitting a large diff, writing a PR description or template, or before requesting review.
---

# Writing Pull Requests

A pull request is a **request for someone else's time** and a **permanent entry in the project's history**. Optimize for the reviewer and for the engineer who reads `git log` in two years — not for the writer. The central test: **can a reviewer learn what changed, why, and where the risk is, without opening the diff or the ticket — and review it in one sitting?**

## Core Philosophy

- **The reviewer is the customer.** Their time and attention are the scarce resource. Every choice — size, title, description, read-order — should reduce their cognitive load.
- **Small, focused, single-concern.** The strongest predictor of a fast, effective review is a small, single-purpose diff. Almost every other problem (slow reviews, missed defects, scope arguments) traces back to a PR that did too much.
- **The description is the contract and the story.** It states intent and the edges crossed; the diff shows the mechanism. A reviewer should be able to validate the diff *against* the description.
- **Self-review first.** Read your own diff hunk-by-hunk as if it were someone else's before you request review. Most "review comments" are things you'd have caught yourself.
- **Ship when it improves code health.** Perfect is the enemy of merged. Approve (and request merge of) a change that definitely improves the codebase, even if it isn't ideal — file follow-ups for the rest.

---

## 1. One Concern Per PR (the splitting rule)

**If you can't describe the PR without the word "and", it is two PRs.** A feature *and* a refactor, a fix *and* a config change, two unrelated bug fixes — split them.

- **Land refactors separately, first.** A cross-cutting rename, an interface reshape, or a client split should be its own PR that merges *before* the feature that needs it. This shrinks the feature diff to only the lines that are actually about the feature, and lets a risky refactor be reviewed (and reverted) on its own.
- **Stack, don't bundle.** When changes genuinely depend on each other, stack them as a chain of small PRs (or sequential commits with clean seams) rather than one mega-PR. A commit-per-step discipline (e.g. test → impl → refactor) already gives you the seams to extract.
- **Why it matters:** a single-concern PR can be reviewed quickly, reverted cleanly during an incident, and understood in isolation later. A braided PR gets rubber-stamped, not reviewed.

---

## 2. Size — keep it to one sitting

The empirical backbone (SmartBear/Cisco study of ~2,500 reviews over 3.2M LOC): **defect detection peaks at 200–400 changed LOC reviewed in a 60–90 minute session and drops sharply beyond ~400 LOC / ~90 minutes.** Google calls ~100 lines a "reasonable" CL and 1,000 lines "usually too large." Merge-velocity data points even smaller (~50 lines ideal; elite teams average a few hundred per PR).

**Practical tiers (production lines):**

| Size | Verdict |
|---|---|
| < 100 LOC | ideal |
| 100–300 | good |
| 300–500 | acceptable **with** a strong description + a "where to look" roadmap |
| > 500 LOC or > ~10 files | split it |

- **File-spread counts as much as raw lines.** 200 lines across 50 files is too large; 200 in one file is fine. Aim for ≤ ~10 files.
- **Judge production code separately from tests.** A PR that's +1,600/-90 but is 1,000 lines of tests still has ~500 production lines that need full-attention review — count those.
- **Hit the budget by scoping, not by counting after the fact.** Pick one concern; stack refactors out. The line count is a *symptom* of scope, not a target to game.
- *Caveat on the numbers:* the per-bucket detection-rate tables circulating in blogs are extrapolations, and vendor telemetry (e.g. "50 lines / 40% faster") is directionally sound, not gospel. The 200–400 band and "small is better" are the robust findings.

---

## 3. The title — a Conventional-Commit line that names the problem

- One imperative line, **Conventional-Commit** form: `type(scope): summary` (e.g. `feat(draft-shipments): copy a draft onto its matching itinerary`). It must stand alone in `git log`.
- **Name the problem, not the fix** — and never the mechanism (`Moving code from A to B`, `Phase 1`, `Fix stuff` all fail).
- **Mark breaking changes with `!`** before the colon (`feat(api)!: …`).
- Don't paste the 40-commit log as the title or body.

---

## 4. The description — make it stand alone

A reviewer (and a future archaeologist) should learn **what changed, why now, and the design decision worth a second look** without opening the diff or the ticket. Write **prose**, not a commit dump.

Structure around **What/Why · Changes · Testing · Risk & rollback**, plus the edges below. Explain the **root cause** (for a fix) and the **decision + the alternative not taken** (for a feature) — not the obvious.

### Enumerate every contract edge the change crosses

A reviewer reads a PR as *edges crossed*, not lines added. List, explicitly (or "none"):

- **Inbound API** — new/changed routes (prefer additive + versioned). Declare the full response contract (every status code).
- **Outbound calls** — new calls to other services; confirm the client has **auth + resilience** wired, and that **transport failures map to typed outcomes** (e.g. 404 / 422 / 502), never a raw exception to a bare 500.
- **Idempotency / retry** — for any **mutating** outbound call under an auto-retrying resilience policy: either confirm the upstream dedupes (with a test pinning "dropped-response-then-success → one side effect") or disable retries for that call. A retried POST can double-apply.
- **Config** — every new/`required` key, with its **per-environment** value, and confirmation that **out-of-repo** sources (Helm/values, secret store, pipeline-injected settings) are updated too. A `required` key missing in one environment is a guaranteed crash-on-boot there. State deploy ordering.
- **Events / schemas** — never mutate or remove a field on an existing event (it's immutable history); add a new versioned event. 
- **Database migrations** — see §5.

### Breaking changes — impossible to miss

A bold **`BREAKING CHANGE:`** block at the top: what breaks, who is affected, and the required consumer action. A breaking config-key rename, a removed/renamed field, a changed response shape, a changed status code — all qualify.

---

## 5. Safety & CI gates the PR must clear

- **The full CI suite is the merge gate**, not the fast local loop. Cross-service contracts only break in the integration/container suites; a green unit run is necessary, not sufficient. Link the green run. Build is warning-clean.
- **No secrets** in the diff (URLs are fine; credentials/connection strings go to the secret store).
- **Migrations follow expand/contract** (zero-downtime): additive nullable/defaulted columns + new tables in an **expand** step; never rename/drop an in-use column in the same deploy that reads the new shape; **contract** (drop old structures) in a later deploy. Each migration has a tested reverse (`Down`), a lock/duration estimate for large tables, and must **not** ship in the same PR as the code that depends on the new shape.
- **Feature-flag** risky or incomplete behaviour so it can be shipped dark and toggled without a redeploy.
- **Observability before merge** — the new unit of work emits one canonical wide event (inputs + decision + outcome + downstream durations) and a span tagged with the slice keys (ids, outcome) you'd group by in an incident; high-cardinality ids go on the span/event, never on metric labels. The description answers: *"how will we know this broke in prod, and why, without shipping new code?"*

---

## 6. Author self-review checklist (before requesting review)

- [ ] I walked the diff **hunk-by-hunk** — no debug artifacts, no commented-out code, no `TODO`s I meant to remove.
- [ ] **One concern**; refactors split out or stacked.
- [ ] No **stray working-tree files** rode along (local-only tooling manifests like a pinned-SDK file, scratch/WIP docs, editor configs).
- [ ] No **secrets** in the diff.
- [ ] Every new/`required` **config key** is present in **all** environments + the out-of-repo sources.
- [ ] Every new **outbound client** has auth + resilience; retry-safety stated for mutating calls.
- [ ] Every new **outcome/branch has a test that fails if it regresses** — happy path **and** each failure arm; tests assert ordering (no downstream side effect on the error/no-match paths), not just return values.
- [ ] Any **intentionally lossy / best-effort** behaviour is flagged as an owned policy with a one-line rationale (mirrored in a test comment) — so it can't be mistaken for a bug.
- [ ] The change is **observable**; the description says how we'll know it broke.
- [ ] **Full CI suite is green**; build warning-clean.
- [ ] Title + description **stand alone**; ticket linked; "where to look" pointer for any non-trivial diff.

---

## 7. The PR description template

```markdown
## What & Why
<!-- One imperative sentence: what changes for the caller/user and why now. Matches the PR title. -->

Closes: <!-- TICKET-NNN / #NNN -->

## Changes
<!-- Prose summary of the net change — NOT a commit-log dump.
     Call out the design decision worth flagging and the alternative not taken. -->

**Contracts crossed** (or "none"):
- Inbound route(s): <!-- e.g. POST v1/resource/{id}/action (additive, versioned) -->
- Outbound call(s): <!-- service + endpoint; auth + resilience wired? retry-safe if mutating? -->
- Config keys added/renamed: <!-- key → per-env value; out-of-repo sources updated? -->
- Events / schema / migrations: <!-- new versioned event? expand/contract migration? or "none" -->

## Testing
- [ ] Full CI suite green (incl. integration/container tests) — link: <!-- run -->
- [ ] New tests cover every new outcome/branch (happy path AND each failure arm)
- [ ] Contract test pins the real upstream wire shape (if a new boundary)
- [ ] Manual / staging validation: <!-- what, where, which edge cases -->

Edge cases & intentional best-effort behaviour:
<!-- empty/null, duplicates, ordering, ties, partial records, stale upstream data;
     name any deliberately lossy choice + one-line rationale -->

## Observability
<!-- Wide event name + key fields; span tags / outcome bucket a responder would group by.
     How will we know this broke in prod without shipping new code? -->

## Risk & rollback
- Deploy profile: <!-- e.g. "stateless — no migration/event-schema change" -->
- Rollback: <!-- "revert this PR / redeploy prior image"; note if a config rename must be reverted per-env too -->
- Breaking change? <!-- if yes: bold BREAKING CHANGE + consumer action; else "none" -->

## Screenshots
<!-- Before | After for any UI/CLI/visible-output change; delete if N/A -->

## Review focus
<!-- "Start here: <file>." Name the 3–4 load-bearing files + a suggested read order. -->

## Deferred / fast-follow
<!-- What was deliberately left out, why it's safe to ship without it, linked ticket. -->
```

Keep it lean — delete sections that are genuinely N/A rather than filling them with noise. A repo-level `.github/pull_request_template.md` makes this the default for every PR.

---

## 8. Anti-patterns (what makes a PR painful)

- **The "and" PR** — a feature + a cross-cutting refactor + config changes braided together. Unreviewable, un-revertable in an incident.
- **The 40-file / 1,000-line review request** — past the defect-detection cliff; gets rubber-stamped. The single biggest controllable driver of missed defects and review latency.
- **Vague or commit-dump title/description** — `Fix copy`, `Phase 1`, the 40 commit subjects concatenated. No standalone context.
- **A breaking `required` config rename buried as a silent line** with no env enumeration → clean review, boot-loop in the environment whose value was missed.
- **A non-idempotent POST left under auto-retry** with no word on double-apply safety → silent duplicate side effects, invisible in happy-path tests.
- **An upstream failure escaping as a bare 500** instead of a typed outcome → callers can't tell "retry me" (502) from "your input is wrong" (422).
- **A new branch/outcome with no test** — especially an untested failure arm.
- **Undocumented best-effort behaviour** — a silently dropped selection, a silent tie-break — indistinguishable from a bug to the reviewer and to on-call six months later.
- **A new endpoint/consumer with no wide event/span**, or high-cardinality ids shoved onto **metric labels**.
- **Mutating an existing event's schema**, or a migration that drops an in-use column / lacks a reverse / ships with the code that depends on it.
- **Drive-by working-tree files** — a local-only SDK pin, scratch docs — that break CI or every teammate's build.
- **"It passed locally" as the merge gate** for behaviour behind a mocked external boundary. Any red/skipped test, or a build with suppressed warnings.
- **A stale narrative** — a PR story (or committed WIP doc) describing behaviour the HEAD no longer has.
- **Comments added to production code** to explain non-obvious logic instead of making the code self-documenting and putting the *why* in the PR description or a test.
- **Reviewer perfectionism** — blocking a net-improvement over imagined-future concerns, or letting a PR stall on unanswered nits instead of approving-with-nits or escalating.

---

## 9. Handling review comments

- **Frame your own review comments as questions** ("what happens if this is empty?") and label nits as nits.
- **Respond to every comment** — acknowledge even when you disagree. Silence stalls the PR.
- **Fix the misunderstanding in the code, not just the thread** — if a reviewer misread it, a rename or an added test usually beats a reply.
- **Escalate a stalled text debate to a synchronous chat**, then post the decision back to the thread so it's on the record.
- **After pushing fixes, use "re-request review"** rather than a bare comment, so reviewers/code-owners are notified. Keep the PR in **Draft** while CI is red or the approach is moving; flip to **Ready** only when it genuinely is.
- **Reviewers: approve when the change improves code health** — don't hold a net-improvement hostage to perfection.

---

## Reading

- **Google Engineering Practices** — *Small CLs*, *Writing good CL descriptions*, *The Standard of Code Review*, *What to look for in a code review*, *Speed of Code Reviews*, *How to handle reviewer comments* (google.github.io/eng-practices).
- **GitHub** — "How to write the perfect pull request" (Keavy McMinn); "How to review code effectively" (Sarah Vessels); GitHub flow; PR templates; draft PRs (github.blog / docs.github.com).
- **SmartBear / Cisco** — *Best Practices for Peer Code Review* and the Cisco case study (defect detection vs review size/speed).
- **Conventional Commits 1.0.0** — conventionalcommits.org.
- **Empirical** — Bacchelli & Bird, *Modern Code Review* (MSR); Zhang et al., *Pull Request Latency* (ESE 2022); "Do small code changes merge faster?" (arXiv 2203.05045); LinearB engineering benchmarks.
- **Delivery & safety** — expand/contract migrations (Prisma DataGuide); rollback strategies (Octopus); feature-flag practices (Octopus); pipeline quality gates (InfoQ); breaking-change discipline (InfoQ, semver); observability-driven development (Charity Majors).
