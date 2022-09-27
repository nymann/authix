from http import HTTPStatus
from uuid import uuid4

from fastapi.testclient import TestClient

from tests.integration_tests.helpers import valid_login


def test_revoke(client: TestClient) -> None:
    _, refresh = valid_login(
        client=client,
        email=f"{uuid4()}@example.org",
        password="test123",
    )
    response = client.delete("/logout", cookies={"refresh_token": refresh})
    assert response.status_code == HTTPStatus.OK
