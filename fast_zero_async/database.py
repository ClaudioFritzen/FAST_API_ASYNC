from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fast_zero_async.settings import settings  # importa a instância única

engine = create_async_engine(settings.DATABASE_URL, echo=False)


async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
