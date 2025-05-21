import requests
import xml.etree.ElementTree as ET
from datetime import datetime

BLOG_ID = 'vlogars.blogspot.com'
MAX_RESULTS = 150
SITEMAP_FILE = 'sitemap.xml'

def fetch_posts(start_index=1):
    url = f'https://{BLOG_ID}/feeds/posts/default?alt=json&start-index={start_index}&max-results={MAX_RESULTS}'
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    return data.get('feed', {}).get('entry', [])

def extract_url_and_date(entry):
    link = next((l['href'] for l in entry['link'] if l['rel'] == 'alternate'), None)
    updated = entry['updated']['$t'].split('T')[0]
    return link, updated

def generate_sitemap():
    urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    start_index = 1
    while True:
        entries = fetch_posts(start_index)
        if not entries:
            break
        for entry in entries:
            loc, lastmod = extract_url_and_date(entry)
            url_elem = ET.SubElement(urlset, 'url')
            ET.SubElement(url_elem, 'loc').text = loc
            ET.SubElement(url_elem, 'lastmod').text = lastmod
        start_index += MAX_RESULTS
    tree = ET.ElementTree(urlset)
    tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)

generate_sitemap()
