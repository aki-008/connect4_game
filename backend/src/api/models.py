from pydantic import BaseModel, Field
from datetime import datetime
from ..constants import PlayerEnum
from .fields import PyObjectId


class MongoDbModel(BaseModel):
    class Meta:
        collection_name: str

    id: PyObjectId
    created_at: datetime
    updated_at: datetime

    @classmethod
    def get_collection_name(cls) -> str:
        return cls.Meta.collection_name


class StartGame(BaseModel):
    player: str


class Game(MongoDbModel):
    class Meta:
        collection_name = "games"

    player1: str = Field(max_length=20)
    player2: str | None = Field(max_length=20, default=None)

    move_number: int = 1
    board: list[list[int]]
    winner: PlayerEnum | None = None

    finished_at: datetime | None = None
