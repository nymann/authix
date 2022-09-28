from authix.domain.password_validation.validator import Validator


class AsciiOnlyValidator(Validator):
    def validate(self, password: str, error_details: list[str]) -> None:
        if password.isascii():
            return
        offending_char_list: list[str] = []
        for character in password:
            if not character.isascii():
                offending_char_list.append(character)
        offending_chars = "".join(offending_char_list)
        error_details.append(f"Must be ascii, offending chars: '{offending_chars}'")
