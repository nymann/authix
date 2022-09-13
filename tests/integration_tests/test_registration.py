from http import HTTPStatus

from fastapi.testclient import TestClient

from tests.integration_tests.helpers import random_email
from tests.integration_tests.helpers import random_password
from tests.integration_tests.helpers import register


def test_user_already_exists(client: TestClient) -> None:
    email = random_email()
    first_status_code = register(client=client, email=email, password=random_password())
    second_status_code = register(client=client, email=email, password=random_password())
    assert first_status_code == HTTPStatus.OK
    assert second_status_code == HTTPStatus.CONFLICT
