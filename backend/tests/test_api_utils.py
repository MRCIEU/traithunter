from typing import Any, Dict, List, Optional, Tuple

import pytest
from starlette.testclient import TestClient

from app.main import app

params: List[Tuple[str, str, Optional[Dict[str, Any]]]] = [
    ("GET", "/ping", None),
    ("GET", "/graphql", None),
    ("GET", "/schema", None),
]


@pytest.mark.parametrize("how, route, payload", params)
def test_endpoint(how: str, route: str, payload: Optional[Dict[str, Any]]):
    with TestClient(app) as client:
        if how == "GET":
            r = client.get(route, params=payload)
        elif how == "POST":
            r = client.post(route, json=payload)
    assert r.ok
