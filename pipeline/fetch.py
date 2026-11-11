"""Polite, cached HTTP fetching. Every response is stored under data/raw/ so nothing is fetched twice.

Sources: Wikipedia (API) and public open datasets on GitHub. Transfermarkt (AWS WAF CAPTCHA), FBref (Cloudflare challenge) and
Understat (maintenance page) block automated clients, see data/features/gaps.md.
"""
import gzip
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
USER_AGENT = "BallonDorFeatures/0.1 (https://github.com/jonathanangsheng/Ballon_d-Or; research script)"
MIN_INTERVAL = 3.0  # seconds between live requests
_last = 0.0


def _get(url, tries=5):
    global _last
    for attempt in range(tries):
        wait = MIN_INTERVAL - (time.time() - _last)
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read().decode("utf-8")
            _last = time.time()
            return body
        except urllib.error.HTTPError as e:
            _last = time.time()
            if e.code not in (429, 503) or attempt == tries - 1:
                raise
            time.sleep(int(e.headers.get("Retry-After") or 0) or 30 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            _last = time.time()
            if attempt == tries - 1:
                raise
            time.sleep(30 * (attempt + 1))


_last_gh = 0.0


def github_raw(repo, path):
    """Return (text, url, fetched_date) for a file in a public GitHub repo (open datasets),
    cached gzip-compressed under data/raw/github/<repo>/<path>.gz."""
    global _last_gh
    url = f"https://raw.githubusercontent.com/{repo}/master/{path}"
    local = RAW_DIR / "github" / repo / (path + ".gz")
    meta = local.with_suffix(local.suffix + ".date")
    if not local.exists():
        wait = 0.3 - (time.time() - _last_gh)
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    body = r.read()
                break
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    raise
                time.sleep(10 * (attempt + 1))
            except (urllib.error.URLError, TimeoutError):
                time.sleep(10 * (attempt + 1))
        else:
            raise RuntimeError(f"failed to fetch {url}")
        _last_gh = time.time()
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_bytes(gzip.compress(body))
        meta.write_text(date.today().isoformat())
    return gzip.decompress(local.read_bytes()).decode("utf-8"), url, meta.read_text().strip()


def web_page(url):
    """Return (html, fetched_date) for a plain web page, cached under data/raw/web/."""
    key = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
    path = RAW_DIR / "web" / f"{key}.json"
    if not path.exists():
        rec = {"url": url, "fetched_date": date.today().isoformat(), "html": _get(url)}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
    rec = json.loads(path.read_text(encoding="utf-8"))
    return rec["html"], rec["fetched_date"]


def wiki_wikitext(title):
    """Return (wikitext, page_url, fetched_date) for an English Wikipedia article, following redirects."""
    key = hashlib.sha1(title.encode("utf-8")).hexdigest()[:16]
    path = RAW_DIR / "wikipedia" / f"{key}.json"
    if not path.exists():
        params = {
            "action": "parse", "page": title, "prop": "wikitext", "redirects": 1,
            "format": "json", "formatversion": 2,
        }
        url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
        data = json.loads(_get(url))
        rec = {"title": title, "api_url": url, "fetched_date": date.today().isoformat(), "response": data}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
    rec = json.loads(path.read_text(encoding="utf-8"))
    parse = rec["response"].get("parse")
    if parse is None:
        return None, None, rec["fetched_date"]
    page_url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(parse["title"].replace(" ", "_"))
    return parse["wikitext"], page_url, rec["fetched_date"]


def wiki_prefetch(titles):
    """Fill the wiki_wikitext cache for many titles, 50 per API request."""
    def cache_path(t):
        return RAW_DIR / "wikipedia" / f"{hashlib.sha1(t.encode('utf-8')).hexdigest()[:16]}.json"

    def save(t, url, resp):
        rec = {"title": t, "api_url": url, "fetched_date": date.today().isoformat(), "response": resp}
        path = cache_path(t)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")

    def run(batch):
        """Fetch a batch; returns titles left without content (response was cut short)."""
        params = {
            "action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
            "redirects": 1, "titles": "|".join(batch), "format": "json", "formatversion": 2,
        }
        url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
        reply = json.loads(_get(url))
        if "query" not in reply:  # e.g. an invalid title in the batch
            if len(batch) == 1:
                save(batch[0], url, {"error": reply.get("error", {"code": "invalid"})})
                return []
            half = len(batch) // 2
            return run(batch[:half]) + run(batch[half:])
        q = reply["query"]
        alias = {t: t for t in batch}
        for key in ("normalized", "redirects"):
            for n in q.get(key, []):
                for t, cur in alias.items():
                    if cur == n["from"]:
                        alias[t] = n["to"]
        pages = {p["title"]: p for p in q["pages"]}
        left = []
        for t in batch:
            p = pages.get(alias[t], {})
            if "revisions" in p:
                save(t, url, {"parse": {"title": p["title"],
                                        "wikitext": p["revisions"][0]["slots"]["main"]["content"]}})
            elif p.get("missing") or p.get("invalid") or not p:
                save(t, url, {"error": {"code": "missingtitle"}})
            else:
                left.append(t)  # content omitted because the reply hit the size limit
        return left

    todo = sorted({t for t in titles if t and not cache_path(t).exists()})
    while todo:
        size = 50 if len(todo) > 10 else len(todo)
        left = []
        for i in range(0, len(todo), size):
            left += run(todo[i:i + size])
        if len(left) == len(todo):  # no progress: fetch one at a time
            for t in left:
                wiki_wikitext(t)
            break
        todo = left


def wiki_redirects(titles):
    """{title: set of titles that redirect to it (incl. the title itself)}, 50 titles per request,
    cached per title under data/raw/wikipedia/redirects/."""
    def cache_path(t):
        return RAW_DIR / "wikipedia" / "redirects" / f"{hashlib.sha1(t.encode('utf-8')).hexdigest()[:16]}.json"

    titles = sorted({t for t in titles if t})
    todo = [t for t in titles if not cache_path(t).exists()]
    for i in range(0, len(todo), 50):
        batch, found, cont = todo[i:i + 50], {}, {}
        while True:
            params = {"action": "query", "prop": "redirects", "rdlimit": "max", "titles": "|".join(batch),
                      "format": "json", "formatversion": 2, **cont}
            url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
            reply = json.loads(_get(url))
            q = reply.get("query", {})
            alias = {n["to"]: n["from"] for n in q.get("normalized", [])}
            for p in q.get("pages", []):
                found.setdefault(alias.get(p["title"], p["title"]), set()).update(r["title"] for r in p.get("redirects", []))
            if "continue" not in reply:
                break
            cont = reply["continue"]
        for t in batch:
            path = cache_path(t)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"title": t, "fetched_date": date.today().isoformat(),
                                        "redirects": sorted(found.get(t, set()))}, ensure_ascii=False), encoding="utf-8")
    return {t: {t, *json.loads(cache_path(t).read_text(encoding="utf-8"))["redirects"]} for t in titles}
