from http import HTTPStatus

import pytest

from fast_zero_async.schemas import UserPublicSchema


def test_root_deve_retornar_ola_mundo(client):

    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_exercicio_ola_mundo_html(client):
    response = client.get('/exercicio-html')
    assert response.status_code == HTTPStatus.OK
    assert '<h1 style="color:blue;">Olá Mundo!</h1>' in response.text


@pytest.mark.xfail(
    reason='Foi implementado o token e com isso'
    ' sempre teremos um usuario autenticado'
)
def test_read_users_without_users(client, token):
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'users': []}


def test_read_users_with_users(client, user, token):
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    user_schema = UserPublicSchema.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'users': [user_schema]}


def test_update_user_deve_atualizar_usuario(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'newpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


@pytest.mark.xfail(
    reason='Foi implementado que temos que estar autenticado,'
    ' para fazer qualquer alteração'
)
def test_update_user_deve_retornar_404_quando_usuario_nao_existir(
    client,
    user,
):
    response = client.put(
        '/users/999',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_must_return_401_when_is_not_authenticated(
    client,
    user,
):
    response = client.put(
        '/users/999',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_update_user_must_return_403_when_try_update_another_user(
    client,
    user,
    token,
):
    response = client.put(
        '/users/999',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to update this user'
    }


def test_delete_user_deve_deletar_usuario(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_must_return_403_when_try_delete_another_user(
    client, user, token
):
    response = client.delete(
        '/users/999', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to update this user'
    }


def test_update_user_integrity_error(client, user, token):

    # Create another user to cause integrity error
    # Inserindo fausto
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user das fixture para fausto
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Username or email already registered'
    }


def test_create_user_integrity_error_name(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'teste2@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already registered'}


def test_create_user_integrity_error_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Email 2',
            'email': 'teste@test.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already registered'}


def test_find_user_by_id_return_user(client, user):

    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    assert response.json() == user_schema


def test_find_user_by_id_return_404_when_not_found(client):

    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_token_return_token_when_credentials_are_valid(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'bearer'


def test_get_token_return_401_when_user_not_found(client):

    response = client.post(
        'token', data={'username': 'nouser', 'password': 'nopass'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_return_401_when_password_is_incorrect(client, user):
    response = client.post(
        '/token', data={'username': user.email, 'password': 'wrongpass'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
