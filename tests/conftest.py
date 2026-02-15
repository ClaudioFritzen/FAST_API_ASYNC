# conftest.py
import importlib
from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio

# --- REDIS PARA TESTES ---
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from fast_zero_async.database import get_session
from fast_zero_async.models import User, table_registry
from fast_zero_async.security import get_password_hash
from fast_zero_async.settings import Settings

print('📌 [conftest.py] APOS OS IMPORTS INICIANDO conftest')


@pytest_asyncio.fixture
async def client(session):
    app_module = importlib.import_module('fast_zero_async.app')
    app = app_module.app

    async def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport, base_url='http://test'
    ) as async_client:
        yield async_client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def engine():
    with PostgresContainer('postgres:15-alpine') as postgres:
        sync_url = postgres.get_connection_url()

        async_url = sync_url.replace(
            'postgresql+psycopg2://', 'postgresql+asyncpg://'
        ).replace('postgresql://', 'postgresql+asyncpg://')

        engine = create_async_engine(async_url)
        yield engine
        await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):

    # Cria tabelas
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    # abre a sessão
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    # Dropa as tabelas
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 12, 7, 12, 0, 0)):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    password = 'testtest'
    user = UserFactory(
        password=get_password_hash(password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password  # essa tecnica se chama monkey patching
    return user


@pytest_asyncio.fixture
async def another_user(session: AsyncSession):
    password = 'testtest'
    user = UserFactory(
        password=get_password_hash(password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password  # essa tecnica se chama monkey patching
    return user


@pytest_asyncio.fixture
async def token(client, user):

    response = await client.post(
        'auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    return response.json()['access_token']


@pytest.fixture
def setting():
    return Settings()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@password')
