from http import HTTPStatus

from devtools import debug
from fastapi import HTTPException

from authix.core.config import AuthConfig
from authix.data.query_exceptions import UserAlreadyExistsError
from authix.data.users.queries.interface import UserQueries
from authix.domain.domain_exceptions import Conflict
from authix.domain.token.service import TokenService


class RegistrationService:
    def __init__(
        self,
        token_service: TokenService,
        user_queries: UserQueries,
        config: AuthConfig,
    ) -> None:
        self._token_service = token_service
        self._user_queries = user_queries
        self._config = config

    async def register(self, email: str, password: str) -> None:
        self.password_is_valid(password=password)
        password_hash = self._token_service.get_password_hash(plain_password=password)
        try:
            await self._user_queries.add_user(email=email, password_hash=password_hash)
        except UserAlreadyExistsError:
            raise Conflict(f"User with email: {email} already exists.")

    def password_is_valid(self, password: str) -> None:
        details: list[str] = []
        self._password_min_length(password=password, details=details)
        self._password_max_length(password=password, details=details)
        self._password_must_contain_symbols(password=password, details=details)
        self._password_must_contain_lowercase(password=password, details=details)
        self._password_must_contain_uppercase(password=password, details=details)
        self._password_must_be_ascii(password=password, details=details)
        if details:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=details)

    def _password_min_length(self, password: str, details: list[str]) -> list[str]:
        if len(password) < self._config.min_password_length:
            details.append(
                f"Minimum {self._config.min_password_length} characters.",
            )
        return details

    def _password_max_length(self, password: str, details: list[str]) -> list[str]:
        if len(password) > self._config.max_password_length:
            details.append(
                f"Maxmimum {self._config.max_password_length} characters.",
            )

        return details

    def _password_must_contain_symbols(self, password: str, details: list[str]) -> list[str]:
        symbols = self._config.password_symbols
        debug(symbols)
        count = sum(symbol in password for symbol in symbols)
        min_symbols = self._config.min_number_of_special_chars
        if count < min_symbols:
            symbol_text = "symbols" if min_symbols > 1 else "symbol"
            details.append(f"Minimum {min_symbols} {symbol_text} ('{symbols}')")
        return details

    def _password_must_contain_digits(self, password: str, details: list[str]) -> list[str]:
        min_digits = self._config.min_number_of_digits
        count = sum(c.isdigit() for c in password)
        if count < min_digits:
            details.append(f"Atleast {min_digits} digits")
        return details

    def _password_must_contain_uppercase(self, password: str, details: list[str]) -> list[str]:
        min_uppercase = self._config.min_number_of_uppercase_chars
        count = sum(c.isupper() for c in password)
        if count < min_uppercase:
            details.append(f"Atleast {min_uppercase} uppercase characters.")
        return details

    def _password_must_contain_lowercase(self, password: str, details: list[str]) -> list[str]:
        min_lowercase = self._config.min_number_of_lowercase_chars
        count = sum(c.islower() for c in password)
        if count < min_lowercase:
            details.append(f"Atleast {min_lowercase} lowercase characters.")
        return details

    def _password_must_be_ascii(self, password: str, details: list[str]) -> list[str]:
        if not password.isascii():
            offending_char_list: list[str] = []
            for p in password:
                if not p.isascii():
                    offending_char_list.append(p)
            offending_chars = "".join(offending_char_list)
            details.append(f"Must be ascii, offending chars: '{offending_chars}'")
        return details
