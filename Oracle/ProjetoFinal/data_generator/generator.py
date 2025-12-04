from pymongo import MongoClient
from .config import MONGO_URI, DB_NAME, COLLECTION_NAME
from .factories import generate_order


def insert_documents(qtd: int = 5000):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    docs = [generate_order() for _ in range(qtd)]
    collection.insert_many(docs)

    return len(docs)
