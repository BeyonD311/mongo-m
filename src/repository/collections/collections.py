from pymongo import MongoClient
from pymongo.database import Database, Collection
from .models import SchemaField, Schema
from pprint import pformat

__all__ = ["find_collections", "get_fields_collections"]


def find_collections(client: MongoClient, db_name: str) -> Database:
    db = client[db_name]
    return db


async def get_fields_collections(db: Database) -> list[Schema]:
    fields_result = []
    tasks = []
    for collection_name in db.list_collection_names():
        collection = db.get_collection(collection_name)
        batches = collection.aggregate([
            {"$project": {"fields": {"$objectToArray": "$$ROOT"}}},
            {"$unwind": "$fields"},
            {"$group": {"_id": None, "fields": {"$addToSet": "$fields.k"}}}
        ])
        collection_data = Schema(name=collection_name)
        [collection_data.fields.append(SchemaField(name=name)) for name in next(batches)["fields"]]
        fields_result.append(collection_data)
        await get_fields_info(collection, collection_data.fields)

    return fields_result


async def get_fields_info(collection: Collection, fields: list[SchemaField]) -> list[SchemaField]:
    pipeline = [{"$project": {f.name: {"$type": "$" + f.name}}} for f in fields]
    if len(pipeline) == 0:
        return []

    result = list(collection.aggregate(pipeline))
    filter(lambda f: f.name in f, result)
    for item in result:
        for field, data_type in item.items():
            print("Поле: {}, Тип данных: {}".format(field, data_type))
