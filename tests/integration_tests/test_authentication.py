from http import HTTPStatus

from fastapi.testclient import TestClient

from tests.integration_tests.helpers import valid_login


def test_create_access_token_from_refresh(client: TestClient) -> None:
    _, refresh = valid_login(client=client)
    client.cookies.set("refresh_token", refresh)
    response = client.post("/access_token")
    assert response.status_code == HTTPStatus.OK
