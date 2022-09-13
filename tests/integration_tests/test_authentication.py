from http import HTTPStatus

from fastapi.testclient import TestClient

from tests.integration_tests.helpers import valid_login


def test_create_access_token_from_refresh(client: TestClient) -> None:
    _, refresh = valid_login(client=client)
    response = client.post("/access_token", cookies={"refresh_token": refresh})
    assert response.status_code == HTTPStatus.OK
