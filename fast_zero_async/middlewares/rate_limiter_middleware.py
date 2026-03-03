from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from fast_zero_async.config import TESTING


async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware de rate limitin para todas as rotas

    """
    limiter = request.app.state.limiter
    print('🔥 MIDDLEWARE CHAMADO:', request.url.path)
    print('🔥 TESTING =', TESTING)
    print('🔥 limmiter =', limiter)

    if TESTING or limiter is None:
        print('🔥 TESTING=True → ignorando rate limit')
        return await call_next(request)

    print('🔥 TESTING=False → aplicando rate limit')
    user_id = request.headers.get('X-User-ID', 'anonymous')
    print('🔥 user_id =', user_id)
    allowed = await limiter.allow_request(user_id)
    print('🔥 allowed =', allowed)

    if not allowed:
        print('🔥 BLOQUEADO POR RATE LIMIT')
        return JSONResponse(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            content={'detail': 'Limite de requisições excedido.'},
        )
    print('🔥 PASSOU PELO RATE LIMIT')
    response = await call_next(request)
    return response
