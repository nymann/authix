from starlette.status import HTTP_200_OK
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.status import HTTP_409_CONFLICT
from starlette.testclient import TestClient

EMAIL = "contact@nymann.dev"
PASSWORD = "test123"  # noqa: S105 test password


def valid_login(client: TestClient) -> tuple[str, str]:
    query_params = {"email": EMAIL, "password": PASSWORD}
    register(query_params=query_params, client=client)

    response = client.post("/login", params=query_params)
    assert response.status_code == HTTP_200_OK
    access_token: str = response.headers["Authorization"].split(" ")[1]
    refresh: str = response.cookies["refresh_token"]
    return access_token, refresh


def register(query_params: dict[str, str], client: TestClient) -> None:
    response = client.post("/register", params=query_params)
    assert response.status_code in {HTTP_409_CONFLICT, HTTP_200_OK}


def test_access_token(client: TestClient) -> None:
    access_token, _ = valid_login(client=client)
    test_response = client.get("/test", headers={"Authorization": access_token})
    assert test_response.status_code == HTTP_200_OK


def test_revoke(client: TestClient) -> None:
    access_token, refresh = valid_login(client=client)
    response = client.delete("/logout", cookies={"refresh_token": refresh})
    assert response.status_code == HTTP_200_OK
    test_response = client.get("/test", headers={"Authorization": access_token})
    assert test_response.status_code == HTTP_401_UNAUTHORIZED


def test_create_access_token_from_refresh(client: TestClient) -> None:
    _, refresh = valid_login(client=client)
    response = client.post("/access_token", params={"refresh_token": refresh})
    assert response.status_code == HTTP_200_OK
