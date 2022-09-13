import pytest

from authix.domain.domain_exceptions import Unauthorized
from tests.service_container import TestServiceContainer

email = "test@example.org"
password = "test123"


@pytest.mark.asyncio()
async def test_revoke_invalid_refresh_token(service_container: TestServiceContainer) -> None:
    service = service_container.revocation_service()
    with pytest.raises(Unauthorized):
        await service.revoke(refresh_token="")


@pytest.mark.asyncio()
async def test_revoke(service_container: TestServiceContainer) -> None:
    registration_service = service_container.registration_service()
    auth_service = service_container.authentication_service()
    await registration_service.register(email=email, password=password)
    auth_response = await auth_service.authenticate(email=email, password=password)
    revocation_service = service_container.revocation_service()
    await revocation_service.revoke(refresh_token=auth_response.refresh_token)
