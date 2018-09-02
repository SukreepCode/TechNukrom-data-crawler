# -*- coding: utf-8 -*-

"""Main module."""

from pprint import pprint
from data_crawler import firestore
from data_crawler import feed_parser

def data_crawler(prouction):
    IS_DUMMY_MODE = False         # No act with DB
    IS_SKIP_DUPLICATE = True
    IS_PRODUCTION = prouction
    IS_INIT_STAT = False

    # TODO: Incremental mode

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


    # stat count all tags
    # generated_tags
    print("Finished crawl!")

    if IS_INIT_STAT:
        print("Start for Init stat")
        print("Loading: ")
        docs = db.collection(post_collection).get()
        stat_tags = {}
        for doc in docs:
            data = doc.to_dict()
            if 'generated_tags' in data:
                # print(data['generated_tags'])
                print('.', end='')
                for tag in data['generated_tags']:
                    if tag in stat_tags:
                        stat_tags[tag] = stat_tags[tag] + 1
                    else:
                        stat_tags[tag] = 1

        doc_ref_stat_tags = db.collection(u'stat_num_tags')
        for key, value in stat_tags.items():
            # print("Update tag: {}".format(key))
            print('.', end='')
            if not IS_DUMMY_MODE:
                doc_ref_stat_tags.document(key).set({'num': value})

        print("Done in Init counting tags")

    # other stats
    # print("Starting for other stats")
    # print("Loading: ")
    # stats = {}
    # stats['num_thai_posts'] = 0
    # stats['num_all_posts'] = 0
    # docs = db.collection(post_collection).get()
    # for doc in docs:
    #     data = doc.to_dict()
    #     print('.', end='')
    #     if 'lang' in data:
    #         if data['lang'] == 'th':
    #             stats['num_post_thai'] = stats['num_post_thai'] + 1
    #     stats['total_post'] = stats['total_post'] + 1

    # stats['num_sources'] = len(sources)
    # if not IS_DUMMY_MODE:
    #     db.collection(u'stats').document("post").set(stats)
    print("Done all jobs")




