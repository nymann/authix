from authix.core.config import AuthConfig
from authix.data.refresh_token.queries.redis import RedisRefreshQueries
from authix.data.refresh_token.refresh_token_queries import RefreshQueries
from authix.data.users.queries.mongodb import MongoDBUserQueries
from authix.data.users.user_queries import UserQueries
from authix.domain.authentication.service import AuthenticationService
from authix.domain.key.service import KeyService
from authix.domain.registration.service import RegistrationService
from authix.domain.revocation.publisher import RevocationPublisher
from authix.domain.revocation.publishers.kafka_publisher import RevocationKafkaPublisher
from authix.domain.revocation.service import RevocationService
from authix.domain.token.service import TokenService


class ServiceContainer:
    def __init__(self, config: AuthConfig) -> None:
        self.config = config
        self.user_queries: UserQueries = MongoDBUserQueries(config=config)
        self.refresh_queries: RefreshQueries = RedisRefreshQueries(dsn=config.refresh_redis)

    def authentication_service(self) -> AuthenticationService:
        return AuthenticationService(
            user_queries=self.user_queries,
            refresh_queries=self.refresh_queries,
            token_service=self.token_service(),
        )

    def revocation_service(self) -> RevocationService:
        return RevocationService(
            refresh_queries=self.refresh_queries,
            revocation_publisher=self._revocation_publisher(),
        )

    def token_service(self) -> TokenService:
        return TokenService(key_service=self.key_service())  # noqa: S106

    def key_service(self) -> KeyService:
        return KeyService(config=self.config)

    def registration_service(self) -> RegistrationService:
        return RegistrationService(
            token_service=self.token_service(),
            user_queries=self.user_queries,
            config=self.config,
        )

    def _revocation_publisher(self) -> RevocationPublisher:
        if self.config.revocation is not None:
            return RevocationKafkaPublisher(config=self.config.revocation)
        return RevocationPublisher()
