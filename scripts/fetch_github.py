"""Fetch the GitHub facts shown on the portfolio and store them in data/github.json.

    python scripts/fetch_github.py            # uses GITHUB_TOKEN if set (higher rate limit), else anonymous

Sources (all first-party GitHub, no widgets): the public REST API for the profile and repositories, and
the public contributions page that github.com itself uses to draw your profile graph. If a call fails
the previous value in data/github.json is kept, so a rate limit never blanks the page.
"""
from __future__ import annotations

import datetime
import html
import json
import os
import pathlib
import re
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "github.json"
USER = "recscse"
FEATURED = [
    ("recscse", "codive"),
    ("growthquantix", "tradingbot"),
    ("growthquantix", "upstox-auth-pro"),
    ("growthquantix", "upstox-auth-pro-java"),
    ("HNDS-HSCI", "ai-model"),
    ("recscse", "career-hub"),
]


def get(url: str, accept: str = "application/vnd.github+json") -> str:
    headers = {"User-Agent": "portfolio-build", "Accept": accept}
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def api(path: str):
    return json.loads(get("https://api.github.com" + path))


def contributions() -> dict:
    """The profile contribution calendar: exact count and level for each day of the last year."""
    t = get(f"https://github.com/users/{USER}/contributions", accept="text/html")
    total = int(re.search(r"([\d,]+)\s+contributions\s+in\s+the\s+last\s+year", t).group(1).replace(",", ""))
    tips = {m.group(1): m.group(2) for m in re.finditer(r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', t)}
    days = []
    for m in re.finditer(r"<td\b([^>]*\bdata-date=[^>]*)>", t):
        attrs = m.group(1)
        date = re.search(r'data-date="([\d-]+)"', attrs).group(1)
        level = int(re.search(r'data-level="(\d)"', attrs).group(1))
        cid = re.search(r'\bid="([^"]+)"', attrs).group(1)
        tip = html.unescape(tips.get(cid, ""))
        n = re.match(r"(\d[\d,]*)\s+contribution", tip)
        days.append({"date": date, "level": level, "count": int(n.group(1).replace(",", "")) if n else 0})
    days.sort(key=lambda d: d["date"])
    return {"total_last_year": total, "days": days}


def repo(owner: str, name: str) -> dict:
    meta = api(f"/repos/{owner}/{name}")
    langs = api(f"/repos/{owner}/{name}/languages")
    people = api(f"/repos/{owner}/{name}/contributors?per_page=100")
    mine = next((p["contributions"] for p in people if p.get("login", "").lower() == USER.lower()), 0) if isinstance(people, list) else None
    return {
        "full_name": meta["full_name"], "url": meta["html_url"], "language": meta.get("language"),
        "description": (meta.get("description") or "")[:200], "stars": meta.get("stargazers_count", 0),
        "pushed_at": (meta.get("pushed_at") or "")[:10], "languages": langs, "my_commits": mine,
    }


def own_repos() -> dict:
    """Public repositories you own (not forks): stars and last push, for the live stats on project cards."""
    out: dict = {}
    for page in (1, 2, 3):
        batch = api(f"/users/{USER}/repos?per_page=100&page={page}&sort=pushed")
        for x in batch:
            if not x["fork"]:
                out[x["full_name"]] = {"url": x["html_url"], "stars": x["stargazers_count"], "pushed_at": (x["pushed_at"] or "")[:10],
                                       "description": (x["description"] or "")[:200], "language": x["language"]}
        if len(batch) < 100:
            break
    return out


def pypi(name: str) -> dict:
    j = json.loads(get(f"https://pypi.org/pypi/{name}/json", accept="application/json"))
    version = j["info"]["version"]
    files = j["releases"].get(version, [])
    return {"version": version, "released": min((f["upload_time"] for f in files), default="")[:10]}


def main() -> None:
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    data = {"generated_at": datetime.date.today().isoformat(), "user": USER}
    steps = {
        "profile": lambda: (lambda u: {"public_repos": u["public_repos"], "followers": u["followers"], "since": u["created_at"][:4]})(api(f"/users/{USER}")),
        "contributions": contributions,
        "own_repos": own_repos,
        "pypi": lambda: {"upstox-auth-pro": pypi("upstox-auth-pro")},
    }
    for key, fn in steps.items():
        try:
            data[key] = fn()
            print(f"fetched {key}")
        except Exception as e:  # keep the last good value
            print(f"WARNING {key}: {type(e).__name__} {str(e)[:80]}; keeping previous value")
            data[key] = old.get(key)
    previous = {r["full_name"]: r for r in old.get("repos", [])}
    data["repos"] = []
    for owner, name in FEATURED:
        try:
            data["repos"].append(repo(owner, name))
            print(f"fetched {owner}/{name}")
        except Exception as e:
            print(f"WARNING {owner}/{name}: {type(e).__name__} {str(e)[:80]}; keeping previous value")
            if f"{owner}/{name}" in previous:
                data["repos"].append(previous[f"{owner}/{name}"])
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(data['repos'])} repos, {len((data.get('contributions') or {}).get('days', []))} calendar days")


if __name__ == "__main__":
    main()
