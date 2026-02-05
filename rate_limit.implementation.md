# 📘 Implementação de Rate Limiting com Redis (Async) no FastAPI
Este documento descreve passo a passo como o rate limiting foi implementado no projeto Fast Zero Async, utilizando Redis, pipelines assíncronos e um middleware global no FastAPI.

A implementação segue boas práticas de arquitetura, isolamento de responsabilidades e compatibilidade com ambientes de teste.


## 🔥 Arquitetura do Rate Limiter

<p align="center">
  <img src="docs/images/rate limit.jpeg" width="600">
</p>


### Passo a passo de como foi implementado o rate limit nesse projeto


🧱 1. Instalação da dependência
poetry add redis

📁 2. Estrutura criada
fast_zero_async/
└── services/
    └── redis/
        ├── client.py
        ├── rate_limiter.py
        └── __init__.py


#### criamos uma pasta chamada services/redis

🔌 3. Arquivo client.py

Cliente Redis assíncrono utilizado pelo rate limiter:

from redis.asyncio import Redis

redis_client = Redis(
    host="redis",  # nome do serviço no docker-compose
    port=6379,
    db=0,
    decode_responses=True,
)

🚦 4. Arquivo rate_limiter.py
Implementação do rate limiter usando Redis + Sorted Sets:

import time

class AsyncRateLimiter:
    """
    Rate limiter assíncrono baseado em Redis.
    """

    def __init__(self, redis_client, max_requests: int = 10, window: int = 60):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window

    async def allow_request(self, user_id: str) -> bool:
        now = time.time()
        key = f"rate_limit:{user_id}"

        async with self.redis.pipeline() as pipe:
            pipe.zadd(key, {now: now})
            pipe.zremrangebyscore(key, 0, now - self.window)
            pipe.zcard(key)
            pipe.expire(key, self.window * 2)

            _, _, request_count, _ = await pipe.execute()

        return request_count <= self.max_requests


🐳 5. Adição do Redis no docker-compose.yml

redis:
  image: redis:7-alpine
  container_name: redis
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data

    
⚙️ 6. Middleware de Rate Limiting
No arquivo principal onde o FastAPI() é instanciado:



-**sempre depois do app**
app = FastAPI(title='Fast Zero Async', version='0.1.0')
limiter = AsyncRateLimiter(redis_client, 10, 60) 

from fast_zero_async.services.redis.client import redis_client
from fast_zero_async.services.redis.rate_limiter import AsyncRateLimiter
from fast_zero_async.config import TESTING

app = FastAPI(title="Fast Zero Async", version="0.1.0")
limiter = AsyncRateLimiter(redis_client, 10, 60)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    print("MIDDLEWARE CHAMADO!", request.url.path)

    if TESTING:
        return await call_next(request)

    user_id = request.headers.get("X-User-ID", "anonymous")
    allowed = await limiter.allow_request(user_id)

    if not allowed:
        return JSONResponse(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            content={"detail": "Limite de requisições excedido."},
        )

    return await call_next(request)

🚀 Futuras Melhorias
Aqui estão melhorias planejadas e desejáveis para evoluir o sistema de rate limiting.

link de referencia. 
https://dev.to/rotirotirafa/como-limitar-e-proteger-suas-apis-com-rate-limit-2n5p