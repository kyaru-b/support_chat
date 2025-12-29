import asyncio

import asyncpg


import logging
LOGGER = logging.getLogger("my_app.database.messages")

class Messages:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    """INSERT requests"""
    async def create_message(self, ticket_id: int, sender_id: int, text: str):
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        """ 
                        INSERT INTO messages (ticket_id, sender_id, text) VALUES ($1, $2, $3);
                        """,
                        ticket_id,
                        sender_id,
                        text
                    )
            LOGGER.info(f"Message for ticket {ticket_id} created successfully.")        
        except Exception as e:
            LOGGER.error(f"Error creating message for ticket {ticket_id}: {e}")
            return e
        
    """SELECT requests"""
    async def get_messages_by_ticket(self, ticket_id: int):
        try:
            async with self.pool.acquire() as conn:
                messages = await conn.fetch(
                    "SELECT * FROM messages WHERE ticket_id = $1;",
                    ticket_id
                )
                return messages
        except Exception as e:
            LOGGER.error(f"Error fetching messages for ticket {ticket_id}: {e}")
            return []