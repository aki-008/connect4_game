from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api.views import router as api_router  # always include the router
from .db.utils import get_mongod


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongodb = get_mongod()
    app.mongodb = mongodb
    yield

    app.mongodb.client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)  # always include the router


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello, sam World!"}
