from pydantic import BaseModel


class StartGame(BaseModel):
    player: str


class Game(BaseModel):
    player1: str
    player2: str
