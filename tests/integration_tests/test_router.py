from starlette.status import HTTP_200_OK
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.testclient import TestClient


def valid_login(client: TestClient) -> tuple[str, str]:
    response = client.post(
        "/login",
        params={"email": "kristian@nymann.dev", "password": "test123"},
    )
    assert response.status_code == HTTP_200_OK
    content = response.json()
    jwt: str = content["jwt"]
    refresh: str = content["refresh_token"]
    return jwt, refresh


def test_jwt(client: TestClient):
    jwt, _ = valid_login(client=client)
    test_response = client.get("/test", params={"access_token": jwt})
    assert test_response.status_code == HTTP_200_OK


def test_revoke(client: TestClient):
    jwt, refresh = valid_login(client=client)
    response = client.delete("/logout", params={"refresh_token": refresh})
    assert response.status_code == HTTP_200_OK
    test_response = client.get("/test", params={"access_token": jwt})
    assert test_response.status_code == HTTP_401_UNAUTHORIZED


def test_create_jwt_from_refresh(client: TestClient):
    _, refresh = valid_login(client=client)
    response = client.post("/jwt", params={"refresh_token": refresh})
    assert response.status_code == HTTP_200_OK
