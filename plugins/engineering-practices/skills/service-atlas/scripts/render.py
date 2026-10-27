"""Render a service atlas (atlas.json + measurements.json) into Canvas Composer SVG frames for Miro.

Usage: python render.py <atlas.json> <measurements.json> <out-dir> [--origin X,Y]
Writes one <nn>_<frame>.svg per frame and manifest.json (order, title, item count, position).
Publish each SVG with canvas_create_from_svg, then verify item counts against the manifest.
"""
import argparse, html, json, math, os, re, sys

e = lambda s: html.escape(str(s), quote=True)
q = lambda s: html.escape(str(s), quote=False)
INK, BODY, GRID = "#1a1a1a", "#595959", "#b0b0b0"
FAM = {  # faint, light, medium, dark
    "red": ("#fff0f0", "#ffc6c6", "#ff6464", "#bd0a0a"), "orange": ("#fff5ed", "#f8d3af", "#fe9f4d", "#9b4a08"),
    "yellow": ("#fffbed", "#fff6b6", "#ffdc4a", "#af7e04"), "green": ("#eaf9ef", "#adf0c7", "#2dc75c", "#067429"),
    "blue": ("#f0f5fd", "#c6dcff", "#659df2", "#305bab"), "purple": ("#f4f2fd", "#dedaff", "#8f7fee", "#6631d7"),
}
TONE = {"bad": "red", "warn": "orange", "ok": "green", "info": "blue"}
F = 'font-family="noto_sans"'
EVENT, HOT, USER, SYSTEM = "#FFB36D", "#FF9296", "#FFF79A", "#FFD2ED"


class Frame:
    def __init__(self, key, title, w, h):
        self.key, self.title, self.w, self.h, self.items = key, title, w, h, []
        self.n = 0

    def nid(self):
        self.n += 1
        return f"{self.key}{self.n}"

    def add(self, s):
        self.items.append(s)

    def text(self, x, y, s, size=24, weight="normal", fill=INK, anchor="start"):
        self.add(f'<text x="{x:.0f}" y="{y:.0f}" {F} font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{e(s)}</text>')

    def area(self, x, y, w, s, size=22, fill=BODY, bold=False):
        body = f"<b>{q(s)}</b>" if bold else q(s)
        self.add(f'<textArea x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" {F} font-size="{size}" fill="{fill}">{body}</textArea>')

    def box(self, x, y, w, h, fill, content="", size=22, color=INK, valign="top", align="left", rx=12, stroke=None, dash=None, id_=None):
        i = id_ or self.nid()
        c = (f' data-content="{e(content)}" data-font-family="noto_sans" data-font-size="{size}" data-text-color="{color}"'
             f' data-text-align="{align}" data-text-align-vertical="{valign}"') if content else ""
        s = f' stroke="{stroke}" stroke-width="3"' if stroke else ' stroke="none"'
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect id="{i}" x="{x:.0f}" y="{y:.0f}" width="{max(w, 8):.0f}" height="{max(h, 8):.0f}" rx="{rx}" fill="{fill}"{s}{d}{c} />')
        return i

    def sticky(self, x, y, color, content, w=199, h=228):
        i = self.nid()
        self.add(f'<rect id="{i}" data-type="sticky" x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" data-color="{color}" data-content="{e(content)}" />')
        return i

    def card(self, x, y, title, desc, color, w=560):
        self.add(f'<rect id="{self.nid()}" data-type="custom-widget" data-widget-type="card" data-title="{e(title)}" '
                 f'data-description="{e(desc)}" data-color="{color}" x="{x:.0f}" y="{y:.0f}" width="{w}" height="88" fill="none" stroke="none" />')

    def link(self, a, b, color="#313131", width=2, label="", start="bottom", end="left", arrow="end", dash=None):
        lab = f' data-content="{e(label)}"' if label else ""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="0" y1="0" x2="1" y2="1" stroke="{color}" stroke-width="{width}" data-arrow="{arrow}" data-shape="elbowed" '
                 f'data-start="{a}" data-end="{b}" data-start-side="{start}" data-end-side="{end}"{lab}{d} />')

    def header(self, title, subtitle):
        self.text(64, 120, title, 67, "bold")
        self.text(64, 180, subtitle, 24, fill=BODY)

    def svg(self, ox, oy):
        head = [f'<g id="{self.key}" transform="translate({ox:.0f},{oy:.0f})" data-frame="{e(self.title)}">',
                f'<rect data-type="frame" x="0" y="0" width="{self.w:.0f}" height="{self.h:.0f}" fill="#ffffff" data-title="{e(self.title)}" />']
        return '<svg xmlns="http://www.w3.org/2000/svg">\n' + "\n".join(head + self.items + ["</g>"]) + "\n</svg>"


def tiles(fr, y, items, cols=4, h=300):
    tw = (fr.w - 128 - (cols - 1) * 32) / cols
    for i, t in enumerate(items):
        fam = FAM[TONE.get(t.get("tone", "info"), "blue")]
        x, ty = 64 + (i % cols) * (tw + 32), y + (i // cols) * (h + 32)
        fr.box(x, ty, tw, h, fam[0])
        fr.area(x + 32, ty + 28, tw - 64, t["label"], 26, INK, True)
        fr.text(x + 32, ty + 150, t["value"], 67, "bold", fam[3])
        fr.area(x + 32, ty + 180, tw - 64, t.get("note", ""), 22, INK)
    return y + math.ceil(len(items) / cols) * (h + 32)


def table(fr, x, y, heads, rows, shade=None, size=20):
    cx = x
    for h_, w_ in heads:
        fr.box(cx, y, w_ - 12, 64, FAM["blue"][1], f"<b>{q(h_)}</b>", 22, FAM["blue"][3], "middle")
        cx += w_
    for i, row in enumerate(rows):
        ry, cx = y + 76 + i * 76, x
        for j, (v, (_, w_)) in enumerate(zip(row, heads)):
            fill = shade(i, j) if shade else "#f7f7f7"
            fr.box(cx, ry, w_ - 12, 64, fill, q(v), size, INK, "middle")
            cx += w_
    return y + 76 + len(rows) * 76


# ---------------------------------------------------------------- frames
def wall(svc, d):
    fr = Frame("w", f"{svc} tech debt wall", 6400, 4400)
    fr.header(f"{svc} tech debt wall", "Up is more valuable to fix, right is more expensive. Drag a card to re-price it. Open a card for problem, why and fix.")
    lens_color = {l["name"]: FAM[l["family"]][2] for l in d["lenses"]}
    x = 160
    for l in d["lenses"]:
        fr.box(x, 215, 44, 44, FAM[l["family"]][2])
        fr.text(x + 60, 248, l["name"], 33)
        x += 120 + len(l["name"]) * 18
    quads = [("No-brainers: high value, low cost, do soon", 160, 320, "start"), ("Worthy investments: good return, needs a negotiated slot", 3210, 320, "end"),
             ("Quick wins: for a slow afternoon", 160, 2290, "start"), ("Nope: not unless cost or value changes", 3210, 2290, "end")]
    for i, (label, qx, qy, anchor) in enumerate(quads):
        fr.box(qx, qy, 3030, 1950, "#f7f7f7")
        fr.text(qx + 32 if anchor == "start" else qx + 2998, qy + 70 if qy < 1000 else qy + 1910, label, 33, "bold", INK, anchor)
    fr.text(3200, 4330, "COST OF FIXING  (1 on the left, 5 on the right)", 33, "bold", BODY, "middle")
    slots, per_cell = {}, {}
    for c in d["cards"]:
        per_cell[(c["value"], c["cost"])] = per_cell.get((c["value"], c["cost"]), 0) + 1
    for c in sorted(d["cards"], key=lambda c: (-c["value"], c["cost"])):
        cell = (c["value"], c["cost"])
        k = slots.get(cell, 0)
        slots[cell] = k + 1
        cols = 2 if per_cell[cell] <= 14 else 3
        cw = 560 if cols == 2 else 370
        cx = 200 + (c["cost"] - 1) * 1216 + (k % cols) * (cw + 20)
        cy = 420 + (5 - c["value"]) * 760 + (k // cols) * 96
        desc = (f'{c["lens"]} | value {c["value"]}, cost {c["cost"]} | PROBLEM: {c["problem"]} | WHY IT MATTERS: {c["why"]} '
                f'| FIX: {c["fix"]} | WHERE: {c.get("where", "")}')
        fr.card(cx, cy, c["title"], desc, lens_color.get(c["lens"], "#2d3142"), cw)
    return fr


def scorecard(svc, d, m):
    fr = Frame("s", f"{svc} health scorecard", 3600, 2120)
    fr.header(f"How healthy is {svc}?", f'Approximate SIG-style ratings from open tools and published thresholds. Not a certified rating. Commit {m["commit"]}, {m["date"]}.')
    tw, th = (3600 - 128 - 2 * 32) / 3, 380
    for i, p in enumerate(d["properties"]):
        stars = int(p["stars"])
        fam = FAM["green" if stars >= 4 else "orange" if stars == 3 else "red"]
        x, y = 64 + (i % 3) * (tw + 32), 260 + (i // 3) * (th + 32)
        fr.box(x, y, tw, th, fam[0])
        fr.area(x + 32, y + 28, tw - 64, p["name"], 26, INK, True)
        fr.text(x + 32, y + 140, "★" * stars + "☆" * (5 - stars), 67, "bold", fam[3])
        fr.area(x + 32, y + 170, tw - 64, p["measure"], 22, INK)
        fr.area(x + 32, y + 250, tw - 64, p.get("note", ""), 20, BODY)
    y = 260 + math.ceil(len(d["properties"]) / 3) * (th + 32)
    fr.box(64, y, 3600 - 128, max(2120 - y - 64, 160), FAM["blue"][0], f"<b>Verdict</b><br>{q(d['verdict'])}", 24)
    return fr


def squarify(items, x, y, w, h):
    """Squarified treemap: [(name, value)] -> [(name, x, y, w, h)]."""
    out, items = [], sorted(items, key=lambda t: -t[1])
    while items:
        total = sum(v for _, v in items)
        scale = w * h / total
        side = min(w, h)
        row, best = [], float("inf")
        for it in items:
            trial = row + [it]
            area = sum(v for _, v in trial) * scale
            thick = area / side
            worst = max(max(thick / (v * scale / thick), (v * scale / thick) / thick) for _, v in trial)
            if worst > best:
                break
            row, best = trial, worst
        thick = sum(v for _, v in row) * scale / side
        off = 0
        for name, v in row:
            length = v * scale / thick
            out.append((name, x, y + off, thick, length) if w >= h else (name, x + off, y, length, thick))
            off += length
        if w >= h:
            x, w = x + thick, w - thick
        else:
            y, h = y + thick, h - thick
        items = items[len(row):]
    return out


def hotspots(svc, d, m):
    g = m["git"]
    fr = Frame("h", "Where the debt charges interest", 3600, 2120)
    fr.header("Where the debt charges interest", f'Hotspots: files that change often and are large. Area is lines of code; colour is changes since {g["since"]}.')
    top = {h["path"]: h for h in g["hotspots"][:16]}
    mx = max(h["revs"] for h in top.values())
    for name, x, y, w_, h_ in squarify([(p, h["loc"]) for p, h in top.items()], 64, 240, 2300, 1800):
        h = top[name]
        r = h["revs"] / mx
        fam = FAM["red" if r > 0.66 else "orange" if r > 0.33 else "yellow"]
        fr.box(x + 4, y + 4, w_ - 8, h_ - 8, fam[1], f"<b>{q(name.split('/')[-1])}</b><br>{h['revs']} changes, {h['loc']} lines", 18, INK, rx=4)
    fr.box(2420, 240, 1116, 1800, FAM["blue"][0],
           f"<b>Reading it</b><br><br>The top 10% of files take {g['top10pct_files_share_of_changes']}% of all changes. "
           f"{g['files_over_1000']} files are over 1,000 lines and hold {g['loc_in_files_over_1000']}% of the code.<br><br>{q(d.get('commentary', ''))}", 24)
    return fr


def change_coupling(svc, d, m):
    pairs = m["git"]["change_coupling"][:12]
    fr = Frame("c", "Files that change together", 3600, 1400 + len(pairs) * 76 - 600)
    fr.header("Files that change together", "Pairs committed together most often (degree = shared commits / average commits). High degree across folders hints at a hidden dependency.")
    heads = [("Degree", 260), ("Shared", 260), ("File A", 1500), ("File B", 1452)]
    rows = [[f'{p["degree"]}%', p["shared"], p["a"].split("/", 1)[-1], p["b"].split("/", 1)[-1]] for p in pairs]
    y = table(fr, 64, 240, heads, rows, lambda i, j: FAM["red"][1] if j == 0 and pairs[i]["degree"] >= 70 else "#f7f7f7")
    if d.get("commentary"):
        fr.area(64, y + 20, 3472, d["commentary"], 22)
    fr.h = y + 160
    return fr


def roadmap(svc, d):
    moves = d["moves"]
    fr = Frame("r", "Moves to pay down the debt", 128 + min(len(moves), 5) * 1840 - 40, 0)
    fr.header("Moves to pay down the debt", "In order. Each move names the wall cards it retires and its rough size.")
    cw = 1800
    for i, mv in enumerate(moves):
        x, y = 64 + (i % 5) * (cw + 40), 260 + (i // 5) * 520
        fam = FAM["green" if mv["effort"] == "S" else "orange" if mv["effort"] == "M" else "red"]
        fr.box(x, y, cw, 480, "#f7f7f7",
               f"<b>{i + 1}  {q(mv['title'])}</b><br><br>{q(mv['why'])}<br><br><i>Retires: {q(', '.join(mv.get('cards', [])))}</i>", 22)
        fr.box(x + cw - 140, y + 24, 108, 56, fam[1], f"<b>{mv['effort']}</b>", 24, fam[3], "middle", "center")
    fr.h = 260 + math.ceil(len(moves) / 5) * 520 + 64
    return fr


def quality_frame(svc, d, m):
    qd = m["quality"]
    fr = Frame("q", "Code quality metrics", 4400, 0)
    fr.header("Code quality metrics", f'Production code: {qd["methods"]:,} methods. lizard on commit {m["commit"]}, {m["date"]}. Thresholds: SIG / Building Maintainable Software.')
    fr.text(64, 290, "Cyclomatic complexity", 44, "bold")
    fr.area(64, 316, 2600, "Share of method code in each SIG risk band (decision points per method).", 22)
    p = qd["profile"]
    x = 64
    bands = [("1-10 low", p["low"], "green"), ("11-20 moderate", p["mod"], "orange"), ("21-50 high", p["high"], "red"), (">50 very high", p["vhigh"], "purple")]
    for _, v, fam in bands:
        w = max(2600 * v / 100, 16)
        fr.box(x, 380, w, 90, FAM[fam][2], rx=4)
        x += w
    for i, (lab, v, fam) in enumerate(bands):
        fr.box(64 + i * 650, 500, 28, 28, FAM[fam][2], rx=6)
        fr.text(104 + i * 650, 524, f"{lab}: {v}%", 24)
    fr.area(64, 560, 2600, "4 stars allows moderate up to 30%, high up to 5%, very high 0%.", 22)
    fr.text(64, 720, "Methods by complexity", 33, "bold")
    hmax = max(qd["hist"].values()) or 1
    for i, (k, fam) in enumerate(zip(["1", "2-5", "6-10", "11-20", "21-50", ">50"], ["green"] * 3 + ["orange", "red", "purple"])):
        y = 750 + i * 62
        fr.text(64, y + 36, f"CCN {k}", 24, fill=BODY)
        w = max(1600 * qd["hist"][k] / hmax, 10)
        fr.box(264, y + 6, w, 40, FAM[fam][2], rx=4)
        fr.text(280 + w, y + 36, f'{qd["hist"][k]:,}', 24, "bold")
    fr.box(2760, 260, 1576, 1060, FAM["blue"][0], f"<b>Reading the numbers</b><br><br>{q(d.get('commentary', ''))}", 24)
    g = m["git"]
    dup = qd["duplication"]
    auto = [
        {"label": "Very-high complexity code", "value": f'{p["vhigh"]}%', "note": "Target 0%", "tone": "bad" if p["vhigh"] > 0 else "ok"},
        {"label": "Methods over complexity 10", "value": str(qd["methods_over_10"]), "note": f'{p["mod"] + p["high"] + p["vhigh"]:.1f}% of method code', "tone": "warn"},
        {"label": "Method code over 15 lines", "value": f'{qd["code_over_15_lines"]}%', "note": "4 stars needs under ~44%", "tone": "bad" if qd["code_over_15_lines"] > 44 else "ok"},
        {"label": "Method code over 60 lines", "value": f'{qd["code_over_60_lines"]}%', "note": "Target under 5%", "tone": "bad" if qd["code_over_60_lines"] > 5 else "ok"},
        {"label": "Methods with 5+ parameters", "value": f'{qd["methods_5_params"]}%', "note": "Target under 3%", "tone": "warn" if qd["methods_5_params"] > 3 else "ok"},
        {"label": "Duplicated code", "value": f"{dup}%" if dup is not None else "n/a", "note": "4 stars needs under 5%", "tone": "bad" if dup and dup > 5 else "ok"},
        {"label": "Files over 1,000 lines", "value": str(g["files_over_1000"]), "note": f'Hold {g["loc_in_files_over_1000"]}% of code', "tone": "bad" if g["files_over_1000"] else "ok"},
        {"label": "Mean complexity", "value": str(qd["mean_ccn"]), "note": f'Median {qd["median_ccn"]}', "tone": "info"},
    ]
    fr.text(64, 1440, "The numbers to watch", 44, "bold")
    y = tiles(fr, 1480, auto + d.get("tiles", []))
    fr.text(64, y + 60, "By project", 44, "bold")
    heads = [("Project", 1100), ("Methods", 400), ("Mean CCN", 400), ("Max CCN", 400), ("Code in methods over CCN 10", 700), ("Methods over 30 lines", 640), ("5+ params", 632)]
    rows = [[r["project"], r["methods"], r["mean"], r["max"], f'{r["nloc_cc10"]}%', f'{r["pct_long30"]}%', f'{r["pct_p5"]}%'] for r in qd["by_project"]]
    y = table(fr, 64, y + 90, heads, rows, lambda i, j: FAM["orange"][1] if (j == 3 and qd["by_project"][i]["max"] > 20) else "#f7f7f7")
    fr.text(64, y + 80, "Most complex methods", 44, "bold")
    heads = [("CCN", 220), ("Lines", 220), ("Params", 220), ("Method", 1500), ("Where", 2112)]
    rows = [[t["ccn"], t["nloc"], t["params"], t["name"], t["where"]] for t in qd["top"]]
    y = table(fr, 64, y + 110, heads, rows, lambda i, j: (FAM["red"][1] if qd["top"][i]["ccn"] > 50 else FAM["orange"][1]) if j == 0 else "#f7f7f7")
    fr.h = y + 64
    return fr


def coupling_map(svc, d):
    fr = Frame("m", f"{svc} system context map", 5600, 4200)
    fr.header(f"{svc} system context map", "Arrows point from the service that depends to the one it depends on. Colour is coupling strength (Khononov): contract, model, functional, intrusive.")
    strength = {"contract": ("green", 2), "model": ("blue", 4), "functional": ("orange", 6), "intrusive": ("red", 10)}
    cx, cy = 2400, 2250
    me = fr.box(cx - 300, cy - 140, 600, 280, FAM["purple"][1], f"<b>{q(svc)}</b>", 44, INK, "middle", "center")
    svcs = d["services"]
    for i, s in enumerate(svcs):
        ang = 2 * math.pi * i / len(svcs) - math.pi / 2
        x, y = cx + 1750 * math.cos(ang), cy + 1500 * math.sin(ang)
        fam, width = strength.get(s["strength"], ("blue", 2))
        node = fr.box(x - 260, y - 110, 520, 220, FAM[fam][0], f"<b>{q(s['name'])}</b><br>{q(s.get('role', ''))}<br><i>{q(s.get('points', ''))}</i>", 20, INK, "middle", "center", stroke=FAM[fam][2])
        sides = ("left", "right") if abs(math.cos(ang)) > 0.5 else ("top", "bottom")
        out_side = sides[1] if (math.cos(ang) > 0.5 or math.sin(ang) > 0 and abs(math.cos(ang)) <= 0.5) else sides[0]
        in_side = {"left": "right", "right": "left", "top": "bottom", "bottom": "top"}[out_side]
        if s["direction"] in ("out", "both"):
            fr.link(me, node, FAM[fam][3], width, start=out_side, end=in_side)
        if s["direction"] in ("in", "both"):
            fr.link(node, me, FAM[fam][3], width, start=in_side, end=out_side, dash="5,5")
    ly = 3900
    for i, (k, (fam, _)) in enumerate(strength.items()):
        fr.box(64 + i * 600, ly, 40, 40, FAM[fam][2], rx=6)
        fr.text(124 + i * 600, ly + 32, k.capitalize(), 24)
    fr.text(2600, ly + 32, f"Solid: {svc} depends on it.  Dashed: it depends on {svc}.", 24, fill=BODY)
    return fr


def coupling_matrix(svc, d):
    svcs = d["services"]
    fr = Frame("x", "Coupling matrix", 6400, 0)
    fr.header("Coupling matrix", "One row per service: direction, how, and how strongly. Read the Strength and Problem columns first.")
    heads = [("Service", 700), ("Direction", 700), ("How", 1700), ("Strength", 600), ("Problem", 2636)]
    dirs = {"out": f"{svc} uses it", "in": f"it uses {svc}", "both": "both ways"}
    rows = [[s["name"], dirs[s["direction"]], s.get("how", ""), s["strength"], s.get("problem", "")] for s in svcs]
    shade = {"intrusive": FAM["red"][1], "functional": FAM["orange"][1], "model": FAM["blue"][1], "contract": FAM["green"][1]}
    y = table(fr, 64, 240, heads, rows, lambda i, j: shade.get(svcs[i]["strength"], "#f7f7f7") if j == 3 else "#f7f7f7", 18)
    for i, note in enumerate(d.get("notes", [])):
        fr.box(64 + i * 2112, y + 40, 2080, 240, FAM["blue"][0], q(note), 22, INK, "middle")
    fr.h = y + 40 + (300 if d.get("notes") else 0) + 64
    return fr


def leaks(svc, d):
    fr = Frame("l", "Domain logic in the application layer", 5600, 0)
    fr.header("Domain logic in the application layer", "How much business logic sits in the application layer instead of the domain. Counts are exact; leaked lines are estimates from reading the code.")
    y = tiles(fr, 240, d["tiles"], cols=min(5, len(d["tiles"])), h=330)
    fr.text(64, y + 80, "Where the leak sits", 44, "bold")
    mx = max(f["loc"] for f in d["files"]) or 1
    for i, f in enumerate(d["files"]):
        ry = y + 110 + i * 70
        fr.text(64, ry + 36, f["name"], 24)
        w = 1500 * f["loc"] / mx
        fam = "red" if f["loc"] >= mx * 0.4 else "orange" if f["loc"] >= mx * 0.15 else "blue"
        fr.box(1100, ry + 6, w, 44, FAM[fam][2], rx=4)
        fr.text(1116 + w, ry + 38, f'{f["loc"]} lines' + (f' · {f["share"]}' if f.get("share") else ""), 24, "bold")
    fr.box(3000, y + 60, 2536, 720, FAM["blue"][0], "<b>What leaks, with examples</b><br><br>" + "<br>".join(q(k) for k in d.get("kinds", [])), 22)
    y = max(y + 110 + len(d["files"]) * 70, y + 800) + 60
    fr.text(64, y, "Worst methods", 44, "bold")
    heads = [("#", 100), ("Method", 1650), ("Lines", 220), ("Decisions", 260), ("Why it is domain logic", 1950), ("Move to", 1292)]
    rows = [[i + 1, mm["method"], mm["lines"], mm["decisions"], mm["why"], mm["move_to"]] for i, mm in enumerate(d["methods"])]
    y = table(fr, 64, y + 30, heads, rows, lambda i, j: (FAM["red"][1] if d["methods"][i]["decisions"] >= 14 else FAM["orange"][1] if d["methods"][i]["decisions"] >= 10 else "#f7f7f7") if j == 3 else "#f7f7f7")
    cw = (5600 - 128 - 64) / 3
    for i, (title, body, fam) in enumerate([("What thin orchestration looks like here", d.get("contrast", ""), "green"),
                                             ("Leaks that already disagree", d.get("disagree", ""), "red"),
                                             ("Moves", "<br>".join(f"{k + 1}. {q(mv)}" for k, mv in enumerate(d.get("moves", []))), "blue")]):
        fr.box(64 + i * (cw + 32), y + 60, cw, 700, FAM[fam][0], f"<b>{title}</b><br><br>{body if fam == 'blue' else q(body)}", 22)
    fr.h = y + 60 + 700 + 64
    return fr


def big_picture(svc, d):
    X0, COL, GAP = 960, 260, 160
    steps, starts = [], []
    for pi, ph in enumerate(d["phases"]):
        starts.append(len(steps))
        steps += [dict(s, phase=pi) for s in ph["steps"]]
    cx = lambda i: X0 + i * COL + steps[i]["phase"] * GAP
    w = cx(len(steps) - 1) + 199 + 160
    lanes = d.get("lanes", [])
    fr = Frame("b", f"{svc} Big Picture", w, 1320 + len(lanes) * 340 + 64)
    fr.header(f"How work moves through {svc}", "Big Picture EventStorming, AS-IS. Read left to right. Pivotal events are bold.")
    fr.text(64, 330, "Legend", 33, "bold")
    for i, (fill, name) in enumerate([(EVENT, "Domain event"), (EVENT, "Pivotal event (bold)"), (HOT, "Hot spot"), (USER, "Person"), (SYSTEM, "External system")]):
        fr.box(64, 380 + i * 130, 260, 100, fill, f"<b>{name}</b>", 20, rx=8)
    fr.box(64, 1030, 260, 100, "none", "<b>Candidate context</b>", 20, rx=8, stroke=FAM["blue"][3], dash="12,8")
    for pi, ph in enumerate(d["phases"]):
        fr.text(cx(starts[pi]), 320, f'{pi + 1}  {ph["title"]}', 33, "bold")
        if pi < len(d["phases"]) - 1:
            last = starts[pi] + len(ph["steps"]) - 1
            fr.box(cx(last) + 199 + (COL - 199 + GAP) / 2 - 10, 300, 20, 900, "#FFCC80", rx=0, stroke="#FF6F00", dash="10,6")
    for i, s in enumerate(steps):
        if s.get("person"):
            fr.box(cx(i), 400, 199, 90, USER, q(s["person"]), 20, valign="middle", align="center", rx=8)
        fr.sticky(cx(i), 520, "orange", f"<b>{q(s['event'])}</b>" if s.get("pivotal") else q(s["event"]))
        if s.get("system"):
            fr.box(cx(i), 780, 199, 110, SYSTEM, q(s["system"]), 18, valign="middle", align="center", rx=8)
        if s.get("hotspot"):
            fr.sticky(cx(i), 920, "red", q(s["hotspot"]))
    cols = ["blue", "green", "purple", "orange", "yellow"]
    for k, c in enumerate(d.get("contexts", [])):
        x1, x2 = cx(c["first"]) - 24, cx(c["last"]) + 199 + 24
        fam = FAM[cols[k % len(cols)]]
        fr.box(x1, 370, x2 - x1, 820, "none", rx=12, stroke=fam[3], dash="12,8")
        fr.text(x1 + 16, 1240, c["name"], 24, "bold", fam[3])
    for li, lane in enumerate(lanes):
        ly = 1320 + li * 340
        fr.box(64, ly, w - 128, 290, "#f7f7f7", rx=0)
        fr.area(96, ly + 32, 760, lane["name"], 24, INK, True)
        for j, it in enumerate(lane["items"]):
            x = X0 + j * COL
            if it["kind"] == "system":
                fr.box(x, ly + 90, 199, 110, SYSTEM, q(it["text"]), 18, valign="middle", align="center", rx=8)
            else:
                fr.sticky(x, ly + 31, "orange" if it["kind"] == "event" else "red", q(it["text"]))
    return fr


STYLE = {"event": ("orange", 199, 228), "command": ("light_blue", 199, 228), "readmodel": ("light_green", 199, 228),
         "actor": ("light_yellow", 150, 172), "hotspot": ("red", 199, 228),
         "aggregate": ("yellow", 300, 195), "system": ("pink", 300, 195), "policy": ("violet", 300, 195)}
LEGEND = [("event", "Domain event"), ("command", "Command"), ("actor", "Actor"), ("readmodel", "Read model"),
          ("aggregate", "Aggregate / process"), ("system", "External system"), ("policy", "Policy"), ("hotspot", "Hot spot")]


def process(svc, proc, k, scope):
    GAPX, X0, TOP, HOT_H, ROW_H = 40, 560, 230, 290, 280
    fr = Frame(f"p{k}_", f"Process: {proc['process']}", 0, 0)
    fr.header(proc["process"], f"Process-level EventStorming{', ' + scope if scope else ''}. Starts: {proc['trigger']}. Ends: {proc['end']}. Happy path on top; alternatives below.")
    fr.text(64, TOP + 40, "Legend", 33, "bold")
    for i, (kind, name) in enumerate(LEGEND):
        fr.sticky(64, TOP + 80 + i * 150, STYLE[kind][0], "", 120, 138)
        fr.text(204, TOP + 160 + i * 150, name, 22)

    def put(kind, x, y, text, code=""):
        color, w, h = STYLE[kind]
        body = q(text) + (f"<br><i>({q(code)})</i>" if code else "")
        i = fr.nid()
        fr.add(f'<rect id="{i}" data-type="sticky" x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" data-color="{color}" data-content="{e(body)}" />')
        return i, w, h

    def row(steps, x, y):
        placed = []
        for s in steps:
            h = STYLE[s["kind"]][2]
            sy = y + (228 - h) / 2
            i, w, _ = put(s["kind"], x, sy, s["text"], s.get("code", ""))
            placed.append((i, x, sy, w, h))
            x += w + GAPX
        return placed, x

    hot_by = {}
    for h in proc.get("hotspots", []):
        hot_by.setdefault(h["on"], []).append(h["text"])
    happy, x_end = row(proc["happy"], X0, TOP + HOT_H)
    for idx, (_, x, *_r) in enumerate(happy):
        for j, t in enumerate(hot_by.get(f"happy:{idx}", [])):
            put("hotspot", x + j * 60, TOP, t)
    y, links = TOP + HOT_H + ROW_H, []
    alts = proc.get("alternatives", [])
    for a in sorted(range(len(alts)), key=lambda n: (-alts[n]["from"], n)):
        alt, src = alts[a], happy[min(alts[a]["from"], len(happy) - 1)]
        fr.text(src[1], y + 30, alt["label"], 24, "bold", BODY)
        placed, xe = row(alt["steps"], src[1] + 60, y + HOT_H)
        x_end = max(x_end, xe)
        for idx, (_, x, *_r) in enumerate(placed):
            for j, t in enumerate(hot_by.get(f"alt{a}:{idx}", [])):
                put("hotspot", x + j * 60, y + 40, t)
        if placed:
            links.append((src[0], placed[0][0]))
        y += HOT_H + ROW_H
    for s, t in links:
        fr.link(s, t)
    fr.w, fr.h = x_end + 64, max(y + 64, TOP + 80 + len(LEGEND) * 150 + 64)
    return fr


# ---------------------------------------------------------------- layout
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("atlas")
    ap.add_argument("measurements")
    ap.add_argument("out")
    ap.add_argument("--origin", default="0,0")
    a = ap.parse_args()
    d = json.load(open(a.atlas, encoding="utf-8"))
    m = json.load(open(a.measurements, encoding="utf-8"))
    svc, scope = d["service"], d.get("scope", "")
    rows = [
        [wall(svc, d["wall"]), scorecard(svc, d["scorecard"], m), hotspots(svc, d.get("hotspots", {}), m)],
        [change_coupling(svc, d.get("change_coupling", {}), m), roadmap(svc, d["roadmap"]), quality_frame(svc, d.get("quality", {}), m)],
        [coupling_map(svc, d["coupling"]), coupling_matrix(svc, d["coupling"])] + ([leaks(svc, d["leaks"])] if d.get("leaks") else []),
        [big_picture(svc, d["big_picture"])],
    ] + [[process(svc, p, k + 1, scope)] for k, p in enumerate(d.get("processes", []))]
    ox, oy = (int(v) for v in a.origin.split(","))
    os.makedirs(a.out, exist_ok=True)
    manifest, n, y = [], 0, oy
    for frames in rows:
        x = ox
        for fr in frames:
            n += 1
            name = f"{n:02d}_{re.sub(r'[^a-z0-9]+', '_', fr.title.lower()).strip('_')}.svg"
            svg = fr.svg(x, y)
            with open(os.path.join(a.out, name), "w", encoding="utf-8") as f:
                f.write(svg)
            items = len(re.findall(r"^<(rect|text|textArea|line)\b", svg, re.M)) - 1
            manifest.append({"file": name, "title": fr.title, "items": items, "x": x, "y": y, "w": round(fr.w), "h": round(fr.h), "chars": len(svg)})
            x += fr.w + 400
        y += max(fr.h for fr in frames) + 400
    with open(os.path.join(a.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    for mf in manifest:
        print(f'{mf["file"]:<52} {mf["items"]:>4} items  {mf["chars"]:>7} chars  at ({mf["x"]},{mf["y"]})')
    big = [mf["file"] for mf in manifest if mf["chars"] > 150000]
    if big:
        sys.exit(f"over the 200k-char publish limit margin, split before publishing: {big}")


if __name__ == "__main__":
    main()
