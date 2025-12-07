# from app.crawler.crawler import get_urls_from_site, fetch_mdx_from_url

# base_url = "https://ahmednoorani258.github.io/ai-book-new/"
# urls = get_urls_from_site(base_url)
# print("Found URLs:", urls)

# # Fetch text from one page
# text = fetch_mdx_from_url(urls[5])
# print(text[:500])  # print first 500 characters


# import requests
# import xml.etree.ElementTree as ET
# def get_all_urls(sitemap_url):
#     xml = requests.get(sitemap_url).text
#     root = ET.fromstring(xml)

#     urls = []
#     for child in root:
#         loc_tag = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
#         if loc_tag is not None:
#             urls.append(loc_tag.text)

#     print("\nFOUND URLS:")
#     for u in urls:
#         print(" -", u)

#     return urls


# sitemap_url = "https://ahmednoorani258.github.io/ai-book-new/sitemap.xml"
# print(get_all_urls(sitemap_url))
