# src/db/client_async.py
import importlib

from typing import Any, cast
from bson import ObjectId, errors as bson_errors
from fastapi import FastAPI, HTTPException
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult
from datetime import datetime, timezone
from ..api.fields import PyObjectId
from ..api.models import MongoDBModel


class MongoDBClient:
    __instance = None
    mongodb: AsyncDatabase

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            app = get_current_app()
            # app.mongodb must be set to an AsyncDatabase instance in startup
            cls.__instance.mongodb = app.mongodb  # type: ignore[attr-defined]
        return cls.__instance

    def get_collection(self, model: MongoDBModel) -> AsyncCollection:
        collection_name = model.get_collection_name()
        # prefer dict-style access for collection names with unusual characters
        return self.mongodb.get_collection(collection_name)

    async def insert(
        self, model: MongoDBModel, data: dict[str, Any]
    ) -> InsertOneResult:
        collection = self.get_collection(model)
        now = datetime.now(timezone.utc)
        data |= {"created_at": now, "updated_at": now}
        # AsyncCollection.insert_one is a coroutine — await it
        return await collection.insert_one(data)

    async def get(self, model: MongoDBModel, id: str) -> dict[str, Any]:
        _id = id
        if not isinstance(_id, ObjectId):
            try:
                _id = ObjectId(str(id))
            except (bson_errors.InvalidId, TypeError):
                raise HTTPException(status_code=400, detail="Invalid id")

        collection = self.get_collection(model)
        result = await collection.find_one({"_id": id})
        if result is None:
            return None  # type: ignore[return-value]
        result = cast(dict[str, Any], result)
        # convert MongoDB _id -> id
        result["id"] = result.pop("_id")
        return result

    async def list(self, model: MongoDBModel) -> list[dict[str, Any]]:
        collection = self.get_collection(model)
        result = collection.find({})
        games = []
        async for game in result:
            game = cast(dict[str, Any], game)
            games.append(game | {"id": game.pop("_id")})
        return games

    async def delete_many(self, model: MongoDBModel) -> DeleteResult:
        collection = self.get_collection(model)
        return await collection.delete_many({})

    async def update_one(
        self, model: MongoDBModel, id: PyObjectId, data: dict[str, Any]
    ) -> UpdateResult:
        collection = self.get_collection(model)
        data |= {"updated_at": datetime.now(timezone.utc)}
        return await collection.update_one({"_id": id}, {"$set": data})


def get_current_app() -> FastAPI:
    module = importlib.import_module("src.main")
    field = "app"
    return cast(FastAPI, getattr(module, field))
