from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str

    DB_NAME: str
    DB_HOST: str = "localhost"

    DERIBIT_BASE_URL: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    @property
    def DB_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    @property
    def DB_URL_SYNC(self):
        return f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()