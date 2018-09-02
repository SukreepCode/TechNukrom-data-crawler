# -*- coding: utf-8 -*-

"""Main module."""

from pprint import pprint
from data_crawler import firebase
from data_crawler import feed_parser

def data_crawler(production):
    IS_DUMMY_MODE = False         # No act with DB
    IS_SKIP_DUPLICATE = True

    # TODO: Incremental mode

    print("Run with stat")
    print("{}: {}".format("IS_DUMMY_MODE",IS_DUMMY_MODE))
    print("{}: {}".format("IS_SKIP_DUPLICATE",IS_SKIP_DUPLICATE))

    db = firebase.init_firestore(production)

    post_collection = u'posts'
    doc_ref = db.collection(post_collection)

    print("Starting crawler")
    print("Loading: ")

    # get all documents
    docs = db.collection(post_collection).get()
    available_feeds = []
    for doc in docs:
        available_feeds.append(doc.id)

    sources = feed_parser.get_all_sources()
    for source in sources:
        feeds = feed_parser.feed_extractor(source)
        for feed in feeds:
            if not IS_SKIP_DUPLICATE:
                if not IS_DUMMY_MODE:
                    doc_ref.document(feed['hash_id']).set(feed)
                print("ADDED: "+ feed['title'])
                # print('.', end='')
            elif feed['hash_id'] not in available_feeds:
                if not IS_DUMMY_MODE:
                    doc_ref.document(feed['hash_id']).set(feed)
                print("ADDED: "+ feed['title'])
                # print('.', end='')
            else:
                print('!') #skip


    print("Finished crawl!")
    print("Done all jobs")




