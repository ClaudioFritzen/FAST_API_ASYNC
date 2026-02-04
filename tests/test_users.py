from http import HTTPStatus

# import pytest
from fast_zero_async.schemas import UserPublicSchema
from fast_zero_async.security import get_password_hash


async def test_create_a_new_user(client):

    password = 'Cfrg!72wX@z'
    novo_usuario = {
        'username': 'testseee',
        'email': 'mail@test.com',
        'password': get_password_hash(password),
    }
    response = await client.post('/users/', json=novo_usuario)

    assert response.status_code == HTTPStatus.CREATED


async def test_read_users_with_users(client, user, token):
    response = await client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    user_schema = UserPublicSchema.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'users': [user_schema]}


async def test_update_user_deve_atualizar_usuario(client, user, token):
    response = await client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user.username,
            'email': 'bob@example.com',
            'password': 'newpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': 'bob@example.com',
        'id': user.id,
    }


async def test_update_user_must_return_401_when_is_not_authenticated(
    client,
    user,
):
    response = await client.put(
        '/users/999',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_update_user_must_return_403_when_try_update_another_user(
    client, user, token, another_user
):
    response = await client.put(
        f'/users/{another_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to update this user'
    }


async def test_delete_user_deve_deletar_usuario(client, user, token):
    response = await client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


async def test_delete_user_must_return_403_when_try_delete_another_user(
    client, another_user, token
):
    response = await client.delete(
        f'/users/{another_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to update this user'
    }


async def test_update_user_integrity_error(client, user, another_user, token):

    # Tentamos atualizar o usuario 'user' para um username que já existe
    response = await client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': another_user.username,  # já existe deve gerar conflito
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Username or email already registered'
    }


async def test_update_user_integrity_error_email(
    client, user, another_user, token
):

    # Tentamos atualizar o usuario 'user' para um email que já existe
    response = await client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',  # já existe → deve gerar conflito
            'email': another_user.email,  # já existe → deve gerar conflito
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Username or email already registered'
    }


async def test_create_user_integrity_error_name(client, user):
    # try a create a new user wtih name that already exists

    response = await client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'teste2@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already registered'}


async def test_create_user_integrity_error_email(client, user):
    # try a create a new user wtih email that already exists

    response = await client.post(
        '/users/',
        json={
            'username': 'Email 2',
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already registered'}


async def test_find_user_by_id_return_user(client, user):

    response = await client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    assert response.json() == user_schema


async def test_find_user_by_id_return_404_when_not_found(client):

    response = await client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


async def test_update_user_return_404_when_not_found(client, token):

    response = await client.put(
        '/users/999',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
