import pytest

from authix.data.users.model import UserModel
from authix.domain.domain_exceptions import Conflict
from tests.service_container import TestServiceContainer

email = "test@example.org"
password = "testing123"


@pytest.mark.asyncio()
async def test_register_positive(service_container: TestServiceContainer) -> None:
    service = service_container.registration_service()
    await service.register(email=email, password=password)
    user: UserModel = await service_container.user_queries.get_user_by_email(email=email)
    assert user.email == email
    assert user.id is not None


@pytest.mark.asyncio()
async def test_user_already_exists(service_container: TestServiceContainer) -> None:
    await service_container.user_queries.add_user(email=email, password_hash="")
    service = service_container.registration_service()
    with pytest.raises(Conflict) as exception_info:
        await service.register(email=email, password=password)
    assert f"User with email: {email} already exists." in str(exception_info)
