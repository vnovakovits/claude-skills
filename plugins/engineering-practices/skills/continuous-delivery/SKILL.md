---
name: continuous-delivery
description: Apply Jez Humble and David Farley's Continuous Delivery — the discipline of making software always release-ready through deployment pipelines, trunk-based development, automated everything, feature flags, branch-by-abstraction, and the four DORA metrics (deployment frequency, lead time, change failure rate, mean time to restore). Use when designing a deployment pipeline, choosing a branching strategy, debating long-lived feature branches vs. trunk-based, deciding how to deploy in-flight changes safely, or evaluating delivery health.
---

# Continuous Delivery (Humble & Farley)

Apply this skill when designing or improving how software gets from commit to production — pipelines, branching, deployment strategies, feature flags, release planning, and the metrics that distinguish high-performing from low-performing engineering organizations.

## Core Philosophy

**Done means released.** Not "feature-complete on a branch", not "merged to main", not "deployed to staging". Done means in production, available to users (or hideable behind a flag).

**Software is always release-ready.** Every commit, every branch, every build — the trunk is always in a deployable state. Releasing becomes a business decision, not a technical event.

**If it hurts, do it more often.** Painful integrations? Integrate continuously. Painful deployments? Deploy continuously. The pain reveals problems; doing it more often forces you to automate and improve the painful parts.

**Build quality in.** Quality is not inspected at the end. It is a property of the process: tests at every stage, automated checks, fast feedback, and a build that breaks loudly when something is wrong.

**Optimize for low MTTR over high MTBF.** Mean Time To Recovery matters more than Mean Time Between Failures. A team that recovers in minutes can move fast; a team that goes weeks without an incident but takes days to recover when one happens cannot.

---

## The Deployment Pipeline

The central pattern of CD. Every commit flows through a series of automated stages; each stage validates a different concern. Progress to the next stage is automatic if the current one passes.

```
Commit ─►  Build & Unit Tests  ─►  Integration Tests  ─►  Acceptance Tests
                                                                  │
                                                                  ▼
            Production  ◄─  Smoke Tests  ◄─  Capacity / Perf Tests
                  ▲                       (optional: manual approval)
                  └─ (final stage: deploy)
```

### Stage characteristics

**Stage 1 — Commit stage (fast feedback)**
- Compile.
- Unit tests.
- Static analysis.
- Lint.
- Package artifact.
- **Target: under 5 minutes.** If it's slow, developers stop running it locally.

**Stage 2 — Acceptance / integration tests**
- Spin up the artifact with real dependencies (or close substitutes).
- Run scenario-level / acceptance tests (BDD scenarios, end-to-end happy paths).
- **Target: under 30 minutes.** Slower than commit, but still on every commit.

**Stage 3 — Non-functional tests**
- Performance, capacity, security scanning.
- May be slower; sometimes run on schedule rather than every commit.

**Stage 4 — Manual approval (optional)**
- For environments where automatic deploy to prod is not yet trusted.
- The pipeline waits; a human approves; the deploy proceeds.

**Stage 5 — Deployment**
- Same automation as previous stages; just the production target.
- Blue/green, canary, rolling — depending on architecture.

### Key rules

- **One artifact through the pipeline.** Build once; promote the same binary through stages. Never rebuild for prod.
- **Same scripts in every environment.** The script that deploys to dev is the same script that deploys to prod. Environment differences live in config, not code.
- **Fail fast.** Order stages cheap-to-expensive. A unit-test failure should not wait for an integration suite.
- **Visibility.** Pipeline status visible to the whole team — wall display, dashboards, alerts.
- **Stop the line.** A red pipeline is the team's top priority. No new commits until green.

---

## Trunk-Based Development

The branching strategy CD almost always assumes.

**Definition:** all developers commit (or merge short-lived branches) to one main branch — *trunk* — at least once a day, ideally many times.

**Why:**
- Integrates continuously; integration debt never accumulates.
- Branches don't diverge; merge conflicts don't surprise.
- Every commit is built and tested by the pipeline.
- Refactorings spread across the codebase atomically.

### Variations

- **Pure trunk-based** — direct commits to main; CI catches problems immediately.
- **Short-lived feature branches** — branches that live hours-to-a-day, PR'd into main with full pipeline running.
- **No long-lived feature branches** — anything longer than a day or two is a smell.

### Trunk-based vs Git Flow

| | Trunk-Based | Git Flow |
|---|---|---|
| Main branch | Always releasable | Releases tagged from main |
| Feature work | On main (or short branches) | On long-lived feature branches |
| Merge frequency | Hourly to daily | Per feature (weeks) |
| Integration risk | Low (continuous) | High (merge bombs) |
| CD compatibility | Native | Difficult |
| Used by | High-performing teams (DORA studies) | Many teams, fewer CD-mature |

Git Flow was designed for *versioned-release* products where features ship in batched releases. For CD with multiple deploys per day, Git Flow is the wrong tool.

### How can you do trunk-based with in-flight features?

Feature flags. Branch by abstraction. Dark launching. See below.

---

## Feature Flags / Toggles

A switch that hides incomplete functionality from users while the code is on trunk.

```csharp
if (features.IsEnabled("new-checkout-flow", customer))
{
    return newCheckout.Render(cart);
}
return legacyCheckout.Render(cart);
```

### Kinds of flags (Pete Hodgson's taxonomy)

- **Release toggles** — short-lived; off in prod until the feature is ready; remove after rollout.
- **Experiment toggles** — split users for A/B testing; remove after experiment ends.
- **Ops toggles** — operational kill-switches; long-lived; flip during incidents.
- **Permission toggles** — entitlements per user/customer; long-lived; effectively configuration.

### Practices

- **Delete release flags promptly.** Stale flags become technical debt; the conditional logic accumulates.
- **Test both sides.** A flagged path that's never been tested with the flag on is unsafe to enable.
- **Centralize flag definitions.** Don't scatter `if FEATURE_X` strings; keep a catalog.
- **Default to off in untested code paths.** Misconfiguration should be safe.
- **Track flag age.** Flags older than a quarter need a decision: enable everywhere and remove, or kill the feature.

---

## Branch by Abstraction

When a large change can't be flagged at one switch (because it spans many files), use Branch by Abstraction instead of a long-lived branch.

**Steps:**
1. Introduce an abstraction (interface) for the code you're going to change.
2. Make all callers depend on the abstraction.
3. Build the new implementation behind the abstraction.
4. Cut over (flag or config).
5. Remove the old implementation.

All steps happen on trunk; nothing is hidden in a branch. The system is always working; the new code is dark until enabled.

---

## Deployment Strategies

How to push the new artifact to production without breaking running users.

### Blue/Green
Two identical production environments — blue (live) and green (idle). Deploy to green; smoke-test; switch traffic; keep blue as immediate rollback. After confidence, blue becomes the next idle.
- **Pro:** instant rollback.
- **Con:** double the infrastructure during deployment.

### Canary
Route a small fraction of traffic (1%, 5%) to the new version; monitor; ramp up if healthy; roll back if not.
- **Pro:** real production exposure with limited blast radius.
- **Con:** requires traffic shifting (load balancer, service mesh).

### Rolling
Replace instances one at a time. New version takes over gradually.
- **Pro:** built into most orchestrators (Kubernetes, ECS).
- **Con:** mixed-version state during deployment; hard to roll back.

### Recreate
Stop everything; deploy new version; start.
- **Pro:** simple.
- **Con:** downtime. Only for batch jobs and tolerant systems.

### Dark Launching
Run new code in production but discard its output (or only log it). Validate it produces correct results against real traffic before turning it on.
- Especially useful for: rewriting a critical pathway, performance-sensitive code, AI/ML models.

---

## Database Migrations

The hardest part of CD for stateful systems.

### Expand / Contract (Parallel Change)
1. **Expand:** add the new schema element (column, table) alongside the old.
2. **Migrate:** dual-write or backfill data.
3. **Cut over:** code uses the new schema element.
4. **Contract:** remove the old schema element.

Every step is backward-compatible with the running code. Deploy can happen between any two steps without breaking anything.

### Migration discipline
- **Forward-only.** Migrations apply in order; you don't roll them back — you migrate forward to a fix.
- **Idempotent.** Running twice is safe.
- **Atomic per migration.** Either fully applied or fully rolled back.
- **Tested in CI.** Migrations run against a real DB during the pipeline.

---

## The DORA Four Key Metrics

Empirical research (Jez Humble, Nicole Forsgren, Gene Kim — *Accelerate*, 2018) identified four metrics that predict software-delivery performance better than any others.

### 1. Deployment Frequency
How often do you deploy to production?
- **Elite:** on demand (multiple per day)
- **High:** between once per day and once per week
- **Medium:** between once per week and once per month
- **Low:** between once per month and once every six months

### 2. Lead Time for Changes
How long from commit to production?
- **Elite:** less than an hour
- **High:** between a day and a week
- **Medium:** between a week and a month
- **Low:** between a month and six months

### 3. Change Failure Rate
What percentage of changes cause incidents?
- **Elite:** 0–15%
- **High:** 16–30%
- **Medium:** 16–30%
- **Low:** 16–30%

(Elite teams are noticeably better even on this; the others cluster.)

### 4. Mean Time to Restore (MTTR)
When something breaks, how fast do you fix it?
- **Elite:** less than an hour
- **High:** less than a day
- **Medium:** less than a day
- **Low:** between a week and a month

The research finding: **elite performers are dramatically better on all four**. They are not trading speed for stability; they have both because of the practices that enable both.

---

## What Makes CD Hard

- **Legacy code without tests.** Pipelines depend on tests; legacy systems often lack them. Get tests in (see Legacy Code skill) before CD discipline applies.
- **Long-lived branches.** Embedded in many teams' Git habits and process.
- **Manual deployment steps.** Each one is a brake; each one needs automation.
- **Database changes.** Stateful schema is hard. Expand/contract works but requires discipline.
- **Coupled monoliths.** A monolith forces all-or-nothing deploys; CD wants smaller blast radii.
- **Risk-averse organizations.** "We can't deploy that often." CD says: deploying often is what makes deploying safer, not less safe.

---

## What CD Enables

- **Smaller, safer releases.** Each deploy is one commit's worth of change, not a quarter's.
- **Faster feedback from users.**
- **Continuous learning.** Hypothesis → ship → measure → iterate, in days not quarters.
- **Recovery as routine.** Rolling back is something you do every week without drama.
- **Better developer experience.** No "release week"; no "merge hell"; no firefighting marathons.

---

## Common Mistakes

- **CI without CD.** Continuous Integration with weekly manual deploys is half-built.
- **Tests in the pipeline but not trusted.** Flaky tests get ignored; ignored failures become real bugs.
- **Long pipelines.** A 90-minute commit stage is broken; developers stop running it locally; integration backs up.
- **Manual approvals at every stage.** The pipeline becomes a ticketing system. Reduce to one approval (or zero) once trust is established.
- **Coupling pipelines to environments.** "The prod pipeline is different." It should not be. Promote the artifact; only config differs.
- **Skipping the test pyramid.** All end-to-end, no unit; or all unit, no end-to-end. Balance.
- **Treating flags as forever.** Flag debt is real debt.
- **Optimizing for one metric in isolation.** All four DORA metrics together.

---

## Quick Application Checklist

For the pipeline:
- [ ] Is the trunk always in a deployable state?
- [ ] Is every commit built and tested automatically?
- [ ] Does the commit stage complete in under 5 minutes?
- [ ] Does the acceptance stage complete in under 30 minutes?
- [ ] Is the same artifact promoted through all stages (built once)?
- [ ] Are the same deployment scripts used in every environment?
- [ ] Is the pipeline status visible to the team?

For branching:
- [ ] Are feature branches short-lived (≤ 1 day)?
- [ ] Is in-flight work hidden behind feature flags or branch-by-abstraction?
- [ ] Are stale flags tracked and removed?

For deployments:
- [ ] Can you deploy without downtime?
- [ ] Can you roll back (or forward-fix) within minutes?
- [ ] Are deploys boring and routine?

For DORA metrics:
- [ ] Are you tracking deployment frequency?
- [ ] Are you tracking lead time?
- [ ] Are you tracking change failure rate?
- [ ] Are you tracking MTTR?
- [ ] What's the team's improvement target on each?

---

## Reading

- **Jez Humble & David Farley**, *Continuous Delivery: Reliable Software Releases Through Build, Test, and Deployment Automation* (2010) — the foundational text.
- **Nicole Forsgren, Jez Humble & Gene Kim**, *Accelerate: The Science of Lean Software and DevOps* (2018) — the empirical case; the DORA four key metrics.
- **David Farley**, *Continuous Delivery Pipelines* (2021) — practical pipeline design.
- **David Farley**, *Modern Software Engineering* (2021) — broader framing.
- **Pete Hodgson**, *Feature Toggles (aka Feature Flags)* — Martin Fowler bliki essay, the canonical taxonomy.
- **Paul Hammant**, *trunkbaseddevelopment.com* — practical guide to trunk-based development.
- **Charity Majors**'s essays on observability, deploys, and on-call — modern CD culture.
- **Gene Kim et al.**, *The Phoenix Project* and *The Unicorn Project* — narrative companions.
