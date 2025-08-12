from pydantic import BaseModel

from .feilds import PyObjectId


class MongoDbModel(BaseModel):
    class Meta:
        collection_name: str

    id: PyObjectId

    @classmethod
    def get_collection_name(cls) -> str:
        return cls.Meta.collection_name


class StartGame(BaseModel):
    player: str


class Game(MongoDbModel, BaseModel):
    class Meta:
        collection_name = "games"

    player1: str
    player2: str
