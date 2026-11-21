"""Generate the static portfolio (plain HTML + Tailwind classes). Run: python scripts/generate.py && npm run build"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from site_data import (BASE, CONCEPTS, DEAD_LINKS, EDUCATION, EXPERIENCE, KEEP_POSTS, PERSON,  # noqa: E402
                       POST_EDITS, PROJECTS, REMOVED_POSTS, SKILL_GROUPS)

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
             ("Writing", f"{r}blog/index.html", "blog"), ("Resume", f"{r}resume.html", "resume"), ("Hire me", f"{r}hire.html", "hire")]
    links = "".join(
        f'<a href="{href}" class="rounded-md px-3 py-2 text-sm font-medium hover:bg-slate-100 dark:hover:bg-slate-800 '
        f'{"text-indigo-700 dark:text-indigo-300" if key == current else "text-slate-700 dark:text-slate-300"}"'
        f'{" aria-current=\"page\"" if key == current else ""}>{label}</a>'
        for label, href, key in items)
    return (f'<header class="sticky top-0 z-10 border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-950/90">'
            f'<div class="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-2 px-4 py-3">'
            f'<a href="{r}index.html" class="text-base font-semibold text-slate-900 dark:text-white">{E(PERSON["name"])}</a>'
            f'<nav aria-label="Main" class="flex flex-wrap gap-1">{links}</nav></div></header>')


def footer(depth: int) -> str:
    r = rel(depth)
    return (f'<footer class="border-t border-slate-200 dark:border-slate-800"><div class="mx-auto max-w-5xl px-4 py-8 text-sm text-slate-600 dark:text-slate-400">'
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


def project_card(p: dict) -> str:
    return (f'<article class="{CARD} flex flex-col"><div class="flex items-start justify-between gap-3">'
            f'<h3 class="text-lg font-semibold text-slate-900 dark:text-white"><a class="hover:underline" href="projects.html#{p["slug"]}">{E(p["name"])}</a></h3>'
            f'<span class="{CHIP} shrink-0">{E(p["status"])}</span></div>'
            f'<p class="mt-2 text-sm text-slate-600 dark:text-slate-400">{E(p["tagline"])}</p>'
            f'<ul class="mt-4 flex flex-wrap gap-1.5" aria-label="Technologies">{chips(p["stack"])}</ul>'
            f'<p class="mt-auto pt-4 text-sm">{ext_links(p["links"])}</p></article>')


def skill_group(name: str, items) -> str:
    tiles = []
    for label, icon in items:
        img = (f'<span class="flex h-9 w-9 items-center justify-center rounded-md bg-white p-1.5 ring-1 ring-slate-200">'
               f'<img src="assets/icons/{icon}.svg" alt="" width="24" height="24" loading="lazy" class="max-h-6 w-auto"></span>') if icon else \
              '<span class="flex h-9 w-9 items-center justify-center rounded-md bg-slate-100 text-xs font-bold text-slate-600 dark:bg-slate-800 dark:text-slate-300">SQL</span>'
        tiles.append(f'<li class="flex items-center gap-2.5 text-sm">{img}<span>{E(label)}</span></li>')
    return (f'<div><h3 class="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">{E(name)}</h3>'
            f'<ul class="mt-3 grid grid-cols-1 gap-3">{"".join(tiles)}</ul></div>')


def index_page() -> str:
    exp = EXPERIENCE[0]
    ld = {"@context": "https://schema.org", "@type": "Person", "name": PERSON["name"], "jobTitle": PERSON["title"],
          "url": BASE, "email": f"mailto:{PERSON['email']}", "address": {"@type": "PostalAddress", "addressLocality": "Mysore", "addressCountry": "IN"},
          "worksFor": {"@type": "Organization", "name": exp["company"]}, "sameAs": [PERSON["github"], PERSON["linkedin"], PERSON["x"]]}
    body = f"""
<section class="py-14 sm:py-20" aria-labelledby="hero">
  <p class="text-sm font-medium text-indigo-700 dark:text-indigo-300">{E(PERSON['title'])} &middot; {E(PERSON['location'])}</p>
  <h1 id="hero" class="mt-2 text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl dark:text-white">{E(PERSON['name'])}</h1>
  <p class="mt-5 max-w-2xl text-lg text-slate-600 dark:text-slate-300">{E(PERSON['summary'])}</p>
  <div class="mt-8 flex flex-wrap gap-3">
    <a class="{BTN_PRIMARY}" href="projects.html">See projects</a>
    <a class="{BTN}" href="resume.html">Resume</a>
    <a class="{BTN}" href="{PERSON['github']}" rel="noopener">GitHub</a>
    <a class="{BTN}" href="{PERSON['linkedin']}" rel="noopener">LinkedIn</a>
    <a class="{BTN}" href="mailto:{PERSON['email']}">Email</a>
  </div>
</section>

<section id="experience" class="py-10" aria-labelledby="experience-h"><h2 id="experience-h" class="{H2}">Experience</h2>
  <div class="{CARD} mt-5"><div class="flex flex-wrap items-baseline justify-between gap-2">
    <h3 class="text-lg font-semibold text-slate-900 dark:text-white">{E(exp['role'])}, {E(exp['company'])}</h3>
    <p class="text-sm text-slate-500 dark:text-slate-400">{E(exp['period'])}</p></div>
    <ul class="mt-4 list-disc space-y-2 pl-5 text-slate-700 dark:text-slate-300">{''.join(f'<li>{E(b)}</li>' for b in exp['bullets'])}</ul></div>
</section>

<section id="projects" class="py-10" aria-labelledby="projects-h">
  <div class="flex items-baseline justify-between"><h2 id="projects-h" class="{H2}">Projects</h2><a class="text-sm {LINK}" href="projects.html">Details</a></div>
  <div class="mt-5 grid gap-5 sm:grid-cols-2">{''.join(project_card(p) for p in PROJECTS)}</div>
</section>

<section id="skills" class="py-10" aria-labelledby="skills-h"><h2 id="skills-h" class="{H2}">Skills</h2>
  <div class="mt-5 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">{''.join(skill_group(n, i) for n, i in SKILL_GROUPS)}</div>
  <ul class="mt-8 flex flex-wrap gap-2" aria-label="Concepts">{chips(CONCEPTS)}</ul>
</section>

<section id="writing" class="py-10" aria-labelledby="writing-h">
  <div class="flex items-baseline justify-between"><h2 id="writing-h" class="{H2}">Writing</h2><a class="text-sm {LINK}" href="blog/index.html">All posts</a></div>
  <ul class="mt-5 divide-y divide-slate-200 dark:divide-slate-800">{''.join(f'<li class="py-3"><a class="font-medium text-slate-900 hover:underline dark:text-white" href="blog/{p["slug"]}.html">{E(p["title"])}</a><span class="ml-2 text-sm text-slate-500 dark:text-slate-400">{E(p["date"])}</span></li>' for p in POSTS[:5])}</ul>
</section>

<section id="education" class="py-10" aria-labelledby="edu-h"><h2 id="edu-h" class="{H2}">Education</h2>
  <div class="{CARD} mt-5"><h3 class="font-semibold text-slate-900 dark:text-white">{E(EDUCATION['school'])}</h3>
  <p class="text-slate-700 dark:text-slate-300">{E(EDUCATION['degree'])} &middot; {E(EDUCATION['period'])} &middot; CGPA {E(EDUCATION['cgpa'])}</p>
  <p class="mt-1 text-sm text-slate-600 dark:text-slate-400">{E(EDUCATION['extra'])}</p></div>
</section>

<section id="contact" class="py-10 pb-16" aria-labelledby="contact-h"><h2 id="contact-h" class="{H2}">Contact</h2>
  <p class="mt-3 text-slate-700 dark:text-slate-300">{E(PERSON['available'])} The quickest way to reach me is email.</p>
  <p class="mt-4"><a class="{BTN_PRIMARY}" href="mailto:{PERSON['email']}">{E(PERSON['email'])}</a></p>
</section>
"""
    head = f'<script type="application/ld+json">{json.dumps(ld)}</script>\n'
    return page(f"{PERSON['name']} | {PERSON['title']}",
                "Backend software engineer (Java, Spring Boot, Python, FastAPI) building microservices, trading infrastructure and open-source developer tools.",
                "index.html", body, current="home", extra_head=head)


def projects_page() -> str:
    secs = []
    for p in PROJECTS:
        writing = "".join(f'<li><a class="{LINK}" href="blog/{s}.html">{E(POST_BY_SLUG[s]["title"])}</a></li>' for s in p["writing"] if s in POST_BY_SLUG)
        secs.append(f"""<section id="{p['slug']}" class="py-8 border-b border-slate-200 dark:border-slate-800" aria-labelledby="{p['slug']}-h">
  <div class="flex flex-wrap items-center gap-3"><h2 id="{p['slug']}-h" class="{H2}">{E(p['name'])}</h2><span class="{CHIP}">{E(p['status'])}</span></div>
  <p class="mt-1 text-slate-600 dark:text-slate-400">{E(p['tagline'])}</p>
  <ul class="mt-4 list-disc space-y-2 pl-5 text-slate-700 dark:text-slate-300">{''.join(f'<li>{E(b)}</li>' for b in p['bullets'])}</ul>
  <ul class="mt-4 flex flex-wrap gap-1.5" aria-label="Technologies">{chips(p['stack'])}</ul>
  <p class="mt-4 text-sm">{ext_links(p['links'])}</p>
  {f'<div class="mt-4"><h3 class="text-sm font-semibold text-slate-500 dark:text-slate-400">Related writing</h3><ul class="mt-1 list-disc pl-5 text-sm">{writing}</ul></div>' if writing else ''}
</section>""")
    body = (f'<div class="py-12"><h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Projects</h1>'
            f'<p class="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">Each project links to its source or live site so claims can be checked.</p></div>'
            + "".join(secs) + '<div class="pb-16"></div>')
    return page(f"Projects | {PERSON['name']}", "Growth Quantix, Upstox Auth Pro, codive, HSCI and Prindox: what each does, the stack, and where to verify it.",
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
                   f'<ul class="mt-1 list-disc space-y-1 pl-5 text-sm">{"".join(f"<li>{E(b)}</li>" for b in p["bullets"][:3])}</ul>'
                   f'<p class="mt-1 text-xs text-slate-500">{E(", ".join(p["stack"]))}</p></div>' for p in PROJECTS)
    skills = "".join(f'<p class="text-sm"><span class="font-semibold">{E(n)}:</span> {E(", ".join(l for l, _ in i))}</p>' for n, i in SKILL_GROUPS)
    body = f"""<div class="py-10 print:py-0"><div class="flex flex-wrap items-baseline justify-between gap-2 print:hidden"><h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Resume</h1>
<p class="text-sm text-slate-500">Use your browser's Print &rarr; Save as PDF for a PDF copy.</p></div>
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
    return page(f"{p['title']} | {PERSON['name']}", p["excerpt"] or p["title"], f"blog/{p['slug']}.html", body, depth=1,
                current="blog", og_type="article", extra_head=mermaid)


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
