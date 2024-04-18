import asyncio
import os
from dotenv import load_dotenv
import pymongo
import pymongo.database as mongo_db
from pathlib import Path
from core import MongoDB
from repository import collections

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
    db_name = os.getenv("MONGO_DB")
    client = await connect_to_mongo()
    db = collections.find_collections(client, db_name)
    print(await collections.get_fields_collections(db))

if __name__ == "__main__":
    asyncio.run(main())
