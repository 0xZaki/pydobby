import logging
from urllib.parse import urlparse, parse_qs


class HTTPRequest:
    def __init__(self, raw_data: str):
        self.method = ''
        self.path = ''
        self.headers = {}
        self.body = ''
        self.query_params = {}
        self._parse_request(raw_data)
    
    def _parse_request(self, raw_data: str):
        try:
            # get header and body
            header_section, *body_section = raw_data.split('\r\n\r\n')
            request_lines = header_section.split('\r\n')
            # parse request line
            if request_lines:
                self._parse_request_line(request_lines[0])

            # parse headers
            for line in request_lines[1:]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    self.headers[key.strip().lower()] = value.strip()

            self.body = body_section[0] if body_section else ''

        except Exception as e:
            logging.error(f"Error parsing request: {e}")

    def _parse_request_line(self, request_line: str):
        try:
            method, path, _ = request_line.split(' ')
            self.method = method.upper()
            url = urlparse(path)
            self.path = path
            self.query_params = parse_qs(url.query)            
        except Exception as e:
            logging.error(f"Error parsing request line: {e}")

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
        503: "Service Unavailable"
    }

    def __init__(self, status_code=200, body: str = "", headers: dict = {}):
        self._validate_status_code(status_code)
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.status_text = self.STATUS_CODES.get(status_code, "temp")
    
    def _validate_status_code(self, status_code: int):
        try:
            self.status_code = int(status_code)
        except (ValueError, TypeError):
            raise TypeError("HTTP status code must be an integer.")
        
        if not 100 <= status_code <= 599:
            raise ValueError("status code must be between 100 and 599")
    
    def to_bytes(self):
        response = f"HTTP/1.1 {self.status_code} {self.status_text}\r\n"
        for header, value in self.headers.items():
            response += f"{header}: {value}\r\n"
        response += "\r\n" + self.body
        return response.encode('utf-8')