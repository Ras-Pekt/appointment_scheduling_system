from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str = "db"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
