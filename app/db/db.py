from contextlib import asynccontextmanager
from functools import wraps
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel import SQLModel

from app.config.settings import Settings, get_settings
from app.models import *    # noqa: F401, F403

settings: Settings = get_settings()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    Manages the lifespan of the FastAPI application by setting up and tearing
    down the database connection.

    This function creates an asynchronous SQLAlchemy engine and session
    factory, initializes the database schema, and ensures proper disposal of
    the engine when the application shuts down.
    """
    engine: AsyncEngine = create_async_engine(
        url=(
            f"postgresql+asyncpg://{settings.POSTGRES_USER}"
            f":{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}"
            f":{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        ),
        echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    global async_sessions_factory
    async_sessions_factory = async_sessionmaker(engine, expire_on_commit=False)
    yield
    await engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession]:
    """
    Creates and yields an asynchronous database session.

    This function is an asynchronous generator that creates a new database
    session using the global `async_sessions_factory`. It yields the session
    for use within an asynchronous context manager.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session object that can be
                      used for database operations.
    """
    async with async_sessions_factory() as session:
        yield session


def async_session_decorator(async_func):
    """
    A decorator that provides an asynchronous database session to the decorated
    function.

    This decorator wraps an asynchronous function and automatically creates and
    manages an asynchronous database session for it. The session is created
    using the global async_sessions_factory and is passed as a keyword
    argument to the decorated function.

    Usage:
    ------
    ```
    @async_session_decorator
    async def my_function(arg1, arg2, session: AsyncSession):
        # Use the session here
        ...
    ```
    """

    @wraps(async_func)
    async def wrapper(*args, **kwargs):
        async with async_sessions_factory() as session:
            return await async_func(*args, **kwargs, session=session)

    return wrapper
