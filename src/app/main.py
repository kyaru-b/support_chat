import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

logger = logging.getLogger("my_app")
logger.setLevel(logging.INFO)


formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
# Логирование в файл
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)

# Логирование в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App starting...")
    yield
    logger.info("App shutting down...")


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=80, reload=True)