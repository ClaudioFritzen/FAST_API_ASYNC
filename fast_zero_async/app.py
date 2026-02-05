import asyncio
import sys
from http import HTTPStatus
from urllib.request import Request

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from fast_zero_async.config import TESTING
from fast_zero_async.routers import (
    auth,
    todos,
    users,
)
from fast_zero_async.schemas import (
    Message,
)
from fast_zero_async.services.redis.client import redis_client
from fast_zero_async.services.redis.rate_limiter import AsyncRateLimiter

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title='Fast Zero Async', version='0.1.0')
limiter = AsyncRateLimiter(redis_client, 10, 60)  # sera removido depois

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.middleware('http')
async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware de rate limitin para todas as rotas

    """
    print("MIDDLEWARE CHAMADO!", request.url.path)
    if TESTING:
        return await call_next(request)
    
    user_id = request.headers.get('X-User-ID', 'anonymous')
    allowed = await limiter.allow_request(user_id)

    if not allowed:
        return JSONResponse(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            content={'detail': 'Limite de requisições excedido.'},
        )
    response = await call_next(request)
    return response


# fastzero/app.py
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
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
