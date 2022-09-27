from pytest import ExitCode
from pytest import Session
from pytest import fixture

from tests.service_container import TestServiceContainer

NO_TEST_RAN_CODE = 5
SUCCESS = 0


def pytest_sessionfinish(session: Session, exitstatus: int | ExitCode) -> None:
    if exitstatus == NO_TEST_RAN_CODE:
        session.exitstatus = SUCCESS


@fixture()
def service_container() -> TestServiceContainer:
    return TestServiceContainer()
