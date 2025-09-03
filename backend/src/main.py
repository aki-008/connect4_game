from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api.views import router as api_router  # always include the router
from .db.utils import get_mongod
from typing import AsyncGenerator
from .core import init_board
from .constants import N, M
from .pet_project.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    mongodb = get_mongod()
    app.mongodb = mongodb
    if hasattr(mongodb, "client"):
        app.state.mongodb_client = mongodb.client
    else:
        app.state.mongodb_client = mongodb
    yield

    client = getattr(app.state, "mongodb_client", None)
    if client is not None:
        await client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)  # always include the router
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello, sam World!"}


# Test the board creation
test_board = init_board()
print(f"Test board dimensions: {len(test_board)}x{len(test_board[0])}")
assert len(test_board) == N, f"Expected {N} rows, got {len(test_board)}"
assert len(test_board[0]) == M, f"Expected {M} cols, got {len(test_board[0])}"
print("Board initialization test passed!")
