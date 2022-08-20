from typing import Any

from fastapi import APIRouter
from fastapi import Depends

from authix.core.config import AuthConfig
from authix.core.service_container import ServiceContainer
from authix.domain.authentication.service import AuthResponse
from authix.domain.authentication.service import AuthenticationService
from authix.domain.client.service import ClientImplementationService
from authix.domain.key.service import KeyService
from authix.domain.registration.service import RegistrationService
from authix.domain.revocation.service import RevocationService

auth_router = APIRouter(tags=["Authentication"])

service_manager = ServiceContainer(config=AuthConfig())
AUTH_SERVICE = Depends(service_manager.authentication_service)
REVOCATION_SERVICE = Depends(service_manager.revocation_service)
CLIENT_IMPLEMENTATION_SERVICE = Depends(service_manager.client_implementation_service)
REGISTRATION_SERVICE = Depends(service_manager.registration_service)
KEY_SERVICE = Depends(service_manager.key_service)


@auth_router.post("/login", response_model=AuthResponse)
async def login(email: str, password: str, service: AuthenticationService = AUTH_SERVICE) -> AuthResponse:
    """Authenticate a user by creating a new refresh token, that can be used to create new JWTs."""
    return await service.authenticate(email=email, password=password)


@auth_router.delete("/logout", response_model=None)
async def logout(refresh_token: str, service: RevocationService = REVOCATION_SERVICE) -> None:
    """Log a user out by deleting their refresh token, and broadcasting a revoke event."""
    return await service.revoke(refresh_token=refresh_token)


@auth_router.post("/access_token", response_model=str)
async def create_access_token(refresh_token: str, service: AuthenticationService = AUTH_SERVICE) -> str:
    """Create a new JWT access token from a refresh token."""
    return await service.create_access_token(refresh_token=refresh_token)


@auth_router.get("/test", response_model=dict[str, Any])
async def test_access_token(
    access_token: str,
    service: ClientImplementationService = CLIENT_IMPLEMENTATION_SERVICE,
) -> dict[str, Any]:
    """Client implementation of Auth Service."""
    return await service.client_implementation(access_token=access_token)


@auth_router.post("/register", response_model=None)
async def register(
    email: str,
    password: str,
    service: RegistrationService = REGISTRATION_SERVICE,
) -> None:
    await service.register(email=email, password=password)


@auth_router.get("/public_key", response_model=str)
async def public_get(service: KeyService = KEY_SERVICE) -> str:
    return service.get_public_key()
