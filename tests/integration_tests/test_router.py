from starlette.status import HTTP_200_OK
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.testclient import TestClient


def valid_login(client: TestClient) -> tuple[str, str]:
    response = client.post(
        "/login",
        params={"email": "kristian@nymann.dev", "password": "test123"},
    )
    assert response.status_code == HTTP_200_OK
    token_dict = response.json()
    access_token: str = token_dict["access_token"]
    refresh: str = token_dict["refresh_token"]
    return access_token, refresh


def test_access_token(client: TestClient) -> None:
    access_token, _ = valid_login(client=client)
    test_response = client.get("/test", params={"access_token": access_token})
    assert test_response.status_code == HTTP_200_OK


def test_revoke(client: TestClient) -> None:
    access_token, refresh = valid_login(client=client)
    response = client.delete("/logout", params={"refresh_token": refresh})
    assert response.status_code == HTTP_200_OK
    test_response = client.get("/test", params={"access_token": access_token})
    assert test_response.status_code == HTTP_401_UNAUTHORIZED


def test_create_access_token_from_refresh(client: TestClient) -> None:
    _, refresh = valid_login(client=client)
    response = client.post("/access_token", params={"refresh_token": refresh})
    assert response.status_code == HTTP_200_OK
