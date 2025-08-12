from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api.views import router as api_router  # always include the router
from .db.utils import get_mongod
from typing import AsyncGenerator


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


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello, sam World!"}
