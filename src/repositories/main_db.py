import asyncpg
import logging
from config import settings

from repositories.users import Users

logger = logging.getLogger("my_app.database")

class DatabaseManager(Users):
    def __init__(self):
        self.pool = None
    
    async def initialization(self):
        """Инициализация пула подключений"""
        try:
            self.pool = await self.__create_pool()
        except Exception as e:
            logger.info(f"Error while trying to create connection pool, Error code: {e}")
        if not self.pool:
            raise RuntimeError("Database pool is None")
        logger.info("DATABASE pool is init.")
        return self
    
    async def __create_pool(self):
        """Создание пула подключений"""
        logger.info("Creating connection pool")
        try:
            pool = await asyncpg.create_pool(
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                host=settings.DB_HOST,
                min_size=5,
                max_size=10
            )
            if pool:
                logger.info("Connection pool created")
                return pool
            logger.error("Connection pool is not created")
            return None
        except Exception as e:
            logger.error(f"Error while create pool: {e}")
            raise 
    
    async def close_pool(self):
        """Закрытие пула"""
        logger.info("Process for close pool")
        if self.pool:
            await self.pool.close()
            logger.info("Pool is closed")

db_manager = DatabaseManager()

async def get_db_pool():
    if not db_manager.pool:
        raise RuntimeError("Database pool is not initialized")
    return db_manager.pool
