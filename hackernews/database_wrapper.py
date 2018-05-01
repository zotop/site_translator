import os
import pymongo

MONGODB_URI = os.environ.get('MONGODB_URI')
DATABASE_NAME = 'hackernews'

class DatabaseWrapper(object):

    def __init__(self, uri = MONGODB_URI, database_name = DATABASE_NAME):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[database_name]

    def upsert_stories(self, stories):
        return self.upsert_many(stories, 'stories')

    def upsert_comments(self, comments):
        return self.upsert_many(comments, 'comments')

    def upsert_many(self, documents, collection_name):
        requests = [pymongo.UpdateOne({'id': document['id']}, {"$set": document}, True) for document in documents]
        return self.db[collection_name].bulk_write(requests)
