# -*- coding: utf-8 -*-

"""Main module."""

import xmltodict
# import requests
import feedparser
import json
from pprint import pprint

def data_crawler():
    with open('data/data-sources.json') as f:
        data_sources = json.load(f)

    for key, sources in data_sources.items():
        for source in sources:
            print(source)
            d = feedparser.parse(source)
            print(d.feed['title'])
            print(d.feed['link'])
            print('-'*30)
            for entry in d.entries:
                pprint(entry)
                print('#'*10)

data_crawler()
#
