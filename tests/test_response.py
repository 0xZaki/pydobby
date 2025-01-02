from pydobby import HTTPResponse


class TestHTTPResponse:
    def test_response_creation(self):
        response = HTTPResponse(
            body="Hello World",
            status_code=200,
            headers={"Server": "pydobby"},
            content_type="text/plain",
        )

        assert response.status_code == 200
        assert response.body == b"Hello World"
        assert response.headers["Server"] == "pydobby"
        assert response.headers["Content-Type"] == "text/plain"

    def test_cookie_setting(self):
        response = HTTPResponse(body="Hello")
        response.set_cookie(
            "session",
            "abc123",
            max_age=3600,
            path="/",
            secure=True,
            httponly=True,
            samesite="Lax",
        )

        assert "Set-Cookie" in response.headers
        cookie_header = response.headers["Set-Cookie"]
        assert "session=abc123" in cookie_header
        assert "Max-Age=3600" in cookie_header
        assert "Path=/" in cookie_header
        assert "Secure" in cookie_header
        assert "HttpOnly" in cookie_header
        assert "SameSite=Lax" in cookie_header

    def test_binary_response(self):
        binary_data = b"binary_data"
        response = HTTPResponse(
            body=binary_data, content_type="application/octet-stream"
        )

        assert response.body == binary_data
        assert response.headers["Content-Type"] == "application/octet-stream"
