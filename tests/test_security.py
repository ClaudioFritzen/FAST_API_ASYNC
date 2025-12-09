from http import HTTPStatus

from jwt import decode

from fast_zero_async.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():

    data = {'test': 'test'}

    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['test'] == data['test']

    assert 'exp' in decoded


def test_jwt_invalid_token_raises_exception(client, user):
    response = client.delete(
        f'users/{user.id}', headers={'Authorization': 'Bearer token_invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_email_not_found_raises_exception(client, user):
    invalid_token = create_access_token(data={'sub': 'coisa@gmail.com'})
    response = client.delete(
        f'users/{user.id}',
        headers={'Authorization': f'Bearer {invalid_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_without_email_raises_exception(client, user):
    invalid_token = create_access_token(data={'nao_sub': ''})
    response = client.delete(
        f'users/{user.id}',
        headers={'Authorization': f'Bearer {invalid_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
