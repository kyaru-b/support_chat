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
                
                    await conn.execute(
                        """ 
                        INSERT INTO tickets (user_id, status) VALUES ($1, $2);
                        """,
                        user_id,
                        "open"
                    )
            LOGGER.info(f"Ticket for user {user_name} created successfully.")        
        except Exception as e:
            LOGGER.error(f"Error creating ticket for user {user_name}: {e}")
            return None
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
            
