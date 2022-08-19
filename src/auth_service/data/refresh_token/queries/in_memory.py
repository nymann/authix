from pydantic import UUID4

from auth_service.data.query_exceptions import QueryResultNotFoundError
from auth_service.data.refresh.refresh_queries import RefreshQueries


class RefreshMemoryQueries(RefreshQueries):
    def __init__(self) -> None:
        self.db: dict[str, UUID4] = {}

    async def get_user_id(self, refresh_token: str) -> UUID4:
        try:
            return self.db[refresh_token]
        except KeyError as error:
            raise QueryResultNotFoundError from error

    async def add(self, refresh_token: str, user_id: UUID4) -> None:
        self.db[refresh_token] = user_id

    async def delete(self, refresh_token: str) -> UUID4:
        try:
            return self.db.pop(refresh_token)
        except KeyError as error:
            raise QueryResultNotFoundError from error
