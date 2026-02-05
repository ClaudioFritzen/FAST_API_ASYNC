# app/services/redis/client.py
from redis.asyncio import Redis

redis_client = Redis(
    host='redis',  # ou "localhost" se não estiver usando Docker
    port=6379,
    db=0,
    decode_responses=True,
)
