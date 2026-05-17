import json
from datetime import datetime
from pymongo import MongoClient

from data_generator.config import (
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
)

from transform import transform_order


def serialize(obj):
    """
    Converte tipos não serializáveis em JSON (datetime, ObjectId etc.)
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)


def export_sample():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    doc = collection.find_one()

    if not doc:
        raise RuntimeError("Nenhum documento encontrado no MongoDB.")

    doc_transformado = transform_order(doc.copy())

    payload = {
        "original": doc,
        "transformado": doc_transformado,
    }

    with open("sample_order.json", "w", encoding="utf-8") as f:
        json.dump(
            payload,
            f,
            ensure_ascii=False,
            indent=4,
            default=serialize,
        )

    print("Arquivo gerado: sample_order.json")


if __name__ == "__main__":
    export_sample()
