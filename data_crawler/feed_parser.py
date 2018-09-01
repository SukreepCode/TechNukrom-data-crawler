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
    return list(set(all_sources))

def feed_extractor(source):
    result = []

    print("Source: {}".format(source))
    domain = url_to_domain(source)

    d = feedparser.parse(source)
    for entry in d.entries:
        result.append({})
        current_item = len(result)-1
        result[current_item]['site_name'] = d.feed['title']
        result[current_item]['rss_link'] = d.feed['link']
        # pprint(entry)
        result[current_item]['title'] = entry['title']
        if 'author' in entry:
            result[current_item]['author'] = entry['author']
        else:
            result[current_item]['author'] = domain

        if 'content' in entry:
            result[current_item]['content'] = entry['content'][0]['value']

        if 'summary' in entry:
            result[current_item]['content'] = entry['summary']

        if 'updated_parsed' in entry:
            result[current_item]['updated'] = datetime.fromtimestamp(mktime(entry['updated_parsed']))

        if 'published_parsed' in entry:
            result[current_item]['published'] = datetime.fromtimestamp(mktime(entry['published_parsed']))

        result[current_item]['created'] = datetime.now()
        result[current_item]['id'] = entry['id']
        result[current_item]['link'] = entry['link']
        if 'tags' in entry:
            result[current_item]['tags'] = []
            for tag in entry['tags']:
                result[current_item]['tags'].append(tag['term'])
        result[current_item]['hash_id'] = hash_id(result[current_item])

        # Preprocessor for searching
        generated_tags = []
        if 'tags' in result[current_item]:
            generated_tags = tags_generator(result[current_item]['tags'])

        generated_tags.extend(tags_generator_from_text(result[current_item]['title']))
        generated_tags = tags_finalize(generated_tags)
        result[current_item]['generated_tags'] = generated_tags
            # print(result['generated_tags'])

        lang = ''
        try:
            if 'content' in result:
                lang = detect(result[current_item]['content'])
            elif 'title' in result:
                lang = detect(result[current_item]['title'])
        except:
            print("Can't detect language, skipping.. ")
        result[current_item]['generated_lang'] = lang

        # result['']


    return result
