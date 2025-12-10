from http import HTTPStatus


def test_get_token_return_token_when_credentials_are_valid(client, user):
    response = client.post(
        'auth/token',
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
        '/auth/token', data={'username': 'nouser', 'password': 'nopass'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_return_401_when_password_is_incorrect(client, user):
    response = client.post(
        'auth/token', data={'username': user.email, 'password': 'wrongpass'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
