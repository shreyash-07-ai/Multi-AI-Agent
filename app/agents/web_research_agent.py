import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
from app.config import WEB_MAX_RESULTS

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MultiAgentResearch/1.0)"}

def research(query):
    url = "https://html.duckduckgo.com/html/?q=" + quote(query)
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    results = []
    for a in soup.select(".result__a")[:WEB_MAX_RESULTS]:
        href = a.get("href", "")
        title = a.get_text(" ", strip=True)
        if not href:
            continue
        results.append({"title": title, "url": href, "domain": urlparse(href).netloc})
    return results
