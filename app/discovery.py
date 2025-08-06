import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

def is_valid_url(url: str) -> bool:
    """Checks if a URL is valid."""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def discover_apis(url: str) -> list[str]:
    """
    Scrapes a given URL to find links to potential API documentation.

    Args:
        url: The URL to scrape.

    Returns:
        A list of potential API documentation URLs found on the page.
    """
    if not is_valid_url(url):
        raise ValueError("Invalid URL provided.")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    # This is a simple heuristic. A more advanced implementation could
    # look for keywords, analyze link text, or even check the content
    # of linked pages.
    api_doc_keywords = [
        "api", "documentation", "developer", "reference", "swagger", "openapi"
    ]

    # Regex to match keywords in the URL path or link text
    keyword_regex = re.compile("|".join(api_doc_keywords), re.IGNORECASE)

    potential_links = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href")
        link_text = a_tag.get_text()

        if keyword_regex.search(href) or keyword_regex.search(link_text):
            # Resolve relative URLs
            full_url = urljoin(url, href)
            if is_valid_url(full_url):
                potential_links.add(full_url)

    return list(potential_links)
