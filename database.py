import asyncpg
import os
import logging
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

handler = logging.FileHandler(filename='database.log', encoding='utf-8', mode='w')

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(DB_URL)
        await self.init_tables()

    async def init_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    discord_id BIGINT PRIMARY KEY
                );
            """)

    async def user_exists(self, discord_id):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM users WHERE discord_id=$1
            """, discord_id)
            return row is not None

    async def add_user(self, discord_id):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users (discord_id) VALUES ($1)
                ON CONFLICT (discord_id) DO NOTHING
            """, discord_id)
