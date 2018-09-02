
from data_crawler import firebase
from data_crawler import feed_parser

POST_COLLECTION = "posts"

def main(production):
    print("hey")
    init_stat(production)

def init_stat(production):
    db_firebase = firebase.init_firebase(production)
    db_firestore = firebase.init_firestore(production)
    print("Start for Init stat")
    print("Loading: ")
    docs = db_firestore.collection(POST_COLLECTION).get()
    stats = {}
    stats['num_thai_posts'] = 0
    stats['num_all_posts'] = 0
    stat_tags = {}
    for doc in docs:
        data = doc.to_dict()
        if 'generated_tags' in data:
            # print(data['generated_tags'])
            print(data['generated_tags'])
            for tag in data['generated_tags']:
                if tag in stat_tags:
                    stat_tags[tag] = stat_tags[tag] + 1
                else:
                    stat_tags[tag] = 1
        if 'generated_lang' in data:
            print('X', end='')
            if data['generated_lang'] == 'th':
                stats['num_thai_posts'] = stats['num_thai_posts'] + 1

        stats['num_all_posts'] = stats['num_all_posts'] + 1

    print("Done in counting")

    num_sources = len(feed_parser.get_all_sources())

    db_firebase.reference('stats/tag/tag_count') \
        .set(stat_tags)

    db_firebase.reference('stats/post') \
        .set(stats)

    db_firebase.reference('stats/source') \
        .set({"num_sources": num_sources})

    print("Done in Init counting tags")
