from http import HTTPStatus

from fast_zero_async.schemas import UserPublicSchema


def test_root_deve_retornar_ola_mundo(client):

    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_exercicio_ola_mundo_html(client):
    response = client.get('/exercicio-html')
    assert response.status_code == HTTPStatus.OK
    assert '<h1 style="color:blue;">Olá Mundo!</h1>' in response.text


def test_read_users_without_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    response = client.get('/users/')
    user_schema = UserPublicSchema.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'users': [user_schema]}


def test_update_user_deve_atualizar_usuario(client, user):
    response = client.put(
        f'/users/{user.id}',
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


def test_update_user_deve_retornar_404_quando_usuario_nao_existir(
    client, user
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


def test_delete_user_deve_deletar_usuario(client, user):
    response = client.delete(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_deve_retornar_404_quando_usuario_nao_existir(
    client, user
):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_integrity_error(client, user):

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
