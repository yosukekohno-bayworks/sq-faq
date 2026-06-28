#!/usr/bin/env python3
import json
import os
import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
URL_INDEX = ROOT / "_analysis" / "04-notion-live-audit-url-index-2026-06-27.json"
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
BASE = "https://www.sqstackstaging.com"

TOKEN_RE = re.compile(r"([A-Za-z0-9_\\-]{32,}|eyJ[A-Za-z0-9_\\-\\.]{20,})")


def redact(text):
    return TOKEN_RE.sub("[REDACTED_LONG_VALUE]", text or "")


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.current = []
        self.text = []
        self.h1 = []
        self.h2 = []
        self.h3 = []
        self.buttons = []
        self.inputs = []
        self.selects = []
        self.links = []
        self._capture = None
        self._attrs = {}

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        self.stack.append(tag)
        if tag in {"h1", "h2", "h3", "button", "a", "label", "option"}:
            self._capture = tag
            self.current = []
            self._attrs = attr
        if tag in {"input", "textarea"}:
            label = attr.get("aria-label") or attr.get("placeholder") or attr.get("name") or attr.get("id") or attr.get("type")
            if label:
                self.inputs.append(redact(label))
        if tag == "select":
            label = attr.get("aria-label") or attr.get("name") or attr.get("id") or "select"
            self.selects.append(redact(label))

    def handle_endtag(self, tag):
        if self._capture == tag:
            value = redact(" ".join(" ".join(self.current).split()))
            if value:
                if tag == "h1":
                    self.h1.append(value)
                elif tag == "h2":
                    self.h2.append(value)
                elif tag == "h3":
                    self.h3.append(value)
                elif tag == "button":
                    self.buttons.append(value)
                elif tag == "a":
                    self.links.append({"text": value, "href": self._attrs.get("href")})
                self.text.append(value)
            self._capture = None
            self.current = []
            self._attrs = {}
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        value = " ".join((data or "").split())
        if not value:
            return
        if self._capture:
            self.current.append(value)
        self.text.append(redact(value))


def parse(html):
    parser = TextExtractor()
    parser.feed(html or "")
    body_text = " ".join(parser.text)
    body_text = " ".join(body_text.split())
    return {
        "h1": parser.h1[:12],
        "h2": parser.h2[:20],
        "h3": parser.h3[:20],
        "buttons": parser.buttons[:80],
        "inputs": parser.inputs[:80],
        "selects": parser.selects[:80],
        "links": parser.links[:80],
        "bodySample": redact(body_text[:1200]),
        "hasTodo": "TODO" in body_text,
        "hasNotFound": "このページは存在しないようです" in body_text,
        "hasUnexpectedError": "予期せぬエラーが発生しました" in body_text,
    }


index = json.loads(URL_INDEX.read_text())
routes = sorted(url for url, meta in index.items() if meta.get("kind") == "concrete")
offset = int(globals().get("SQ_CRAWL_OFFSET", os.environ.get("SQ_CRAWL_OFFSET", "0")))
limit = int(globals().get("SQ_CRAWL_LIMIT", os.environ.get("SQ_CRAWL_LIMIT", str(len(routes)))))
OUT = OUT_DIR / f"route-crawl-20260628-part-{offset:03d}.json"
routes = routes[offset:offset + limit]
results = []

for i, route in enumerate(routes, 1):
    requested = BASE + route
    error = None
    try:
        browser.goto(requested)
        browser.wait(1.4)
        html = browser.html
        parsed = parse(html)
        final_url = browser.url
        title = browser.title
    except Exception as exc:
        error = repr(exc)
        parsed = {}
        final_url = None
        title = None
    results.append({
        "route": route,
        "requestedUrl": requested,
        "finalUrl": final_url,
        "title": title,
        "error": error,
        **parsed,
    })
    if i % 25 == 0:
        OUT.write_text(json.dumps({
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "count": len(results),
            "complete": False,
            "results": results,
        }, ensure_ascii=False, indent=2))
    time.sleep(0.15)

OUT.write_text(json.dumps({
    "generatedAt": datetime.now(timezone.utc).isoformat(),
    "offset": offset,
    "limit": limit,
    "count": len(results),
    "complete": True,
    "results": results,
}, ensure_ascii=False, indent=2))
print(json.dumps({
    "count": len(results),
    "errors": sum(1 for row in results if row.get("error")),
    "notFound": [row["route"] for row in results if row.get("hasNotFound")],
    "unexpectedError": [row["route"] for row in results if row.get("hasUnexpectedError")],
    "todo": [row["route"] for row in results if row.get("hasTodo")],
}, ensure_ascii=False, indent=2))
