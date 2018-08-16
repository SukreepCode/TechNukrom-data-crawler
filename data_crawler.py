# -*- coding: utf-8 -*-

"""Main module."""

# import xmltodict
# import requests
import feedparser
import hashlib
import json
from time import mktime
from datetime import datetime
from urllib.parse import urlparse

from pprint import pprint
from helper import firestore

ENCODING = "utf-8"

def hash_id(feed):
    m = hashlib.sha1()
    m.update(feed['id'].encode())
    m.update(feed['rss_link'].encode())
    return m.hexdigest()

def url_to_base_url(url):
    # Input:  https://dev.mildronize.com/hello/world
    # Return: https://dev.mildronize.com/
    return '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))

def url_to_domain(url):
    # Input:  https://dev.mildronize.com/hello/world
    # Return: dev.mildronize.com
    return '{uri.netloc}'.format(uri=urlparse(url))

# gives
'http://stackoverflow.com/'

def feed_extractor():
    result = []

    with open('data/data-sources.json') as f:
        data_sources = json.load(f)

    for key, sources in data_sources.items():
        for source in sources:
            print("Source: {}".format(source))
            domain = url_to_domain(source)

            d = feedparser.parse(source)
            for entry in d.entries:
                result.append({})
                current_item = len(result)-1
                result[current_item]['site_name'] = d.feed['title']
                result[current_item]['rss_link'] = d.feed['link']
                pprint(entry)
                result[current_item]['title'] = entry['title']
                if 'author' in entry:
                    result[current_item]['author'] = entry['author']
                else:
                    result[current_item]['author'] = domain
                result[current_item]['content'] = entry['content'][0]['value']
                result[current_item]['published'] = datetime.fromtimestamp(mktime(entry['published_parsed']))
                if 'updated_parsed' in entry:
                    result[current_item]['updated'] = datetime.fromtimestamp(mktime(entry['updated_parsed']))
                else:
                    result[current_item]['updated'] = result[current_item]['published']
                result[current_item]['created'] = datetime.now()
                result[current_item]['id'] = entry['id']
                result[current_item]['link'] = entry['link']
                if 'tags' in entry:
                    result[current_item]['tags'] = []
                    for tag in entry['tags']:
                        result[current_item]['tags'].append(tag['term'])
                result[current_item]['hash_id'] = hash_id(result[current_item])
    return result

def data_crawler():
    db = firestore.init_env()
    collection_name = u'posts'
    doc_ref = db.collection(collection_name)

    # get all documents
    docs = db.collection(collection_name).get()
    available_feeds = []
    for doc in docs:
        available_feeds.append(doc.id)

    feeds = feed_extractor()
    for feed in feeds:
        if feed['hash_id'] not in available_feeds:
            doc_ref.document(feed['hash_id']).set(feed)
            print("DONE: "+ feed['title'])
        else:
            print("SKIP: "+ feed['title'])

data_crawler()

