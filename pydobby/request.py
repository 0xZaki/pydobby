import logging
from urllib.parse import parse_qs, urlparse


class HTTPRequest:
    def __init__(self, raw_data: str):
        self.method = ""
        self.path = ""
        self.headers = {}
        self.body = ""
        self.query_params = {}
        self.is_valid = True
        self._parse_request(raw_data)

    def _parse_request(self, raw_data: str):
        try:
            # get header and body
            header_section, *body_section = raw_data.split("\r\n\r\n")
            request_lines = header_section.split("\r\n")
            # parse request line
            if request_lines:
                self._parse_request_line(request_lines[0])
            else:
                self.is_valid = False
                return

            # parse headers
            for line in request_lines[1:]:
                if ":" in line:
                    key, value = line.split(":", 1)
                    self.headers[key.strip().lower()] = value.strip()

            self.body = body_section[0] if body_section else ""

        except Exception as e:
            logging.error(f"Error parsing request: {e}")
            self.is_valid = False

    def _parse_request_line(self, request_line: str):
        try:
            method, path, _ = request_line.split(" ")
            self.method = method.upper()
            url = urlparse(path)
            self.path = url.path
            self.query_params = parse_qs(url.query)
        except Exception as e:
            logging.error(f"Error parsing request line: {e}")
            self.is_valid = False
