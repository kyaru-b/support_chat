import asyncio

import asyncpg

import logging

LOGGER = logging.getLogger("my_app.database.users")

class Users:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool


    async def create_user(self, username: str, email: str, role: str):
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        """ 
                        INSERT INTO users (username, mail, role) VALUES ($1, $2, $3);
                        """,
                        username,
                        email,
                        role
                    )
            LOGGER.info(f"User {username} created successfully.")        
        except Exception as e:
            LOGGER.error(f"Error creating user {username}: {e}")
            return None       
    

    async def get_user_by_username(self, username: str):
        try:
            async with self.pool.acquire() as conn:
                user = await conn.fetchrow(
                    "SELECT * FROM users WHERE username = $1;",
                    username
                )
                return user
        except Exception as e:
            LOGGER.error(f"Error fetching user {username}: {e}")
            return None
    
    async def get_all_users(self):
        try:
            async with self.pool.acquire() as conn:
                users = await conn.fetch("SELECT * FROM users;")
                return users
        except Exception as e:
            LOGGER.error(f"Error fetching all users: {e}")
            return []