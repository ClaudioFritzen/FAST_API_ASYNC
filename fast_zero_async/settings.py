from functools import lru_cache
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    TESTING: bool = False

    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_PROD_DB: str   | None = None
    POSTGRES_HOST: str = 'db_prod'
    POSTGRES_PORT: int = 5432

    SECRET_KEY: str | None = None
    ALGORITHM: str  | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = None

    @property
    def DATABASE_URL(self) -> str:
        # CI / Testes
        if self.TESTING:
            return os.getenv('DATABASE_URL')
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:'
            f'{self.POSTGRES_PORT}/{self.POSTGRES_PROD_DB}'
        )


@lru_cache
def get_settings():
    return Settings()
