import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

# === CONFIG ===
ARTICLE_URL = "https://norbertpulik.github.io/articleFeed/medium_ready_articles/best-crypto-exchange-in-canada.html"
STORAGE_STATE = "storageState.json"  # your logged-in Medium session

def fetch_html_and_extract():
    response = requests.get(ARTICLE_URL)
    if response.status_code != 200:
        raise Exception(f"❌ Failed to load article: {ARTICLE_URL}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Try to find <h1>, <h2>, or <h3>
    title_tag = soup.find(["h1", "h2", "h3"])
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        filename = urlparse(ARTICLE_URL).path.split("/")[-1]
        title = filename.replace("-", " ").replace(".html", "").title()
        print(f"⚠️ No heading found. Using fallback title: {title}")

    body = soup.find("body")
    if not body:
        raise Exception("❌ <body> tag not found.")
    return title, body.decode_contents()

def publish_to_medium(title, html_content):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context(storage_state=STORAGE_STATE)
        page = context.new_page()

        print("🚀 Opening Medium...")
        page.goto("https://medium.com/new-story")
        page.wait_for_selector('[data-testid="editorTitleParagraph"]')

        print("📝 Inserting title...")
        page.locator('[data-testid="editorTitleParagraph"]').fill(title)

        print("📰 Inserting HTML content...")
        editor = page.locator('[data-testid="editorParagraphText"]').nth(1)
        page.evaluate("(el, html) => el.innerHTML = html", editor, html_content)

        print("✅ Article pasted — review and publish manually.")
        page.pause()

if __name__ == "__main__":
    print("📥 Fetching article content from GitHub Pages...")
    title, html_content = fetch_html_and_extract()
    publish_to_medium(title, html_content)
