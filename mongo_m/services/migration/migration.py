import os, sys, json, hashlib, pymongo
from pathlib import Path
from mongo_m.core import check_catalog, create_catalog, MongoDB, get_config
from mongo_m.core.inspect_module import make_module, inspect_module
from pprint import pformat, pprint
from datetime import datetime

__all__ = ["create_migration_catalog", "make_migration", "update_migration_file", 'connect_to_mongo']

PATH = Path(f"{os.getcwd()}/migration")

def create_migration_catalog():
    if not check_catalog(PATH.name):
        create_catalog(PATH.name)


async def make_migration(module_path: str):
    modules = []
    async for module in make_module(module_path):
        module = inspect_module(module)
        if module != {}:
            modules.append(module)
    modules = json.dumps(modules, indent=4)
    hash_name = hashlib.md5(modules.encode())
    file_name = f"{hash_name.hexdigest()}.json"
    with open(file=f"{PATH.name}/{file_name}", mode='w') as f:
        f.write(modules)
    return file_name

def update_migration_file(file_migration: str):
    """
    Обновляет стек выполненых миграций
    """
    file_name = f"{PATH.name}/update.json"

    try:
        with open(file=file_name, mode="r+") as f:
            file_data = f.read()
            items = json.loads(file_data)

            if len(items) == 0:
                items.append(file_migration)
            elif file_migration != items[-1]:
                items.append(file_migration)

            f.truncate(0)
            f.seek(0)
            f.write(json.dumps(items, indent=4))
            f.seekable()

    except FileNotFoundError:
        with open(file=file_name, mode="w") as f:
            f.write(json.dumps([file_migration], indent=4))

def connect_to_mongo() -> pymongo.MongoClient:
    """
    Connects to a MongoDB database using environment variables for configuration.

    Returns:
    - pymongo.database.Database: The connected MongoDB database.
    """
    config = get_config()
    return MongoDB(config.get("MONGO", "host"),
                   config.get("MONGO", "port"),
                   config.get("MONGO", "user"),
                   config.get("MONGO", "password"))

def get_collection() -> pymongo.collection.Collection:
    config = get_config()
    db_name = os.getenv("MONGO_DB")
    client = connect_to_mongo()
    db = collections.find_collections(client, db_name)
    db_collections = collections.get_fields_collections(db)
    print(db_collections)