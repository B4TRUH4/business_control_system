from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    DATABASE_URL: str

    MODE: str


class JWTSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'


settings = Settings()
jwt_settings = JWTSettings()
