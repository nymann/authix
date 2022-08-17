from uuid import uuid4

from auth_service.core.config import AuthConfig
from auth_service.data.refresh.in_memory_refresh_queries import RefreshMemoryQueries
from auth_service.data.revoke.in_memory_revoke_queries import InMemoryRevokeQueries
from auth_service.data.users.in_memory_user_query import InMemoryUserQueries
from auth_service.data.users.user_model import UserModel
from auth_service.domain.authentication_service import AuthenticationService
from auth_service.domain.revocation_service import RevocationService
from auth_service.domain.token_service import TokenService


class ServiceManager:
    def __init__(self, config: AuthConfig) -> None:
        self._config = config
        self._token_service = TokenService(secret=config.settings.secret)  # noqa: S106
        seeded_user = UserModel(
            id=uuid4(),
            email="kristian@nymann.dev",
            password_hash=self._token_service.get_password_hash(plain_password="test123"),  # noqa: S106
        )
        self._user_queries = InMemoryUserQueries(seeded_users=[seeded_user])
        self._revoke_queries = InMemoryRevokeQueries()
        self._refresh_queries = RefreshMemoryQueries()
        self._authentication_service = AuthenticationService(
            user_queries=self._user_queries,
            revoke_queries=self._revoke_queries,
            refresh_queries=self._refresh_queries,
            token_service=self.token_service(),
        )
        self._revocation_service = RevocationService(
            revoke_queries=self._revoke_queries,
            refresh_queries=self._refresh_queries,
        )

    def authentication_service(self) -> AuthenticationService:
        return self._authentication_service

    def revocation_service(self) -> RevocationService:
        return self._revocation_service

    def token_service(self) -> TokenService:
        return self._token_service
