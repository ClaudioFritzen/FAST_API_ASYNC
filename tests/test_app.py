from http import HTTPStatus


def test_root_deve_retornar_ola_mundo(client):

    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_exercicio_ola_mundo_html(client):
    response = client.get('/exercicio-html')
    assert response.status_code == HTTPStatus.OK
    assert '<h1 style="color:blue;">Olá Mundo!</h1>' in response.text


def test_create_user_deve_criar_usuario(client):

    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'senha': 'password123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'users': [
            {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user_deve_atualizar_usuario(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'senha': 'newpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_deve_retornar_404_quando_usuario_nao_existir(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'senha': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_deve_deletar_usuario(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_deve_retornar_404_quando_usuario_nao_existir(client):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
