---
name: qa-handoff
description: Update a ticket with what shipped and tell QA what to test, in lean, empathetic, user-journey language. Verifies what is actually merged, released and deployed, maps each change to the ticket it fixes, writes a short status (in production / open / left, by owner) and a numbered list of user journeys to test with expected outcomes and what to report. Use when a change is merged or deployed and someone asks "what should QA test", "update the ticket", "post what we merged", "is this live", or wants a tester note, release note or status comment for any tracker (Linear, Jira, GitHub Issues).
---

# QA handoff: lean ticket update + what to test

The reader is a tester or a product person who knows the product, not the code. On the first
pass they want four things: **what changed for users, the rule behind it, what to try, and what
to report.** Everything else is noise.

**The PR and the handoff describe the same change from two sides.** The PR follows the *flow*:
the requests, services, events and code paths a reviewer must reason about. The handoff follows
the *user journey*: who the customer is, what they do, what they see, and the business rule that
decides it. Translate; never paste the PR's flow, diagram or class names into the handoff.

## 1. Establish the facts before writing

Never write "live" or "in production" from memory, or because something merged.

1. **What merged.** Check each pull request's state, merge commit and base branch. A change merged
   into another feature branch (a stacked PR) is not on the main branch yet.
2. **What released.** Find the release tag or build that contains the merge commit
   (`git tag --contains <commit>`, or the pipeline's build for it).
3. **What is deployed.** Check the running version: the deployment tool, the cluster, the
   pipeline, or a telemetry field the change added. If none is reachable, say so in one line
   and name whose word you rely on ("per <person>; release X contains it"). Never hide an
   unverified claim.
4. **Which ticket.** The pull request body, branch name or commits name the ticket. Post on the
   ticket the change *fixes*. A related ticket gets one line, not the test plan.
5. **Read the ticket's comments first.** If someone asked "can I close this?" or "does it need
   testing?", reply in that thread and answer the question in the first sentence.

## 2. Write the update

Lead with the answer. Drop any section with nothing in it.

**Tester note**, for the ticket the change fixes:

```
**Merged: <change link>, <date>.** <Answer to any open question, e.g. "It needs testing on staging before we close it.">

**What changed for users:** <one or two sentences: what they experienced before, what happens now>

**The rule, in plain words:** <the domain change as a business rule a tester can reason with: "A booking counts the terms as accepted if the customer accepted them on this account, or as the guest who started the booking." Then one or two concrete examples: who, what they did, what they now see.>

<If timing-dependent: "It depends on timing, so it won't show every time. Repeat each journey several times and move quickly.">

**Journeys to test** (<platforms, products or environments>)

1. **<Who does what>.** <Steps, in the order the tester does them>. <Expected outcome, stated positively>.
2. ...
N. **<One full happy path, end to end>.** Checks that nothing else broke.

**Please report:** <the failure signs>, with <the identifiers, environment, user type, time, screenshot>.

**How we'll know in production:** <the metric, error count or trace field that should move>.
```

**Status comment**, for a wider ticket with several fixes:

```
**Status, <date>: what's live, what's open, what's left**

**Live:** <change: what it fixes for users (release)>
**Open, needs review:** <change: what it fixes; merge order if stacked>
**Still to do, by owner:** <Team: the change they own>
```

## 3. Rules for the words

- **Journeys, not internals.** Write "a new user picks a plan right after signing up", not
  "POST /subscriptions returns 201". Keep endpoints, class names, status codes and storage
  details out of the tester part.
- **State the domain change as a rule.** Name the business concept the change touches (the
  booking, the customer's account, the terms) and say what the rule was and what it is now, in
  the words a support agent would use with a customer. "Who accepted the terms now counts if they
  started the booking as a guest" beats "the decision reads the draft's original account". If the
  rule needs a mechanism to make sense (a booking moving to another account), describe it as what
  the customer does and sees, not as what the system does.
- **Empathy without padding.** Name the user's experience once ("they saw an error and gave
  up"). That tells the tester why it matters. Skip apologies and adjectives.
- **Each journey has a who, the steps, and an expected result.** Bold the who-does-what. Use one
  or two sentences, in parallel form across the list.
- **Cover the axes the change touches.** Examples: anonymous vs signed-in, each product or brand,
  each variant of the flow, changing your mind midway, and one complete journey end to end.
- **Make expectations positive and concrete.** Write "the next page loads", not "no unexpected
  errors".
- **One idea per sentence, about 20 words.** No em-dashes, no parentheticals, no hedges.
- **Lean means cut, not compress.** Remove what the tester doesn't need. Never drop the expected
  outcome or what to report.
- **Say what is not ready.** If related fixes are still open, write one line, such as "The other
  two fixes are still in review, so there's nothing to test there yet."

## 4. Posting

- Show the draft when the user asked only for text. Post it when they asked you to post.
- After posting, give the link and two or three lines on what it says. Flag anything you could
  not verify.
- If someone asks only "what should we test now?", give the leanest answer:
  - the ticket;
  - a one-line test;
  - the axes to repeat it on;
  - what is not ready yet.
