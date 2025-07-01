import os
import re
from datetime import datetime, timezone

ARTICLES_DIR = "gpt_generated_articles"

for fname in os.listdir(ARTICLES_DIR):
    if not fname.endswith(".md"):
        continue

    path = os.path.join(ARTICLES_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        print(f"⛔ Skipping {fname}: No frontmatter.")
        continue

    # Split YAML frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"⚠️ Skipping {fname}: Malformed frontmatter.")
        continue

    before, frontmatter, body = parts
    if "date:" in frontmatter:
        print(f"✅ {fname}: Already has date.")
        continue

    # Add ISO 8601 UTC date
    modified_time = datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)
    iso_date = modified_time.isoformat().replace("+00:00", "Z")
    updated_frontmatter = frontmatter.strip() + f"\ndate: {iso_date}\n"

    # Rebuild full content
    updated_content = f"---\n{updated_frontmatter}---\n{body.lstrip()}"

    with open(path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"📝 Added date to {fname}: {iso_date}")
