import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/student_db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# Supabase requires SSL but the asyncpg driver doesn't support the "?sslmode" URL text.
# We split the URL to remove the query parameters, and pass ssl="require" instead.
if "supabase.com" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        connect_args={
            "ssl": "require",
            "prepared_statement_cache_size": 0,
            "statement_cache_size": 0
        }
    )
else:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        connect_args={
            "prepared_statement_cache_size": 0,
            "statement_cache_size": 0
        }
    )
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
# generator - uses yield and after it uses it can be used in try block 
# after the use it is closed
# prevents the memory leek , connection to db is closed properly
# it creates session for each request and closes it after the request
# ensures that each request has its own session