import requests
import time
import urllib.parse
import csv

# ✅ Zoznam základných fráz, ktoré sa budú dopĺňať
base_phrases = [
    "how to buy bitcoin in",
    "best crypto exchange in",
    "how to invest 100 dollars in",
    "is bitcoin legal in",
    "buy ethereum in",
    "sell crypto in",
    "which crypto wallet is best for",
    "how to start investing in",
    "best way to invest money in",
    "how to withdraw bitcoin in"
]

# 🔗 Google Autocomplete API URL
autocomplete_url = "https://suggestqueries.google.com/complete/search?client=firefox&q="

# 📦 Výsledky
results = []

for phrase in base_phrases:
    print(f"Scraping suggestions for: {phrase}")
    encoded_query = urllib.parse.quote(phrase)
    full_url = autocomplete_url + encoded_query

    try:
        # ➕ Nastavenie headers, aby ťa Google nezablokoval
        response = requests.get(full_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            suggestions = response.json()[1]
            for suggestion in suggestions:
                results.append({
                    "base_phrase": phrase,
                    "suggested_keyword": suggestion
                })
        else:
            print(f"Non-200 response: {response.status_code}")
    except Exception as e:
        print(f"Error with phrase '{phrase}': {e}")

    time.sleep(1.5)  # 🕐 Pauza, aby sa znížilo riziko blokovania

# 💾 Uloženie do CSV
with open("google_autocomplete_keywords.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["base_phrase", "suggested_keyword"])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"\n✅ Done! {len(results)} suggestions saved to google_autocomplete_keywords.csv")