---
name: pragmatic-programmer
description: Apply the broad heuristics from Andy Hunt & Dave Thomas's "The Pragmatic Programmer" (1999, 20th-anniversary ed. 2019) — DRY, orthogonality, tracer bullets, reversibility, programming by coincidence, design by contract, broken windows, knowledge portfolio, good-enough software, and the dozens of tips that shape a craftsperson's everyday judgment. Use when stuck on a non-pattern-specific problem, when reasoning about engineering trade-offs, when picking up a new technology, when growing as a developer, or when articulating habits and stances that don't fit neatly into any single methodology.
---

# The Pragmatic Programmer (Hunt & Thomas)

Apply this skill when reasoning about software at the level of *general engineering judgment* rather than specific patterns, methodologies, or technologies. The book is a collection of stances — DRY, orthogonality, reversibility, tracer bullets, broken windows — that apply across languages, stacks, and decades.

## Core Philosophy

**Software engineering is craft, not assembly.** Pragmatic programmers care about the work, take ownership of outcomes, and refuse to treat code as someone else's problem.

**Think about your work.** The single trait that distinguishes good engineers from average ones: deliberate reflection on what they're doing and why.

**Care about your craft.** Aesthetics, ergonomics, longevity — these matter. The team that doesn't care about quality ships worse software.

**Take responsibility.** Don't blame the language, the framework, the previous developer, the deadline. Own your decisions; own your communications about them.

**Provide options, not excuses.** When something is going wrong, the pragmatic response is "here are three things we could do, with these trade-offs" — not "this is broken because…".

---

## The Big Heuristics

### DRY — Don't Repeat Yourself
> *Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.*

Duplication is the prime enemy of maintainable software. **But DRY is not about "same-looking code".** It is about *knowledge* — facts, rules, configurations.

Three kinds of duplication:
- **Imposed duplication** — the environment forces it (e.g., schema repeated in code and DB). Mitigate with code generation.
- **Inadvertent duplication** — designers didn't notice the overlap. Refactor when discovered.
- **Impatient duplication** — "I'll fix it later." Almost never gets fixed. Resist.
- **Interdeveloper duplication** — multiple developers solve the same problem in different ways. Mitigate with communication and shared utilities.

**Pseudo-DRY trap:** two pieces of code that look identical but represent different knowledge. Forcing them to share an abstraction couples them — when one changes, the other has to change with it, but its requirements went somewhere else. *Same shape, different reasons, separate code.*

### Orthogonality
**Two things are orthogonal when changing one doesn't affect the other.**

Orthogonal design is the engineering analog of independence: features, modules, layers, components — each capable of changing without breaking the others.

Benefits:
- Productivity gains compound (small changes have small consequences).
- Reuse becomes feasible (an orthogonal component doesn't drag the rest of the system into a new context).
- Risk is contained (a failure in one component doesn't cascade).

Tests for orthogonality:
- If I change this module, what else must change?
- Can I test this module in isolation?
- Can I deploy / configure / scale this module independently?

### Tracer Bullets
**Don't simulate; integrate.** When facing an unknown system, the temptation is to build subsystems in isolation and integrate at the end. The pragmatic alternative is the *tracer bullet*: build a thin slice end-to-end that hits the target, even if it does almost nothing yet. Then enhance.

Tracer bullets:
- **Hit the target now**, not at the end.
- **Reveal integration risk** early, when it's cheap.
- **Demonstrate progress** to stakeholders.
- **Provide a platform** for incremental enhancement.

Distinct from prototypes: prototypes are throwaway; tracer bullets become the production system.

### Reversibility
**There are no final decisions.** Architecture, vendor choice, deployment platform, framework — all reversible at some cost. The pragmatic move is to keep costs of reversal low by:
- Hiding decisions behind interfaces.
- Avoiding hard coupling to vendor-specific features.
- Documenting decisions and assumptions.

**Reversible decisions can be made fast. Irreversible decisions deserve care.** Distinguish them.

### Programming by Coincidence
**Some programs work, but the programmer doesn't know why.**

Symptoms:
- "It works, don't touch it."
- "If I add this `sleep(100)` here it stops crashing."
- "I'm not sure what this line does but the tests passed."

Programming by coincidence is fragile, hard to debug, and breeds tribal lore. The pragmatic alternative: **understand why your code works**. If a test passes, know which behavior the test exercises. If a bug fix worked, know which underlying error it corrected.

### Design by Contract
From Bertrand Meyer. Every piece of code has:
- **Preconditions** — what must be true for the routine to work.
- **Postconditions** — what the routine guarantees on completion.
- **Invariants** — what holds before and after, throughout the routine's life.

Document them. Enforce them with assertions. Crash early when violated. **Dead programs tell no lies** — a process that crashes loudly when assumptions break is more diagnosable than one that silently produces wrong answers.

### Broken Windows
> *Don't leave broken windows (bad designs, wrong decisions, poor code) unrepaired. Fix each one as soon as it is discovered.*

Borrowed from urban criminology: a building with one broken window soon has many; one signals "nobody cares". A codebase with one tolerated bad pattern soon has many.

The corollary: **when joining a project, the first window you don't fix is the start of a slide.** Fix it the first day, even cosmetically.

### Good-Enough Software
**Perfect is the enemy of shipped.** Some software needs to be perfect (medical devices, aviation). Most doesn't. Good-enough software:
- Meets its users' actual requirements (which are often less strict than developers imagine).
- Ships on time, in budget, with tolerable defects.
- Improves iteratively.

Pragmatic engineers know when good-enough is good enough. They also know when it isn't.

### Knowledge Portfolio
**Invest regularly in your own learning.** Like a financial portfolio:
- **Diversify** — multiple languages, paradigms, problem domains.
- **Manage risk** — don't bet everything on one technology.
- **Buy low, sell high** — learn emerging technologies before they're mainstream.
- **Review and rebalance** — drop technologies that aren't paying off; add new ones.

Concrete habits:
- Learn a new language each year.
- Read a technical book each month (or quarter).
- Read non-technical books.
- Take classes.
- Participate in user groups.
- Experiment with different environments.

### Communicate!
**Engineering is communication, not just code.** The best ideas die in poor presentations. The worst ideas thrive in great ones. Skills:
- Know what you want to say.
- Know your audience.
- Choose the right moment.
- Choose the right style.
- Make it look good.
- Involve your audience.
- Listen — *really* listen.
- Get back to people.

Plain English (the right kind of plain English) beats jargon every time.

---

## Selected Tips (a Sample of the 100)

The book sprinkles numbered "Tips" throughout. A sample:

- **Tip 4:** Don't live with broken windows.
- **Tip 6:** Be a catalyst for change.
- **Tip 9:** Invest regularly in your knowledge portfolio.
- **Tip 11:** English is just a programming language.
- **Tip 12:** It's both what you say and the way you say it.
- **Tip 15:** Make it easy to reuse.
- **Tip 18:** Eliminate effects between unrelated things.
- **Tip 20:** Use tracer bullets to find the target.
- **Tip 23:** Always design for concurrency.
- **Tip 26:** Listen to nagging doubts — start when you're ready.
- **Tip 30:** You can't write perfect software.
- **Tip 32:** Crash early.
- **Tip 33:** Use assertions to prevent the impossible.
- **Tip 34:** Use exceptions for exceptional problems.
- **Tip 38:** Don't program by coincidence.
- **Tip 40:** Don't gather requirements — dig for them.
- **Tip 42:** Some things are better done than described.
- **Tip 45:** Don't fall prey to the lure of the new.
- **Tip 48:** Find bugs once.
- **Tip 50:** Don't use wizard code you don't understand.
- **Tip 51:** Don't think outside the box — find the box.
- **Tip 53:** Refactor early, refactor often.
- **Tip 58:** Test your software, or your users will.

(The 2019 anniversary edition revises and expands these. Treat as flavor; don't memorize numbers.)

---

## Stances and Habits

### Stone Soup
When a team is stuck and the obvious right thing requires more authority than you have — start small, with something obviously useful, and let momentum gather. "Just a little stone in some water" becomes a feast as others contribute. The original story is parable; the engineering version is *demonstrate value first; ask permission second*.

### Engineering Daybook
Keep a journal. Decisions made, alternatives considered, bugs hunted, ideas to follow up. Sounds quaint; pays off enormously. Externalizes memory; provides receipts when accused of "you never told me that".

### Programming Deliberately
A composite habit: think before typing, write tests, refactor, review your own code, take notes, profile, measure, sleep on big decisions, write down what you learn. Most "programming" mistakes are *not-programming-deliberately* mistakes.

### Plain Text (over binary)
Plain text resists obsolescence, diffs cleanly, integrates with tools, and survives the next platform shift. Use it as the default for configuration, data interchange, and documentation. Reach for binary formats only when there's a specific reason.

### Power Editing
Master your editor. Make it serve you, not the other way around. Investment compounds: hours saved daily, every day, for the rest of your career. (The point is investment in tools, not a specific editor.)

### Source Control Always
Even on solo projects, even on throwaways. The cost is zero; the upside (recovering from a mistake) is unbounded.

### Estimating
- Start coarse, refine as you learn.
- Use experience, not optimism.
- Track your estimates against actuals; recalibrate.
- When asked for an estimate of an unknown, the right answer is sometimes "I don't know yet — let me spike for a day".

### Debugging
- **Don't panic.** The bug is in the code, not in the universe.
- **Reproduce first**, then fix.
- **The "select" isn't broken.** Suspect your code before suspecting the library, the OS, the compiler.
- **Read the error message.** All of it. Including the stack trace. Including the cause-chain.
- **Rubber-ducking.** Explain the bug to a rubber duck (or a colleague). The act of formulating the problem aloud usually reveals it.

### Cargo Cults
After observing successful practitioners, novices imitate the *form* without understanding the *substance*. "We use Scrum" without understanding empirical process control. "We use TDD" without understanding the design feedback loop. The pragmatic move: understand *why* before adopting *what*.

---

## When to Use This Skill

- When a problem is too small or too cross-cutting for a methodology-specific skill.
- When making a decision under uncertainty (reversibility, good-enough, tracer bullets).
- When debugging stubbornly or stuck in programming-by-coincidence.
- When facing a "broken window" decision (let it slide or fix it).
- When planning your own development as an engineer (knowledge portfolio).
- When teaching juniors the *attitude* that underlies the technique.

---

## Common Mistakes

- **Treating the book as a checklist.** It's a collection of stances; internalize, don't tick.
- **Quoting tips as authority.** "The Pragmatic Programmer says…" usually means "I haven't thought about this myself." The book invites thinking; don't substitute it for thinking.
- **Confusing 'pragmatic' with 'lazy'.** Pragmatic means clear-eyed about trade-offs, not minimum-effort.
- **Stopping at 'good enough'** when the situation actually demands rigor.
- **Treating 'no broken windows' as 'perfectionism'.** Fixing broken windows is small, fast, opportunistic — not an excuse for rewriting the building.

---

## Quick Application Checklist

When making a decision:
- [ ] Is this decision reversible? If yes, make it fast; if no, make it carefully.
- [ ] Have I provided options, not excuses?
- [ ] Have I considered the orthogonality cost (what will I have to change in concert)?
- [ ] Is this duplicating knowledge that already exists elsewhere?

When approaching a new system:
- [ ] Tracer bullet first, or full system?
- [ ] What's the smallest end-to-end thing I can build today?
- [ ] What broken windows am I about to inherit — and which will I fix in week one?

When debugging:
- [ ] Have I reproduced the bug reliably before trying to fix it?
- [ ] Am I suspecting my code first, library code last?
- [ ] Have I rubber-ducked the problem?

When growing:
- [ ] When was the last time I learned a new language, paradigm, or tool?
- [ ] What's currently in my knowledge portfolio that I should sell off?

When communicating:
- [ ] Do I know my audience?
- [ ] Have I actually listened to them, or just waited my turn to talk?

---

## Reading

- **Andy Hunt & Dave Thomas**, *The Pragmatic Programmer* (1st ed. 1999, 20th-anniversary ed. 2019) — read the 20th-anniversary edition; substantially revised.
- **Andy Hunt**, *Pragmatic Thinking and Learning* (2008) — follow-up on the cognitive side: how engineers learn, the Dreyfus model, mind hacks.
- **Robert Glass**, *Facts and Fallacies of Software Engineering* (2002) — empirical companion; 55 facts and 10 fallacies that pragmatic engineers should know.
- **Steve McConnell**, *Code Complete* (2nd ed., 2004) — encyclopedic; pragmatic engineers reference it for construction details.
- **Eric Raymond**, *The Cathedral and the Bazaar* (1999) — adjacent; pragmatic engineering values map closely.
