from pydantic import BaseSettings

from auth_service import version


class AuthSettings(BaseSettings):
    auth_title: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class AuthConfig:
    def __init__(self) -> None:
        self.version: str = version.__version__
        self.settings: AuthSettings = AuthSettings()
