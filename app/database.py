from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

# Loading the variables from our .env file into the environment
load_dotenv()

# Reading each variable from the environment
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Building the connection string PostgreSQL needs
# Format: postgresql+asyncpg://user:password@host:port/database
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Creating the engine, our connection to the database
engine = create_async_engine(DATABASE_URL, echo=True)

# Creating a session factory, generating the sessions on demand
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

#Base Class - All table models with ingerit from this
class Base(DeclarativeBase):
        pass

# This is a dependency, FastAPI will call this to get a database session
# It opens a session, yields it to the endpoint, then closes it when done
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

