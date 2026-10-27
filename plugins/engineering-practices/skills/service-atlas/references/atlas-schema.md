# atlas.json

`render.py` reads two files: `measurements.json` (written by `measure.py`, do not edit) and `atlas.json` (you assemble it). Optional sections are marked; omit them and their frames are skipped or fall back to measurements only.

```jsonc
{
  "service": "Orders",                       // used in frame titles
  "scope": "v2 API flow",                     // optional, shown on process frames

  "wall": {                                   // from the debt-lenses agent
    "lenses": [{"name": "Security", "family": "red"}],   // family: red|orange|yellow|green|blue|purple
    "cards": [{"title": "", "lens": "Security", "value": 1, "cost": 1,
               "problem": "", "why": "", "fix": "", "where": ""}]
  },

  "scorecard": {                              // you write it from measurements.json
    "properties": [{"name": "Unit size", "stars": 1, "measure": "63% of code in methods over 15 lines", "note": ""}],
    "verdict": "One or two sentences."
  },

  "hotspots":        {"commentary": "optional"},
  "change_coupling": {"commentary": "optional"},
  "quality":         {"commentary": "", "tiles": []},   // tiles: extra {label, value, note, tone}

  "roadmap": {"moves": [{"title": "", "why": "", "effort": "S|M|L", "cards": ["wall card titles or codes"]}]},

  "coupling": {                               // from the coupling agent
    "services": [{"name": "", "role": "", "direction": "out|in|both",
                  "strength": "contract|model|functional|intrusive", "points": "", "how": "", "problem": ""}],
    "notes": ["fan-out summary", "fan-in summary"]
  },

  "leaks": { /* optional, from the leaks agent: tiles, files, kinds, methods, contrast, disagree, moves */ },

  "big_picture": {                            // from the Big Picture agent
    "phases": [{"title": "", "steps": [{"event": "", "pivotal": false, "person": "", "system": "", "hotspot": ""}]}],
    "contexts": [{"name": "", "first": 0, "last": 3}],   // indexes into the flattened step list
    "lanes": [{"name": "", "items": [{"kind": "event|system|hotspot", "text": ""}]}]
  },

  "processes": [ /* one object per phase, from the process agents (see briefs.md) */ ]
}
```

## Scorecard thresholds (SIG 2007 / *Building Maintainable Software*)

Rate each property 1-5 stars; this is an approximation from open tools, say so on the board.

| Property | Measure from `measurements.json` | 4 stars needs |
|---|---|---|
| Volume | `git.loc` | under ~250K lines (Java-equivalent) |
| Duplication | `quality.duplication` | under 5% |
| Unit size | `quality.code_over_15_lines`, `code_over_60_lines` | over 15 lines ≤ ~44%, over 60 ≤ ~7% |
| Unit complexity | `quality.profile` | moderate ≤ 30%, high ≤ 5%, very high 0% |
| Unit interfacing | `quality.methods_5_params` | 5+ params ≤ ~3% of code |
| Module coupling | hotspots, files over 1,000 lines, coupling agent | judgement; justify in `note` |

Tones for tiles: `bad` (red), `warn` (orange), `ok` (green), `info` (blue).
