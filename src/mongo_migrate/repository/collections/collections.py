from pymongo import MongoClient
from pymongo.database import Database, Collection
from .models import SchemaField, Schema
from .query import get_fields
from pprint import pformat

__all__ = ["find_collections", "get_fields_collections"]


def find_collections(client: MongoClient, db_name: str) -> Database:
    db = client[db_name]
    return db


async def get_fields_collections(db: Database) -> list[Schema]:
    fields_result = []
    query_field = get_fields()
    for collection_name in db.list_collection_names():
        collection = db.get_collection(collection_name)
        batches = list(collection.aggregate(query_field))
        collection_data = Schema(name=collection_name)
        [collection_data.fields.append(SchemaField(name=batch['field'], type=batch['type'])) for batch in batches]
        fields_result.append(collection_data)
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
