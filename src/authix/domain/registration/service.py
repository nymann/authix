from authix.core.config import AuthConfig
from authix.data.query_exceptions import UserAlreadyExistsError
from authix.data.users.user_queries import UserQueries
from authix.domain.domain_exceptions import Conflict
from authix.domain.password_validation.password_validator import PasswordValidator
from authix.domain.token.service import TokenService


class RegistrationService:
    def __init__(
        self,
        token_service: TokenService,
        user_queries: UserQueries,
        config: AuthConfig,
    ) -> None:
        self._token_service = token_service
        self._user_queries = user_queries
        self._config = config
        self._password_validator = PasswordValidator(config=config)

    async def register(self, email: str, password: str) -> None:
        self._password_validator.validate(password=password)
        password_hash = self._token_service.create_password_hash(plain_password=password)
        try:
            await self._user_queries.add_user(email=email, password_hash=password_hash)
        except UserAlreadyExistsError:
            raise Conflict(f"User with email: {email} already exists.")
