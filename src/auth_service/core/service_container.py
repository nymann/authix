from auth_service.core.config import AuthConfig
from auth_service.data.refresh_token.queries.redis import RedisRefreshQueries
from auth_service.data.revocation.queries.redis import RedisRevokeQueries
from auth_service.data.users.queries.in_memory import InMemoryUserQueries
from auth_service.domain.authentication.service import AuthenticationService
from auth_service.domain.client.service import ClientImplementationService
from auth_service.domain.key.service import KeyService
from auth_service.domain.registration.service import RegistrationService
from auth_service.domain.revocation.service import RevocationService
from auth_service.domain.token.service import TokenService


class ServiceContainer:
    def __init__(self, config: AuthConfig) -> None:
        self._config = config
        self._user_queries = InMemoryUserQueries()
        self._revoke_queries = RedisRevokeQueries(dsn=config.settings.client_redis)
        self._refresh_queries = RedisRefreshQueries(dsn=config.settings.refresh_redis)

    def authentication_service(self) -> AuthenticationService:
        return AuthenticationService(
            user_queries=self._user_queries,
            refresh_queries=self._refresh_queries,
            token_service=self.token_service(),
        )

    def revocation_service(self) -> RevocationService:
        return RevocationService(
            revoke_queries=self._revoke_queries,
            refresh_queries=self._refresh_queries,
        )

    def token_service(self) -> TokenService:
        return TokenService(key_service=self.key_service())  # noqa: S106

    def key_service(self) -> KeyService:
        return KeyService(config=self._config)

    def client_implementation_service(self) -> ClientImplementationService:
        return ClientImplementationService(
            revoke_queries=self._revoke_queries,
            token_service=self.token_service(),
        )

    def registration_service(self) -> RegistrationService:
        return RegistrationService(
            token_service=self.token_service(),
            user_queries=self._user_queries,
        )
