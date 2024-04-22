import asyncio
import os, sys, importlib
from importlib import util
from pprint import pformat

from dotenv import load_dotenv
import pymongo
import pymongo.database as mongo_db
from pathlib import Path
from .core import MongoDB
from .repository import collections

from .services.migration import create_migration_catalog

load_dotenv()
PATH = Path(__file__).parent.resolve()


async def connect_to_mongo() -> pymongo.MongoClient:
    """
    Connects to a MongoDB database using environment variables for configuration.

    Returns:
    - pymongo.database.Database: The connected MongoDB database.
    """

    host = os.getenv("MONGO_HOST")
    port = os.getenv("MONGO_PORT")
    pwd = os.getenv("MONGO_PASSWORD")
    user = os.getenv("MONGO_USER")
    return MongoDB(host, int(port), user, pwd)


async def main():
    '''
    path = Path(f"{os.getcwd()}/../db_schemas_text.py")
    p = util.spec_from_file_location("read", path)
    module = util.module_from_spec(p)
    p.loader.exec_module(module)
    '''
    print(sys.argv)
    # db_name = os.getenv("MONGO_DB")
    # client = await connect_to_mongo()
    # db = collections.find_collections(client, db_name)
    # db_collections = await collections.get_fields_collections(db)
    # print(db_collections)
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