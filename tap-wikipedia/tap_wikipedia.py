import singer
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone
import os

# Globals
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
SCHEMA_DIR = os.path.join(ROOT_DIR, "schemas", "schema.json")
URL = r"https://en.wikipedia.org/wiki"
NOW = now = datetime.now(timezone.utc).isoformat()
with open(SCHEMA_DIR, "r") as f:
    SCHEMA = json.load(f)

def get_tfa_info(url):
    """
    Get the article link and article title for todays featured article on Wikipedia.

    """

    soup = BeautifulSoup(requests.get(f"{url}/MainPage").text, 'lxml')

    # Get DIV for Todays Featured Article
    tfa_div = soup.find("div", {"id":"mp-tfa"})
    b_elements = list(tfa_div.b.children)

    # Get dict values
    article_link = b_elements[0].attrs['href']
    article_title = b_elements[0].attrs['title']

    record = {'article_title': article_title, 'article_link': f"{url}{article_link}", 'timestamp': NOW}

    return record

record = get_tfa_info(URL)
singer.write_schema(stream_name='tfa', schema=SCHEMA, key_properties='timestamp')
singer.write_record(stream_name='tfa', record=record)