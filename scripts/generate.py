"""Generate the static portfolio (plain HTML + Tailwind classes). Run: python scripts/generate.py && npm run build"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from site_data import (BASE, CONCEPTS, DEAD_LINKS, EDUCATION, EXPERIENCE, GITHUB_REPOS, KEEP_POSTS,  # noqa: E402
                       PERSON, POST_EDITS, PROJECTS, REMOVED_POSTS, SKILL_GROUPS)

ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape

LINK = "text-indigo-700 underline decoration-indigo-300 underline-offset-2 hover:decoration-indigo-600 dark:text-indigo-300 dark:decoration-indigo-700"
CARD = "rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900"
CHIP = "rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-700 dark:bg-slate-800 dark:text-slate-300"
BTN = ("inline-flex items-center rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-800 "
       "hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 "
       "dark:border-slate-700 dark:text-slate-100 dark:hover:bg-slate-800")
BTN_PRIMARY = ("inline-flex items-center rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 "
               "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600")
H2 = "text-2xl font-semibold tracking-tight text-slate-900 dark:text-white"


def rel(depth: int) -> str:
    return "../" * depth


def nav(depth: int, current: str) -> str:
    r = rel(depth)
    items = [("Home", f"{r}index.html", "home"), ("Projects", f"{r}projects.html", "projects"),
             ("GitHub", f"{r}index.html#github", "github"), ("Writing", f"{r}blog/index.html", "blog"), ("Resume", f"{r}resume.html", "resume"), ("Hire me", f"{r}hire.html", "hire")]
    links = "".join(
        f'<a href="{href}" class="rounded-md px-3 py-2 text-sm font-medium hover:bg-slate-100 dark:hover:bg-slate-800 '
        f'{"text-indigo-700 dark:text-indigo-300" if key == current else "text-slate-700 dark:text-slate-300"}"'
        f'{" aria-current=\"page\"" if key == current else ""}>{label}</a>'
        for label, href, key in items)
    return (f'<header class="print:hidden sticky top-0 z-10 border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-950/90">'
            f'<div class="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-2 px-4 py-3">'
            f'<a href="{r}index.html" class="text-base font-semibold text-slate-900 dark:text-white">{E(PERSON["name"])}</a>'
            f'<nav aria-label="Main" class="flex flex-wrap items-center gap-1">{links}<a href="mailto:{PERSON["email"]}" class="ml-1 hidden rounded-lg bg-indigo-600 px-3 py-1.5 text-sm font-semibold text-white hover:bg-indigo-500 sm:inline-flex">Email me</a></nav></div></header>')


def footer(depth: int) -> str:
    r = rel(depth)
    return (f'<footer class="print:hidden border-t border-slate-200 dark:border-slate-800"><div class="mx-auto max-w-5xl px-4 py-8 text-sm text-slate-600 dark:text-slate-400">'
            f'<p>&copy; 2026 {E(PERSON["name"])}. Built with Tailwind CSS. Skill icons by <a class="{LINK}" href="https://devicon.dev">Devicon</a> (MIT).</p>'
            f'<p class="mt-2"><a class="{LINK}" href="{PERSON["github"]}">GitHub</a> &middot; <a class="{LINK}" href="{PERSON["linkedin"]}">LinkedIn</a> '
            f'&middot; <a class="{LINK}" href="{PERSON["x"]}">X</a> &middot; <a class="{LINK}" href="mailto:{PERSON["email"]}">Email</a> '
            f'&middot; <a class="{LINK}" href="{r}sitemap.xml">Sitemap</a></p></div></footer>')


def page(title: str, desc: str, path: str, body: str, *, depth: int = 0, current: str = "", og_type: str = "website",
         extra_head: str = "") -> str:
    r = rel(depth)
    url = BASE + path
    return f"""<!doctype html>
<html lang="en" class="scroll-smooth">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{E(PERSON['name'])}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f172a">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{r}assets/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="{r}assets/icon-192.png">
<link rel="manifest" href="{r}site.webmanifest">
<link rel="stylesheet" href="{r}assets/site.css">
<script defer data-domain="recscse.github.io" src="https://plausible.io/js/script.js"></script>
{extra_head}</head>
<body class="min-h-screen bg-white text-slate-800 antialiased dark:bg-slate-950 dark:text-slate-200 print:bg-white print:text-black">
<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:z-20 focus:rounded focus:bg-white focus:px-3 focus:py-2 focus:text-slate-900">Skip to content</a>
{nav(depth, current)}
<main id="main" class="mx-auto max-w-5xl px-4">
{body}
</main>
{footer(depth)}
</body>
</html>
"""


def chips(items) -> str:
    return "".join(f'<li class="{CHIP}">{E(i)}</li>' for i in items)


def ext_links(links) -> str:
    return " &middot; ".join(f'<a class="{LINK}" href="{E(u)}" rel="noopener">{E(t)}</a>' for t, u in links)


# ---- blog data ---------------------------------------------------------------------------


def load_posts() -> list[dict]:
    posts = []
    for slug in KEEP_POSTS:
        src = (ROOT / "content" / "blog" / f"{slug}.html").read_text(encoding="utf-8")
        art = re.search(r"<article[^>]*>(.*?)</article>", src, re.S)
        if not art:
            raise SystemExit(f"no <article> in {slug}")
        inner = art.group(1)
        header = re.search(r"<header[^>]*>(.*?)</header>", inner, re.S)
        h = header.group(1) if header else ""
        title = re.sub(r"<[^>]+>", "", (re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S) or re.search(r"<h1[^>]*>(.*?)</h1>", inner, re.S)).group(1)).strip()
        meta = [re.sub(r"<[^>]+>", "", m).strip() for m in re.findall(r"<span[^>]*>(.*?)</span>", re.search(r'post-meta[^>]*>(.*?)</div>', h, re.S).group(1) if re.search(r'post-meta', h) else "", re.S)]
        meta = [m for m in meta if m and m not in ("·", "•", "|", "-", "�") and len(m) > 2]
        tags = [re.sub(r"<[^>]+>", "", t).strip() for t in re.findall(r'<span class="tag[^"]*">(.*?)</span>', h, re.S)]
        body = inner.replace(header.group(0), "") if header else inner
        for s, old, new in POST_EDITS:
            if s == slug:
                if old not in body:
                    raise SystemExit(f"edit target not found in {slug}: {old[:40]}")
                body = body.replace(old, new)
        # Drop list items that link to removed posts or to dead URLs.
        for gone in [f"{s}.html" for s in REMOVED_POSTS] + DEAD_LINKS:
            body = re.sub(r'\s*<li>\s*<a href="' + re.escape(gone) + r'"[^>]*>.*?</a>\s*</li>', "", body, flags=re.S)
        body = re.sub(r'\s+target="_blank"', '', body)  # links open in the same tab
        lead = re.search(r"<p[^>]*>(.*?)</p>", body, re.S)
        excerpt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", lead.group(1))).strip() if lead else ""
        date = meta[0] if meta else ""
        posts.append({"slug": slug, "title": title, "date": date, "read": meta[1] if len(meta) > 1 else "", "tags": tags,
                      "body": body, "excerpt": excerpt[:200]})
    from datetime import datetime

    def key(p):
        for fmt in ("%b %d, %Y", "%B %d, %Y"):
            try:
                return datetime.strptime(p["date"], fmt)
            except ValueError:
                pass
        return datetime.min
    return sorted(posts, key=key, reverse=True)


POSTS = load_posts()
POST_BY_SLUG = {p["slug"]: p for p in POSTS}


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


# ---- pages -------------------------------------------------------------------------------


def arch_svg(uid: str) -> str:
    """Growth Quantix market-data pipeline, simplified from the architecture write-up (which matches the code)."""
    def node(x, y, title):
        return (f'<rect x="{x}" y="{y}" width="204" height="76" rx="14" class="fill-white stroke-indigo-300 dark:fill-slate-900 dark:stroke-indigo-700" stroke-width="3"/>'
                f'<text x="{x + 102}" y="{y + 49}" text-anchor="middle" font-size="27" font-weight="700" class="fill-slate-900 dark:fill-slate-100">{E(title)}</text>')

    def edge(x1, y1, x2, y2):
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="stroke-slate-400 dark:stroke-slate-500" stroke-width="4" marker-end="url(#arrow-{uid})"/>'

    return (f'<svg viewBox="0 0 960 440" role="img" aria-labelledby="arch-{uid}" class="h-full w-full">'
            f'<title id="arch-{uid}">Growth Quantix market-data pipeline: broker WebSocket feed, FastAPI ingestion, Redis Pub/Sub, then the strategy engine, paper-trading tracker and the live dashboard</title>'
            f'<defs><marker id="arrow-{uid}" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="fill-slate-400 dark:fill-slate-500"/></marker></defs>'
            + node(6, 182, "Broker feed") + node(256, 182, "FastAPI") + node(506, 182, "Redis Pub/Sub")
            + node(750, 30, "Strategies") + node(750, 182, "Paper trading") + node(750, 334, "Live dashboard")
            + edge(212, 220, 252, 220) + edge(462, 220, 502, 220)
            + edge(714, 200, 746, 100) + edge(714, 220, 746, 220) + edge(714, 240, 746, 356) + '</svg>')


def media(p: dict, uid: str) -> str:
    img = p.get("image")
    if img:
        src, w, h, alt = img
        return f'<img src="{src}" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy" class="h-full w-full object-cover object-top">'
    if p["slug"] == "growth-quantix":
        return f'<div class="flex h-full w-full items-center bg-slate-50 p-3 dark:bg-slate-950">{arch_svg(uid)}</div>'
    return ""


def _gh() -> dict:
    return load_github() or {}


def pypi_version() -> str:
    return (_gh().get("pypi") or {}).get("upstox-auth-pro", {}).get("version", "1.1.3")


def live(text: str) -> str:
    return text.replace("{PYPI_VERSION}", pypi_version())


def live_stats(p: dict) -> str:
    """One line of live GitHub facts for a project (stars, commits by you, last update), from data/github.json."""
    gh = _gh()
    feat = {r["full_name"]: r for r in gh.get("repos", [])}
    own = gh.get("own_repos") or {}
    stars = commits = 0
    pushed = ""
    for name in p.get("repos", []):
        r = feat.get(name) or own.get(name)
        if not r:
            continue
        stars += r.get("stars", 0)
        commits += r.get("my_commits") or 0
        pushed = max(pushed, r.get("pushed_at", ""))
    bits = []
    if commits:
        bits.append(f"{commits:,} commits by me")
    if stars:
        bits.append(f"{stars} star{'s' if stars != 1 else ''}")
    if pushed:
        bits.append(f"updated {pushed}")
    if p["slug"] == "upstox-auth-pro":
        v = (gh.get("pypi") or {}).get("upstox-auth-pro")
        if v:
            bits.insert(0, f"PyPI v{v['version']}")
    return " · ".join(bits)


def project_card(p: dict, href_prefix: str = "") -> str:
    m = media(p, "home") if p.get("featured") else ""
    top = f'<div class="aspect-[2/1] overflow-hidden border-b border-slate-200 dark:border-slate-800">{m}</div>' if m else ""
    return (f'<article class="flex flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-0.5 hover:shadow-md dark:border-slate-800 dark:bg-slate-900">{top}'
            f'<div class="flex flex-1 flex-col p-6"><div class="flex items-start justify-between gap-3">'
            f'<h3 class="text-lg font-semibold text-slate-900 dark:text-white"><a class="hover:underline" href="{href_prefix}projects.html#{p["slug"]}">{E(p["name"])}</a></h3>'
            f'<span class="{CHIP} shrink-0">{E(p["status"])}</span></div>'
            f'<p class="mt-2 text-sm text-slate-600 dark:text-slate-400">{E(p["tagline"])}</p>'
            f'<ul class="mt-4 flex flex-wrap gap-1.5" aria-label="Technologies">{chips(p["stack"])}</ul>'
            f'<p class="mt-auto pt-5 text-sm">{ext_links(p["links"])}</p>'
            f'{("<p class=\"mt-2 text-xs text-slate-500 dark:text-slate-400\">" + E(live_stats(p)) + "</p>") if live_stats(p) else ""}</div></article>')


def skill_group(name: str, items) -> str:
    pills = []
    for label, icon in items:
        ic = (f'<span class="flex h-6 w-6 items-center justify-center rounded-full bg-white ring-1 ring-slate-200">'
              f'<img src="assets/icons/{icon}.svg" alt="" width="16" height="16" loading="lazy" class="max-h-4 w-auto"></span>') if icon else ""
        pills.append(f'<li class="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white py-1 pr-3 text-sm text-slate-800 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-200 {"pl-1" if icon else "pl-3"}">{ic}{E(label)}</li>')
    return (f'<div class="grid gap-3 sm:grid-cols-[11rem_1fr] sm:items-start"><h3 class="pt-1 text-sm font-semibold text-slate-500 dark:text-slate-400">{E(name)}</h3>'
            f'<ul class="flex flex-wrap gap-2">{"".join(pills)}</ul></div>')


EYEBROW = "text-sm font-semibold uppercase tracking-wide text-indigo-700 dark:text-indigo-300"
BTN_LIGHT = ("inline-flex items-center rounded-lg bg-white px-4 py-2 text-sm font-semibold text-slate-900 hover:bg-slate-100 "
             "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white")
BTN_GHOST = ("inline-flex items-center rounded-lg border border-slate-600 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 "
             "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white")


NON_PROGRAMMING = {"HTML", "CSS", "SCSS", "Less", "Shell", "PowerShell", "Batchfile", "Makefile", "Dockerfile", "Jupyter Notebook"}
LANG_BG = {"Python": "bg-sky-500", "JavaScript": "bg-amber-400", "Go": "bg-teal-500", "Java": "bg-orange-500",
           "TypeScript": "bg-blue-600", "Rust": "bg-red-500", "C++": "bg-pink-500", "Kotlin": "bg-violet-500"}


def load_github() -> dict | None:
    f = ROOT / "data" / "github.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def heatmap_svg(days: list[dict]) -> str:
    """GitHub-style contribution calendar drawn from the real per-day counts (no third-party widget)."""
    import datetime as dt
    step, left, top = 15, 30, 20
    first = dt.date.fromisoformat(days[0]["date"])
    start_col_offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday
    cells, labels, last_month = [], [], None
    fills = ["fill-slate-100 dark:fill-slate-800", "fill-emerald-200 dark:fill-emerald-900", "fill-emerald-300 dark:fill-emerald-700",
             "fill-emerald-500 dark:fill-emerald-500", "fill-emerald-700 dark:fill-emerald-300"]
    for i, d in enumerate(days):
        date = dt.date.fromisoformat(d["date"])
        pos = i + start_col_offset
        col, row = pos // 7, pos % 7
        x, y = left + col * step, top + row * step
        when = date.strftime("%b %d, %Y").replace(" 0", " ")
        n = d["count"]
        cells.append(f'<rect x="{x}" y="{y}" width="12" height="12" rx="2" class="{fills[d["level"]]}"><title>{n} contribution{"s" if n != 1 else ""} on {when}</title></rect>')
        if row == 0 and date.month != last_month and (not labels or x - labels[-1][0] > 40):
            labels.append((x, date.strftime("%b")))
            last_month = date.month
    cols = (len(days) + start_col_offset + 6) // 7
    width, height = left + cols * step, top + 7 * step
    month_txt = "".join(f'<text x="{x}" y="12" font-size="11" class="fill-slate-500 dark:fill-slate-400">{m}</text>' for x, m in labels)
    day_txt = "".join(f'<text x="0" y="{top + r * step + 10}" font-size="10" class="fill-slate-500 dark:fill-slate-400">{t}</text>' for r, t in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
    total = sum(d["count"] for d in days)
    return (f'<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="gh-cal" class="h-auto w-full min-w-[760px]">'
            f'<title id="gh-cal">GitHub contribution calendar for the last year: {total} contributions</title>{month_txt}{day_txt}{"".join(cells)}</svg>')


def language_bar(repos: list[dict]) -> str:
    totals: dict[str, int] = {}
    for r in repos:
        for k, v in r["languages"].items():
            if k not in NON_PROGRAMMING:
                totals[k] = totals.get(k, 0) + v
    whole = sum(totals.values()) or 1
    top = [(k, v) for k, v in sorted(totals.items(), key=lambda kv: -kv[1])[:6] if 100 * v / whole >= 1]
    other = whole - sum(v for _, v in top)
    parts = [(k, 100 * v / whole) for k, v in top] + ([("Other", 100 * other / whole)] if other > 0.5 * whole / 100 else [])
    bar = "".join(f'<span class="{LANG_BG.get(k, "bg-slate-400")} h-full" style="width:{p:.2f}%" title="{E(k)} {p:.1f}%"></span>' for k, p in parts)
    legend = "".join(f'<li class="inline-flex items-center gap-1.5 text-sm"><span class="h-2.5 w-2.5 rounded-full {LANG_BG.get(k, "bg-slate-400")}" aria-hidden="true"></span>{E(k)} <span class="text-slate-500 dark:text-slate-400">{p:.0f}%</span></li>' for k, p in parts)
    return (f'<div class="flex h-3 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800" role="img" aria-label="Language share across the featured repositories">{bar}</div>'
            f'<ul class="mt-3 flex flex-wrap gap-x-5 gap-y-1">{legend}</ul>')


def github_section() -> str:
    gh = load_github()
    if not gh or not gh.get("contributions"):
        return ""
    c, prof = gh["contributions"], gh["profile"]
    stats = [(f"{c['total_last_year']:,}", "contributions in the last year"), (str(prof["public_repos"]), "public repositories"),
             (str(prof["followers"]), "followers"), (prof["since"], "on GitHub since")]
    stat_html = "".join(f'<div class="{CARD} !p-4"><dt class="text-2xl font-semibold text-slate-900 dark:text-white">{E(a)}</dt><dd class="text-sm text-slate-600 dark:text-slate-400">{E(b)}</dd></div>' for a, b in stats)
    cards = []
    for r in gh["repos"]:
        desc, chips_ = GITHUB_REPOS.get(r["full_name"], (r["description"], []))
        meta = []
        if r["stars"]:
            meta.append(f'{r["stars"]} star{"s" if r["stars"] != 1 else ""}')
        if r["my_commits"]:
            meta.append(f'{r["my_commits"]:,} commits by me')
        meta.append(f'updated {r["pushed_at"]}')
        cards.append(f'<article class="{CARD} !p-5"><h3 class="font-semibold"><a class="{LINK}" href="{E(r["url"])}">{E(r["full_name"])}</a></h3>'
                     f'<p class="mt-1 text-sm text-slate-600 dark:text-slate-400">{E(desc)}</p><ul class="mt-3 flex flex-wrap gap-1.5">{chips(chips_)}</ul>'
                     f'<p class="mt-3 text-xs text-slate-500 dark:text-slate-400">{E(" · ".join(meta))}</p></article>')
    return f"""
<section id="github" class="py-10" aria-labelledby="github-h">
  <p class="{EYEBROW}">GitHub</p>
  <div class="flex items-baseline justify-between"><h2 id="github-h" class="mt-1 {H2}">Open-source activity</h2><a class="text-sm {LINK}" href="{PERSON['github']}">View profile</a></div>
  <dl class="mt-6 grid grid-cols-2 gap-3 lg:grid-cols-4">{stat_html}</dl>
  <div class="{CARD} mt-4"><h3 class="text-sm font-semibold text-slate-600 dark:text-slate-300">Contribution calendar</h3>
    <div class="mt-3 overflow-x-auto">{heatmap_svg(c['days'])}</div>
    <p class="mt-2 text-xs text-slate-500 dark:text-slate-400">Contributions as counted by GitHub (commits, pull requests, issues and reviews), fetched {E(gh['generated_at'])}.</p></div>
  <div class="{CARD} mt-4"><h3 class="text-sm font-semibold text-slate-600 dark:text-slate-300">Languages in the featured repositories</h3>
    <div class="mt-3">{language_bar(gh['repos'])}</div>
    <p class="mt-3 text-xs text-slate-500 dark:text-slate-400">Programming languages only, as measured by GitHub across the repositories below. HTML, CSS and shell scripts are left out.</p></div>
  <h3 class="mt-8 text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Featured repositories</h3>
  <div class="mt-3 grid gap-4 md:grid-cols-2">{''.join(cards)}</div>
</section>
"""


def index_page() -> str:
    exp = EXPERIENCE[0]
    ld = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": BASE + "#person",
        "name": PERSON["name"],
        "url": BASE + "index.html",
        "description": PERSON["summary"],
        "jobTitle": PERSON["title"],
        "email": f"mailto:{PERSON['email']}",
        "worksFor": {"@type": "Organization", "name": exp["company"]},
        "sameAs": [PERSON["github"], PERSON["linkedin"]],
        "knowsAbout": [
            "Java", "Spring Boot", "Python", "FastAPI", "Backend Engineering",
            "System Design", "Algorithmic Trading", "AI Developer Tools"
        ]
    }
    featured = [p for p in PROJECTS if p.get("featured")]
    more = [p for p in PROJECTS if not p.get("featured")]
    proof = [("5+ years", "Java and Python backends"), ("Growth Quantix", "public trading-platform repo"),
             ("codive", "MCP server written in Go"), ("upstox-auth-pro", f"SDK on PyPI, v{pypi_version()}")]
    proof_html = "".join(f'<div class="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"><dt class="text-lg font-semibold text-slate-900 dark:text-white">{E(a)}</dt><dd class="text-sm text-slate-600 dark:text-slate-400">{E(b)}</dd></div>' for a, b in proof)
    body = f"""
<section class="pt-8 sm:pt-12" aria-labelledby="hero">
  <div class="rounded-3xl bg-gradient-to-br from-indigo-50 via-white to-sky-50 p-8 ring-1 ring-slate-200 sm:p-12 dark:from-slate-900 dark:via-slate-950 dark:to-indigo-950/40 dark:ring-slate-800">
    <p class="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-800 ring-1 ring-emerald-200 dark:bg-emerald-950/50 dark:text-emerald-300 dark:ring-emerald-900"><span class="h-2 w-2 rounded-full bg-emerald-500" aria-hidden="true"></span>{E(PERSON['open'])}</p>
    <p class="mt-5 text-base font-medium text-slate-600 dark:text-slate-400">{E(PERSON['name'])} &middot; {E(PERSON['title'])} &middot; {E(PERSON['location'])}</p>
    <h1 id="hero" class="mt-2 max-w-3xl text-3xl font-bold tracking-tight text-slate-900 sm:text-5xl dark:text-white">{E(PERSON['name'])}</h1>
    <p class="mt-3 max-w-3xl text-lg font-semibold text-slate-700 dark:text-slate-300">{E(PERSON['headline'])}</p>
    <p class="mt-3 max-w-2xl text-lg text-slate-600 dark:text-slate-300">{E(PERSON['hero_sub'])}</p>
    <div class="mt-8 flex flex-wrap gap-3">
      <a class="{BTN_PRIMARY}" href="mailto:{PERSON['email']}">Email me</a>
      <a class="{BTN}" href="projects.html">See my work</a>
      <a class="{BTN}" href="assets/Brijesh_Yadav_Resume.pdf">Resume (PDF)</a>
    </div>
  </div>
  <dl class="mt-4 grid grid-cols-2 gap-3 lg:grid-cols-4">{proof_html}</dl>
</section>

<section id="projects" class="py-14" aria-labelledby="projects-h">
  <p class="{EYEBROW}">Selected work</p>
  <div class="flex items-baseline justify-between"><h2 id="projects-h" class="mt-1 {H2}">Things I have built</h2><a class="text-sm {LINK}" href="projects.html">Details</a></div>
  <div class="mt-6 grid gap-6 md:grid-cols-2">{''.join(project_card(p) for p in featured)}</div>
  <div class="mt-6 grid gap-6 md:grid-cols-2">{''.join(project_card(p) for p in more)}</div>
</section>

{github_section()}
<section id="experience" class="py-10" aria-labelledby="experience-h"><p class="{EYEBROW}">Experience</p><h2 id="experience-h" class="mt-1 {H2}">Where I work</h2>
  <div class="{CARD} mt-6"><div class="flex flex-wrap items-baseline justify-between gap-2">
    <h3 class="text-lg font-semibold text-slate-900 dark:text-white">{E(exp['role'])}, {E(exp['company'])}</h3>
    <p class="text-sm text-slate-500 dark:text-slate-400">{E(exp['period'])}</p></div>
    <ul class="mt-4 list-disc space-y-2 pl-5 text-slate-700 dark:text-slate-300">{''.join(f'<li>{E(b)}</li>' for b in exp['bullets'])}</ul>
    <div class="mt-6 border-t border-slate-200 pt-4 text-sm text-slate-600 dark:border-slate-800 dark:text-slate-400"><span class="font-semibold text-slate-800 dark:text-slate-200">{E(EDUCATION['school'])}</span> &middot; {E(EDUCATION['degree'])} &middot; {E(EDUCATION['period'])} &middot; CGPA {E(EDUCATION['cgpa'])}<br>{E(EDUCATION['extra'])}</div></div>
</section>

<section id="skills" class="py-10" aria-labelledby="skills-h"><p class="{EYEBROW}">Skills</p><h2 id="skills-h" class="mt-1 {H2}">What I work with</h2>
  <div class="mt-6 space-y-4">{''.join(skill_group(n, i) for n, i in SKILL_GROUPS)}
  <div class="grid gap-3 sm:grid-cols-[11rem_1fr] sm:items-start"><h3 class="pt-1 text-sm font-semibold text-slate-500 dark:text-slate-400">Concepts</h3><ul class="flex flex-wrap gap-2">{chips(CONCEPTS)}</ul></div></div>
  <p class="mt-5 text-sm text-slate-600 dark:text-slate-400">Currently learning: Kubernetes and system design patterns.</p>
</section>

<section id="writing" class="py-10" aria-labelledby="writing-h">
  <p class="{EYEBROW}">Writing</p><div class="flex items-baseline justify-between"><h2 id="writing-h" class="mt-1 {H2}">Engineering notes</h2><a class="text-sm {LINK}" href="blog/index.html">All posts</a></div>
  <div class="mt-6 grid gap-4 md:grid-cols-3">{''.join(f'<a class="{CARD} block transition hover:-translate-y-0.5 hover:shadow-md" href="blog/{p["slug"]}.html"><p class="text-xs text-slate-500 dark:text-slate-400">{E(p["date"])}</p><h3 class="mt-2 font-semibold text-slate-900 dark:text-white">{E(p["title"])}</h3></a>' for p in POSTS[:3])}</div>
</section>

<section id="contact" class="py-10 pb-20" aria-labelledby="contact-h">
  <div class="rounded-3xl bg-slate-900 p-8 text-white sm:p-12 dark:bg-slate-900 dark:ring-1 dark:ring-slate-800">
    <h2 id="contact-h" class="text-2xl font-semibold tracking-tight sm:text-3xl">Let's talk</h2>
    <p class="mt-3 max-w-xl text-slate-300">{E(PERSON['open'])}. {E(PERSON['available'])} Email is the quickest way to reach me.</p>
    <div class="mt-6 flex flex-wrap gap-3"><a class="{BTN_LIGHT}" href="mailto:{PERSON['email']}">{E(PERSON['email'])}</a>
      <a class="{BTN_GHOST}" href="{PERSON['linkedin']}">LinkedIn</a><a class="{BTN_GHOST}" href="{PERSON['github']}">GitHub</a><a class="{BTN_GHOST}" href="{PERSON['x']}">X</a></div>
  </div>
</section>
"""
    head = f'<script type="application/ld+json">{json.dumps(ld)}</script>\n'
    return page(f"{PERSON['name']} | {PERSON['title']}",
                "Backend software engineer (Java, Spring Boot, Python, FastAPI) building trading infrastructure, developer tools for AI agents and an Android wellbeing app.",
                "index.html", body, current="home", extra_head=head)


def projects_page() -> str:
    secs = []
    for p in PROJECTS:
        writing = "".join(f'<li><a class="{LINK}" href="blog/{s}.html">{E(POST_BY_SLUG[s]["title"])}</a></li>' for s in p["writing"] if s in POST_BY_SLUG)
        m = media(p, "proj") if p.get("featured") else ""
        visual = f'<div class="aspect-[2/1] overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800">{m}</div>' if m else ""
        text = f"""<div class="flex flex-wrap items-center gap-3"><h2 id="{p['slug']}-h" class="{H2}">{E(p['name'])}</h2><span class="{CHIP}">{E(p['status'])}</span></div>
  <p class="mt-1 text-slate-600 dark:text-slate-400">{E(p['tagline'])}</p>
  <ul class="mt-4 list-disc space-y-2 pl-5 text-slate-700 dark:text-slate-300">{''.join(f'<li>{E(live(b))}</li>' for b in p['bullets'])}</ul>
  <ul class="mt-4 flex flex-wrap gap-1.5" aria-label="Technologies">{chips(p['stack'])}</ul>
  <p class="mt-4 text-sm">{ext_links(p['links'])}</p>
  {('<p class="mt-2 text-xs text-slate-500 dark:text-slate-400">' + E(live_stats(p)) + '</p>') if live_stats(p) else ''}
  {f'<div class="mt-4"><h3 class="text-sm font-semibold text-slate-500 dark:text-slate-400">Related writing</h3><ul class="mt-1 list-disc pl-5 text-sm">{writing}</ul></div>' if writing else ''}"""
        layout = f'<div class="grid gap-8 lg:grid-cols-2 lg:items-start"><div>{text}</div>{visual}</div>' if visual else f'<div class="max-w-3xl">{text}</div>'
        secs.append(f'<section id="{p["slug"]}" class="border-b border-slate-200 py-10 dark:border-slate-800" aria-labelledby="{p["slug"]}-h">{layout}</section>')
    body = (f'<div class="py-12"><h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Projects</h1>'
            f'<p class="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">Each project links to its live site, package or source code so the details can be checked.</p></div>'
            + "".join(secs) + '<div class="pb-16"></div>')
    return page(f"Projects | {PERSON['name']}", "Growth Quantix, Graylane, Prindox, codive, Upstox Auth Pro and HSCI: what each does, the stack, and where to verify it.",
                "projects.html", body, current="projects")


def hire_page() -> str:
    services = [
        ("Backend APIs and services", "REST APIs and microservices in Python (FastAPI) or Java (Spring Boot) with PostgreSQL, MySQL or MongoDB."),
        ("Real-time data pipelines", "WebSocket ingestion, Redis caching and Pub/Sub fan-out, with reconnection and back-pressure handled."),
        ("SDKs and automation", "Authentication flows, browser automation with Playwright, packaged and published with CI release workflows."),
        ("AI developer tooling", "MCP servers and local-first tools that give AI coding agents structured access to code and data."),
    ]
    cards = "".join(f'<div class="{CARD}"><h3 class="font-semibold text-slate-900 dark:text-white">{E(t)}</h3><p class="mt-2 text-sm text-slate-600 dark:text-slate-400">{E(d)}</p></div>' for t, d in services)
    body = f"""<div class="py-12"><h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Hire me</h1>
<p class="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">{E(PERSON['available'])} Here is the kind of work I can take on, all based on things I have built (see <a class="{LINK}" href="projects.html">projects</a>).</p></div>
<div class="grid gap-5 sm:grid-cols-2">{cards}</div>
<div class="py-12"><p class="text-slate-700 dark:text-slate-300">Send a short description of the problem, the timeline, and anything I should read first.</p>
<p class="mt-4"><a class="{BTN_PRIMARY}" href="mailto:{PERSON['email']}?subject=Project%20enquiry">Email me</a> <a class="{BTN}" href="{PERSON['linkedin']}" rel="noopener">LinkedIn</a></p></div>"""
    return page(f"Hire me | {PERSON['name']}", "Freelance and contract backend work: APIs, real-time data pipelines, SDKs and AI developer tooling.",
                "hire.html", body, current="hire")


def resume_page() -> str:
    exp = EXPERIENCE[0]
    proj = "".join(f'<div class="mt-4 break-inside-avoid"><h3 class="font-semibold text-slate-900 dark:text-white print:text-black">{E(p["name"])} <span class="font-normal text-slate-500">- {E(p["tagline"])}</span></h3>'
                   f'<ul class="mt-1 list-disc space-y-1 pl-5 text-sm">{"".join(f"<li>{E(live(b))}</li>" for b in p["bullets"][:3])}</ul>'
                   f'<p class="mt-1 text-xs text-slate-500">{E(", ".join(p["stack"]))}</p></div>' for p in PROJECTS if p.get('resume'))
    skills = "".join(f'<p class="text-sm"><span class="font-semibold">{E(n)}:</span> {E(", ".join(l for l, _ in i))}</p>' for n, i in SKILL_GROUPS)
    body = f"""<div class="py-10 print:py-0"><div class="flex flex-wrap items-baseline justify-between gap-2 print:hidden"><h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Resume</h1>
<p class="text-sm"><a class="{LINK}" href="assets/Brijesh_Yadav_Resume.pdf">Download PDF</a></p></div>
<div class="{CARD} mt-6 print:border-0 print:p-0 print:shadow-none">
<h2 class="text-2xl font-bold text-slate-900 dark:text-white print:text-black">{E(PERSON['name'])}</h2>
<p class="text-slate-600 dark:text-slate-300">{E(PERSON['title'])} &middot; {E(PERSON['location'])} &middot; {E(PERSON['email'])}</p>
<p class="text-sm text-slate-500">{PERSON['github'].replace('https://', '')} &middot; {PERSON['linkedin'].replace('https://www.', '')}</p>
<h3 class="mt-6 border-b border-slate-300 pb-1 text-sm font-bold uppercase tracking-wide">Summary</h3><p class="mt-2 text-sm">{E(PERSON['summary'])}</p>
<h3 class="mt-6 border-b border-slate-300 pb-1 text-sm font-bold uppercase tracking-wide">Skills</h3><div class="mt-2 space-y-1">{skills}<p class="text-sm"><span class="font-semibold">Concepts:</span> {E(", ".join(CONCEPTS))}</p></div>
<h3 class="mt-6 border-b border-slate-300 pb-1 text-sm font-bold uppercase tracking-wide">Experience</h3>
<div class="mt-2"><p class="font-semibold">{E(exp['role'])}, {E(exp['company'])} <span class="font-normal text-slate-500">&middot; {E(exp['period'])}</span></p>
<ul class="mt-1 list-disc space-y-1 pl-5 text-sm">{''.join(f'<li>{E(b)}</li>' for b in exp['bullets'])}</ul></div>
<h3 class="mt-6 border-b border-slate-300 pb-1 text-sm font-bold uppercase tracking-wide">Projects</h3>{proj}
<h3 class="mt-6 border-b border-slate-300 pb-1 text-sm font-bold uppercase tracking-wide">Education</h3>
<p class="mt-2 text-sm"><span class="font-semibold">{E(EDUCATION['school'])}</span> &middot; {E(EDUCATION['degree'])} &middot; {E(EDUCATION['period'])} &middot; CGPA {E(EDUCATION['cgpa'])}</p>
<p class="text-sm text-slate-600">{E(EDUCATION['extra'])}</p></div></div>"""
    return page(f"Resume | {PERSON['name']}", "Resume of Brijesh Yadav, backend software engineer.", "resume.html", body, current="resume")


def blog_index() -> str:
    items = "".join(
        f'<li class="py-5"><a class="text-lg font-semibold text-slate-900 hover:underline dark:text-white" href="{p["slug"]}.html">{E(p["title"])}</a>'
        f'<p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{E(p["date"])}{" &middot; " + E(p["read"]) if p["read"] else ""}</p>'
        f'<p class="mt-2 text-slate-600 dark:text-slate-300">{E(p["excerpt"])}</p>'
        f'<ul class="mt-2 flex flex-wrap gap-1.5">{chips(p["tags"])}</ul></li>' for p in POSTS)
    body = (f'<div class="py-12"><h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Writing</h1>'
            f'<p class="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">Engineering notes about systems I have built. The technical details match the public source code linked from each project.</p></div>'
            f'<ul class="divide-y divide-slate-200 pb-16 dark:divide-slate-800">{items}</ul>')
    return page(f"Writing | {PERSON['name']}", "Engineering notes on trading infrastructure, OAuth2 automation, risk management and AI system design.",
                "blog/index.html", body, depth=1, current="blog")


def blog_post_schema(p: dict) -> str:
    """Build structured data for an article from the same metadata shown on the page."""
    from datetime import datetime

    article_url = BASE + f"blog/{p['slug']}.html"
    article = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": article_url + "#article",
        "headline": p["title"],
        "description": p["excerpt"] or p["title"],
        "url": article_url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": article_url},
        "author": {"@id": BASE + "#person"},
        "image": BASE + "assets/og.png",
        "keywords": p["tags"]
    }

    for date_format in ("%b %d, %Y", "%B %d, %Y"):
        try:
            article["datePublished"] = datetime.strptime(
                p["date"], date_format
            ).date().isoformat()
            break
        except ValueError:
            continue

    return '<script type="application/ld+json">' + json.dumps(article) + '</script>\\n'


def blog_post(p: dict) -> str:
    body = (f'<article class="mx-auto max-w-3xl py-12"><p class="text-sm"><a class="{LINK}" href="index.html">&larr; All posts</a></p>'
            f'<h1 class="mt-4 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl dark:text-white">{E(p["title"])}</h1>'
            f'<p class="mt-3 text-sm text-slate-500 dark:text-slate-400">{E(p["date"])}{" &middot; " + E(p["read"]) if p["read"] else ""}</p>'
            f'<ul class="mt-3 flex flex-wrap gap-1.5">{chips(p["tags"])}</ul>'
            f'<div class="post prose prose-slate mt-8 max-w-none dark:prose-invert prose-pre:overflow-x-auto prose-img:rounded-lg">{p["body"]}</div>'
            f'<p class="mt-12 border-t border-slate-200 pt-6 text-sm dark:border-slate-800"><a class="{LINK}" href="index.html">&larr; All posts</a> &middot; <a class="{LINK}" href="../projects.html">Projects</a></p></article>')
    # Diagrams are Mermaid text blocks. Load a PINNED Mermaid build (strict security) only on pages that have them.
    mermaid = ""
    if 'class="mermaid"' in p["body"]:
        mermaid = ('<script type="module">\n'
                   'import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";\n'
                   'const dark = window.matchMedia("(prefers-color-scheme: dark)").matches;\n'
                   'mermaid.initialize({ startOnLoad: true, securityLevel: "strict", theme: dark ? "dark" : "default" });\n'
                   '</script>\n')
    schema = blog_post_schema(p)
    return page(f"{p['title']} | {PERSON['name']}", p["excerpt"] or p["title"], f"blog/{p['slug']}.html", body, depth=1,
                current="blog", og_type="article", extra_head=mermaid + schema)


def not_found() -> str:
    body = (f'<div class="py-24 text-center"><p class="text-sm font-medium text-indigo-700 dark:text-indigo-300">404</p>'
            f'<h1 class="mt-2 text-3xl font-bold text-slate-900 dark:text-white">Page not found</h1>'
            f'<p class="mt-3 text-slate-600 dark:text-slate-300">That page does not exist.</p>'
            f'<p class="mt-6"><a class="{BTN_PRIMARY}" href="{BASE}index.html">Go to the home page</a></p></div>')
    return page(f"Page not found | {PERSON['name']}", "Page not found.", "404.html", body)


def sitemap() -> str:
    urls = ["index.html", "projects.html", "resume.html", "hire.html", "blog/index.html"] + [f"blog/{p['slug']}.html" for p in POSTS]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")


def manifest() -> str:
    return json.dumps({
        "name": f"{PERSON['name']} - Portfolio", "short_name": "Brijesh Yadav", "description": PERSON["title"],
        "start_url": "./index.html", "scope": "./", "display": "standalone", "background_color": "#0f172a", "theme_color": "#0f172a",
        "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "assets/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, indent=2) + "\n"


def main() -> None:
    write("index.html", index_page())
    write("projects.html", projects_page())
    write("hire.html", hire_page())
    write("resume.html", resume_page())
    write("404.html", not_found())
    write("blog/index.html", blog_index())
    for p in POSTS:
        write(f"blog/{p['slug']}.html", blog_post(p))
    write("sitemap.xml", sitemap())
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    write("site.webmanifest", manifest())
    print(f"generated {7 + len(POSTS)} pages for {len(POSTS)} posts")


if __name__ == "__main__":
    main()
