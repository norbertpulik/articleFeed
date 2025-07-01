import os
import re

# 📁 Cesta k priečinku s článkami
directory = "gpt_generated_articles"

for filename in os.listdir(directory):
    if filename.endswith(".md"):
        filepath = os.path.join(directory, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original = content

        # 1️⃣ Odstráni affiliate linky so slovom Coinbase, ponechá len text
        content = re.sub(
            r"\[([^\]]*Coinbase[^\]]*)\]\(https:\/\/affiliate\.coinbase\.com\/[^\)]+\)",
            r"\1",
            content
        )

        # 2️⃣ Odstráni holé affiliate URL linky, ak sú na samostatnom riadku
        content = re.sub(
            r"^.*https:\/\/affiliate\.coinbase\.com\/[^\n]*\n?", "", content, flags=re.MULTILINE
        )

        # 3️⃣ Odstráni všetky affiliate URL, aj keď nie sú v markdown formáte
        content = re.sub(
            r"https:\/\/affiliate\.coinbase\.com\/[^\s\)]+", "", content
        )

        # 4️⃣ Odstráni celý disclaimer riadok
        content = re.sub(
            r"> _Disclosure:.*?_\n?", "", content, flags=re.IGNORECASE | re.DOTALL
        )

        # 💾 Ak došlo k zmene, prepíš súbor
        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Upravený: {filename}")

print("\n🎉 Všetky affiliate odkazy a disclajmre boli odstránené.")