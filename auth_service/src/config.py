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
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class SMTPSettings(BaseSettings):
    PORT: int
    SMTP_SERVER: str
    LOGIN: str
    PASSWORD: str
    SENDER: str


settings = Settings()
jwt_settings = JWTSettings()
smtp_settings = SMTPSettings()
