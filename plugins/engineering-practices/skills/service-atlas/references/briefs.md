# Agent briefs

Paste each brief verbatim into a read-only agent (`Explore`), replacing the `<placeholders>`. Every brief starts with the common preamble.

## Common preamble

```
Repository: <repo path> (<src dir>). Service: <service>, <one line on what it does>. Scope: <scope, e.g. "the v3 API flow only: ignore legacy V1/V2 code except to flag it">. Read-only: modify nothing.
Ground every claim in the code and give file:line evidence. Say which numbers are exact counts and which are estimates. Business language on anything a reader sees; code names go in separate fields.
Return ONLY the JSON described below (no prose before it), then a short "Evidence" list of file:line for every claim.
```

## 1. Debt lenses (wall cards)

```
Goal: find the technical debt in this service for a Pete Hodgson tech debt wall, focusing on maintainability and simplicity. Look through these lenses (adjust names to the codebase): Security; Domain model; Persistence / event sourcing; Application / API layer; Tests; Build & ops. For each lens look for: god classes and long methods, duplication and near-copies, dead code and dead config, rules living in the wrong layer, missing failure handling, unsafe data handling, slow or brittle tests, CI gaps, secrets in the repo (report location only, never the value), outdated dependencies, and anything a newcomer would trip over.
Rate each item value of fixing 1-5 (5 = it hurts every week or it is a risk) and cost of fixing 1-5 (5 = months). 25-80 cards; merge near-duplicates.
JSON: {"lenses":[{"name":"...","family":"red|yellow|blue|green|purple|orange"}],
 "cards":[{"title":"<=8 words","lens":"<lens name>","value":1-5,"cost":1-5,"problem":"one sentence","why":"one sentence: what it costs us","fix":"one sentence","where":"files or paths"}]}
```

## 2. Coupling

```
Goal: a systems-level map of how this service is coupled to others. Efferent: every service it calls or sends to (HTTP clients, message commands, shared databases or event streams it reads). Afferent: every service that calls it, consumes its events, or reads its stores (search the repo for published contracts, and say where you could not see the other side). For each neighbour give direction, how (HTTP, bus, stream, DB), the number of endpoints and message types, how contracts are shared (package, copied types, none), and the coupling strength in Vlad Khononov's terms: contract (published contract), model (shares a model or copied types), functional (shares business rules or must change together), intrusive (reads another's private store or internal events). Flag the strongest, most distant, most volatile links.
JSON: {"services":[{"name":"...","role":"<=4 words","direction":"out|in|both","strength":"contract|model|functional|intrusive","points":"short counts, e.g. 3 endpoints, 2 events in","how":"...","problem":"one sentence or empty"}],
 "notes":["fan-out summary","fan-in summary"]}
```

## 3. Application-layer leaks

```
Goal: measure how much domain logic leaks into the application layer (application services, handlers, message consumers, policies/sagas, controllers) instead of the domain layer. Leak categories: (a) business decisions branching on domain state, (b) calculations (money, tax, weights, dates), (c) invariants duplicating or replacing domain guards, (d) domain events constructed outside the domain, (e) reading domain state to decide, (f) mapping that encodes business meaning. Count exactly where you can (lines, decision points, event constructions); estimate leaked lines per file. Also name the good examples of thin orchestration.
JSON: {"tiles":[{"label":"...","value":"...","note":"...","tone":"bad|warn|ok|info"}],
 "files":[{"name":"<class>","loc":<leaked lines>,"share":"<% of file>"}],
 "kinds":["<category>: <examples>", ...],
 "methods":[{"method":"Class.Method","lines":n,"decisions":n,"why":"...","move_to":"<domain module>"}],
 "contrast":"<thin orchestration examples>","disagree":"<copies of a rule that already disagree>","moves":["...","..."]}
```

## 4. Big Picture EventStorming

```
Goal: a Big Picture EventStorming (Brandolini) of this service's business process, for onboarding. Stay high level: about 15 domain events in business language and past tense, split into about 5 phases each ending in a pivotal event. Per event, optionally one person (role), one external system ("Name: role", no integration types), and at most 6 hot spots overall (specific questions or risks). Group consecutive events into 3-5 candidate bounded contexts (first/last are indexes into the flattened event list). Up to two lanes for things running alongside the main flow (for example account setup, or systems reacting to this service's events). Do not list every code event: abstract.
JSON: {"phases":[{"title":"...","steps":[{"event":"...","pivotal":true|false,"person":"...","system":"...","hotspot":"..."}]}],
 "contexts":[{"name":"...","first":i,"last":j}],
 "lanes":[{"name":"...","items":[{"kind":"event|system|hotspot","text":"..."}]}]}
```

## 5. Process (one agent per phase)

```
Process to model: <phase title> — from <trigger> until <pivotal event>, including <the main alternatives you expect>. Likely code: <paths>.
Goal: a Brandolini process-level EventStorming model of this one process, grounded in the code, for an onboarding board. Grammar: Read Model (what a person looked at) -> Actor -> Command (imperative, business words) -> Aggregate/Process or External System ("Name: role") -> Domain Event (past tense) -> Policy ("Whenever X -> do Y") -> next Command. Every command has an issuer; every event a source; after every event comes a policy or read model + actor unless it is the terminal event; conditions are policies, never labels; external systems sit inline between the command invoked on them and the event they produce.
Keep it process level: business words on every sticky, the code type in the separate "code" field. Happy path 10-18 stickies; at most 3 alternative chains of at most 6 stickies; 3-6 hot spots, each a specific question or claim grounded in code (missing failure path, rule in the wrong place, silence check "what if <system> never answers?", out-of-order arrival of inbound messages).
JSON: {"process":"...","trigger":"...","end":"...",
 "happy":[{"kind":"readmodel|actor|command|aggregate|system|event|policy","text":"<=7 words","code":"..."}],
 "alternatives":[{"from":<index into happy>,"label":"...","steps":[same shape]}],
 "hotspots":[{"on":"happy:<i>" or "alt<k>:<i>","text":"<=14 words"}]}
```
