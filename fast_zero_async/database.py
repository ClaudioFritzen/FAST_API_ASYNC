from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os

from fast_zero_async.settings import Settings

settings = Settings()

# Se estiver em testes, NÃO criar engine de produção
if settings.TESTING:
    # Engine será criado pelo conftest.py
    engine = None
else:
    engine = create_async_engine(settings.DATABASE_URL)


async def get_session():  # pragma: no cover
    if settings.TESTING:
        raise RuntimeError(
            "get_session não deve ser usado em testes; o conftest faz override."
        )

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
