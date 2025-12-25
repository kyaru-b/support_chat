import asyncpg

import asyncio

import logging

LOGGER = logging.getLogger("my_app.database.users")

class Tickets:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

