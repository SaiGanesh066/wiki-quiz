import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

SKIP_SECTIONS = {
    "contents",
    "references",
    "external links",
    "see also",
    "notes",
    "bibliography",
    "sources",
    "further reading",
    "works cited",
}

HEADERS = {
    # Wikipedia blocks requests without UA sometimes
    "User-Agent": "WikiQuizGenerator/1.0 (SaiGanesh; educational project) Mozilla/5.0"
}


def scrape_wikipedia(url: str):
    # Validate url
    url = url.strip()
    if not url:
        raise ValueError("Empty URL")

    parsed = urlparse(url)
    if parsed.netloc not in {"en.wikipedia.org", "www.en.wikipedia.org"}:
        raise ValueError("Only en.wikipedia.org links allowed")

    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # ---- TITLE ----
    title_tag = soup.select_one("h1#firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else "Unknown"

    # ---- CONTENT ----
    content = soup.select_one("div#mw-content-text")
    if not content:
        raise ValueError("Could not find page content")

    # ---- SECTIONS (h2 headlines) ----
    sections = []
    for h2 in content.select("h2"):
        span = h2.select_one("span.mw-headline")
        if not span:
            continue

        name = span.get_text(strip=True)
        if not name:
            continue

        low = name.lower()
        if low in SKIP_SECTIONS:
            continue

        if name not in sections:
            sections.append(name)

    sections = sections[:15]  # limit

    # ---- PARAGRAPHS ----
    paragraphs = content.select("p")

    # Full text (for LLM prompt)
    full_text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
    full_text = full_text.replace("[edit]", "").strip()
    full_text = full_text[:12000]

    # Summary: first meaningful paragraph
    summary = ""
    for p in paragraphs:
        text = p.get_text(" ", strip=True)
        if text and len(text) > 60:
            summary = text
            break

    return {
        "title": title,
        "summary": summary,
        "sections": sections,
        "text": full_text,
    }
