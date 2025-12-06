import pytest
from fastapi.testclient import TestClient

from fast_zero_async.app import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
