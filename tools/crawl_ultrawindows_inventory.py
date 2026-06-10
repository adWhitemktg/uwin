#!/usr/bin/env python3
import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


BASE = "https://ultrawindows.net/"
SITEMAPS = [
    "https://ultrawindows.net/page-sitemap.xml",
    "https://ultrawindows.net/post-sitemap.xml",
]
OUT_DIR = Path("notas/ultrawindows-content-inventory-2026-06-10")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 Chrome/125 Safari/537.36"
)
CRAWL_DELAY_SECONDS = 3


def fetch(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read(), response.geturl(), response.status


def norm_space(value):
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def normalize_url(url, base=BASE):
    if not url:
        return ""
    joined = urllib.parse.urljoin(base, html.unescape(url.strip()))
    parsed = urllib.parse.urlparse(joined)
    if parsed.scheme in ("tel", "mailto"):
        return joined
    parsed = parsed._replace(fragment="")
    return urllib.parse.urlunparse(parsed)


class PageParser(HTMLParser):
    def __init__(self, page_url):
        super().__init__(convert_charrefs=True)
        self.page_url = page_url
        self.title = ""
        self.meta = {}
        self.headings = []
        self.links = []
        self.images = []
        self.schema_json = []
        self.text_chunks = []
        self._tag_stack = []
        self._capture = None
        self._capture_data = []
        self._skip_depth = 0
        self._current_link = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self._tag_stack.append(tag)
        if tag in {"script", "style", "noscript", "svg"}:
            if tag == "script" and attrs.get("type") == "application/ld+json":
                self._capture = "schema"
                self._capture_data = []
            else:
                self._skip_depth += 1
            return
        if tag in {"header", "footer", "nav"}:
            self._skip_depth += 1
        if tag == "title":
            self._capture = "title"
            self._capture_data = []
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._capture = tag
            self._capture_data = []
        elif tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            content = attrs.get("content")
            if key and content:
                self.meta[key] = norm_space(content)
        elif tag == "a":
            href = normalize_url(attrs.get("href"), self.page_url)
            self._current_link = {"url": href, "text_parts": []}
        elif tag == "img":
            src = normalize_url(attrs.get("src") or attrs.get("data-src"), self.page_url)
            if src:
                self.images.append(
                    {
                        "src": src,
                        "alt": norm_space(attrs.get("alt", "")),
                        "title": norm_space(attrs.get("title", "")),
                        "width": attrs.get("width", ""),
                        "height": attrs.get("height", ""),
                    }
                )

    def handle_endtag(self, tag):
        if self._capture == "title" and tag == "title":
            self.title = norm_space("".join(self._capture_data))
            self._capture = None
            self._capture_data = []
        elif self._capture in {"h1", "h2", "h3", "h4", "h5", "h6"} and tag == self._capture:
            text = norm_space("".join(self._capture_data))
            if text:
                self.headings.append({"level": self._capture, "text": text})
            self._capture = None
            self._capture_data = []
        elif self._capture == "schema" and tag == "script":
            raw = "".join(self._capture_data).strip()
            if raw:
                self.schema_json.append(raw)
            self._capture = None
            self._capture_data = []
        elif tag == "a" and self._current_link:
            link = {
                "url": self._current_link["url"],
                "text": norm_space(" ".join(self._current_link["text_parts"])),
            }
            if link["url"]:
                self.links.append(link)
            self._current_link = None
        if tag in {"script", "style", "noscript", "svg", "header", "footer", "nav"} and self._skip_depth:
            self._skip_depth -= 1
        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data):
        if self._capture:
            self._capture_data.append(data)
        if self._current_link is not None:
            self._current_link["text_parts"].append(data)
        if not self._skip_depth:
            text = norm_space(data)
            if text:
                self.text_chunks.append(text)


def sitemap_urls():
    found = []
    for sitemap in SITEMAPS:
        body, _, _ = fetch(sitemap)
        root = ET.fromstring(body)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for url_node in root.findall("sm:url", ns):
            loc = url_node.findtext("sm:loc", default="", namespaces=ns).strip()
            lastmod = url_node.findtext("sm:lastmod", default="", namespaces=ns).strip()
            if loc:
                found.append({"url": loc, "lastmod": lastmod, "sitemap": sitemap})
    deduped = []
    seen = set()
    for item in found:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def schema_types(schema_json):
    types = []
    parsed = []
    for raw in schema_json:
        try:
            payload = json.loads(raw)
            parsed.append(payload)
        except json.JSONDecodeError:
            continue
        nodes = payload.get("@graph", []) if isinstance(payload, dict) else []
        if isinstance(payload, dict) and payload.get("@type"):
            nodes.append(payload)
        for node in nodes:
            t = node.get("@type") if isinstance(node, dict) else None
            if isinstance(t, list):
                types.extend(str(x) for x in t)
            elif t:
                types.append(str(t))
    return sorted(set(types)), parsed


def detect_entity_type(url, title, headings, schema):
    text = " ".join([url, title] + [h["text"] for h in headings]).lower()
    stypes = {t.lower() for t in schema}
    if "article" in stypes or any(x in text for x in ["how ", "why ", "questions every", "vs", "mistakes"]):
        return "blog_post_or_article"
    if "contact" in text:
        return "contact_page"
    if "financing" in text:
        return "financing_page"
    if any(x in text for x in ["replacement-windows-in-", "windows-in-", "-tx", "texas/"]):
        return "location_service_page"
    if any(x in text for x in ["aluminum", "vinyl", "fiberglass", "composite", "wood", "garden", "bow", "bay"]):
        return "product_or_service_page"
    if "project" in text:
        return "project_gallery"
    if url.rstrip("/") == BASE.rstrip("/"):
        return "homepage"
    return "page"


def classify_links(links):
    internal = []
    outbound = []
    base_host = urllib.parse.urlparse(BASE).netloc
    seen = set()
    for link in links:
        url = link["url"]
        key = (url, link["text"])
        if key in seen:
            continue
        seen.add(key)
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme in {"tel", "mailto"} or parsed.netloc == base_host:
            internal.append(link)
        else:
            outbound.append(link)
    return internal, outbound


def extract_faqs(headings, body_text, schema_payloads):
    faqs = []
    for payload in schema_payloads:
        nodes = payload.get("@graph", []) if isinstance(payload, dict) else []
        for node in nodes:
            if isinstance(node, dict) and node.get("@type") == "FAQPage":
                for item in node.get("mainEntity", []):
                    faqs.append(
                        {
                            "question": norm_space(item.get("name", "")),
                            "answer": norm_space(
                                item.get("acceptedAnswer", {}).get("text", "")
                                if isinstance(item.get("acceptedAnswer"), dict)
                                else ""
                            ),
                        }
                    )
    if faqs:
        return faqs
    # Conservative heuristic: only capture obvious question headings.
    for h in headings:
        if h["text"].endswith("?"):
            faqs.append({"question": h["text"], "answer": ""})
    return faqs


def audit_notes(page):
    notes = []
    body = page["body_text"]
    word_count = len(re.findall(r"\b[\w'-]+\b", body))
    page["word_count"] = word_count
    if word_count < 250:
        notes.append("Thin content candidate: fewer than 250 extracted body words.")
    if not page["h1"]:
        notes.append("Missing H1 in parsed HTML.")
    if len(page["h1_all"]) > 1:
        notes.append("Multiple H1s detected.")
    if not page["meta_description"]:
        notes.append("Missing meta description.")
    if re.search(r"-[0-9a-f]{6,}bc/?$", urllib.parse.urlparse(page["url"]).path):
        notes.append("Spam/generated-page candidate: URL ends in machine-like hexadecimal suffix.")
    if page["url"].endswith("-610595bc/") or "Resources" in page["body_text"][:1000]:
        notes.append("Resource/spam-footprint candidate: appears tied to SEO automation resource pages.")
    return notes


def slug_for(url):
    path = urllib.parse.urlparse(url).path.strip("/") or "home"
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", path)[:120]


def markdown_page(page):
    lines = [
        f"# {page['title'] or page['url']}",
        "",
        f"- URL: {page['url']}",
        f"- Entity type: {page['detected_entity_type']}",
        f"- H1: {page['h1']}",
        f"- Meta title: {page['meta_title']}",
        f"- Meta description: {page['meta_description']}",
        f"- Word count: {page['word_count']}",
        "",
        "## Headings",
    ]
    lines.extend(f"- {h['level'].upper()}: {h['text']}" for h in page["headings"])
    lines.extend(["", "## Notes"])
    lines.extend(f"- {note}" for note in (page["notes"] or ["No duplicate/thin/spam flags from heuristic checks."]))
    lines.extend(["", "## Body Text", "", page["body_text"]])
    return "\n".join(lines) + "\n"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    page_items = sitemap_urls()
    pages = []
    for index, item in enumerate(page_items, start=1):
        if index > 1:
            time.sleep(CRAWL_DELAY_SECONDS)
        url = item["url"]
        try:
            raw, final_url, status = fetch(url)
            markup = raw.decode("utf-8", errors="replace")
            parser = PageParser(final_url)
            parser.feed(markup)
            stypes, schema_payloads = schema_types(parser.schema_json)
            internal, outbound = classify_links(parser.links)
            headings = parser.headings
            h1_all = [h["text"] for h in headings if h["level"] == "h1"]
            body_text = norm_space(" ".join(parser.text_chunks))
            body_hash = hashlib.sha256(body_text.lower().encode("utf-8")).hexdigest()
            page = {
                "url": url,
                "final_url": final_url,
                "status": status,
                "sitemap_lastmod": item["lastmod"],
                "sitemap": item["sitemap"],
                "title": parser.title,
                "h1": h1_all[0] if h1_all else "",
                "h1_all": h1_all,
                "meta_title": parser.title,
                "meta_description": parser.meta.get("description", ""),
                "headings": headings,
                "body_text": body_text,
                "body_hash": body_hash,
                "detected_entity_type": detect_entity_type(url, parser.title, headings, stypes),
                "internal_links": internal,
                "outbound_links": outbound,
                "images": parser.images,
                "faqs": extract_faqs(headings, body_text, schema_payloads),
                "schema_types": stypes,
                "schema": schema_payloads,
                "notes": [],
            }
            page["notes"] = audit_notes(page)
            pages.append(page)
            print(f"[{index}/{len(page_items)}] {status} {url}")
        except (urllib.error.URLError, TimeoutError, ET.ParseError) as exc:
            pages.append(
                {
                    "url": url,
                    "status": "error",
                    "error": str(exc),
                    "sitemap_lastmod": item["lastmod"],
                    "sitemap": item["sitemap"],
                    "notes": ["Fetch or parse failed; content fields unavailable."],
                }
            )
            print(f"[{index}/{len(page_items)}] ERROR {url}: {exc}")

    by_hash = {}
    for page in pages:
        body_hash = page.get("body_hash")
        if body_hash:
            by_hash.setdefault(body_hash, []).append(page["url"])
    for page in pages:
        matches = by_hash.get(page.get("body_hash"), [])
        if len(matches) > 1:
            page.setdefault("notes", []).append(
                "Exact duplicate body text hash shared with: " + ", ".join(u for u in matches if u != page["url"])
            )

    summary = {
        "source": BASE,
        "crawled_at": datetime.now(timezone.utc).isoformat(),
        "crawl_delay_seconds": CRAWL_DELAY_SECONDS,
        "sitemaps": SITEMAPS,
        "page_count": len(pages),
        "error_count": sum(1 for p in pages if p.get("status") == "error"),
        "entity_type_counts": {},
        "flagged_pages": [
            {"url": p["url"], "notes": p.get("notes", [])}
            for p in pages
            if p.get("notes")
        ],
    }
    for page in pages:
        entity = page.get("detected_entity_type", "unknown")
        summary["entity_type_counts"][entity] = summary["entity_type_counts"].get(entity, 0) + 1

    inventory = {"summary": summary, "pages": pages}
    (OUT_DIR / "content-inventory.json").write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT_DIR / "summary.md").write_text(
        "# Ultra Windows Content Inventory\n\n"
        f"- Source: {BASE}\n"
        f"- Crawled at: {summary['crawled_at']}\n"
        f"- Pages/posts crawled: {summary['page_count']}\n"
        f"- Fetch errors: {summary['error_count']}\n"
        f"- Crawl delay honored: {CRAWL_DELAY_SECONDS}s\n\n"
        "## Entity Type Counts\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in sorted(summary["entity_type_counts"].items()))
        + "\n\n## Flagged Pages\n\n"
        + "\n".join(
            f"- {item['url']}: {'; '.join(item['notes'])}"
            for item in summary["flagged_pages"]
        )
        + "\n",
        encoding="utf-8",
    )

    pages_dir = OUT_DIR / "pages"
    pages_dir.mkdir(exist_ok=True)
    for page in pages:
        if page.get("status") != "error":
            (pages_dir / f"{slug_for(page['url'])}.md").write_text(markdown_page(page), encoding="utf-8")


if __name__ == "__main__":
    main()
