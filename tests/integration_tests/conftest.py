from typing import Iterable

from fastapi import FastAPI
import pytest
from starlette import testclient
from starlette.testclient import TestClient

from auth_service.api import AuthService
from auth_service.core.config import AuthConfig


@pytest.fixture
def app():
    return AuthService(config=AuthConfig()).api


@pytest.fixture
def client(app: FastAPI) -> Iterable[TestClient]:
    with testclient.TestClient(app) as client:
        yield client
