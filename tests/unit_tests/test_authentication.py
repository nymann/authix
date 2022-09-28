from uuid import uuid4

import pytest
import pytest_asyncio

from authix.domain.authentication.service import AuthenticationService
from authix.domain.domain_exceptions import Unauthorized
from tests.service_container import TestServiceContainer
from tests.unit_tests.conftest import TEST_EMAIL
from tests.unit_tests.conftest import TEST_PASSWORD

str_uuid4 = str(uuid4())


@pytest_asyncio.fixture()
async def auth_service(service_container: TestServiceContainer) -> AuthenticationService:
    registration_service = service_container.registration_service()
    await registration_service.register(email=TEST_EMAIL, password=TEST_PASSWORD)
    return service_container.authentication_service()


@pytest.mark.asyncio()
async def test_authenticate(auth_service: AuthenticationService) -> None:
    auth_response = await auth_service.authenticate(email=TEST_EMAIL, password=TEST_PASSWORD)
    assert auth_response.access_token is not None
    assert auth_response.refresh_token is not None


@pytest.mark.asyncio()
async def test_authenticate_user_not_found(service_container: TestServiceContainer) -> None:
    service = service_container.authentication_service()
    with pytest.raises(Unauthorized):
        await service.authenticate(email=TEST_EMAIL, password=TEST_PASSWORD)


@pytest.mark.asyncio()
async def test_authenticate_wrong_password(auth_service: AuthenticationService) -> None:
    with pytest.raises(Unauthorized):
        await auth_service.authenticate(email=TEST_EMAIL, password="wrong123")


@pytest.mark.asyncio()
async def test_create_access_token_invalid_refresh_token(service_container: TestServiceContainer) -> None:
    auth_service = service_container.authentication_service()
    with pytest.raises(Unauthorized):
        await auth_service.create_access_token(refresh_token=str_uuid4)


@pytest.mark.asyncio()
async def test_create_access_token(auth_service: AuthenticationService) -> None:
    auth_response = await auth_service.authenticate(email=TEST_EMAIL, password=TEST_PASSWORD)
    access_token: str = await auth_service.create_access_token(refresh_token=auth_response.refresh_token)
    assert access_token is not None


@pytest.mark.asyncio()
async def test_create_access_token_valid_refresh_token_no_user(service_container: TestServiceContainer) -> None:
    random_uuid = uuid4()
    await service_container.refresh_queries.add(refresh_token=str_uuid4, user_id=random_uuid)
    service = service_container.authentication_service()

    with pytest.raises(Unauthorized):
        await service.create_access_token(refresh_token=str_uuid4)
