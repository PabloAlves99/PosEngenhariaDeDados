import pprint
from pymongo import MongoClient
from .config import MONGO_URI, DB_NAME, COLLECTION_NAME


# client = MongoClient(
#     "mongodb://sa:oracle123@localhost:27017/salesdb?authSource=admin")
def view_content():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    for doc in collection.find().limit(5):
        pprint.pp(doc)


def drop_content():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    result = collection.delete_many({})

    print("Removidos:", result.deleted_count)


if __name__ == "__main__":
    view_content()
    # drop_content()
