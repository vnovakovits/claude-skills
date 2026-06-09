---
name: observability
description: Apply modern observability practices from Charity Majors / Liz Fong-Jones / George Miranda's "Observability Engineering" (O'Reilly), Charity Majors' recent Observability 2.0 writing (charity.wtf & honeycomb.io, 2024-2025 — one source of truth via arbitrarily-wide structured events, aggregate at read time, observability-driven development), Cindy Sridharan's essays, Google's SRE books, and the OpenTelemetry standard. Covers observability vs. monitoring, Observability 1.0 vs 2.0, wide/canonical high-cardinality structured events, the three signals (traces/metrics/logs) with OpenTelemetry semantic conventions + context propagation, metrics (RED, USE, Four Golden Signals), distributed tracing, sampling, SLO/SLI/error-budget discipline, observability-driven development, symptom-based alerting, and what to instrument vs what's noise. Use when adding instrumentation to new code, deciding what to log/measure/trace, structuring log events, choosing metric labels vs trace/event attributes, debugging a production issue, setting up SLOs, or evaluating whether code is actually observable.
---

# Observability

Apply this skill when instrumenting a service, debugging a production issue, defining SLOs, choosing what to log and what to measure, evaluating an existing system's observability, or designing alerting. The central question: **"Can I answer any question about what my system is doing right now, without shipping new code?"**

## Core Philosophy

**Observability is the ability to ask new questions of your running system without re-deploying.** Not "did the alert fire?" — that's monitoring. Observability is "this customer reports a slow checkout; what happened on their last 5 requests, and what was different about the slowest one?"

**Monitoring is for known-unknowns; observability is for unknown-unknowns.** Monitoring tells you that a known failure mode is happening. Observability lets you investigate a failure mode you didn't anticipate.

**Production is the only environment that matters.** Tests and staging cannot reproduce production's load, data distributions, or strange-corner-of-the-graph users. Observability is how you understand production while it's running.

**Wide, high-cardinality structured events beat the "three pillars".** The traditional split into logs / metrics / traces is increasingly seen as artificial. A well-structured event (one per request, with all relevant attributes) can serve as log, metric, and trace span — and crucially supports debugging questions that pre-aggregated metrics cannot answer.

**Debug from data, not intuition.** Engineers who can interrogate production directly fix bugs faster than those who guess based on what the system *should* be doing.

---

## Observability 2.0 — One Source of Truth (Charity Majors, 2024–2025)

Majors' recent writing sharpens the three-pillars critique into a versioned distinction:

> "Observability 1.0 has three pillars and many sources of truth, scattered across disparate tools and formats. Observability 2.0 has one source of truth — arbitrarily-wide structured log events — from which you can derive all the other data types." — Charity Majors

The single key difference is **when you aggregate and where you store**:

- **1.0 aggregates at *write* time.** You decide up front what to measure, increment a counter, drop the context, and store the same request's telemetry again and again across separate silos (APM, RUM, logs, metrics, tracing, profiling, product analytics). You pay to store it repeatedly and fight cardinality forever.
- **2.0 aggregates at *read* time.** Store one wide structured event per unit of work, keep the raw context, and decide how to slice and aggregate later, at query time. Metrics, traces, heatmaps, and SLOs are all *derived* from those events. "Store it once, use it for everything."

Why it matters:

- **No dead ends.** From one event you can pivot to its trace, watch it over time, derive a metric, or define an SLO — without switching tools or losing context.
- **Arbitrary slicing.** Because raw events keep high-cardinality fields (`user_id`, `build_id`, feature-flag values), you can answer questions you never anticipated. *"Observability 1.0 is a dinner knife; 2.0 is a scalpel."*
- **Cost tracks the business.** In 2.0 the cost drivers are traffic × architecture × instrumentation density — they grow with your business and the value you get, not with how many pillars you bought. *"Poor observability is the dark matter of engineering teams."*
- **It's for *developing*, not just operating.** 1.0 answers "how do I operate my code"; 2.0 answers "how do I develop my code" — fast, interactive feedback while you build, not just incident response.

**You don't need a new vendor to get most of this — change how you instrument.** On any backend (including OpenTelemetry over "1.0" stores): attach all the context to each unit of work (one rich event/span per request — see *High-Cardinality Wide Events* below), prefer high-cardinality attributes on events/spans over new metric labels, and debug from traces + structured events rather than from pre-built dashboards.

---

## Observability-Driven Development (ODD)

Majors frames observability as a development feedback loop, not just an ops safety net:

- **Instrument as you write the code** — add the span and event fields in the *same change* as the behaviour, not as a follow-up.
- **Then inspect your code through the lens of that instrumentation** right after it deploys.
- **You're not done when it merges — you're done when you've watched it work in production.** Look at the new path's real latency, errors, and the cohort that hit it before calling it complete.
- **Tie the work to outcomes.** Wide events let you connect "my change" to "this effect on a user / the business."

Pairs naturally with progressive delivery: ship behind a flag, watch the instrumented behaviour for the cohort on the new path, then widen the rollout.

---

## Observability vs Monitoring

| Monitoring | Observability |
|---|---|
| Pre-defined dashboards & alerts | Ad-hoc queries over event data |
| Known-unknowns | Unknown-unknowns |
| "Is X working?" | "Why is Y experiencing slow Z?" |
| Aggregates, percentiles | Individual events with full context |
| Symptom detection | Root-cause investigation |
| Low cardinality fine | High cardinality essential |

The two are complementary. Monitoring tells you something is wrong. Observability tells you *what* is wrong and *who* is affected. You need both — but if forced to choose, observability wins for systems beyond trivial size.

---

## The "Three Pillars" — and Their Critique

Traditional framing: **logs, metrics, traces**.

### Logs
- Discrete events with detail.
- Best when structured (key-value pairs / JSON), worst as free-form strings.
- Searchable, debuggable, expensive to retain at high volume.

### Metrics
- Numeric values aggregated over time (counters, gauges, histograms).
- Cheap to retain, fast to query.
- Cardinality-bounded — you can't slice by user_id at scale.

### Traces
- The path of one request through a distributed system, broken into spans.
- Tells you *where time went* and which services participated.
- Most useful for latency analysis and dependency understanding.

### The critique (Majors, Sridharan)
The three pillars overlap heavily and are partially redundant. A **wide structured event** can carry log-level detail (every relevant attribute), feed metrics (counts, durations, sums derived from events), and be a trace span (with parent/child relationships, duration, service).

Modern practice: emit one wide event per unit of work. Derive metrics and traces from it. Use it directly for ad-hoc debugging. This is the architecture behind Honeycomb, and broadly aligned with what OpenTelemetry now supports.

---

## Structured Logging

The lowest-friction win. Replace string-interpolated logs with structured key-value pairs.

```csharp
// Bad — string interpolation; not queryable
_logger.LogInformation($"Order {orderId} processed for customer {customerId} in {elapsed}ms");

// Good — structured; each field independently searchable
_logger.LogInformation(
    "Order processed: {OrderId} {CustomerId} {DurationMs}",
    orderId, customerId, elapsed);
```

ASP.NET Core's `ILogger` supports message templates natively — values become structured properties in the resulting log record. Most modern logging libraries (Serilog, NLog, Zerolog, Pino, structlog) do the same.

### Practices

- **Wide events.** One log line per unit of work (request, message handled, job run) containing *all* relevant context — customer ID, tenant, feature flags, downstream call durations, decision outcomes. Avoid sprinkling 20 narrow log lines through one request.
- **Canonical log lines** (Stripe pattern). At the end of every request handler, emit a single canonical log line containing every important field. Becomes the queryable record of that request.
- **Log levels used meaningfully.** TRACE/DEBUG for development; INFO for routine events; WARN for unexpected-but-handled; ERROR for unhandled; FATAL for process-ending. If everything is INFO, levels carry no signal.
- **Correlation IDs.** Every log must carry the request ID / trace ID so you can join all logs for one request.
- **No PII / secrets** in logs. Audit what's logged; redact at the source if needed.
- **No log-level dynamic strings** (`"Customer " + customerId + " did X"`). Pass as a separate field. Otherwise queries on customer_id fail.

### Anti-patterns

- One log line per for-loop iteration in a hot path.
- Logging the same fact at multiple severity levels in different places ("am I seeing each one or many?").
- "We just `tail -f` the log file" as the debugging strategy — works until the system has more than one instance.

---

## Metrics

Numeric aggregates over time. Cheap, fast, low cardinality. Best for dashboards, alerts, and capacity questions.

### The RED Method (Tom Wilkie)
For request-driven services:
- **R**ate — requests per second
- **E**rrors — failed requests
- **D**uration — latency distribution

Three metrics, one signal of service health. The minimum viable instrumentation for any service exposed via RPC/HTTP.

### The USE Method (Brendan Gregg)
For resources (CPU, memory, disk, network, queues):
- **U**tilization — percent of resource in use
- **S**aturation — extra work waiting
- **E**rrors — error events

Use for infrastructure and shared resources; combine with RED at the service layer.

### The Four Golden Signals (Google SRE)
- **Latency** — request duration
- **Traffic** — demand on the system (requests/sec, transactions/sec)
- **Errors** — failed requests
- **Saturation** — how full the system is

A superset of RED with explicit saturation. Use this for any user-facing service.

### Cardinality discipline

A metric's labels (tags, dimensions) multiply its storage cost. A counter `http_requests_total{method, path, status}` with 5 methods × 100 paths × 10 statuses = 5,000 time series. **Add a `customer_id` label and explode to millions.**

Rules:
- **No high-cardinality labels on metrics.** Customer ID, user ID, request ID, trace ID, raw URL → these belong on events, not on metric labels.
- **Bound label values.** Normalize paths (`/users/{id}` not `/users/12345`). Bucket status codes (`2xx`/`4xx`/`5xx`) where appropriate.
- **Histograms beat means.** A mean latency of 100ms hides a p99 of 5s. Always emit histograms / percentiles, never raw means.
- **Percentiles, not averages.** Report p50, p95, p99, p99.9. The tail is where users hurt.

### What to measure

- Request rate, error rate, latency distribution per endpoint (RED).
- Resource utilization, saturation, errors per host/pod (USE).
- Business metrics: orders/sec, signups/min, payment-success rate. *These are often more meaningful than technical metrics.*
- Queue depths, retry counts, circuit-breaker states.
- Cache hit rates, DB connection pool utilization.

---

## Distributed Tracing

The path of one request through a distributed system, broken into **spans** (units of work).

```
Trace: order-place-7f3a
├─ HTTP POST /orders                          (root span, 312ms)
│  ├─ AuthService.Verify                      (15ms)
│  ├─ OrderValidator.Validate                 (4ms)
│  ├─ InventoryService.Reserve                (87ms)
│  │  └─ PostgreSQL: SELECT FROM inventory    (62ms)
│  ├─ PaymentGateway.Charge                   (180ms) ← bulk of latency here
│  └─ EventBus.Publish OrderPlaced            (12ms)
```

### Concepts

- **Trace** — the whole journey of one request.
- **Span** — one unit of work, with a name, start, end, attributes.
- **Parent / child** relationship — child span runs within parent's lifetime.
- **Trace context** — the ID + parent ID propagated across service boundaries via headers (`traceparent` per W3C standard).
- **Baggage** — additional key-value data propagated alongside trace context.

### What it answers
- **Where did time go?** (latency analysis across services)
- **Who depends on whom?** (dependency mapping)
- **What ran in parallel vs serially?** (concurrency analysis)
- **What was the state at each step?** (with span attributes)

### Sampling

Tracing every request is usually too expensive. Strategies:

- **Head sampling.** Decide at the root span (1% of all traces). Cheap; misses interesting tails.
- **Tail sampling.** Decide after the full trace is collected (always sample errors, always sample slow requests). Accurate; requires buffering.
- **Adaptive sampling.** Vary rate by endpoint, customer, or load.
- **Always sample errors.** Even at 1% sampling overall, sample 100% of error traces.

---

## OpenTelemetry

The vendor-neutral standard for instrumentation. Replaces a fragmented past (OpenTracing + OpenCensus + vendor-specific SDKs).

### The pieces
- **API** — what you call from application code (`tracer.StartActivity`, `meter.CreateCounter`).
- **SDK** — implementation of the API, handles sampling, batching, exporting.
- **Collector** — out-of-process agent that receives, processes, and exports telemetry to backends (Honeycomb, Datadog, Tempo, Jaeger, Prometheus, etc.).
- **Semantic conventions** — standardized attribute names (`http.method`, `db.system`, `messaging.destination`). Use them.

### .NET specifics
A typical ASP.NET Core host wires OpenTelemetry once at startup (use your service name for the source/meter):

```csharp
services.AddOpenTelemetry()
    .WithTracing(b => b
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddNpgsql()                                     // PostgreSQL
        .AddSource(ServiceName)                          // custom spans
        .AddOtlpExporter())
    .WithMetrics(b => b
        .AddAspNetCoreInstrumentation()
        .AddRuntimeInstrumentation()
        .AddMeter(ServiceName)
        .AddOtlpExporter());
```

Custom spans use `Activity` (System.Diagnostics) from a shared `ActivitySource`; tags become span attributes:
```csharp
using var activity = activitySource.StartActivity("Copy.SelectItinerary");
activity?.SetTag("carrier_service.count", reference.CarrierServices.Length);
// ... work ...
activity?.SetTag("copy.outcome", outcome);
```

Metrics use a `Meter` + a counter/histogram. Keep high-cardinality fields (ids) OFF metric tags and ON the span/event instead.

### Auto-instrumentation
Adds spans automatically for HTTP, DB, queues, runtime. Get most of the value for almost no code. Always start here before hand-instrumenting.

---

## SLI / SLO / Error Budgets

The Google SRE framework. The discipline that connects observability to product decisions.

### SLI — Service Level Indicator
A specific measurement of service health. Examples:
- "Percent of HTTP requests that return 2xx in under 500ms."
- "Percent of orders processed without manual intervention."
- "Percent of search queries that return at least one result."

Choose SLIs that **reflect what users actually experience**, not internal-server metrics.

### SLO — Service Level Objective
A target for the SLI over a window. Examples:
- "99.9% of HTTP requests return 2xx in under 500ms, measured over 30 days."
- "99.5% of orders are processed within 60 seconds, measured over 7 days."

The SLO is a contract with your users (implicit) and your own team (explicit).

### Error Budget
`1 - SLO`. With a 99.9% SLO, the error budget is 0.1% — ~43 minutes per month of allowed downtime.

The error budget enables explicit trade-offs:
- **Budget remaining → ship faster.** Take risks; deploy aggressively.
- **Budget exhausted → slow down.** Stop feature work; fix reliability.

Without an error budget, "reliability" is an unbounded demand competing with shipping. With one, it's a measured constraint.

### SLA vs SLO
- **SLO** — your internal target.
- **SLA** — your contractual target with customers, usually weaker than the SLO (you alert on the SLO before breaching the SLA).

---

## High-Cardinality Wide Events

The argument from Honeycomb / Charity Majors: store one event per unit of work, with as many attributes as possible.

```json
{
  "timestamp": "2026-05-11T14:32:01Z",
  "service": "cedar-api",
  "operation": "POST /v1/markups/calculate",
  "duration_ms": 87,
  "status_code": 200,
  "trace_id": "abc123",
  "span_id": "def456",
  "customer_id": "c_42",
  "tenant_id": "t_acme",
  "template_name": "EU-Express",
  "weight_kg": 12.4,
  "bound_type": "Import",
  "country": "DE",
  "feature_flag.new_markup": true,
  "db.query_count": 3,
  "db.duration_ms": 22,
  "http_client.request_count": 1,
  "http_client.duration_ms": 41,
  "outcome": "success"
}
```

Now you can ask:
- "Which customers had p99 > 1s in the last hour?" (group by customer, percentile by duration)
- "Did the new_markup feature flag cause slower responses for tenant_acme?" (filter by flag and tenant, compare durations)
- "Which template + country combos have the highest error rates?" (group by template+country, count errors)

These queries are impossible against pre-aggregated metrics with bounded cardinality. Wide events make them trivial.

### When to choose wide events
- Debugging questions you can't anticipate.
- Multi-tenant systems where per-tenant slicing matters.
- Performance investigations where the tail matters more than the median.

### Cost concerns
Wide events are more expensive than metrics. Mitigate with:
- Sampling at the event level (always sample errors, slow requests).
- Tiered retention (recent: full detail; older: aggregated).
- Cardinality-aware backends (Honeycomb, Datadog APM, Grafana Tempo + Loki).

---

## Alerting

The discipline of converting signals into pages.

### Symptom-based, not cause-based
**Page on user-visible symptoms**, not on internal causes.

- **Good:** "Error rate on /orders is above 1% for 5 minutes."
- **Bad:** "CPU on instance X is above 90%."

Why: high CPU may or may not affect users. If users are fine, no human needs to wake up. If users are affected, the symptom-based alert fires.

### SLO-burn alerting
Modern best practice: alert when error budget is being consumed faster than the SLO window allows.

- **Fast burn** — exhausting a month's budget in an hour. Page immediately.
- **Slow burn** — exhausting a month's budget in a week. Open a ticket; investigate within the day.

### Alerts should be actionable
Every alert should answer:
- **What** is broken? (user impact)
- **How urgent** is it? (SLO context)
- **What to do** about it? (runbook or starting point)

If an alert fires and the on-call's response is "I don't know what this means", the alert is broken — too vague, no runbook, or it shouldn't have been an alert.

### Alert fatigue
The #1 operational killer. Symptoms:
- On-call goes through hundreds of alerts per week.
- People ack alerts without investigating.
- Real incidents are missed in the noise.

Mitigation:
- Delete alerts that haven't been actionable in 6 months.
- Group correlated alerts.
- Raise thresholds for alerts that fire frequently without action.
- Page only for SLO violations and clear customer impact.

---

## Debugging in Production

Observability's payoff. The workflow:

1. **A symptom appears.** SLO alert; customer complaint; you noticed a graph.
2. **Localize.** Which service? Which endpoint? Which customer cohort? Which version?
3. **Investigate.** Query wide events; group by hypothesis-relevant attributes; find the slice with the problem.
4. **Compare.** "What's different about the slow requests vs the fast ones?" Group by attributes; find the discriminator.
5. **Trace.** Pick one bad request; look at its trace; find which span is slow / failed.
6. **Hypothesize.** Form a hypothesis. Test it with more queries before changing code.
7. **Fix and verify.** Deploy. Confirm the SLI improves.

Without observability, this loop relies on reading code and guessing. With it, the loop is empirical — minutes instead of days.

---

## Common Anti-patterns

- **Logs at every level of every function.** Volume swamps signal; cost balloons; nothing is queryable.
- **String-interpolated log messages.** Values disappear into the message; can't query.
- **Per-customer metric labels.** Cardinality explodes; backend bills explode; metrics become useless.
- **Mean latency dashboards.** The mean hides the tail. Show p50, p95, p99, p99.9.
- **Alerts on causes instead of symptoms.** CPU is high → maybe a problem, maybe not. Use customer impact as the alert trigger.
- **Alerts that never fire.** Untested = unknown.
- **Alerts that fire constantly without action.** Trained noise.
- **Tracing without sampling.** Too expensive; you sample by accident (overloading the collector).
- **Sampling without sampling errors.** You discard exactly the events you need most.
- **No correlation IDs.** Logs from one request scattered across services with no way to join them.
- **Building dashboards instead of investigating.** Dashboards show known-unknowns; debugging needs ad-hoc queries.
- **Believing the staging environment matches production.** It doesn't. Observe production.
- **Treating observability as ops's problem.** Engineers who don't instrument can't debug. Observability is a development discipline.

---

## Applying this to a new feature

When you add or change a unit of work (an endpoint, a consumer, a job):

- **Wrap the business operation in a span** (`ActivitySource.StartActivity`) and tag it with the inputs that identify the work plus the outcome.
- **Wrap each outbound call** (HTTP, DB, queue) in its own span with timeout / error attributes — slow or failing downstreams are usually the top operational concern.
- **Emit one canonical event** at the end with the full context (ids, the decision taken, the outcome, downstream durations) instead of scattering narrow log lines through the request.
- **Tag with the slice keys** you'll want to group by later (tenant, customer, country, feature-flag value).
- **Emit an outcome metric** (e.g. a `{operation}_outcome{result=...}` counter) so dashboards and alerts can track success vs each failure mode — with the outcome *bucketed*, never a high-cardinality id.
- **Define an SLO** for the operation's user-visible success + latency, and alert on its burn rate.

---

## Quick Application Checklist

For a new service:
- [ ] Structured logging configured (key-value, not string interpolation)?
- [ ] Correlation / trace IDs flowing through every log?
- [ ] OpenTelemetry instrumentation for HTTP server, HTTP client, DB?
- [ ] Custom spans around business-critical operations?
- [ ] Wide canonical log line per request?
- [ ] RED metrics per endpoint?
- [ ] USE metrics for shared resources?
- [ ] Health endpoint that reflects real health, not just process aliveness?

For metrics:
- [ ] No high-cardinality labels?
- [ ] Histograms (with percentiles), not means?
- [ ] Both technical and business metrics?

For tracing:
- [ ] Trace context propagated to all downstream calls?
- [ ] Spans named meaningfully (verb + noun)?
- [ ] Attributes on spans for important request data?
- [ ] Sampling strategy chosen; errors always sampled?

For SLOs:
- [ ] SLIs reflect user experience?
- [ ] SLOs documented with error budget?
- [ ] Alerts based on SLO burn rate, not raw metric thresholds?

For alerting:
- [ ] Every alert is symptom-based?
- [ ] Every alert is actionable?
- [ ] Every alert has a runbook link?
- [ ] On-call load is sustainable?

For debugging:
- [ ] Can I answer "which customers experienced the bug?" without re-deploying?
- [ ] Can I see the full path of one specific request?
- [ ] Can I compare slow requests to fast ones by their attributes?

---

## Reading

- **Charity Majors, Liz Fong-Jones, George Miranda**, *Observability Engineering* (O'Reilly, 2022) — the canonical modern text.
- **Cindy Sridharan**, *Distributed Systems Observability* (O'Reilly, 2018) — free; foundational essays.
- **Google SRE**, *Site Reliability Engineering* (2016) and *The Site Reliability Workbook* (2018) — SLI/SLO/error budgets, alerting, postmortems. Free online.
- **Niall Murphy & Liz Fong-Jones**, *Implementing Service Level Objectives* (O'Reilly, 2020) — practical SLO design.
- **Brendan Gregg**, *Systems Performance* (2nd ed., 2020) — USE method, performance analysis fundamentals.
- **Charity Majors**, *Observability 2.0* writing (2024-2025): "It's Time to Version Observability: Introducing Observability 2.0" (honeycomb.io) and "There Is Only One Key Difference Between Observability 1.0 and 2.0" (charity.wtf, Nov 2024) — the single-source-of-truth / wide-events thesis; plus "Observability: the present and future" (The Pragmatic Engineer, 2025). Ongoing essays on honeycomb.io and charity.wtf.
- **OpenTelemetry documentation** — opentelemetry.io. Specs, semantic conventions, language SDKs.
- **Stripe Engineering**, *Canonical Log Lines* essay — the wide-event pattern in practice.
- **Tom Wilkie**, *The RED Method* — original talk and Weaveworks blog post.
- **Brendan Gregg**, *The USE Method* — brendangregg.com/usemethod.
- **W3C Trace Context** — w3.org/TR/trace-context.
