from http import HTTPStatus
from uuid import uuid4

from fastapi.testclient import TestClient

from tests.integration_tests.helpers import valid_login
from tests.unit_tests.conftest import TEST_PASSWORD


def test_revoke(client: TestClient) -> None:
    _, refresh = valid_login(
        client=client,
        email=f"{uuid4()}@example.org",
        password=TEST_PASSWORD,
    )
    client.cookies.set("refresh_token", refresh)
    response = client.delete("/logout")
    assert response.status_code == HTTPStatus.OK
