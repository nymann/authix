from auth_service.api import AuthService
from auth_service.core.config import AuthConfig

api = AuthService(config=AuthConfig()).api
