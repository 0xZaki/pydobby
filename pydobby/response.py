class HTTPResponse:
    STATUS_CODES = {
        200: "OK",
        201: "Created",
        204: "No Content",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
    }

    def __init__(
        self,
        status_code=200,
        body: str = "",
        headers: dict = None,
        content_type: str = "text/plain",
    ):
        self._validate_status_code(status_code)
        self.status_code = status_code
        self.body = body
        self.status_text = self.STATUS_CODES.get(status_code, "temp")
        self.content_type = content_type
        self.headers = {}
        if headers:
            self.headers.update(headers)

        if body:
            if "Content-Type" not in self.headers:
                self.headers["Content-Type"] = content_type
            elif self.headers["Content-Type"] != content_type:
                raise ValueError(
                    "Content-Type header must be the same as the content_type argument"
                )
            self.headers["Content-Length"] = str(len(self.body.encode("utf-8")))

    def _validate_status_code(self, status_code: int):
        try:
            self.status_code = int(status_code)
        except (ValueError, TypeError):
            raise TypeError("HTTP status code must be an integer.")

        if not 100 <= status_code <= 599:
            raise ValueError("status code must be between 100 and 599")

    def to_bytes(self):
        response = f"HTTP/1.1 {self.status_code} {self.status_text}\r\n"
        if self.headers:
            for header, value in self.headers.items():
                response += f"{header}: {value}\r\n"
        response += "\r\n" + self.body
        return response.encode("utf-8")
