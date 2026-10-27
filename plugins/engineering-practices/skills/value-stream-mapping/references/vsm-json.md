# vsm.py input

```jsonc
{
  "title": "Current state: one feature, from request to release",   // optional; leave out when the page has a heading
  "subtitle": "Triangles are queues; striped arrows are push.",     // optional, shown only with a title
  "unit": "days",                                                    // label for LT/PT values
  "rows": [[0, 7], [8, 14]],             // optional: step index ranges per row; default one row
  "row_labels": ["Getting to start", "Delivering"],
  "min_width": 1600,                     // optional: pad the canvas so several maps share a scale

  "info": [                              // information flow boxes across the top
    {"label": "Jira board", "to": [0]},  // "to": step indexes in the first row to draw a dashed line to
    {"label": "Weekly planning meeting", "to": [2]}
  ],

  "steps": [                             // in order, left to right
    {"kind": "wait", "name": "Backlog", "lt": 12, "note": "unmeasured"},
    {"kind": "work", "name": "Refinement", "who": "PO, devs", "lt": 3, "pt": 1, "ca": 70, "cadence": "weekly"},
    {"kind": "mix",  "name": "Code review", "who": "Devs", "lt": 2, "pt": 0.3}
  ],
  // kind: "work" (process box), "mix" (process box with waiting inside, shaded), "wait" (queue triangle)
  // lt: lead time; pt: process time (omit for waits); ca: %C&A (optional, enables rolled %C&A); n: label override

  "kaizen": [{"at": 0, "text": "Cap the backlog at 10"}],          // bursts placed above a step
  "summary_extra": [{"label": "Without the backlog", "value": "9 days, 30%"}],
  "estimates_note": "Estimates from cadences; replace with tracker state times."
}
```

The summary box always shows total lead time, total process time and flow efficiency, and adds rolled %C&A when any step has `ca`.
