import os
import re

directory = "gpt_generated_articles"

for filename in os.listdir(directory):
    if filename.endswith(".md"):
        filepath = os.path.join(directory, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Odstráni celý odsek/link s affiliate linkom na Coinbase
        cleaned = re.sub(
            r'\[Coinbase\]\(https:\/\/affiliate\.coinbase\.com\/[^\)]+\)', 
            'Coinbase',  # necháme názov Coinbase ako čistý text
            content
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(cleaned)

print("✅ Affiliate linky boli odstránené.")