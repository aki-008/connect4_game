from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from ..pet_project.settings import (
    settings,
)  # correct import for importing the settings variable from the backen/src/pet_project/settings.py \
# not the correct import statement :- from ..pet_project import settings


def get_mongod() -> AsyncDatabase:
    client = AsyncMongoClient(settings.MONGO_DB_URL)
    return client[settings.MONGO_DB_NAME]
