import re

from pydobby.request import HTTPRequest
from pydobby.response import HTTPResponse


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path: str, method: str, handler):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.upper()] = handler
        return handler

    def get(self, path: str):
        return lambda handler: self.add_route(path, "GET", handler)

    def post(self, path: str):
        return lambda handler: self.add_route(path, "POST", handler)

    def put(self, path: str):
        return lambda handler: self.add_route(path, "PUT", handler)

    def delete(self, path: str):
        return lambda handler: self.add_route(path, "DELETE", handler)

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        handlers, params = self._match_path(request)
        if not handlers:
            return HTTPResponse(
                status_code=404,
            )
        if request.method not in handlers:
            return HTTPResponse(
                status_code=405,
            )

        return handlers[request.method](request, **params)

    def _match_path(self, request: HTTPRequest) -> dict:
        for path, handlers in self.routes.items():
            regex_path = re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", path)

            regex_path = f"^{regex_path}$"

            match = re.match(regex_path, request.path)

            if match:
                params = match.groupdict()
                return handlers, params

        return None, None
