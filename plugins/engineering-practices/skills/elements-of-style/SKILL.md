---
name: elements-of-style
description: Write clearly and concisely by applying William Strunk Jr.'s "The Elements of Style" (1918; Strunk & White from 1959) to any English prose — PR descriptions, commit messages, READMEs, ADRs, design docs, tickets, release notes, emails, chat replies, UI copy, error messages, code comments, marketing pages. Covers the rules of usage (commas, independent clauses, dangling participles), the principles of composition (one topic per paragraph, active voice, positive form, definite concrete language, omit needless words, parallel form, related words together, emphatic word last), the misused-words list, White's reminders on style (nouns and verbs, no qualifiers, don't overstate, avoid fancy words), a needless-phrase substitution table, and an editing pass for other people's text. Use whenever you draft, rewrite, tighten, proofread, or review prose — especially when asked to make text shorter, clearer, plainer, less wordy, or more professional, even if nobody says "Strunk", "style", or "concise".
---

# The Elements of Style (William Strunk Jr.)

Strunk wrote a forty-page rulebook for his Cornell students in 1918 because he was tired of correcting the same faults in every essay. E. B. White expanded it in 1959 and it has been the standard short guide to plain English since. Its whole argument fits in one passage from the original: **"Vigorous writing is concise. A sentence should contain no unnecessary words, a paragraph no unnecessary sentences, for the same reason that a drawing should have no unnecessary lines and a machine no unnecessary parts."**

The central test for any piece of prose: **can a busy reader get the point on the first pass, and is there nothing left they could skip without losing meaning?**

## Core Philosophy

- **The reader's attention is the scarce resource.** Every needless word spends it. Write for the person who reads it once, quickly, on a phone, three weeks from now.
- **Conciseness is a by-product of clarity, not a target.** Cut what carries no meaning; never cut what does. "Make it shorter" means "remove what the reader does not need", not "compress until it is cryptic".
- **Definite beats vague, concrete beats abstract, active beats passive, positive beats negative.** Most of the rules below are instances of these four preferences.
- **Rules first, then judgment.** Strunk himself notes that the best writers sometimes break these rules — but only when the sentence gains by it, and only writers who know the rules can tell. Break a rule on purpose, never by accident.
- **Revise.** A first draft exists to be cut. Expect to remove a quarter of it.

---

## 1. Elementary rules of usage (Strunk's rules 1–7)

These are mechanics. Get them right so the reader never stumbles.

| # | Rule | Wrong | Right |
|---|---|---|---|
| 1 | Form the possessive singular of nouns by adding `'s`, whatever the final consonant. | `Charles' book`, `the class' teacher` | `Charles's book`, `the class's teacher` (exceptions: ancient names — `Jesus'`, `Moses'`) |
| 2 | In a series of three or more, put a comma after each term except the last (the serial comma). | `students, teachers and parents` | `students, teachers, and parents` |
| 3 | Enclose parenthetic expressions between commas — or between none at all. Never one. | `The cache, which is optional is cleared.` | `The cache, which is optional, is cleared.` |
| 4 | Put a comma before a conjunction that introduces an independent clause. | `The build passed but the deploy failed.` | `The build passed, but the deploy failed.` |
| 5 | Do not join independent clauses with a comma. Use a semicolon, a period, or a conjunction. | `The job retries, it never gives up.` | `The job retries. It never gives up.` / `The job retries; it never gives up.` |
| 6 | Do not break a sentence in two. A fragment after a period must be deliberate. | `We shipped the fix. Which nobody tested.` | `We shipped the fix, which nobody tested.` |
| 7 | A participial phrase at the start of a sentence must refer to the grammatical subject. | `Being out of memory, the admin restarted the pod.` | `Because the pod was out of memory, the admin restarted it.` |

Rule 7 is the one that most often produces unintentional comedy in technical writing ("Having failed three times, we deleted the job"). Ask *who* is doing the participle's action, and make that the subject.

**On the serial comma:** Strunk requires it. If a house style guide forbids it, the house style wins — consistency within a document matters more than either rule.

---

## 2. Elementary principles of composition (rules 8–18)

This is the heart of the book. Each rule below states the principle, says why it matters, and shows it applied to the kind of prose engineers actually write.

### 8. Make the paragraph the unit of composition: one paragraph to each topic

A paragraph is a promise: "everything here is about one thing." A reader skims by paragraph. When two topics share one, the second gets lost; when one topic is split across several, the reader cannot tell where it ends.

- One-sentence paragraphs are fine for transitions and emphasis, not for whole documents.
- In a PR description or ADR, each heading's body is a paragraph in this sense: one concern per section.

### 9. Begin each paragraph with a topic sentence; end it in conformity with the beginning

Put the point first, then the support. A reader who stops after the first sentence should still know what the paragraph says. Close by returning to the point, not by wandering to the next one.

> **Before:** We looked at several options. The cache could live in Redis, or in-process, or we could skip it. Redis adds an operational dependency. In-process is simplest. We chose in-process.
>
> **After:** We chose an in-process cache. Redis would add an operational dependency we do not need yet, and skipping the cache would leave the dashboard at four seconds. In-process gives us the speed without the ops cost.

### 10. Use the active voice

The active voice is shorter, more direct, and names the actor. "The migration was applied" hides *who* applied it; "Deploy applies the migration" tells the reader where to look when it fails. Passive also breeds needless words: "there were a great number of dead leaves lying on the ground" → "dead leaves covered the ground".

Passive is right when the actor is unknown or irrelevant, or when the receiver is the topic: "The database was corrupted overnight." Use it on purpose; do not let it be the default.

> **Before:** A retry will be performed by the worker if the request is rejected by the upstream.
>
> **After:** The worker retries when the upstream rejects the request.

### 11. Put statements in positive form

Say what *is*, not what is not. Negatives make the reader compute the inverse. "Not honest" → "dishonest"; "did not remember" → "forgot"; "not important" → "trivial"; "did not pay attention to" → "ignored".

> **Before:** The parent is not able to see the balance unless the school has not disabled the feature.
>
> **After:** The parent sees the balance when the school has the feature on.

*Not* is fine as a means of denial or antithesis ("Not charity, but simple justice"). It is weak as a means of evasion.

### 12. Use definite, specific, concrete language

Prefer the specific to the general, the definite to the vague, the concrete to the abstract. The reader remembers pictures and numbers, not categories. "A period of unfavorable weather set in" → "It rained every day for a week."

> **Before:** Performance improvements were made to several areas of the seasons screen.
>
> **After:** The seasons screen now loads in 400 ms instead of 2.1 s: the class list is paged and the enrolment count is one query instead of one per class.

Vagueness in a PR or incident note is usually not a style fault; it is a sign the writer does not yet know the specific thing. Find it out, then write it.

### 13. Omit needless words

The rule everyone quotes. The common offenders are phrases that take three to six words to say what one word says, and sentences that begin with a wind-up ("the fact that", "there is … which", "it should be noted that"). See the substitution table in §3.

A whole sentence can be needless too: a sentence that announces the next sentence ("The following section describes the approach."), or repeats the heading, or restates the previous paragraph.

> **Before:** It should be noted that, owing to the fact that the endpoint is one which is not idempotent, there is a possibility that a retry could potentially result in a duplicate charge being created.
>
> **After:** The endpoint is not idempotent, so a retry can create a duplicate charge.

### 14. Avoid a succession of loose sentences

A "loose" sentence is two clauses joined by *and*, *but*, *so*, *which*, *who*. One is fine. A run of them reads like a list of afterthoughts. Break the run: make one sentence short and simple, another periodic (point at the end), turn a clause into a phrase.

> **Before:** The job runs at midnight and it reads the ledger, and then it emails the parents who have an outstanding balance, but it skips schools that have billing off, which is most of them.
>
> **After:** The job runs at midnight. It reads the ledger and emails every parent with an outstanding balance. Schools with billing off — most of them — are skipped.

### 15. Express co-ordinate ideas in similar form (parallelism)

Ideas of equal weight get the same grammatical shape. Parallel form tells the reader "these belong together" before they have read them. This matters most in lists, headings, and bullet points.

> **Before:**
> - Adding a student
> - Students can be archived
> - To move a class, drag it
>
> **After:**
> - Add a student
> - Archive a student
> - Move a class by dragging it

Also applies to correlatives: *both … and*, *not only … but also*, *either … or*, *first, second, third*. What follows each half must match.

### 16. Keep related words together

Put the subject next to its verb, the modifier next to what it modifies, the relative pronoun next to its antecedent. Words that drift apart create ambiguity or a moment of re-parsing.

> **Before:** He noticed a large stain in the rug that was right in the center.
>
> **After:** He noticed a large stain right in the center of the rug.

> **Before:** The service only retries the request twice.
>
> **After:** The service retries the request only twice.

### 17. In summaries, keep to one tense

When summarising a document, a process, or a sequence of events, pick a tense and stay in it. Shifting tenses ("the user clicks Save, the form was validated, then it will POST") makes the reader wonder whether something changed. For describing how code behaves, use the present tense.

### 18. Place the emphatic words of a sentence at the end

The end of a sentence is its most prominent position; the beginning is second. What the reader should remember goes last. "This steel is principally used for making razors, because of its hardness" → "Because of its hardness, this steel is used principally for making razors."

> **Before:** Duplicate charges are possible because the endpoint is not idempotent, in rare cases.
>
> **After:** Because the endpoint is not idempotent, a retry can produce a duplicate charge.

The same rule scales up: the emphatic sentence goes at the end of the paragraph, the emphatic paragraph at the end of the section.

---

## 3. Omit needless words — the substitution table

Reach for the right-hand column by reflex. Each left-hand phrase is grammatical and common, which is why it survives; each also makes the reader do extra work for nothing.

| Instead of | Write |
|---|---|
| the question as to whether | whether |
| there is no doubt but that | no doubt, doubtless |
| used for fuel purposes | used for fuel |
| he is a man who | he |
| in a hasty manner | hastily |
| this is a subject which | this subject |
| the fact that | (rewrite — *because*, *although*, *that*) |
| owing to the fact that / due to the fact that | because, since |
| in spite of the fact that | although |
| call your attention to the fact that | remind you |
| I was unaware of the fact that | I did not know |
| in order to | to |
| for the purpose of | to, for |
| in the event that | if |
| at this point in time | now |
| prior to / subsequent to | before / after |
| with regard to / in relation to / in terms of | about (or rewrite) |
| on a daily basis | daily |
| a number of | several, some, or the number itself |
| is able to / has the ability to | can |
| make a decision / perform an analysis / conduct a review | decide / analyse / review |
| utilize / leverage | use |
| it should be noted that / it is important to note that | (delete) |
| basically / essentially / actually / really / very / quite / rather / somewhat | (delete, or pick a stronger word) |
| going forward / at the end of the day / moving forward | (delete) |
| each and every | each |
| the reason is because | because |
| in the process of | (delete — *is migrating*, not *is in the process of migrating*) |
| whether or not | whether (unless the *or not* carries weight) |
| currently / presently (with a present-tense verb) | (delete) |
| as a matter of fact | (delete) |
| has been shown to be | is |

**"Which" hunting:** *there is / there are … which / that / who* almost always hides a stronger sentence. "There are three services that call this endpoint" → "Three services call this endpoint."

**"Case" and "-tion" nouns:** *in many cases the rooms were poorly ventilated* → *many of the rooms were poorly ventilated*. A verb turned into a noun (*perform validation of*, *make an assessment of*) turns back into the verb (*validate*, *assess*).

---

## 4. Words and expressions commonly misused

Strunk's Chapter V is a list of words that writers misuse in ways that blur meaning. The entries that still bite, plus a few software-era cousins in the same spirit:

- **Claim** — means *lay claim to*, not *assert*. "The test claims the endpoint is fast" → "The test shows".
- **Comprise** — the whole comprises the parts; the parts compose the whole. Never "is comprised of".
- **Data** — plural in Strunk's day; treat as a mass noun today if the house style does. Be consistent.
- **Different than** — write *different from*.
- **Due to** — adjectival; "the outage was due to a bad config" is fine, "the pod crashed due to a bad config" wants *because of*.
- **Effect / affect** — *effect* (n.) result, (v.) bring about; *affect* (v.) influence. "The change affects billing" / "the change has no effect on billing".
- **Etc.** — never after *such as* or *for example*; never for a list the reader could not complete themselves. In technical writing, name the items or say "and others".
- **Fewer / less** — *fewer* for things you count (fewer requests), *less* for things you measure (less latency).
- **However** — do not start a sentence with it meaning *nevertheless*; put it after the word it qualifies, or use *but*.
- **Impact** — a noun (the collision) and, in Strunk's spirit, not a verb. "This affects/changes/slows" says which.
- **Literally** — means *not figuratively*. If it can be deleted without changing the meaning, delete it.
- **Nature** — "acts of a hostile nature" → "hostile acts". Same for *character*, *type*, *kind of*, *sort of*.
- **One of the most** — feeble; say what it is.
- **Respective(ly)** — nearly always deletable.
- **So** as an intensifier ("so good") — avoid. *So* as a conjunction is fine.
- **Very** — use sparingly; where emphasis is needed, choose a strong word instead.
- **While** — use only for *during the time that*. For *although* or *whereas*, write those.
- **Would** — in conditionals, once is enough. "If it would rain, the game would be off" → "If it rained, the game would be off."
- **Jargon verbs** — *action*, *architect*, *incentivize*, *operationalize*, *productionize*, *sunset*. Each has a plain verb: do, design, encourage, run, ship, retire.

---

## 5. An approach to style (White's reminders, 1959)

E. B. White added a closing chapter of reminders on the *manner* of writing. Paraphrased and trimmed to the ones that apply to work prose:

1. **Place yourself in the background.** The subject is the reader's problem, not the writer's cleverness. "I think", "in my opinion", "I'd like to point out" — usually delete.
2. **Work from a design.** Know the shape before the first sentence: for a PR, what/why → changes → risk; for an incident note, timeline → cause → fix → prevention; for a how-to, steps in the order the reader does them.
3. **Write with nouns and verbs**, not adjectives and adverbs. A precise noun ("timeout") beats a modified vague one ("slow-ish network thing").
4. **Revise and rewrite.** The first draft is raw material. Reading it aloud, or as the recipient, finds most faults.
5. **Do not overwrite.** Rich, ornate prose is hard to digest. When in doubt, plainer.
6. **Do not overstate.** One overstatement ("catastrophic", "completely broken", "massively faster") costs the writer the reader's trust for everything else they say. Say the number.
7. **Avoid qualifiers.** *Rather*, *very*, *little*, *pretty*, *somewhat*, *fairly* — White calls them leeches on the prose.
8. **Do not affect a breezy manner.** Forced casualness ("So, funny story, the DB kinda fell over lol") wastes the reader's time and hides the point.
9. **Do not explain too much.** Trust the reader. One reason per claim, not three.
10. **Avoid fancy words.** *Utilize*, *facilitate*, *leverage*, *paradigm*, *synergy*, *robust* (when you mean *works*). Anglo-Saxon over Latinate when both exist: *use*, *help*, *start*, *end*, *show*.
11. **Be clear.** When a sentence is muddy, do not patch it — start over.
12. **Do not inject opinion** where the reader wanted information. An ADR states the trade-off; it does not editorialise about the losing option.
13. **Use figures of speech sparingly**, and never mix them. One metaphor per document is plenty.
14. **Do not take shortcuts at the cost of clarity.** Abbreviations, private acronyms, and elided words save the writer seconds and cost every reader minutes. Expand the acronym the first time.
15. **Prefer the standard to the offbeat.** Novelty in spelling, punctuation, or phrasing draws attention from the message to the writer.

---

## 6. Applying the rules to specific artefacts

### Commit messages and PR titles
- Imperative, active, specific, emphatic word near the end: `fix(billing): voiding a duplicate does not cancel the month`.
- Name the problem or the behaviour, not the mechanism ("Moved code to X" fails rule 12).
- No qualifiers, no "various", "some", "minor", "misc".

### PR descriptions, ADRs, design docs
- Topic sentence per section (rule 9). A reviewer who reads only the first line of each section should get the story.
- Concrete: numbers, file names, the exact error text — in code spans or blocks, out of the prose.
- One tense for describing behaviour (present). Past tense only for what *happened* (the incident, the old design).
- Parallel bullets (rule 15): every item in a list starts with the same part of speech.

### Tickets and bug reports
- Positive form: "Parents see the wrong balance after a refund", not "The balance is not correct for parents in the case of refunds not being handled properly."
- Steps in the order the reader does them; expected vs actual as two short lines.

### UI copy, error messages, empty states
- Definite and concrete: "No classes yet. Add your first class to start taking attendance." beats "There are currently no items to display."
- Active and second person: "Enter a valid email" not "A valid email address must be entered."
- Positive where possible: "Save to keep your changes" rather than "Changes will not be kept unless saved."
- Omit needless words hardest here — every word on a phone screen is expensive. Localised strings (Greek, etc.) follow the *spirit* (concrete, positive, short); the English rules of usage do not transfer.

### Emails, chat replies, release notes
- Point first (rule 9), then support. The reader may only see the first line in a notification.
- One paragraph per topic; one topic per message when you can.
- Do not explain too much. If the reader might want the detail, link it.

### Code comments and docstrings
- Say *why*, in one sentence, in the present tense. Delete comments that restate the code.
- "This function is responsible for the handling of" → "Handles …" or, better, no comment and a better name.

---

## 7. The editing pass — revising yours or someone else's text

Work in this order; each pass is cheap and catches a different fault.

1. **Design.** Is the point stated first? Is each section one topic? Reorder before you rewrite a sentence.
2. **Cut.** Delete needless words (§3), throat-clearing sentences, repeated ideas, and qualifiers. Aim to remove a quarter; you will usually find it.
3. **Verbs.** Turn passives active where the actor matters; turn *-tion* nouns back into verbs; replace *is / are / there is* constructions with the real verb.
4. **Concreteness.** Every "several", "some", "improved", "faster", "various", "certain" — replace with the number, the name, or the specific behaviour, or admit you do not know it yet.
5. **Order within the sentence.** Related words together (rule 16); emphatic word last (rule 18); participle referring to the subject (rule 7).
6. **Parallelism.** Every list, every heading set, every *both … and*.
7. **Mechanics.** Commas (rules 2–5), fragments (rule 6), tense (rule 17), misused words (§4).
8. **Read it as the recipient**, once, fast. Anywhere you slowed down, the reader will stop.

When editing **someone else's** text:
- Preserve their meaning and their voice. The goal is their point delivered better, not your point instead.
- Prefer deletion to substitution; prefer substitution to restructuring. Smaller edits are easier to accept.
- Do not "correct" a rule they broke deliberately (§8). Ask if unsure.
- Show the before/after for anything beyond a word swap so they can see what changed and why.
- Never edit quoted material, proper names, product strings the user did not write, legal text, or code identifiers — even when they break every rule.

---

## 8. When to break the rules

Strunk's own preface: rules are for the writer who has not yet earned the right to ignore them. Break one when the sentence is better for it, and know which one you are breaking.

- **Passive voice** when the actor is unknown, unimportant, or you are deliberately not blaming anyone ("The key was leaked" in a blameless post-mortem).
- **A fragment** for emphasis. Once.
- **A loose, conjunction-heavy sentence** to mimic the feel of a fast sequence of events.
- **A negative** when the contrast *is* the point ("Not a bug. A missing feature.").
- **House style** over Strunk on the serial comma, spelling (UK/US), and heading capitalisation — consistency beats correctness.
- **Voice and warmth** in customer-facing copy: a little more than Strunk allows is fine, so long as it never displaces the information.

The rule that is never broken: **omit needless words.**

---

## Reading

- **William Strunk Jr., *The Elements of Style* (1918)** — the original, public domain; Bartleby and Project Gutenberg host the full text. Chapters II (usage), III (composition), and V (misused words) are the substance.
- **Strunk & White, *The Elements of Style* (4th ed., 2000)** — adds White's Chapter V, "An Approach to Style", the reminders paraphrased in §5.
- **George Orwell, "Politics and the English Language" (1946)** — six rules that overlap Strunk's and add: never use a long word where a short one will do; if it is possible to cut a word out, cut it.
- **Joseph M. Williams, *Style: Toward Clarity and Grace*** — the "characters as subjects, actions as verbs" method; the best modern explanation of *why* active voice and concrete nouns read faster.
- **Steven Pinker, *The Sense of Style* (2014)** — the "curse of knowledge" as the root cause of unclear writing; the classic style; a sympathetic critique of Strunk & White's usage claims.
- **Google Developer Documentation Style Guide; Microsoft Writing Style Guide** — house-style layers for technical prose that assume Strunk underneath.
