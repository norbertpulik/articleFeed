import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# 🧪 Načítanie API kľúča z .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📥 Načítanie CSV
df = pd.read_csv("csv/processed_keywords_for_gpt.csv")  # uprav cestu podľa potreby

# 📤 Výstupný adresár
output_dir = "gpt_generated_articles"
os.makedirs(output_dir, exist_ok=True)

# ✍️ Prompt šablóna (zameraná na Coinbase)
def build_prompt(keyword, category):
    return f"""
Write a 600-word SEO article titled: "{keyword}".
- Make the introduction specific to the location (if it's a place).
- Focus only on Coinbase as the recommended platform.
- Include a short legal disclaimer paragraph (e.g., regulations vary).
- Add a simple 3-step buying guide.
- End with a strong CTA encouraging readers to sign up.
"""

# 🔁 Generovanie článkov
for idx, row in df.iterrows():
    keyword = row['suggested_keyword']
    category = row['base_phrase']

    prompt = build_prompt(keyword, category)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful SEO assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        # 🏷️ SEO Frontmatter
        frontmatter = f"""---
title: "{keyword.title()}"
slug: "{keyword.lower().replace(' ', '-').replace('?', '')}"
description: "Learn how to {keyword.lower()} using Coinbase in this beginner-friendly guide."
category: {category}
---\n
"""

        # ✅ Affiliate CTA a disclaimer
        affiliate_cta = """\n> _Disclosure: This post may contain affiliate links. If you sign up through these links, I may earn a small commission at no extra cost to you._\n
Start trading today on [Coinbase](https://affiliate.coinbase.com/xyz) and explore the world of digital currencies with confidence.
"""

        # 👉 Pridaj CTA ak chýba
        if "coinbase.com" not in content.lower():
            content += affiliate_cta
        elif "affiliate.coinbase.com" not in content.lower():
            content += affiliate_cta

        final_content = frontmatter + content

        # 💾 Uloženie článku
        safe_filename = keyword.lower().replace(" ", "-").replace("?", "") + ".md"
        filepath = os.path.join(output_dir, safe_filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)

        print(f"✅ Vygenerovaný: {safe_filename}")

    except Exception as e:
        print(f"❌ Chyba pri: {keyword} – {e}")