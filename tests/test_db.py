from dataclasses import asdict

from sqlalchemy import select

from fast_zero_async.models import User


def test_create_user_adiciona_usuario_ao_database(session, mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User(
            username='johndoe',
            email='johndoe@example.com',
            password='securepassword',
        )

        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'johndoe'))

    assert asdict(user) == {
        'id': 1,
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password': 'securepassword',
        'created_at': time,
        'updated_at': time,
    }
