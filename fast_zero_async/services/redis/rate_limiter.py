import time


class AsyncRateLimiter:
    """
    Docstring for AsyncRateLimiter

    ## Rate limiter para APIS.
    Limita o número de requisições por usuário em um
    determinado intervalo de tempo.

    redis_client: Cliente Redis para armazenar os dados de rate limiting.

    max_requests: Número máximo de requisições permitidas

    window: Intervalo de tempo (em segundos) para o rate limiting.

    """

    def __init__(self, redis_client, max_requests: 10, window: 60):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window

    async def allow_request(self, user_id: str) -> bool:
        """
        Verifica se uma requisição do usuário é permitida com
          base no rate limiting.

        user_id: Identificador único do usuário.

        Retorna True se a requisição for permitida, False caso contrário.
        """
        now = time.time()
        key = f'rate_limit:{user_id}'

        async with self.redis.pipeline() as pipe:
            pipe = self.redis.pipeline()
            pipe.zadd(key, {now: now})
            pipe.zremrangebyscore(key, 0, now - self.window)
            pipe.zcard(key)
            pipe.expire(key, self.window * 2)

            _, _, request_count, _ = await pipe.execute()

            result = request_count <= self.max_requests

        return result
