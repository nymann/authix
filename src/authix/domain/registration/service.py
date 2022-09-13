from authix.data.query_exceptions import UserAlreadyExistsError
from authix.data.users.queries.interface import UserQueries
from authix.domain.domain_exceptions import Conflict
from authix.domain.token.service import TokenService


class RegistrationService:
    def __init__(self, token_service: TokenService, user_queries: UserQueries) -> None:
        self._token_service = token_service
        self._user_queries = user_queries

    async def register(self, email: str, password: str) -> None:
        password_hash = self._token_service.get_password_hash(plain_password=password)
        try:
            await self._user_queries.add_user(email=email, password_hash=password_hash)
        except UserAlreadyExistsError:
            raise Conflict(f"User with email: {email} already exists.")
