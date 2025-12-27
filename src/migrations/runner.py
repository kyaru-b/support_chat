import asyncio
import os
import sys

# Add the project root to sys.path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# Add src to sys.path to allow imports like 'from config import ...'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.repositories.main_db import db_manager

async def run_migrations():
    print("Starting migration runner...")
    
    # Initialize the pool if it's not already initialized
    if not db_manager.pool:
        print("Pool not initialized, initializing now...")
        await db_manager.initialization()
        
    migration_file = os.path.join(os.path.dirname(__file__), '001_init.sql')

    if not os.path.exists(migration_file):
        print(f"Error: Migration file not found at {migration_file}")
        return

    with open(migration_file, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    print("Applying migrations...")
    try:
        # Acquire a connection from the pool to execute the SQL
        async with db_manager.pool.acquire() as conn:
            await conn.execute(sql)
        print("Migrations applied successfully!")
    except Exception as e:
        print(f"Error applying migrations: {e}")
    finally:
        await db_manager.close_pool()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_migrations())
