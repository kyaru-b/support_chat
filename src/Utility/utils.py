import random
import string
import asyncio

from repositories.main_db import db_manager


class Utils:
    def __init__(self):
        pass
    async def generate_username(self, length: int = 8) -> str:
        """
        Генерирует случайное имя пользователя.
        Пример: user_a1b2c3d4
        """
        try:

            while True:
                letters_and_digits = string.ascii_lowercase + string.digits
                rand_string = ''.join(random.choice(letters_and_digits) for _ in range(length))
                new_username = f"user_{rand_string}"
                if not await db_manager.get_user_by_username(new_username):
                    return new_username
                else:
                    continue
        except Exception as e:
            raise RuntimeError(f"Error generating username: {e}")