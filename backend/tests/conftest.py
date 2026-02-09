import os
import sys

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client():
    backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if backend_root not in sys.path:
        sys.path.insert(0, backend_root)

    from app.main import app

    return TestClient(app)
