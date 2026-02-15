from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero_async.models import User


@pytest.mark.asyncio
async def test_create_user_adiciona_usuario_ao_database(
    session: AsyncSession, mock_db_time
):

    with mock_db_time(model=User) as time:
        new_user = User(
            username='johndoe',
            email='johndoe@example.com',
            password='securepassword',
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    user = await session.scalar(select(User).where(User.username == 'johndoe'))

    assert asdict(user) == {
        'id': user.id,
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password': 'securepassword',
        'created_at': time,
        'updated_at': time,
        'todos': [],
    }
