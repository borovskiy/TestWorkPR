import os
from contextlib import asynccontextmanager

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.services.currency_services import PriceRepoService

SessionLocal = async_sessionmaker(
    bind=create_async_engine(os.environ.get("DATABASE_URL"), echo=False, ),
    expire_on_commit=False,
)

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_async_db():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

def price_repo_services(session: AsyncSession = Depends(get_db)) -> PriceRepoService:
    return PriceRepoService(session)
