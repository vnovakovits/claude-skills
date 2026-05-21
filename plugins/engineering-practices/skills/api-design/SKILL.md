---
name: api-design
description: Design APIs that are clear, evolvable, and idiomatic to their protocol — covering REST (Fielding, Richardson Maturity Model, Massé), GraphQL, gRPC/protobuf, versioning strategies, pagination, error responses (RFC 7807 Problem Details), idempotency, authentication, documentation (OpenAPI), and the pragmatic trade-offs between RESTful purity and developer ergonomics. Use when designing a new endpoint, choosing between REST/GraphQL/gRPC, defining versioning, structuring error responses, deciding pagination strategy, or evaluating an existing API's evolvability.
---

# API Design

Apply this skill when designing any API — internal or public, REST or GraphQL or RPC. The goal is clarity for consumers, evolvability for the producer, and operational sanity for everyone.

## Core Philosophy

**APIs are forever.** Internal APIs you can refactor; public APIs you cannot. Design assuming external consumers will outlive the team that built it.

**Consumers are the product.** An API is a user interface for developers. Optimize for the developer reading it for the first time, not the engineer who wrote it.

**Be conservative in what you send; liberal in what you accept.** Postel's Robustness Principle. Tolerate input variations; emit strict, predictable output. (Caveat: liberal acceptance can also enable abuse — see "When Postel goes wrong" below.)

**Evolve, don't break.** Breaking changes are expensive and usually unnecessary. Most "redesigns" can be additions that leave old shapes intact.

**Pragmatism beats purity.** RESTful purity is a tool, not a religion. When a small deviation (an action-style endpoint, a non-standard verb) produces a clearer API, take it — but document the deviation.

---

## Choosing the Protocol

Different problems want different protocols. The three dominant choices:

### REST
**Best for:** public APIs, resource-oriented domains, web-friendly clients, caching-friendly read patterns.
- HTTP-native. Verbs match operations. Status codes match outcomes. Caches work.
- Mature tooling: OpenAPI, postman, curl, every HTTP client library.
- Loose typing of payloads; schema discipline via JSON Schema / OpenAPI.

### GraphQL
**Best for:** UIs with diverse query needs over a unified data graph; aggregating multiple backends; mobile clients that need to minimize round trips.
- Strongly typed schema.
- Clients ask for exactly the fields they need.
- One endpoint; one HTTP method.
- Trade-off: caching is harder; queries are runtime-shaped (n+1, depth limits).

### gRPC
**Best for:** service-to-service communication in microservices, performance-sensitive paths, streaming, polyglot back-ends.
- Protobuf schema; compiled clients; strong contracts.
- HTTP/2 streaming.
- Less browser-friendly (gRPC-Web bridges this).
- Tooling stronger in backend than in frontend.

**Decision shorthand:**
- *External-facing, browser/mobile, varied clients →* REST.
- *Internal service-to-service, polyglot, performance-sensitive →* gRPC.
- *Complex UI data needs from many sources →* GraphQL.

Most large systems use more than one. Internal mesh = gRPC; public API = REST; some BFFs = GraphQL.

---

## REST Design

### Resources, not actions
URLs identify *things*, not *operations*. Operations are HTTP methods.

```
GET    /v1/orders                  # List orders
GET    /v1/orders/{id}             # Read one order
POST   /v1/orders                  # Create an order
PUT    /v1/orders/{id}             # Replace an order
PATCH  /v1/orders/{id}             # Partial update
DELETE /v1/orders/{id}             # Remove an order
```

**Naming conventions:**
- Plural nouns for collections (`/orders`, not `/order`).
- Lowercase, hyphens for multi-word (`/markup-templates`, not `/markupTemplates`).
- Hierarchies for ownership (`/orders/{id}/line-items`).
- No file extensions (`.json` belongs in `Accept` headers).
- No verbs in paths *as a default* — but see "Action endpoints" below for exceptions.

### HTTP methods, properly used

| Method | Safe | Idempotent | Use |
|---|---|---|---|
| GET | yes | yes | Read; never mutates |
| HEAD | yes | yes | Headers only |
| OPTIONS | yes | yes | Capability discovery |
| POST | no | no | Create; or process; or trigger action |
| PUT | no | yes | Replace entirely; can also create at known URI |
| PATCH | no | yes (when idempotently designed) | Partial update |
| DELETE | no | yes | Remove |

**Safe** = no observable state change.
**Idempotent** = repeating the same call has the same effect as one call.

GET must never mutate. Caches, proxies, and bots will retry GETs freely.

### Status codes

The most common, used correctly:

| Code | Meaning | When |
|---|---|---|
| 200 OK | Success with body | Most successful GETs, PUTs, PATCHes |
| 201 Created | Resource created | Successful POST that creates; include `Location` header |
| 202 Accepted | Async; will be processed | Long-running operations queued |
| 204 No Content | Success, no body | DELETEs; PUTs where no body is useful |
| 301 / 308 | Permanent redirect | Resource moved |
| 304 Not Modified | Conditional GET | When client cache is still valid |
| 400 Bad Request | Malformed request | Cannot be parsed or fails schema |
| 401 Unauthorized | Not authenticated | Token missing / invalid |
| 403 Forbidden | Not authorized | Token valid; user lacks permission |
| 404 Not Found | Resource doesn't exist | Or hidden for security reasons |
| 405 Method Not Allowed | Wrong verb for resource | e.g., DELETE on a read-only resource |
| 409 Conflict | Conflicting state | Duplicate creation; outdated optimistic lock |
| 410 Gone | Was here, now permanently removed | When clients should stop asking |
| 422 Unprocessable Entity | Syntactically valid, semantically invalid | Validation failure |
| 429 Too Many Requests | Rate limited | Include `Retry-After` header |
| 500 Internal Server Error | Server bug | Don't leak details |
| 502 / 503 / 504 | Upstream / overloaded / timeout | Operational |

Resist the temptation to invent new codes or use 200 for everything. The codes carry meaning that intermediaries (proxies, browsers, retries) interpret.

### Pagination

Two patterns:

**Offset/limit** — `GET /orders?offset=100&limit=20`.
- **Pro:** simple, jumpable ("page 5").
- **Con:** unstable as the underlying collection changes (insertions shift offsets); inefficient for large offsets.

**Cursor** — `GET /orders?cursor=eyJpZCI6MTIzfQ&limit=20`.
- **Pro:** stable under insertion; efficient.
- **Con:** can't jump to arbitrary page.

**Recommendation:** cursor pagination for large or volatile collections; offset for small, stable ones. Always include a `next_cursor` or `next_link` in the response.

**Page metadata:**
```json
{
  "items": [...],
  "next_cursor": "eyJpZCI6MTQzfQ",
  "total": 1284
}
```

### Error responses

**RFC 7807 Problem Details** is the standard:

```json
{
  "type": "https://example.com/probs/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 422,
  "detail": "The account balance is $10; the requested amount was $50.",
  "instance": "/accounts/12345/transfers/789",
  "balance": 10,
  "requested": 50
}
```

- `type` — a URI identifying the problem class (often docs URL).
- `title` — human-readable summary.
- `status` — HTTP status, repeated for client convenience.
- `detail` — human-readable specifics.
- `instance` — URI identifying this occurrence.
- Custom fields — domain-specific data.

**Content-Type:** `application/problem+json`.

For validation errors, an array of problems is acceptable:
```json
{
  "type": "...",
  "title": "Validation failed",
  "status": 422,
  "errors": [
    {"field": "email", "code": "invalid_format"},
    {"field": "age", "code": "out_of_range", "min": 0, "max": 120}
  ]
}
```

### Idempotency

For non-idempotent operations (POSTs that create), support an **idempotency key**:

```
POST /v1/payments
Idempotency-Key: 8c7d3f2a-9b1e-4...

{"amount": 100, "to": "acct_42"}
```

Server stores `(idempotency_key, response)` for some retention period. If the same key is seen again, return the original response — do not process again.

Essential for: payments, account creation, anything where a retry could cause double execution.

### Versioning

Three common approaches:

**URI versioning** — `/v1/orders`, `/v2/orders`.
- **Pro:** explicit, cacheable, easy to route.
- **Con:** "version" applies to the whole API, even when only some resources changed.
- Most common in practice.

**Header versioning** — `Accept: application/vnd.example.v2+json`.
- **Pro:** clean URIs; per-request versioning.
- **Con:** less discoverable; can be hard to test from a browser.

**Query parameter** — `/orders?version=2`.
- **Pro:** simple.
- **Con:** mixes versioning with content; not idiomatic.

**Pragmatic recommendation:** URI versioning for public APIs. Bump major versions only for breaking changes; additive changes don't need a new version.

**Best of all:** avoid bumping versions by designing for evolution — add fields, don't remove; tolerate extra fields; never repurpose existing fields.

### HATEOAS and the Richardson Maturity Model

Leonard Richardson's four-level model:

- **Level 0:** HTTP as transport; one URL, one verb (a la SOAP).
- **Level 1:** Multiple resources (URIs).
- **Level 2:** Multiple verbs (correct HTTP methods).
- **Level 3:** Hypermedia controls (HATEOAS) — responses include links to next actions.

Most "RESTful" APIs in the wild are Level 2. Level 3 (HATEOAS) is rare in practice; it adds complexity for benefit that few clients actually exploit.

**Recommendation:** target Level 2 with consistency. Add hypermedia links only where they provide real client value (paginated lists, state-machine workflows). Don't HATEOAS everything just to claim Level 3.

### Action endpoints (pragmatic deviations)

Some operations don't map to CRUD. Pure REST forces awkward shapes; pragmatic REST accepts named action endpoints:

```
POST /v1/orders/{id}/cancel
POST /v1/accounts/{id}/transfer
POST /v1/reservations/{id}/confirm
```

These are not RESTful in the purist sense, but they communicate intent better than:

```
PATCH /v1/orders/{id}  with body {"status": "cancelled"}
POST  /v1/account-transfers
```

**Rule:** use action endpoints when they make the API clearer; document them; keep them rare.

---

## GraphQL

### Schema design

- **Strongly typed.** Every field has a type; nullability is explicit.
- **Single endpoint.** Usually `/graphql`. All queries via POST.
- **Queries** for reads; **mutations** for writes; **subscriptions** for streams.
- **Input types** for mutation arguments.

### Patterns
- **Nullable by default? Or non-nullable?** Lean toward non-nullable for fields that should always be present (e.g., IDs). Reserve nullable for genuinely optional.
- **Avoid deep nesting** — clients can construct expensive queries; rate-limit or depth-limit on the server.
- **Connections / pagination** — Relay-style cursor connections are the de facto standard.
- **Errors** — GraphQL has a top-level `errors` array; HTTP usually 200 even when errors are present. Use the errors array deliberately.

### Anti-patterns
- **Exposing internal structure** as your schema. The schema is a contract; design it.
- **One mutation that does everything** ("updateUser" with 30 nullable fields). Prefer specific mutations.
- **N+1 problems** — solve with DataLoader or equivalent.

---

## gRPC / Protobuf

### Schema design (proto3)

```proto
service OrderService {
  rpc PlaceOrder(PlaceOrderRequest) returns (PlaceOrderResponse);
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc StreamOrders(StreamOrdersRequest) returns (stream Order);
}

message Order {
  string id = 1;
  string customer_id = 2;
  repeated LineItem line_items = 3;
  google.protobuf.Timestamp placed_at = 4;
}
```

### Patterns
- **Field numbers are forever.** Never change them; never reuse a number for a different field.
- **Add fields, don't remove.** Mark removed fields `reserved`.
- **Optional handling.** Proto3 fields are all optional in wire terms; use explicit "presence" types (`optional`, wrapper types) where presence matters semantically.
- **Streaming** — server-streaming, client-streaming, bidirectional. Use when batch is too slow or push semantics are needed.
- **Status codes** — gRPC's own set (`OK`, `NOT_FOUND`, `INVALID_ARGUMENT`, etc.). Map deliberately to HTTP if bridging.

---

## Cross-Protocol Concerns

### Authentication

- **OAuth 2.0 / OpenID Connect** for human-user APIs.
- **JWT bearer tokens** for service-to-service (short-lived; refresh tokens for long sessions).
- **API keys** for service identification only — not for end-user auth.
- **mTLS** for high-assurance internal services.

### Authorization
- Always at the API layer (don't trust the client).
- Resource-level: who can read this order, modify this account?
- Field-level: who can see this PII field?

### Rate limiting
- Per consumer, per endpoint.
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
- Status 429 with `Retry-After`.

### Documentation
- **OpenAPI (Swagger)** for REST. Generate from code where possible.
- **GraphQL** is self-documenting via introspection.
- **gRPC** is self-documenting via the `.proto` files + reflection.
- Beyond schemas: include examples, common errors, integration recipes, and a getting-started guide.

### Observability
- Request IDs propagated through every call (`X-Request-Id`).
- Structured logging with the request ID.
- Metrics: latency, throughput, error rates per endpoint.
- Distributed tracing (OpenTelemetry).

---

## Evolution and Backward Compatibility

### Safe changes (additive)
- Adding new endpoints / resources.
- Adding optional request fields.
- Adding new response fields (clients must tolerate unknown fields).
- Adding new enum values (clients must handle "unknown" gracefully).

### Breaking changes
- Removing or renaming endpoints.
- Changing response field types or semantics.
- Making optional fields required.
- Tightening validation.

**Discipline:** never break without versioning. When versioning, support old versions for as long as the consumers need (a defined deprecation window, then sunset).

### Deprecation
- Mark deprecated fields/endpoints in the docs.
- Add a `Deprecation` and `Sunset` HTTP header.
- Communicate to consumers; give them time.
- Monitor usage; turn off only when traffic is gone.

---

## When Postel's Principle Goes Wrong

"Be liberal in what you accept" enables ambiguity and abuse: clients depend on undocumented quirks (Hyrum's Law); attackers find weird inputs that produce surprising effects.

**Refined principle:** accept what the schema says; reject what it doesn't. Be strict in validation; be helpful in error messages. Don't silently accept malformed input and try to guess intent.

---

## Common Mistakes

- **Returning 200 for everything.** Status codes have meaning; use them.
- **Inconsistent naming.** Some endpoints in camelCase, some in snake_case, some in kebab-case. Pick one.
- **Exposing internal IDs / structure.** Database PKs in URLs; ORM-shaped JSON. Design the resource; don't expose the table.
- **Chatty APIs.** Designs that require five round trips for one user action. Aggregate where it makes sense.
- **Over-fetching APIs.** Returning massive objects when the client needs three fields. Consider sparse fieldsets (`?fields=id,name`) or GraphQL.
- **Versioning at the wrong granularity.** "v2 of everything" because one resource changed. Add fields; deprecate slowly.
- **Skipping the OpenAPI / Proto / GraphQL schema.** No schema = no contract = drift.
- **Forgetting idempotency for create operations.** Network retries will create duplicates.
- **Errors as 200s with a `"success": false` field.** Now every client must parse the body to detect failure.
- **Pagination footguns.** Defaulting to "all rows" with no limit; returning unbounded responses.
- **Auth as an afterthought.** Bolted on after the API ships; never quite right thereafter.

---

## Quick Application Checklist

When designing a new endpoint:
- [ ] Is it the right protocol (REST / GraphQL / gRPC)?
- [ ] Is it resource-shaped (or a deliberate action endpoint)?
- [ ] Does it use the correct HTTP method?
- [ ] Does it return the correct status code?
- [ ] Are errors in RFC 7807 Problem Details?
- [ ] Does the response have consistent naming / structure with the rest of the API?
- [ ] Is the response paginated if it returns a collection?
- [ ] Does it support idempotency where retry safety matters?

When evolving an API:
- [ ] Is this change additive (safe)?
- [ ] If breaking, do I have a versioning strategy?
- [ ] Have consumers been notified?
- [ ] Have I added `Deprecation` / `Sunset` headers?

For the API as a whole:
- [ ] Is there a canonical schema document (OpenAPI / Proto / GraphQL)?
- [ ] Is authentication / authorization at the API layer?
- [ ] Is rate limiting in place?
- [ ] Are requests traceable (request IDs)?
- [ ] Are errors observable and structured?
- [ ] Does the documentation include examples?

---

## Reading

- **Roy Fielding**, *Architectural Styles and the Design of Network-based Software Architectures* (2000 PhD thesis) — REST's foundation. Chapter 5 is where REST is defined.
- **Mark Massé**, *REST API Design Rulebook* (2011) — concise rules and conventions.
- **Arnaud Lauret**, *The Design of Web APIs* (2019) — modern, practical, opinionated.
- **JJ Geewax**, *API Design Patterns* (2021) — Google's API design experience distilled.
- **Sam Ruby et al.**, *RESTful Web Services* (2007) — foundational REST patterns.
- **RFC 7807** — Problem Details for HTTP APIs.
- **RFC 9110** — HTTP Semantics (current authoritative reference).
- **Microsoft**, *REST API Guidelines* — github.com/microsoft/api-guidelines, widely-referenced.
- **Google**, *AIP-1xx* — Google's API Improvement Proposals; cloud.google.com/apis/design.
- **Zalando**, *RESTful API Guidelines* — opnesource.zalando.com.
- **GraphQL**: graphql.org spec; Marc-André Giroux, *Production Ready GraphQL* (2020).
- **gRPC**: grpc.io documentation; Kasun Indrasiri & Danesh Kuruppu, *gRPC: Up and Running* (2020).
- **Pete Hodgson**, *Hyrum's Law* — implicit interface contracts.
