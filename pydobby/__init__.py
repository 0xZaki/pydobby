from .request import HTTPRequest
from .response import HTTPResponse
from .router import Router
from .server import HTTPServer


class PyDobby:
    def __init__(self):
        self.server = HTTPServer()

    def get(self, path):
        """Register a GET route"""
        return self.server.router.get(path)

    def post(self, path):
        """Register a POST route"""
        return self.server.router.post(path)

    def put(self, path):
        """Register a PUT route"""
        return self.server.router.put(path)

    def delete(self, path):
        """Register a DELETE route"""
        return self.server.router.delete(path)

    def register_middleware(self, middleware_class):
        """Register a middleware class"""
        self.server.register_middleware(middleware_class)

    def start(self):
        """Start the server"""
        self.server.start()
