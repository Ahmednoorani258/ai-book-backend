import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
import trafilatura

def get_urls_from_sitemap(base_url):
    """
    Crawl all book pages starting from base_url.
    Returns a clean list of full URLs.
    """
    # html = requests.get(base_url).text
    # soup = BeautifulSoup(html, "html.parser")
    
    # links = set()  # use set to avoid duplicates
    
    # for a in soup.find_all("a", href=True):
    #     href = a["href"]
    #     # Convert relative URL to absolute URL
    #     full_url = urljoin(base_url, href)
    #     # Keep only URLs within the book site
    #     if base_url in full_url:
    #         links.add(full_url)
    
    # return list(links)

    xml = requests.get(base_url).text
    root = ET.fromstring(xml)

    urls = []
    for child in root:
        loc_tag = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc_tag is not None:
            urls.append(loc_tag.text)

    print("\nFOUND URLS:")
    for u in urls:
        print(" -", u)

    return urls


def fetch_mdx_from_url(url):
    """
    Fetch text content from a book page.
    """
    html = requests.get(url).text
    text = trafilatura.extract(html)

    if not text:
        print("[WARNING] No text extracted from:", url)

    return text
    # html = requests.get(url).text
    # soup = BeautifulSoup(html, "html.parser")

    # container = soup.select_one(".theme-doc-markdown")
    # if not container:
    #     return ""

    # # Clean text with line breaks
    # return container.get_text("\n")
