import os
import markdown
import yaml
from datetime import datetime

# === KONFIGURÁCIA ===
MD_DIR = "gpt_generated_articles"
OUTPUT_DIR = "medium_ready_articles"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === PREVOD VŠETKÝCH .MD SÚBOROV ===
for fname in sorted(os.listdir(MD_DIR)):
    if not fname.endswith(".md"):
        continue

    md_path = os.path.join(MD_DIR, fname)
    with open(md_path, encoding="utf-8") as f:
        raw = f.read()

    # --- EXTRAKCIA FRONTMATTERU ---
    if raw.startswith("---"):
        try:
            _, fm, body_md = raw.split("---", 2)
            meta = yaml.safe_load(fm)
        except ValueError:
            print(f"⚠️ Preskočený (zle formátovaný frontmatter): {fname}")
            continue
    else:
        meta = {}
        body_md = raw

    # --- METADÁTA ---
    title = meta.get("title", os.path.splitext(fname)[0])
    slug = meta.get("slug", os.path.splitext(fname)[0])
    description = meta.get("description", "")
    
    # --- KONVERZIA MARKDOWN NA HTML ---
    body_html = markdown.markdown(
        body_md.strip(),
        extensions=["fenced_code", "codehilite", "tables"]
    )

    # --- ZOSTAVENIE HTML STRÁNKY ---
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
</head>
<body>
  <h1>{title}</h1>
  {body_html}
</body>
</html>
"""

    # --- ULOŽENIE HTML SÚBORU ---
    out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"✅ {fname} → {slug}.html")
