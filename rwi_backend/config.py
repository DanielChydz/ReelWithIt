from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOSTNAME: str = ""
    DB_PORT: str = ""
    DB_PWD: str = ""
    DB_NAME: str = ""
    DB_USERNAME: str = ""
    SECRET_KEY: str = ""
    ENCODING_ALGORITHM: str = ""
    HASHING_ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: float = 60

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()