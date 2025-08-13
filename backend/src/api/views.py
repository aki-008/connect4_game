from fastapi import APIRouter, HTTPException, status

from .models import Game, StartGame
from .crud import (
    get_game_by_id,
    list_games_from_db,
    start_new_game,
    delete_games_from_db,
    join_new_game,
)
from .fields import PyObjectId


router = APIRouter(prefix="/games", tags=["Games"])


@router.post("/")
async def start_game(player_data: StartGame) -> Game:
    game = await start_new_game(player_data.player)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="game cannot start right now, please try again later",
        )
    return game


@router.get("/")
async def list_games() -> list[Game]:
    return await list_games_from_db()  # type: ignore[return-value]


@router.get("/{game_id}/")
async def get_game(game_id: PyObjectId) -> Game:
    game = await get_game_by_id(game_id)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="game not found",
        )
    return game


@router.delete("/")
async def delete_games() -> dict[str, int]:
    deleted_count = await delete_games_from_db()
    return {"deleted_count": deleted_count}


@router.post("/{game_id}/join/")
async def join_game(game_id: PyObjectId, player_data: StartGame) -> Game:
    game = await get_game_by_id(id=game_id)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="game not found",
        )
    if game.player2 is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="game already started",
        )
    updated_game = await join_new_game(game, player_data.player)
    if updated_game is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="game cannot start right now, please try again later",
        )
    return updated_game
