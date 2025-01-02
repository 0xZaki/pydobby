import pytest
from urllib.parse import urlencode
from pydobby import PyDobby, HTTPRequest


@pytest.fixture
def app():
    return PyDobby(port=8001)


@pytest.fixture
def make_request():
    def _make_request(method="GET", path="/", headers=None, body="", query_params=None):
        headers = headers or {}
        query_params = query_params or {}

        if query_params:
            query_string = urlencode(query_params, doseq=True)
            path = f"{path}?{query_string}"

        headers_str = "\r\n".join([f"{k}: {v}" for k, v in headers.items()])
        raw_request = (
            f"{method} {path} HTTP/1.1\r\n"
            f"Host: localhost:8001\r\n"
            f"{headers_str}\r\n"
            f"\r\n"
            f"{body}"
        )
        return HTTPRequest(raw_request)

    return _make_request
