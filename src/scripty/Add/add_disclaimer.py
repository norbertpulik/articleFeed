import os

directory = "gpt_generated_articles"
disclaimer = "> _Disclosure: This post may contain affiliate links. If you sign up through these links, I may earn a small commission at no extra cost to you._\n"

for filename in os.listdir(directory):
    if filename.endswith(".md"):
        filepath = os.path.join(directory, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.readlines()

        # 👉 Pridaj lepšiu detekciu
        if any("affiliate links" in line.lower() for line in content):
            print(f"✅ {filename}: Already has disclaimer.")
            continue

        new_content = []
        disclaimer_inserted = False

        for line in content:
            # Viac voľná kontrola
            if not disclaimer_inserted and "start trading today" in line.lower():
                new_content.append(disclaimer)
                disclaimer_inserted = True
            new_content.append(line)

        with open(filepath, "w", encoding="utf-8") as file:
            file.writelines(new_content)

        print(f"🟢 Updated: {filename}")