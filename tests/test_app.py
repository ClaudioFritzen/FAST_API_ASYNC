from http import HTTPStatus


async def test_root_deve_retornar_ola_mundo(client):

    response = await client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


async def test_exercicio_ola_mundo_html(client):
    response = await client.get('/exercicio-html')
    assert response.status_code == HTTPStatus.OK
    assert '<h1 style="color:blue;">Olá Mundo!</h1>' in response.text
