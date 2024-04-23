import asyncio
import inspect
import os, sys, importlib
import re
from importlib import util
from pprint import pformat
from dotenv import load_dotenv
import pymongo
import pymongo.database as mongo_db
from pathlib import Path
from .repository import collections
from types import UnionType
from .core import get_default_value, create_file_ini, get_config
from .services.migration import create_migration_catalog, make_migration, update_migration_file, connect_to_mongo

load_dotenv()
PATH = Path(__file__).parent.resolve()


def create_migration():
    db_name = os.getenv("MONGO_DB")
    client = connect_to_mongo()
    db = collections.find_collections(client, db_name)
    db_collections = collections.get_fields_collections(db)
    print(db_collections)

async def update_migration():
    connect_to_mongo()

async def create_migration(module_path):
    migration_file = await make_migration(module_path)
    update_migration_file(migration_file)

async def main():
    create_migration_catalog()
    params = tuple(sys.argv[1:])
    module_path = "app/src/app/schemes"
    # module_path = "utils/schemas/db_schemas_q_service"
    if params[0] == "--create-migration":
        await create_migration(module_path)
    elif params[0] == "--update-migration":
        await update_migration()
    elif params[0] == "--init":
        create_file_ini()
    # for collection in db_collections:
    #     if collection.name == "text_queue":
    #         for field in collection.fields:
    #             print(collection.name, field.name, field.type)
    # find_collection = list(filter(lambda x: x.name in {"customer_request"}, db_collections))
    # query = {
    #     "$or": [{field.name: {"$exists": False}} for field in find_collection[0].fields]
    # }
    # set_field = {field.name for field in find_collection[0].fields}
    # get_collection = db.get_collection("customer_request").find(query)
    # for item in get_collection:
    #     fields = set_field ^ set(item.keys())
    #     update_fields = {"$set": {field: None for field in fields}}
    #     db.get_collection("customer_request").update_many(
    #         query, update_fields
    #     )

if __name__ == "__main__":
    asyncio.run(main())