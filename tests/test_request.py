from pydobby import HTTPRequest


class TestHTTPRequest:
    def test_request_parsing(self, make_request):
        request = make_request(
            method="GET",
            path="/hello",
            query_params={"name": "world"},
            headers={
                "Host": "localhost:8001",
                "User-Agent": "test",
                "Cookie": "session=abc123; user=john",
            },
        )

        assert request.is_valid
        assert request.method == "GET"
        assert request.path == "/hello"
        assert request.query_params == {"name": ["world"]}
        assert request.headers["host"] == "localhost:8001"
        assert request.headers["user-agent"] == "test"
        assert request.cookies == {"session": "abc123", "user": "john"}

    def test_request_with_body(self, make_request):
        request = make_request(
            method="POST",
            path="/submit",
            headers={"Content-Type": "application/json"},
            body='{"name": "test"}',
        )

        assert request.is_valid
        assert request.method == "POST"
        assert request.path == "/submit"
        assert request.body == '{"name": "test"}'

    def test_invalid_request(self):
        raw_request = "Invalid Request Format"
        request = HTTPRequest(raw_request)
        assert not request.is_valid
