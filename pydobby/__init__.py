from .request import HTTPRequest as HTTPRequest
from .response import HTTPResponse as HTTPResponse
from .router import Router as Router
from .server import HTTPServer
from .middlewares import CORSMiddleware as CORSMiddleware


class PyDobby:
    def __init__(self, host="127.0.0.1", port=8000, conf=None):
        self.server = HTTPServer(host, port)
        self.conf = conf if conf else {}

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
        middleware_class.app = self
        self.server.register_middleware(middleware_class)

    def serve_static(self, directory):
        """Configure the static file directory"""
        return self.server.serve_static(directory)

    def get_static_file(self, path):
        """Serve a static file from the configured directory"""
        return self.server.get_static_file(path)

    def start(self):
        """Start the server"""
        self.server.start()
