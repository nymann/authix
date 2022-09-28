import pytest

from authix.domain.domain_exceptions import Unauthorized
from tests.service_container import TestServiceContainer
from tests.unit_tests.conftest import TEST_EMAIL
from tests.unit_tests.conftest import TEST_PASSWORD


@pytest.mark.asyncio()
async def test_revoke_invalid_refresh_token(service_container: TestServiceContainer) -> None:
    service = service_container.revocation_service()
    with pytest.raises(Unauthorized):
        await service.revoke(refresh_token="")


@pytest.mark.asyncio()
async def test_revoke(service_container: TestServiceContainer) -> None:
    registration_service = service_container.registration_service()
    auth_service = service_container.authentication_service()
    await registration_service.register(email=TEST_EMAIL, password=TEST_PASSWORD)
    auth_response = await auth_service.authenticate(email=TEST_EMAIL, password=TEST_PASSWORD)
    revocation_service = service_container.revocation_service()
    await revocation_service.revoke(refresh_token=auth_response.refresh_token)
