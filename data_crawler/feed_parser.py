import feedparser
import hashlib
import json
from time import mktime
from datetime import datetime
from urllib.parse import urlparse

# preprocessor
from langdetect import detect
from data_crawler.generator import tags_generator, tags_generator_from_text, tags_finalize

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

def get_all_sources():
    with open('data/data-sources.json') as f:
        data_sources = json.load(f)

    all_sources = data_sources['rss-sources']
    for medium_id in data_sources['medium-sources']:
        all_sources.append("https://medium.com/feed/@{}".format(medium_id))
    return all_sources

def feed_extractor(source):
    result = {}

    print("Source: {}".format(source))
    domain = url_to_domain(source)

    d = feedparser.parse(source)
    for entry in d.entries:
        result['site_name'] = d.feed['title']
        result['rss_link'] = d.feed['link']
        # pprint(entry)
        result['title'] = entry['title']
        if 'author' in entry:
            result['author'] = entry['author']
        else:
            result['author'] = domain

        if 'content' in entry:
            result['content'] = entry['content'][0]['value']

        if 'summary' in entry:
            result['content'] = entry['summary']

        if 'updated_parsed' in entry:
            result['updated'] = datetime.fromtimestamp(mktime(entry['updated_parsed']))

        if 'published_parsed' in entry:
            result['published'] = datetime.fromtimestamp(mktime(entry['published_parsed']))

        result['created'] = datetime.now()
        result['id'] = entry['id']
        result['link'] = entry['link']
        if 'tags' in entry:
            result['tags'] = []
            for tag in entry['tags']:
                result['tags'].append(tag['term'])
        result['hash_id'] = hash_id(result)

        # Preprocessor for searching

        result['generated_tags'] = []
        if 'tags' in result:
            result['generated_tags'] = tags_generator(result['tags'])
            result['generated_tags'].extend(tags_generator_from_text(result['title']))
            result['generated_tags'] = tags_finalize(result['generated_tags'])
            print(result['generated_tags'])

        lang = ''
        try:
            if 'content' in result:
                lang = detect(result['content'])
            elif 'title' in result:
                lang = detect(result['title'])
        except:
            print("Can't detect language, skipping.. ")
        result['generated_lang'] = lang

        # result['']


    return result
