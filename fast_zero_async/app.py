import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero_async.config import TESTING
from fast_zero_async.routers import (
    auth,
    todos,
    users,
)
from fast_zero_async.schemas import (
    Message,
)

if not TESTING:
    from fast_zero_async.services.redis.client import redis_client
    from fast_zero_async.services.redis.rate_limiter import AsyncRateLimiter

    print('📌 [app.py] redis_client importado =', redis_client)

    limiter = AsyncRateLimiter(redis_client, 10, 60)
else:
    limiter = None

if sys.platform == 'win32' and not TESTING:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title='Fast Zero Async', version='0.1.0')
print('VALOR DE TESTING NO APP:', TESTING)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


# fastzero/app.py
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    print('🌱 ROTA ROOT CHAMADA')
    return {'message': 'Olá Mundo!'}


@app.get('/exercicio-html', response_class=HTMLResponse)
def exercicio_aula_02():
    html_content = """
    <html>
        <head>
            <title>Exercício Aula 02</title>
        </head>
        <body>
            <h1 style="color:blue;">Olá Mundo!</h1>
            <p>Este é um exercício de FastAPI retornando HTML.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
