#!/usr/bin/env python3
import os
import yaml
import markdown
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator

# === CONFIGURATION ===
ARTICLES_DIR = "gpt_generated_articles"
OUTPUT_FEED = "feed.xml"
BASE_URL = "https://github.com/norbertpulik/articleFeed"
FEED_TITLE = "My Medium Import Feed"
FEED_LINK = f"{BASE_URL}/feed.xml"
FEED_DESC = "Automatically generated feed for IFTTT → Medium"

# === SETUP FEED ===
fg = FeedGenerator()
fg.id(FEED_LINK)
fg.title(FEED_TITLE)
fg.link(href=BASE_URL, rel="alternate")
fg.link(href=FEED_LINK, rel="self")
fg.description(FEED_DESC)
fg.language("en")

# === PROCESS EACH ARTICLE ===
for fname in sorted(os.listdir(ARTICLES_DIR)):
    if not fname.lower().endswith(".md"):
        continue

    path = os.path.join(ARTICLES_DIR, fname)
    raw = open(path, encoding="utf-8").read()

    # split off YAML front-matter (--- ... ---)
    if raw.startswith("---"):
        _, fm, body_md = raw.split("---", 2)
        meta = yaml.safe_load(fm)
    else:
        meta = {}
        body_md = raw

    # required fields
    title = meta.get("title", os.path.splitext(fname)[0])
    slug = meta.get("slug", os.path.splitext(fname)[0])
    date = meta.get("date")

    if not date:
        date = datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)
    elif isinstance(date, str):
        dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
        date = dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    elif isinstance(date, datetime):
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
    else:
        raise ValueError(f"Unrecognized date format: {date}")

    tags = meta.get("tags") or meta.get("category", "").split(",")

    # build the public URL for this article
    link = f"{BASE_URL}/{slug}.html"

    # convert Markdown to HTML
    html = markdown.markdown(body_md, extensions=["fenced_code", "codehilite"])

    # add entry to the feed
    fe = fg.add_entry()
    fe.id(link)
    fe.title(title)
    fe.link(href=link)
    fe.published(date)
    fe.description(f"<![CDATA[{meta.get('description', '')}]]>")
    fe.content(f"<![CDATA[{html}]]>", type="CDATA")
    for tag in tags:
        if tag:
            fe.category(term=tag.strip())

# === WRITE OUT THE RSS ===
fg.rss_file(OUTPUT_FEED)
print(f"✅ RSS feed written to {OUTPUT_FEED}")
