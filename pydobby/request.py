import logging
from urllib.parse import parse_qs, urlparse
import re


class HTTPRequest:
    def __init__(self, raw_data: str):
        self.method = ""
        self.path = ""
        self.headers = {}
        self.body = ""
        self.query_params = {}
        self.cookies = {}
        self.is_valid = True
        self._parse_request(raw_data)

    def _parse_request(self, raw_data: str):
        try:
            parts = raw_data.split("\r\n\r\n")
            if len(parts) < 2:
                self.is_valid = False
                return

            header_section, body_section = parts
            request_lines = header_section.split("\r\n")

            # parse request line
            if request_lines:
                if not self._parse_request_line(request_lines[0]):
                    self.is_valid = False
                    return
            else:
                self.is_valid = False
                return

            # parse headers
            self._parse_headers(request_lines[1:])

            self.body = body_section

        except Exception as e:
            logging.error(f"Error parsing request: {e}")
            self.is_valid = False
            return

    def _parse_request_line(self, request_line: str):
        VALID_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"}

        components = request_line.split(" ")
        if len(components) < 3:
            return False

        method, path, version = components
        self.method = method.upper()
        if self.method not in VALID_METHODS:
            self.is_valid = False
            return False

        url = urlparse(path)
        self.path = url.path
        self.query_params = parse_qs(url.query)

        if not re.match(r"^HTTP/\d\.\d$", version):
            return False
        return True

    def _parse_headers(self, headers: list):
        for header in headers:
            if ":" in header:
                key, value = header.split(":", 1)
                self.headers[key.strip()] = value.strip()

        if "Cookie" in self.headers:
            cookies = self.headers["Cookie"].split("; ")
            for cookie in cookies:
                name, value = cookie.split("=", 1)
                self.cookies[name.strip()] = value.strip()
