from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    # Variáveis do banco
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PROD_DB: str
    POSTGRES_HOST: str = 'db_prod'
    POSTGRES_PORT: int = 5432

    # Segurança
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DATABASE_URL(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:'
            f'{self.POSTGRES_PORT}/{self.POSTGRES_PROD_DB}'
        )


settings = Settings()
