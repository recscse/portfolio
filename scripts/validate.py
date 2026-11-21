"""Validate the generated site. Exit code 1 if anything is wrong.

    python scripts/validate.py            # offline checks (fast)
    python scripts/validate.py --online   # also checks every external link
"""
from __future__ import annotations

import concurrent.futures as cf
import pathlib
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urldefrag, urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from site_data import BASE  # noqa: E402

PAGES = sorted(p for p in ROOT.rglob("*.html") if not any(x in p.parts for x in ("node_modules", "content", ".git")))
BANNED = {  # claims that were found to be unsupported and must not come back
    r"\bkafka\b": "Kafka is only in design docs, not in running code",
    r"4\+\s*years": "experience is 5+ years (Oct 2021 start)",
    r"2,600": "download count could not be verified",
    r"<\s*2\s*ms|&lt;\s*2\s*ms": "'< 2ms' is not backed by the codive benchmark report",
    r"github\.com/recscse/prindox": "that repository does not exist (private)",
    r"prindox\.com": "prindox.com is a parked domain; the live site is prindox.netlify.app",
    r"AWS Certified|Oracle Certified|Docker Certified|Kafka Developer": "certifications are not held",
    r"Medium\.com/@brijeshyadav/": "the Medium articles never existed",
}
# Real sites that answer 403 to scripts, so they cannot be checked automatically.
BOT_BLOCKED = ("linkedin.com", "x.com", "twitter.com", "growthquantix.com", "upstox.com", "sourceforge.net")
errors: list[str] = []


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.imgs_without_alt = 0
        self.links, self.assets, self.ids, self.tags = [], [], set(), []
        self.title = ""
        self._in_title = False
        self.canonical = None
        self.desc = None
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._in_title = True
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "img":
            if "alt" not in a:
                self.imgs_without_alt += 1
            if a.get("src"):
                self.assets.append(a["src"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and a.get("href"):
            if a.get("rel") == "canonical":
                self.canonical = a["href"]
            else:
                self.assets.append(a["href"])
        if tag == "script" and a.get("src"):
            self.assets.append(a["src"])
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, d):
        if self._in_title:
            self.title += d


def check_page(p: pathlib.Path, ext: set[str]) -> None:
    text = p.read_text(encoding="utf-8")
    rel = p.relative_to(ROOT).as_posix()
    s = Scan()
    s.feed(text)
    if s.lang != "en":
        errors.append(f"{rel}: <html lang> missing")
    if s.h1 != 1:
        errors.append(f"{rel}: expected exactly one <h1>, found {s.h1}")
    if not s.title.strip() or not s.desc:
        errors.append(f"{rel}: missing <title> or meta description")
    if s.imgs_without_alt:
        errors.append(f"{rel}: {s.imgs_without_alt} <img> without alt")
    expect = BASE + ("index.html" if rel == "index.html" else rel)
    if s.canonical != expect:
        errors.append(f"{rel}: canonical is {s.canonical!r}, expected {expect!r}")
    if "mermaid" in text and "mermaid@" not in text and 'class="mermaid"' in text:
        errors.append(f"{rel}: has diagrams but no pinned Mermaid script")
    if "mermaid@" in text and not re.search(r"mermaid@\d+\.\d+\.\d+", text):
        errors.append(f"{rel}: Mermaid version is not pinned")
    for pat, why in BANNED.items():
        if re.search(pat, text, re.I):
            errors.append(f"{rel}: banned claim /{pat}/ - {why}")
    if 'target="_blank"' in text:
        errors.append(f"{rel}: links must open in the same tab (found target=_blank)")
    for m in re.finditer(r"<img [^>]*>", text):
        if "width=" not in m.group(0) or "height=" not in m.group(0):
            errors.append(f"{rel}: <img> without width/height (causes layout shift): {m.group(0)[:70]}")
    for ref in s.links + s.assets:
        if ref.startswith(("mailto:", "tel:", "javascript:", "data:")):
            continue
        if ref.startswith("//"):
            ref = "https:" + ref
        if ref.startswith("http"):
            if not ref.startswith(BASE):
                ext.add(urldefrag(ref)[0])
                continue
            ref = ref[len(BASE):]
        target, frag = urldefrag(ref)
        if not target:  # same-page anchor
            if frag and frag not in s.ids:
                errors.append(f"{rel}: anchor #{frag} not found on the page")
            continue
        f = (ROOT / target) if ref.startswith("/") else (p.parent / target)
        f = f.resolve()
        if not f.exists():
            errors.append(f"{rel}: broken local reference {ref}")
        elif frag and f.suffix == ".html":
            ids = Scan()
            ids.feed(f.read_text(encoding="utf-8"))
            if frag not in ids.ids:
                errors.append(f"{rel}: {target}#{frag} - anchor not found")


def head(u: str):
    for method in ("HEAD", "GET"):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, method=method, headers={"User-Agent": "Mozilla/5.0"}), timeout=20) as r:
                return u, r.status, r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405):
                continue
            return u, e.code, ""
        except Exception as e:
            if method == "GET":
                return u, type(e).__name__, ""
    return u, "ERR", ""


def main() -> int:
    ext: set[str] = set()
    for p in PAGES:
        check_page(p, ext)
    for f in ("sitemap.xml", "robots.txt", "site.webmanifest"):
        if not (ROOT / f).exists():
            errors.append(f"missing {f}")
    for u in re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8")):
        if not u.startswith(BASE) or not (ROOT / u[len(BASE):]).exists():
            errors.append(f"sitemap entry has no file: {u}")
    gh = ROOT / "data" / "github.json"
    if not gh.exists():
        errors.append("data/github.json is missing (run scripts/fetch_github.py)")
    else:
        import datetime, json
        age = (datetime.date.today() - datetime.date.fromisoformat(json.loads(gh.read_text(encoding="utf-8"))["generated_at"])).days
        if age > 100:
            errors.append(f"data/github.json is {age} days old; refresh it")
    for png, size in (("og.png", (1200, 630)), ("icon-192.png", (192, 192)), ("icon-512.png", (512, 512))):
        data = (ROOT / "assets" / png).read_bytes()[:24]
        if data[:8] != b"\x89PNG\r\n\x1a\n" or tuple(int.from_bytes(data[i:i + 4], "big") for i in (16, 20)) != size:
            errors.append(f"assets/{png} is not a {size[0]}x{size[1]} PNG")
    pdf = ROOT / "assets" / "Brijesh_Yadav_Resume.pdf"
    if not pdf.exists() or pdf.read_bytes()[:5] != b"%PDF-":
        errors.append("assets/Brijesh_Yadav_Resume.pdf is missing or not a PDF")
    else:
        try:
            from pypdf import PdfReader
        except ImportError:
            print("  note: pypdf not installed, so the resume PDF text was not checked (uv run --with pypdf python scripts/validate.py)")
        else:
            pdf_text = "\n".join(pg.extract_text() or "" for pg in PdfReader(str(pdf)).pages)
            if len(pdf_text) < 500:
                errors.append("resume PDF has almost no extractable text")
            for pat, why in BANNED.items():
                if re.search(pat, pdf_text, re.I):
                    errors.append(f"resume PDF: banned claim /{pat}/ - {why}")
    for svg in (ROOT / "assets" / "icons").glob("*.svg"):
        if b"<svg" not in svg.read_bytes()[:400]:
            errors.append(f"{svg.name} is not an SVG")
    print(f"pages checked: {len(PAGES)} | distinct external links: {len(ext)}")
    if "--online" in sys.argv:
        with cf.ThreadPoolExecutor(8) as ex:
            for u, st, ct in ex.map(head, sorted(ext)):
                host = urlparse(u).hostname or ""
                if any(host == b or host.endswith("." + b) for b in BOT_BLOCKED):
                    continue
                if st != 200:
                    errors.append(f"external link not OK ({st}): {u}")
                elif u.endswith((".mjs", ".js")) and "javascript" not in ct:
                    errors.append(f"wrong content-type {ct!r}: {u}")
                elif u.endswith(".svg") and "svg" not in ct:
                    errors.append(f"wrong content-type {ct!r}: {u}")
    for e in errors:
        print("  FAIL", e)
    print("OK: no problems found" if not errors else f"{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
