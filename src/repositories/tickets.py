import asyncpg

import asyncio

import logging

LOGGER = logging.getLogger("my_app.database.users")

class Tickets:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    """INSERT requests"""

    async def create_ticket(self, user_name: str ):
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():

                    user_id = await conn.fetchrow("""
                        SELECT id FROM users WHERE username = $1;
                    """, user_name)
                    if not user_id:
                        raise Exception(f"User {user_name} not found")

                    row = await conn.fetchrow(
                        """ 
                        INSERT INTO tickets (user_id, status) VALUES ($1, $2) RETURNING id;
                        """,
                        int(user_id['id']),
                        "open"
                    )
                    ticket_id = row['id'] if row and 'id' in row else None
            LOGGER.info(f"Ticket for user {user_name} created successfully. id={ticket_id}")        
            return ticket_id
        except Exception as e:
            LOGGER.error(f"Error creating ticket for user {user_name}: {e}")
            return e
            
    async def close_ticket(self, ticket_id: int):
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        """
                        UPDATE tickets SET status = $1 WHERE id = $2;
                        """,
                        "closed",
                        ticket_id
                    )
            LOGGER.info(f"Ticket {ticket_id} closed successfully.")
        except Exception as e:
            LOGGER.error(f"Error closing ticket {ticket_id}: {e}")
            return e
        
    """SELECT requests"""
    async def get_ticket_by(self, ticket_id: int = None, user_id: int = None):
        if ticket_id is not None:
            try:
                async with self.pool.acquire() as conn:
                    ticket = await conn.fetchrow(
                        "SELECT * FROM tickets WHERE id = $1;",
                        ticket_id
                    )
                    return ticket
            except Exception as e:
                LOGGER.error(f"Error fetching ticket {ticket_id}: {e}")
                return None
            
        if user_id is not None:
            try:
                async with self.pool.acquire() as conn:
                    tickets = await conn.fetchrow(
                        "SELECT * FROM tickets WHERE user_id = $1;",
                        user_id
                    )
                    return tickets
            except Exception as e:
                LOGGER.error(f"Error fetching tickets for user {user_id}: {e}")
                return []

    async def get_open_ticket(self, user_id: int):
        try:
            async with self.pool.acquire() as conn:
                ticket = await conn.fetchrow(
                    "SELECT * FROM tickets WHERE user_id = $1 AND status = 'open';",
                    user_id
                )
                return ticket
        except Exception as e:
            LOGGER.error(f"Error fetching open ticket for user {user_id}: {e}")
            return None
            
