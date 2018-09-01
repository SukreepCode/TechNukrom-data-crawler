# -*- coding: utf-8 -*-

"""Main module."""

from pprint import pprint
from data_crawler import firestore
from data_crawler import feed_parser

def data_crawler():
    IS_DUMMY_MODE = False

    IS_SKIP_DUPLICATE = False
    IS_PRODUCTION = True

    IS_INIT_STAT = True

    print("Run with stat")
    print("{}: {}".format("IS_DUMMY_MODE",IS_DUMMY_MODE))
    print("{}: {}".format("IS_SKIP_DUPLICATE",IS_SKIP_DUPLICATE))
    print("{}: {}".format("IS_PRODUCTION",IS_PRODUCTION))
    print("{}: {}".format("IS_INIT_STAT",IS_INIT_STAT))

    if IS_PRODUCTION:
        db = firestore.init_env()
    else:
        db = firestore.init()

    post_collection = u'posts'
    doc_ref = db.collection(post_collection)

    print("Starting crawler")

    # get all documents
    docs = db.collection(post_collection).get()
    available_feeds = []
    for doc in docs:
        available_feeds.append(doc.id)

    for source in feed_parser.get_all_sources():
        feed = feed_parser.feed_extractor(source)
        if not IS_SKIP_DUPLICATE:
            if not IS_DUMMY_MODE:
                doc_ref.document(feed['hash_id']).set(feed)
            # print("DONE: "+ feed['title'])
        elif feed['hash_id'] not in available_feeds:
            if not IS_DUMMY_MODE:
                doc_ref.document(feed['hash_id']).set(feed)
            # print("DONE: "+ feed['title'])
        # else:
        #     print("SKIP: "+ feed['title'])


    # stat count all tags
    # generated_tags
    print("Finished crawl!")

    if IS_INIT_STAT:
        print("Start for Init stat")
        docs = db.collection(post_collection).get()
        stat_tags = {}
        for doc in docs:
            data = doc.to_dict()
            if 'generated_tags' in data:
                # print(data['generated_tags'])
                for tag in data['generated_tags']:
                    if tag in stat_tags:
                        stat_tags[tag] = stat_tags[tag] + 1
                    else:
                        stat_tags[tag] = 1

        doc_ref_stat_tags = db.collection(u'stat_num_tags')
        for key, value in stat_tags.items():
            # print("Update tag: {}".format(key))
            if not IS_DUMMY_MODE:
                doc_ref_stat_tags.document(key).set({'num': value})

        print("Done in Init counting tags")

    print("Done all jobs")




