"""Measure a service's code: complexity profile (lizard), hotspots and change coupling (git).

Usage: python measure.py <repo> <src-subdir> <out.json> [--since YYYY-MM-DD] [--ext .cs] [--exclude GLOB ...]
Read-only on the repo. Needs `lizard` (pip install lizard) and git on PATH.
"""
import argparse, csv, fnmatch, io, itertools, json, os, statistics, subprocess, sys
from collections import Counter, defaultdict
from datetime import date, timedelta

DEFAULT_EXCLUDES = ["*/obj/*", "*/bin/*", "*/node_modules/*", "*/Migrations/*", "*/migrations/*",
                    "*Test*/*", "*test*/*", "*/tests/*", "*/__tests__/*", "*/vendor/*", "*/dist/*", "*/build/*"]


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def excluded(path, globs):
    p = "/" + path.replace(os.sep, "/")
    return any(fnmatch.fnmatch(p, g) for g in globs)


def lizard_functions(root, exts, globs):
    args = [sys.executable, "-m", "lizard", "--csv"] + [a for g in globs for a in ("-x", g)] + [root]
    rows = []
    for r in csv.reader(io.StringIO(run(args))):
        if len(r) < 11 or not r[0].isdigit():
            continue
        nloc, ccn, _tok, params, length, _loc, file, func, long_name, start, _end = r[:11]
        rel = os.path.relpath(file, root).replace(os.sep, "/")
        if func == "*global*" or (exts and not rel.endswith(tuple(exts))):
            continue
        rows.append({"file": rel, "name": func, "long_name": long_name, "line": int(start),
                     "nloc": int(nloc), "ccn": int(ccn), "params": int(params)})
    return rows


def share(rows, pred):
    total = sum(r["nloc"] for r in rows) or 1
    return round(100 * sum(r["nloc"] for r in rows if pred(r)) / total, 1)


def duplication(root, globs):
    out = run([sys.executable, "-m", "lizard", "-Eduplicate"] + [a for g in globs for a in ("-x", g)] + [root])
    for line in out.splitlines():
        if "duplicate rate" in line.lower():
            try:
                return float(line.split(":")[-1].strip().rstrip("%"))
            except ValueError:
                pass
    return None


def quality(rows, root, globs):
    ccns = [r["ccn"] for r in rows]
    bands = {"1": lambda c: c == 1, "2-5": lambda c: 2 <= c <= 5, "6-10": lambda c: 6 <= c <= 10,
             "11-20": lambda c: 11 <= c <= 20, "21-50": lambda c: 21 <= c <= 50, ">50": lambda c: c > 50}
    groups = defaultdict(list)
    for r in rows:
        groups[r["file"].split("/")[0]].append(r)
    by_dir = []
    for g, rs in groups.items():
        by_dir.append({"project": g, "methods": len(rs), "mean": round(statistics.mean(x["ccn"] for x in rs), 2),
                       "max": max(x["ccn"] for x in rs), "nloc_cc10": share(rs, lambda x: x["ccn"] > 10),
                       "pct_long30": round(100 * sum(x["nloc"] > 30 for x in rs) / len(rs), 1),
                       "pct_p5": round(100 * sum(x["params"] >= 5 for x in rs) / len(rs), 1)})
    by_dir.sort(key=lambda d: -d["methods"])
    top = sorted(rows, key=lambda r: (-r["ccn"], -r["nloc"]))[:10]
    return {
        "methods": len(rows), "nloc": sum(r["nloc"] for r in rows),
        "mean_ccn": round(statistics.mean(ccns), 2) if ccns else 0, "median_ccn": statistics.median(ccns) if ccns else 0,
        "profile": {"low": share(rows, lambda r: r["ccn"] <= 10), "mod": share(rows, lambda r: 11 <= r["ccn"] <= 20),
                    "high": share(rows, lambda r: 21 <= r["ccn"] <= 50), "vhigh": share(rows, lambda r: r["ccn"] > 50)},
        "hist": {k: sum(1 for c in ccns if f(c)) for k, f in bands.items()},
        "methods_over_10": sum(c > 10 for c in ccns),
        "code_over_15_lines": share(rows, lambda r: r["nloc"] > 15),
        "code_over_60_lines": share(rows, lambda r: r["nloc"] > 60),
        "methods_5_params": round(100 * sum(r["params"] >= 5 for r in rows) / max(len(rows), 1), 1),
        "duplication": duplication(root, globs),
        "by_project": by_dir[:10],
        "top": [{"ccn": r["ccn"], "nloc": r["nloc"], "params": r["params"], "name": r["name"],
                 "where": f'{r["file"]}:{r["line"]}'} for r in top],
    }


def git_metrics(repo, src, exts, globs, since):
    tracked = [p for p in run(["git", "-C", repo, "ls-files", src]).splitlines()
               if (not exts or p.endswith(tuple(exts))) and not excluded(p, globs)]
    tracked_set = set(tracked)
    loc = {}
    for p in tracked:
        with open(os.path.join(repo, p), encoding="utf-8", errors="replace") as f:
            loc[p] = sum(1 for line in f if line.strip())
    raw = run(["git", "-C", repo, "log", f"--since={since}", "--no-merges", "--no-renames",
               "--format=@@%h", "--name-only", "--", src])
    commits, cur = [], None
    for line in raw.splitlines():
        if line.startswith("@@"):
            cur = set()
            commits.append(cur)
        elif line.strip() and cur is not None and line.strip() in tracked_set:
            cur.add(line.strip())
    revs = Counter(f for c in commits for f in c)
    hot = sorted(revs, key=lambda f: revs[f] * loc[f], reverse=True)[:25]
    shared = Counter()
    for c in commits:
        if len(c) <= 30:
            shared.update(itertools.combinations(sorted(c), 2))
    pairs = []
    for (a, b), s in shared.items():
        if s >= 5:
            pairs.append({"a": a, "b": b, "shared": s, "degree": round(100 * s / ((revs[a] + revs[b]) / 2))})
    pairs.sort(key=lambda p: (-p["degree"], -p["shared"]))
    total_revs = sum(revs.values()) or 1
    ordered = sorted(tracked, key=lambda f: -revs.get(f, 0))
    top10 = ordered[:max(1, len(ordered) // 10)]
    return {
        "since": since, "commits": len(commits), "files": len(tracked), "loc": sum(loc.values()),
        "files_over_1000": sum(1 for v in loc.values() if v > 1000),
        "loc_in_files_over_1000": round(100 * sum(v for v in loc.values() if v > 1000) / max(sum(loc.values()), 1), 1),
        "top10pct_files_share_of_changes": round(100 * sum(revs.get(f, 0) for f in top10) / total_revs, 1),
        "hotspots": [{"path": f, "revs": revs[f], "loc": loc[f]} for f in hot],
        "change_coupling": pairs[:15],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("src", help="source folder relative to the repo, e.g. src")
    ap.add_argument("out")
    ap.add_argument("--since", default=(date.today() - timedelta(days=365)).isoformat())
    ap.add_argument("--ext", action="append", default=[], help="file extension(s) to include, e.g. .cs")
    ap.add_argument("--exclude", action="append", default=[], help="extra glob(s) to exclude")
    a = ap.parse_args()
    globs = DEFAULT_EXCLUDES + a.exclude
    root = os.path.join(a.repo, a.src)
    rows = lizard_functions(root, a.ext, globs)
    if not rows:
        sys.exit("lizard found no functions: check the path, --ext, and that lizard is installed")
    data = {"commit": run(["git", "-C", a.repo, "rev-parse", "--short", "HEAD"]).strip(),
            "date": date.today().isoformat(),
            "quality": quality(rows, root, globs),
            "git": git_metrics(a.repo, a.src, a.ext, globs, a.since)}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    q, g = data["quality"], data["git"]
    print(f'{q["methods"]} methods, {g["files"]} files, {g["loc"]} lines, {g["commits"]} commits since {a.since} -> {a.out}')


if __name__ == "__main__":
    main()
