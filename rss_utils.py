import xml.etree.ElementTree as ET
import requests
import re

def find_first_telegraph_link(description_html):
    matches = re.findall(r'https://telegra\.ph[^\s"<>]+', description_html)
    return matches[0] if matches else None

def clean_title(title_text):
    return re.sub(r'https?://[^\s]+', '', title_text).strip()

def process_rss_from_url(url, output_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(output_path + ".tmp", "wb") as f:
            f.write(response.content)
        return process_rss_from_file(output_path + ".tmp", output_path)
    except Exception as e:
        print("Failed to fetch URL:", e)
        return False

def process_rss_from_file(input_path, output_path):
    tree = ET.parse(input_path)
    root = tree.getroot()

    for item in root.iter("item"):
        description = item.find("description")
        link_tag = item.find("link")
        title_tag = item.find("title")

        telegraph_link = None
        if description is not None and description.text:
            telegraph_link = find_first_telegraph_link(description.text)

        if telegraph_link and link_tag is not None:
            link_tag.text = telegraph_link

        if title_tag is not None and title_tag.text:
            title_tag.text = clean_title(title_tag.text)

    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return True