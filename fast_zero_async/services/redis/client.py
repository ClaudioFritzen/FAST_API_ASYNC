# app/services/redis/client.py
from redis.asyncio import Redis

redis_client = Redis(
    host='redis',  # ou "redis" se estiver rodando o Backend via Docker
    port=6379,
    db=0,
    socket_connect_timeout=2,
    decode_responses=True,
)
