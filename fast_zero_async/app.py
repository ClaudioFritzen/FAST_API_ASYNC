import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from prometheus_fastapi_instrumentator import Instrumentator

from fast_zero_async.config import TESTING
from fast_zero_async.middlewares.rate_limiter_middleware import (
    rate_limit_middleware,
)
from fast_zero_async.routers import (
    auth,
    todos,
    users,
)
from fast_zero_async.schemas import (
    Message,
)

if sys.platform == 'win32' and not TESTING:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

""" @asynccontextmanager
async def lifespan(app: FastAPI):

    yield
 """

app = FastAPI(title='Fast Zero Async', version='0.1.0')  # lifespan=lifespan)

Instrumentator(should_instrument_requests_inprogress=False).instrument(
    app
).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Liberando qualquer origem (localhost/127.0.0.1)
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
if not TESTING:
    from fast_zero_async.services.redis.client import redis_client
    from fast_zero_async.services.redis.rate_limiter import AsyncRateLimiter

    print('📌 [app.py] redis_client importado =', redis_client)

    app.state.limiter = AsyncRateLimiter(redis_client, 50, 90)
else:
    limiter = None

print('VALOR DE TESTING NO APP:', TESTING)

# 🔥 SÓ DEPOIS REGISTRA O MIDDLEWARE
app.middleware('http')(rate_limit_middleware)

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
