from typing import Iterable

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from authix.api import AuthService
from tests.service_container import TestServiceContainer


@pytest.fixture
def app() -> FastAPI:
    test_service_container = TestServiceContainer()
    return AuthService(
        config=test_service_container.config,
        service_container=test_service_container,
    ).api


@pytest.fixture
def client(app: FastAPI) -> Iterable[TestClient]:
    with TestClient(app) as client:
        yield client
