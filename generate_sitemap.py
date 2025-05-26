import requests
import xml.etree.ElementTree as ET
from datetime import datetime

rss_url = 'https://vlogars.blogspot.com/feeds/posts/default?alt=rss'

response = requests.get(rss_url)
root = ET.fromstring(response.content)

ns = {'atom': 'http://www.w3.org/2005/Atom'}

urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

for entry in root.findall('atom:entry', ns):
    loc = entry.find('atom:link[@rel="alternate"]', ns).attrib['href']
    lastmod_raw = entry.find('atom:updated', ns).text
    lastmod = datetime.strptime(lastmod_raw, '%Y-%m-%dT%H:%M:%S.%fZ').date()

    url = ET.SubElement(urlset, 'url')
    ET.SubElement(url, 'loc').text = loc
    ET.SubElement(url, 'lastmod').text = lastmod.isoformat()
    ET.SubElement(url, 'changefreq').text = 'weekly'
    ET.SubElement(url, 'priority').text = '0.8'

tree = ET.ElementTree(urlset)
tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)
