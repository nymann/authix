from http import HTTPStatus
from typing import Optional
from uuid import uuid4

from fastapi.testclient import TestClient


def valid_login(
    client: TestClient,
    email: Optional[str] = None,
    password: Optional[str] = None,
) -> tuple[str, str]:
    email = email or random_email()
    password = password or random_password()

    register(client=client, email=email, password=password)
    response = client.post("/login", json={"email": email, "password": password})
    assert response.status_code == HTTPStatus.OK
    access_token: str = response.headers["Authorization"].split(" ")[1]
    refresh: str = response.cookies["refresh_token"]
    return access_token, refresh


def register(client: TestClient, email: str, password: str) -> int:
    return client.post("/register", json={"email": email, "password": password}).status_code


def random_email() -> str:
    return f"{uuid4()}@example.org"


def random_password() -> str:
    return f"{uuid4()}!Aa"
