import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from repositories.main_db import db_manager
from routers import users, tickets

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("my_app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App starting...")
    await db_manager.initialization()
    yield
    await db_manager.close_pool()
    logger.info("App shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(tickets.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, log_level="info")
