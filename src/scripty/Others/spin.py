import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

input_dir = "gpt_generated_articles"
output_dir = "medium_variants"
os.makedirs(output_dir, exist_ok=True)

# Prompt na prepísanie
def build_spin_prompt(original_content):
    return f"""
You're a professional content editor. Please rewrite the following SEO article for publication on Medium:

- Change at least 25% of the phrasing while preserving meaning.
- Use a more narrative and engaging tone.
- Avoid obvious keyword stuffing.
- Keep the structure (headings, sections), but change sentence flow.
- Don't repeat affiliate links. Keep only one CTA at the end.
- Don't mention “this article” or “this post”.

--- START OF ARTICLE ---
{original_content}
--- END OF ARTICLE ---
"""

for filename in os.listdir(input_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(input_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            original = f.read()

        prompt = build_spin_prompt(original)

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful SEO copywriter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            spun_content = response.choices[0].message.content.strip()

            output_path = os.path.join(output_dir, filename)
            with open(output_path, "w", encoding="utf-8") as out:
                out.write(spun_content)

            print(f"✅ Spun for Medium: {filename}")

        except Exception as e:
            print(f"❌ Failed to spin {filename}: {e}")