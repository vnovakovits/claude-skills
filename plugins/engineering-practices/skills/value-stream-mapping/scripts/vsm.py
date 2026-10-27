"""Render a value stream map (current or future state) from JSON to a standalone SVG.

Usage: python vsm.py <map.json> <out.svg>
The SVG uses CSS classes with var(--token, fallback) colours, so it themes itself when inlined
into an HTML page that defines --surface, --fg, --muted, --line, --accent, --warn, --good.
See references/vsm-json.md for the input format.
"""
import html, json, math, sys

e = lambda s: html.escape(str(s), quote=True)
W_WORK, W_WAIT, GAP, PAD = 176, 96, 26, 24
CSS = """
.vsm text{font-family:var(--font-body,'IBM Plex Sans',system-ui,sans-serif);fill:var(--fg,#16202b)}
.vsm .t{font-size:15px;font-weight:600}.vsm .s{font-size:13px}.vsm .xs{font-size:12px;fill:var(--muted,#566474)}
.vsm .h{font-size:17px;font-weight:700}.vsm .big{font-size:22px;font-weight:700}
.vsm .box{fill:var(--surface,#fff);stroke:var(--fg,#16202b);stroke-width:1.6}
.vsm .band{fill:var(--sky,#e8f1f7);stroke:var(--fg,#16202b);stroke-width:1.6}
.vsm .mix{fill:var(--warn-bg,#fbefdc)}
.vsm .tri{fill:var(--warn-bg,#fbefdc);stroke:var(--warn,#9a5b00);stroke-width:1.6}
.vsm .tri-t{font-size:15px;font-weight:700;fill:var(--warn,#9a5b00)}
.vsm .push{stroke:var(--fg,#16202b);stroke-width:5;stroke-dasharray:7 5;fill:none}
.vsm .arrowhead{fill:var(--fg,#16202b)}
.vsm .info{fill:var(--surface,#fff);stroke:var(--accent,#1f5f8b);stroke-width:1.4}
.vsm .infol{stroke:var(--accent,#1f5f8b);stroke-width:1.4;fill:none;stroke-dasharray:5 4}
.vsm .ladder{stroke:var(--fg,#16202b);stroke-width:1.6;fill:none}
.vsm .kz{fill:var(--kaizen-bg,#fdecea);stroke:var(--kaizen,#c0392b);stroke-width:1.8}
.vsm .kzt{font-size:12.5px;font-weight:600;fill:var(--kaizen,#c0392b)}
.vsm .sum{fill:var(--sky,#e8f1f7);stroke:var(--fg,#16202b);stroke-width:1.6}
.vsm .est{font-size:11px;font-style:italic;fill:var(--muted,#566474)}
"""


def fmt(v):
    return f"{v:g}" if isinstance(v, (int, float)) else str(v)


def wrap(text, width_chars):
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > width_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + ([cur] if cur else [])


def tspan_lines(x, y, lines, cls, dy=16, anchor="middle"):
    out = [f'<text x="{x:.0f}" y="{y:.0f}" class="{cls}" text-anchor="{anchor}">']
    for i, l in enumerate(lines):
        out.append(f'<tspan x="{x:.0f}" dy="{0 if i == 0 else dy}">{e(l)}</tspan>')
    return "".join(out) + "</text>"


def star(cx, cy, r1, r2, n=12):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def render(m):
    steps, unit = m["steps"], m.get("unit", "days")
    rows = m.get("rows") or [[0, len(steps) - 1]]
    widths = [W_WORK if s["kind"] != "wait" else W_WAIT for s in steps]
    row_w = max(sum(widths[a:b + 1]) + GAP * (b - a) for a, b in rows)
    info = m.get("info", [])
    head = 70 if m.get("title") else 10
    top = head + (110 if info else 0)
    ROW_H, LIFT = 440, 120
    W = max(PAD * 2 + row_w + 300, m.get("min_width", 0))
    H = top + ROW_H * len(rows) + 20
    o = [f'<svg class="vsm" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{e(m.get("title", "Value stream map"))}">',
         f"<style>{CSS}</style>",
         '<defs><marker id="vsmah" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0L10,5L0,10z" class="arrowhead"/></marker></defs>']
    if m.get("title"):
        o.append(f'<text x="{PAD}" y="30" class="h">{e(m["title"])}</text>')
    if m.get("title") and m.get("subtitle"):
        o.append(f'<text x="{PAD}" y="52" class="xs">{e(m["subtitle"])}</text>')
    xs = {}
    for r, (a, b) in enumerate(rows):
        x = PAD
        for i in range(a, b + 1):
            xs[i] = (x, r)
            x += widths[i] + GAP
    if info:
        iw = min(260, (row_w - GAP * (len(info) - 1)) / len(info))
        for k, inf in enumerate(info):
            ix = PAD + k * (iw + GAP)
            o.append(f'<rect x="{ix:.0f}" y="{head}" width="{iw:.0f}" height="64" rx="4" class="info"/>')
            o.append(tspan_lines(ix + iw / 2, head + 22, wrap(inf["label"], int(iw / 8)), "s"))
            for t in inf.get("to", []):
                tx, tr = xs[t]
                if tr == 0:
                    o.append(f'<path d="M{ix + iw / 2:.0f},{head + 64} L{tx + widths[t] / 2:.0f},{top + LIFT - 20}" class="infol" marker-end="url(#vsmah)"/>')
    for r, (a, b) in enumerate(rows):
        y0 = top + r * ROW_H + LIFT
        if m.get("row_labels"):
            o.append(f'<text x="{PAD}" y="{y0 - LIFT + 24}" class="t">{e(m["row_labels"][r])}</text>')
        for i in range(a, b + 1):
            s, (x, _), w = steps[i], xs[i], widths[i]
            if s["kind"] == "wait":
                cx = x + w / 2
                o.append(f'<path d="M{cx - 30:.0f},{y0 + 38} L{cx + 30:.0f},{y0 + 38} L{cx:.0f},{y0 + 90} Z" class="tri"/>')
                o.append(f'<text x="{cx:.0f}" y="{y0 + 62}" class="tri-t" text-anchor="middle">{e(s.get("n", i + 1))}</text>')
                o.append(tspan_lines(cx, y0 + 114, wrap(s["name"], 12), "s", 15))
                o.append(tspan_lines(cx, y0 + 170, [f'{fmt(s["lt"])} {unit}'] + wrap(s.get("note", ""), 14)[:2], "xs", 14))
            else:
                cls = "box mix" if s["kind"] == "mix" else "box"
                title = wrap(s["name"], 18)[:3]
                o.append(f'<rect x="{x}" y="{y0 - 16}" width="{w}" height="56" class="band"/>')
                o.append(f'<text x="{x + 8}" y="{y0 + 18}" class="tri-t">{e(s.get("n", i + 1))}</text>')
                o.append(tspan_lines(x + w / 2 + 8, y0 + 16 - 7 * (len(title) - 1), title, "t", 15))
                o.append(f'<rect x="{x}" y="{y0 + 40}" width="{w}" height="64" class="{cls}"/>')
                o.append(tspan_lines(x + w / 2, y0 + 64, wrap(s.get("who", ""), 20)[:2], "s", 16))
                o.append(f'<rect x="{x}" y="{y0 + 112}" width="{w}" height="{88 if s.get("cadence") else 66}" class="box"/>')
                lines = [f'LT {fmt(s["lt"])} {unit}', f'PT {fmt(s["pt"])} {unit}']
                if "ca" in s:
                    lines.append(f'%C&A {fmt(s["ca"])}%')
                if s.get("cadence"):
                    lines.append(s["cadence"])
                o.append(tspan_lines(x + 10, y0 + 134, lines, "s", 20, "start"))
            if i < b:
                nx = xs[i + 1][0]
                ay = y0 + 64
                o.append(f'<path d="M{x + w + 3:.0f},{ay} L{nx - 6:.0f},{ay}" class="push" marker-end="url(#vsmah)"/>')
        ly = y0 + 240
        path = [f"M{PAD},{ly}"]
        for i in range(a, b + 1):
            s, (x, _), w = steps[i], xs[i], widths[i]
            right = x + w + (GAP if i < b else 0)
            if s["kind"] == "wait":
                path.append(f"L{right:.0f},{ly}")
                o.append(f'<text x="{x + w / 2:.0f}" y="{ly - 8}" class="s" text-anchor="middle">{fmt(s["lt"])}</text>')
            else:
                path += [f"L{x:.0f},{ly}", f"L{x:.0f},{ly + 44}", f"L{x + w:.0f},{ly + 44}", f"L{x + w:.0f},{ly}", f"L{right:.0f},{ly}"]
                o.append(f'<text x="{x + w / 2:.0f}" y="{ly - 8}" class="s" text-anchor="middle">{fmt(s["lt"])}</text>')
                o.append(f'<text x="{x + w / 2:.0f}" y="{ly + 64}" class="s" text-anchor="middle">{fmt(s["pt"])}</text>')
        o.append(f'<path d="{" ".join(path)}" class="ladder"/>')
        if r == len(rows) - 1:
            o.append(f'<text x="{PAD}" y="{ly + 90}" class="xs">Timeline: upper line is lead time per step, lower line is process (touch) time, in {e(unit)}.</text>')
    for k in m.get("kaizen", []):
        x, r = xs[k["at"]]
        cx, cy = x + widths[k["at"]] / 2, top + r * ROW_H + LIFT - 70
        lines = wrap(k["text"], 16)[:3]
        o.append(f'<polygon points="{star(cx, cy, 64, 48)}" class="kz"/>')
        o.append(tspan_lines(cx, cy + 4 - 7 * (len(lines) - 1), lines, "kzt", 14))
    total_lt = sum(s["lt"] for s in steps)
    total_pt = sum(s.get("pt", 0) for s in steps)
    sx, sy = PAD + row_w + 40, top + LIFT - 16
    lines = [("Total lead time", f"{fmt(round(total_lt, 1))} {unit}"), ("Total process time", f"{fmt(round(total_pt, 1))} {unit}"),
             ("Flow efficiency", f"{100 * total_pt / total_lt:.0f}%")]
    cas = [s["ca"] for s in steps if "ca" in s]
    if cas:
        rolled = 1.0
        for c in cas:
            rolled *= c / 100
        lines.append(("Rolled %C&A", f"{100 * rolled:.0f}%"))
    lines += [(x["label"], x["value"]) for x in m.get("summary_extra", [])]
    o.append(f'<rect x="{sx}" y="{sy}" width="236" height="{40 + 58 * len(lines)}" rx="6" class="sum"/>')
    for k, (lab, val) in enumerate(lines):
        o.append(f'<text x="{sx + 16}" y="{sy + 30 + 58 * k}" class="xs">{e(lab)}</text>')
        o.append(f'<text x="{sx + 16}" y="{sy + 56 + 58 * k}" class="big">{e(val)}</text>')
    if m.get("estimates_note"):
        o.append(tspan_lines(sx, sy + 70 + 58 * len(lines), wrap(m["estimates_note"], 34), "est", 14, "start"))
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(render(data))
    lt = sum(s["lt"] for s in data["steps"])
    pt = sum(s.get("pt", 0) for s in data["steps"])
    print(f"{len(data['steps'])} steps, lead time {lt:g}, process time {pt:g}, flow efficiency {100 * pt / lt:.0f}% -> {sys.argv[2]}")
