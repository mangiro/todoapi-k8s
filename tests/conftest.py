import os
import pytest
from typing import Generator

from fastapi.testclient import TestClient

from todoapp.main import app
from tests.utils.timer import Timer


@pytest.fixture(scope="function", autouse=True)
def timer() -> None:
    test_name = \
        os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].split(" ")[0]

    with Timer(test_name):
        yield
    return


@pytest.fixture(scope="function")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def session_fixture():
    try:
        os.remove("./tasks.db")
    except:
        ...
    yield
    try:
        os.remove("./tasks.db")
    except:
        ...
