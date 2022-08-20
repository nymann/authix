from typing import Iterable

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from authix.api import AuthService
from authix.core.config import AuthConfig


@pytest.fixture
def app() -> FastAPI:
    return AuthService(config=AuthConfig()).api


@pytest.fixture
def client(app: FastAPI) -> Iterable[TestClient]:
    with TestClient(app) as client:
        yield client
