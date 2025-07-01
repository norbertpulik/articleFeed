import os
import re

directory = "gpt_generated_articles"

for filename in os.listdir(directory):
    if filename.endswith(".md"):
        filepath = os.path.join(directory, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Odstráni disclaimer (vrátane celej riadky)
        cleaned = re.sub(
            r'>\s*_Disclosure:.*?_\n?', '', content, flags=re.IGNORECASE | re.DOTALL
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(cleaned)

print("✅ Affiliate disclaimery boli odstránené.")