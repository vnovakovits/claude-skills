---
name: debugging
description: Find and fix bugs systematically with David Agans's "Debugging — The 9 Indispensable Rules" (2002) and Andreas Zeller's "Why Programs Fail" (2nd ed. 2009), led by a feedback-loop-first discipline — no theory until one fast, deterministic command goes red on this exact bug. Covers the defect → infection → failure chain, Zeller's TRAFFIC procedure and scientific method (falsifiable hypotheses, a debugging log), Agans's nine rules (make it fail, quit thinking and look, divide and conquer, change one thing at a time, check the plug, if you didn't fix it it ain't fixed), minimising repros, delta debugging and git bisect, intermittent and concurrency bugs, performance regressions, regression tests at the right seam, and cleanup. Use when something is broken, throwing, failing, flaky or slow; when asked to debug, diagnose, root-cause or troubleshoot; when a fix didn't hold; or when a test passes locally and fails in CI.
---

# Debugging (David Agans, Andreas Zeller)

Apply this skill whenever something is broken and the cause isn't obvious at first glance: a wrong result, an exception, a failing or flaky test, a slowdown, a bug that only happens in one environment. It combines two complementary books. Agans gives nine rules of conduct that keep a debugger honest; Zeller gives the theory and the systematic techniques (the infection chain, the scientific method, delta debugging). On top of both sits one rule that decides most debugging sessions: **build the feedback loop first**.

## Core Philosophy

**No loop, no theory.** If you have a fast, deterministic command that goes red on *this* bug, you will find the cause: bisection, hypotheses and instrumentation all just consume that signal. Without one, no amount of reading code will save you. Spend disproportionate effort on the loop. Most failed debugging sessions are sessions that started theorising before they could make the bug happen on demand.

**Quit thinking and look.** (Agans, rule 3.) Bugs live in the gap between what you think the code does and what it does. Reasoning about the code repeats the same assumptions that let the bug in. Observe the actual behaviour: values, timings, the order of events. Guess only to decide where to look next.

**A failure is the end of a chain.** (Zeller.) A **defect** in the code creates an **infection** (an erroneous program state) that propagates until it becomes a visible **failure**. You see the failure; you must fix the defect. Debugging is walking that chain backwards, from the symptom to the first place where state went wrong.

**Debugging is the scientific method.** Observe, form a hypothesis, derive a prediction, run an experiment, accept or reject. A hypothesis that makes no testable prediction is a hunch. Write it all down: the log is what stops you re-running the same experiment and forgetting what you ruled out.

**If you didn't fix it, it ain't fixed.** (Agans, rule 9.) Bugs never go away by themselves. "It stopped happening" means the conditions changed, not that the defect is gone. A fix is proven only when you can make the failure come back by removing the fix.

---

## Vocabulary (Zeller)

| Term | Meaning |
| --- | --- |
| **Defect** | The incorrect code: what you will change. ("Bug" is ambiguous; prefer the precise term.) |
| **Infection** | A program state that differs from the intended one. It may be overwritten and vanish, or propagate. |
| **Failure** | The externally visible symptom: the wrong output, the exception, the timeout. |
| **Cause** | A difference between a run where the failure occurs and one where it doesn't. The *actual cause* is a minimal such difference. |
| **Feedback loop** | One command that drives the failing code path and reports pass or fail. |
| **Red-capable** | A loop that asserts the *reported* symptom, so it goes red on this bug and green once it is fixed. |
| **Heisenbug** | A failure that changes or disappears when you observe it (debugger, logging, timing). |

---

## The Procedure

Zeller's **TRAFFIC** gives the order: **T**rack the problem, **R**eproduce the failure, **A**utomate and simplify, **F**ind possible infection origins, **F**ocus on the most likely origins, **I**solate the infection chain, **C**orrect the defect. The phases below follow it, with the feedback loop as the centre of gravity. Skip a phase only when you can say why.

### Phase 0: Track and understand

- Record the report: the exact symptom, the steps, the environment, the version, when it started. Keep the original wording: "intermittent 500 on checkout" and "checkout is slow" are different bugs.
- **Understand the system** (Agans, rule 1): read the docs for the library or API involved, know what "normal" looks like, and know your tools. Many bugs are a misread contract.
- **Check the plug** (Agans, rule 7): is it running the code you think (build output, deployed version, feature flag, config, cached artefact)? Is the input what you think? Is the test even executing? Question the obvious before the clever.

### Phase 1: Build the feedback loop

Ways to construct one, roughly in order of preference:

1. **A failing test** at the seam that reaches the bug: unit, integration or end-to-end.
2. **An HTTP call** (`curl`, a `.http` file) against a locally running service, asserting on the response.
3. **A CLI run** with a fixture input, diffed against known-good output.
4. **A browser script** (Playwright and friends) asserting on the DOM, console or network.
5. **Replay a captured artefact**: save the real request, message or event log, and push it through the code path in isolation.
6. **A throwaway harness**: the smallest slice of the system (one component, faked neighbours) that runs the failing path in one call.
7. **A fuzz or property loop** for "sometimes wrong": run a thousand generated inputs and catch the one that fails.
8. **A bisection script** when the bug appeared between two known states (commits, versions, datasets): one script that exits non-zero on failure, for `git bisect run`.
9. **A differential loop**: the same input through old and new versions, or two configurations, diffing the outputs.
10. **A human in the loop** as a last resort: a script that tells the person exactly what to do and captures what they see, so the loop stays structured.

**Tighten the loop.** Treat it as a product. Make it faster (narrow the test filter, skip unrelated start-up, cache set-up). Make the signal sharper (assert on the specific symptom, not "didn't crash"). Make it deterministic (pin the clock, seed randomness, isolate the filesystem and network). A thirty-second flaky loop is barely better than none; a two-second deterministic one finds the bug.

**Intermittent bugs.** The goal is a higher reproduction rate, not a clean repro. Loop the trigger a hundred times, run in parallel, add load, inject delays at suspected race windows. A bug that fails half the time is debuggable; one in a hundred is not yet. Agans: don't *simulate* the failure (hand-crafting the state you think causes it) — *stimulate* it (create the conditions and let the real failure happen).

```bash
for i in $(seq 100); do dotnet test --filter "FullyQualifiedName~Checkout_ConcurrentOrders" >/dev/null || echo FAIL; done | grep -c FAIL
```

```powershell
@(1..100 | ForEach-Object { dotnet test --filter "FullyQualifiedName~Checkout_ConcurrentOrders" *> $null; if ($LASTEXITCODE -ne 0) { 'FAIL' } }).Count
```

**Done when** you can name one command that you have already run, with its output, and it is:

- [ ] **Red-capable**: it drives the real failing path and asserts the user's exact symptom.
- [ ] **Deterministic**: the same verdict every run (or, for intermittent bugs, a stable and high failure rate).
- [ ] **Fast**: seconds, not minutes.
- [ ] **Unattended**: it runs without a human, except through an explicit human-in-the-loop script.

**If you cannot build a loop, stop and say so.** List what you tried. Ask for access to the environment that reproduces it, a captured artefact (logs, a payload, a trace, a recording with timestamps), or permission to add temporary instrumentation where it happens. Do not move on to hypotheses.

### Phase 2: Reproduce and minimise

Run the loop and watch it go red. Confirm it fails with the **reported** symptom, not a different failure nearby: the wrong bug gets the wrong fix.

Then **minimise**: cut inputs, steps, callers, configuration and data one piece at a time, re-running after each cut, and keep only what the failure needs. You are done when every remaining element is load-bearing — removing any one turns the loop green. This is Zeller's **delta debugging** done by hand: halve the difference between passing and failing input, keep the half that still fails, repeat. Automate it when the input is large (a long file, a big payload, a long event stream).

A minimal repro shrinks the hypothesis space and becomes the regression test in Phase 5.

### Phase 3: Hypothesise

Write down **three to five ranked hypotheses** before testing any of them. A single hypothesis anchors you on the first plausible idea.

Each must make a falsifiable prediction:

> If *X* is the cause, then changing *Y* will make the failure disappear, and changing *Z* will make it worse.

If you cannot state the prediction, discard or sharpen the hypothesis. Where to look for origins (Zeller's *Find* and *Focus*): known infections in the state at the failure point, recent changes, anomalies (what differs between passing and failing runs), and code that is already suspect (complex, recently churned, previously buggy).

Share the ranked list before testing when someone with context is available. They often re-rank it instantly ("we changed the retry policy yesterday") or have already ruled one out.

### Phase 4: Isolate the infection chain

Test hypotheses with the narrowest experiment that separates them.

**Divide and conquer** (Agans, rule 4). Narrow the search space by halves: in the code path (is the value already wrong here?), in history (`git bisect`), in input (delta debugging), in configuration. Start from the bad end and work backwards along the data flow: *where did this wrong value come from?*

**Change one thing at a time** (Agans, rule 5). Use a rifle, not a shotgun. If you change three things and it works, you don't know which one mattered, or whether two of them broke something else. **Compare with a good one**: a passing run, the last working version, a healthy environment. **Ask what changed** since it last worked.

**Instrument to observe, not to wander.** Each probe maps to a prediction from Phase 3.

1. A debugger or REPL if the environment supports one: one breakpoint beats ten log lines.
2. Targeted logs at the points that distinguish hypotheses.
3. Never "log everything and grep".

Tag every temporary log with a unique prefix (`[DEBUG-7f3a]`) so cleanup is a single search. Watch for Heisenberg: logging and breakpoints change timing, so a race may hide while you watch.

**Keep an audit trail** (Agans, rule 6). Write down what you did, in what order, and what happened, including the experiments that changed nothing. The detail you didn't think mattered is often the clue. "The shortest pencil is longer than the longest memory."

**Zeller's reasoning ladder** — pick the cheapest rung that can answer the question:

| Reasoning | Runs | Techniques |
| --- | --- | --- |
| **Deduction** | 0 | Reading the code, static analysis, slicing back from the failure ("what could have influenced this value?"). |
| **Observation** | 1 | Logging, debuggers, assertions, watching one run. |
| **Induction** | n | Comparing many runs: coverage of passing vs failing, logs side by side, statistical debugging. |
| **Experimentation** | n, controlled | Testing hypotheses, delta debugging on input or changes, bisection. |

**Get a fresh view** (Agans, rule 8) when the loop is tight but you are going in circles. Explain the problem to someone (or a rubber duck). Report **symptoms, not theories** — your theory is what has failed so far, and it will steer the helper down the same path.

### Phase 5: Correct the defect, with a regression test

Before changing code, check that you have found a **defect**, not another symptom. Ask whether the infection starts here or merely passes through. Patching the place where the failure shows (a null check, a retry, a catch) hides the chain instead of cutting it.

Write the regression test **before** the fix, but only at a **correct seam**: one where the test exercises the real failure pattern as it occurs. A test at a seam that is too shallow (a single caller when the bug needs two, a unit test that can't reproduce the sequence that triggered it) gives false confidence. **If no correct seam exists, that is a finding**: record it, because the design is stopping the bug from being locked down.

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail for the right reason.
3. Fix the defect.
4. Watch it pass.
5. Re-run the original, un-minimised loop from Phase 1.

Then ask Zeller's follow-up questions: did the fix introduce new failures (run the wider suite)? Was the same mistake made elsewhere (search for the pattern)?

### Phase 6: Verify and clean up

- [ ] **It's really fixed**: the original loop is green.
- [ ] **It's your fix that fixed it** (Agans, rule 9): remove the fix, see the failure return, restore the fix. Otherwise you may have been lucky.
- [ ] The regression test passes, or the missing seam is documented.
- [ ] Every `[DEBUG-…]` probe is gone (search for the prefix).
- [ ] Throwaway harnesses and scripts are deleted, or kept deliberately in a clearly named place.
- [ ] The root cause — the hypothesis that turned out true — is written in the commit or PR, so the next person learns from it.
- [ ] **Fix the process** (Agans, rule 9): if this class of bug could recur, what check, test, type or alert would have caught it earlier?

---

## Agans's Nine Rules at a Glance

| # | Rule | In practice |
| --- | --- | --- |
| 1 | **Understand the system** | Read the manual and the contract. Know what normal looks like. Know your tools. |
| 2 | **Make it fail** | Reproduce on demand from a known start. Stimulate the failure; don't simulate it. Raise the rate of intermittent failures. |
| 3 | **Quit thinking and look** | Observe the actual failure and its details. Build instrumentation in; add more when needed. Guess only to focus the search. |
| 4 | **Divide and conquer** | Halve the search space. Find which side of the bug you're on. Fix the known bugs and the noise first; they mask the real one. |
| 5 | **Change one thing at a time** | One variable per experiment. Compare with a good run. Find what changed since it last worked. |
| 6 | **Keep an audit trail** | Write down actions, order and results. Any detail may matter. Correlate timestamps across logs. |
| 7 | **Check the plug** | Question assumptions. Start from the beginning, not "square three". Test the tool before trusting it. |
| 8 | **Get a fresh view** | Ask for help early. Report symptoms, not theories. You don't have to be sure to ask. |
| 9 | **If you didn't fix it, it ain't fixed** | Prove the fix by removing it. Fix the cause, not the symptom. Fix the process that let it in. |

---

## Situations

**Regression between two known states.** Use bisection before reading code. Write a script that exits 0 on good and non-zero on bad (125 to skip an unbuildable commit), then let git do the search:

```bash
git bisect start <bad-commit> <good-commit>
git bisect run ./repro.sh
git bisect reset
```

Zeller's *isolating failure-inducing changes* generalises this to configurations, dependency versions and input files: find the minimal difference between the passing and failing world.

**Works on my machine.** The cause is a difference between environments. List them explicitly — runtime and dependency versions, configuration and secrets, data, time zone and locale, OS and file-system case sensitivity, CPU count and timing, network and DNS — and close them one at a time.

**Passes alone, fails in the suite (or in CI).** Suspect shared state: test order, static or singleton state, leftover data, shared containers or ports, parallel execution, the clock. Run the failing test with its neighbours, then bisect the set of tests that runs before it. Meszaros's *Erratic Test* causes (interacting tests, resource leakage, nondeterminism) are the checklist.

**Concurrency and races.** Raise the reproduction rate (stress, parallelism, injected delays at the suspected window). Log with thread or task ids and high-resolution timestamps. Prefer a design fix (immutability, a single writer, idempotency, an explicit lock or ordering) over a sleep. A sleep that makes a test pass is a hypothesis confirmed, not a fix.

**Performance regressions.** Logs rarely help. Measure first: establish a baseline with a timing harness, a profiler, or a query plan, on the same machine and data. Then bisect the regression the same way as a functional bug, with "slower than threshold" as the red signal. Change one thing, measure again.

**Only in production.** Build the loop from what production already records: traces, structured logs, the captured payload or message. Replay it locally. If the data isn't there, the first fix is instrumentation, added deliberately and removed or kept on purpose.

**Flaky test.** It's a bug, either in the test or in the code. Never retry until green, mark it skipped without a ticket, or raise the timeout as a fix. Diagnose it like any other intermittent failure.

---

## When Claude Is Debugging

- **Redact secrets** in everything shown: commands, output, captured payloads. Build loops against environment variables so credentials never appear in the transcript, and quote only the lines that carry the signal.
- **Show the loop**: the exact command and its (redacted) output, before any hypothesis.
- **Don't edit until you can observe.** Speculative edits to "see if it helps" are shotgun debugging; each one is an experiment that needs a prediction.
- **Separate this change from what was already broken.** Before blaming a branch, run the loop on the base commit. Label each failure as a regression introduced by the change or a pre-existing or environmental problem.
- **Don't trust a single green run** of a flaky or reported-failing check. Re-run it, and check for leftover processes, containers or files from earlier runs.
- **Say when you're stuck** and what you need, rather than lowering the bar for "fixed".

---

## Anti-patterns

- **Theorising before reproducing.** Reading code and building a story without a loop. The story is usually wrong and always unverified.
- **Shotgun debugging.** Changing several things at once, or changing things at random until the symptom moves.
- **Fixing the symptom.** A null check, a try/catch, a retry or a default value at the point of failure, while the infection keeps starting upstream.
- **"It went away."** Declaring victory when the failure stops without knowing why.
- **Debugging the wrong bug.** Reproducing *a* failure in the same area instead of *the* reported one.
- **Log everything and grep.** Instrumentation with no hypothesis behind it, which buries the signal and is never cleaned up.
- **Trusting the tool.** The debugger, the profiler, the test runner, or a stale build artefact can be wrong too. Check the plug.
- **Single hypothesis.** Testing only the first idea, then bending the evidence to fit it.
- **No audit trail.** Re-running experiments already done, and losing the result that ruled something out.
- **Sleep as a fix.** Masking a race with a delay; it returns under load.

---

## Output Template: Diagnosis Report

Use when reporting a diagnosis to someone else, or as the root-cause section of a PR.

```markdown
## Diagnosis: <one-line symptom>

**Symptom:** <exact error / wrong output / timing, as reported>
**Feedback loop:** `<command>` → <red output, redacted>
**Minimal repro:** <the smallest input or steps that still fail>

### Hypotheses
| # | Hypothesis | Prediction | Result |
| - | ---------- | ---------- | ------ |
| 1 | ... | If so, <change> makes it pass | Confirmed / Rejected: <evidence> |

### Root cause
<the defect, where the infection starts, and how it reaches the failure>

### Fix
<what changed and why it cuts the chain, not just the symptom>

### Verification
- Regression test: `<test name>` (red before, green after) — or: no correct seam, because <reason>
- Fix removed → failure returns: yes / no
- Same pattern elsewhere: <searched where, found what>

### Prevention
<the check, test, type, or alert that would have caught this class of bug>
```

---

## How This Skill Pairs with Others

- **test-driven-development** — the regression test is a red-green cycle: the minimal repro is the red test, the fix is the green.
- **working-effectively-with-legacy-code** (Feathers) — when there is no seam to put the regression test at, use characterization tests and dependency-breaking moves to create one.
- **unit-testing-principles** (Khorikov) and **xunit-test-patterns** (Meszaros) — choosing where the regression test belongs, and Meszaros's *Erratic Test* and *Fragile Test* causes for flaky suites.
- **observability** — Agans's "build instrumentation in": structured events and traces turn production-only bugs into replayable loops.
- **systems-thinking-iceberg** and **toyota-way** — when the same kind of bug keeps coming back, fix the structure that produces it (the "fix the process" step), and stop the line rather than work around it.
- **pr-writer** — the root cause and the verification evidence go in the PR description.

---

## Quick Application Checklist

Before theorising:
- [ ] Do I have the exact reported symptom, environment and version?
- [ ] Have I checked the plug (right build, right config, right input, test actually running)?
- [ ] Do I have one fast, deterministic command that goes red on *this* failure, and have I run it?

While narrowing:
- [ ] Is the repro minimal — is every remaining element load-bearing?
- [ ] Do I have three to five ranked hypotheses, each with a prediction?
- [ ] Am I changing one thing at a time and comparing with a good run?
- [ ] Is every temporary probe tagged, and am I writing down what I tried?

Before calling it fixed:
- [ ] Did I fix the defect where the infection starts, not where the failure shows?
- [ ] Is there a regression test at a correct seam (or a documented reason there isn't)?
- [ ] Does removing the fix bring the failure back?
- [ ] Are the probes and throwaway code gone, and the root cause written down?
- [ ] What would stop this class of bug from recurring?

---

## Reading

- **David J. Agans**, *Debugging: The 9 Indispensable Rules for Finding Even the Most Elusive Software and Hardware Problems* (AMACOM, 2002) — the nine rules, with war stories from hardware and software. Companion site: debuggingrules.com.
- **Andreas Zeller**, *Why Programs Fail: A Guide to Systematic Debugging* (Morgan Kaufmann, 2nd ed. 2009) — the infection chain, TRAFFIC, scientific debugging, the reasoning ladder, delta debugging and cause-effect chains.
- **Andreas Zeller et al.**, *The Debugging Book* (debuggingbook.org) — the same techniques as executable Python chapters: delta debugging, statistical debugging, slicing.
- **Andreas Zeller & Ralf Hildebrandt**, "Simplifying and Isolating Failure-Inducing Input" (IEEE TSE, 2002) — the delta debugging algorithm.
- **Andreas Zeller**, "Yesterday, my program worked. Today, it does not. Why?" (ESEC/FSE, 1999) — isolating failure-inducing changes, the idea behind automated bisection.
- **Matt Pocock**, `diagnosing-bugs` skill (github.com/mattpocock/skills) — the feedback-loop-first discipline, the loop completion criteria and the correct-seam rule for regression tests.
- **Brian Kernighan & Rob Pike**, *The Practice of Programming* (1999), chapter 5 "Debugging" — short, practical, and still accurate.
- **Andrew Hunt & David Thomas**, *The Pragmatic Programmer* (20th anniversary ed., 2019) — "Debugging" and rubber-duck explanation.
- **Julia Evans**, *The Pocket Guide to Debugging* (Wizard Zines, 2022) — a compact, modern catalogue of debugging strategies.
