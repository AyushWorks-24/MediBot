import asyncio
import asyncpg
from config import settings

async def migrate():
    db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(db_url)
    
    try:
        await conn.execute("""
            ALTER TABLE chat_messages
            ADD COLUMN IF NOT EXISTS session_id VARCHAR REFERENCES chat_sessions(id);
        """)
        print("✓ chat_messages session_id FK ensured")
    finally:
        await conn.close()
        print("Done.")

asyncio.run(migrate())