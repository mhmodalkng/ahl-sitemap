import requests
import xml.etree.ElementTree as ET
from datetime import datetime

BLOG_URL = "https://vlogars.blogspot.com"
MAX_RESULTS = 150
START_INDEX = 1
XML_FILE = "sitemap.xml"

def fetch_posts(start_index):
    url = f"{BLOG_URL}/feeds/posts/default?alt=json&start-index={start_index}&max-results={MAX_RESULTS}"
    response = requests.get(url)
    return response.json()

def generate_sitemap():
    ns = {'ns': 'http://www.w3.org/2005/Atom'}
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    index = START_INDEX
    while True:
        data = fetch_posts(index)
        entries = data.get("feed", {}).get("entry", [])
        if not entries:
            break

        for entry in entries:
            loc = next(link['href'] for link in entry['link'] if link['rel'] == 'alternate')
            lastmod = entry['updated']['$t'].split('T')[0]

            url_el = ET.SubElement(urlset, "url")
            ET.SubElement(url_el, "loc").text = loc
            ET.SubElement(url_el, "lastmod").text = lastmod

        index += MAX_RESULTS

    tree = ET.ElementTree(urlset)
    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_sitemap()
