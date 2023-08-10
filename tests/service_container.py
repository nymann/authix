from authix.core.config import AuthConfig
from authix.core.service_container import ServiceContainer
from authix.data.refresh_token.queries.in_memory import InMemoryRefreshQueries
from authix.data.users.queries.in_memory import InMemoryUserQueries


class TestServiceContainer(ServiceContainer):
    __test__ = False

    def __init__(self) -> None:
        self.config = AuthConfig()  # type: ignore
        self.user_queries = InMemoryUserQueries()
        self.refresh_queries = InMemoryRefreshQueries()
