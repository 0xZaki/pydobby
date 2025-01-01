import logging
import mimetypes
import os
import socket
import threading

from pydobby.request import HTTPRequest
from pydobby.response import HTTPResponse
from pydobby.router import Router


class HTTPServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port
        self.static_folder = None

        # refer to https://docs.python.org/3/library/socket.html (unix sockets)
        self.server_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )

        # allow reuse of the same address if socket is in TIME_WAIT state
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.router = Router()
        self.middlewares = []

    def register_middleware(self, middleware_class):
        self.middlewares.append(middleware_class)

    # method shortcuts
    def get(self, path: str):
        return self.router.get(path)

    def post(self, path: str):
        return self.router.post(path)

    def put(self, path: str):
        return self.router.put(path)

    def delete(self, path: str):
        return self.router.delete(path)

    def serve_static(self, directory: str):
        """set the static file directory"""
        self.static_folder = os.path.abspath(directory)

    def get_static_file(self, path: str) -> HTTPResponse:
        """serve a static file from the configured directory"""
        if not self.static_folder:
            return HTTPResponse(status_code=404)

        file_path = os.path.join(self.static_folder, path.lstrip("/"))

        # prevent directory traversal
        if not os.path.abspath(file_path).startswith(self.static_folder):
            return HTTPResponse(status_code=403)

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return HTTPResponse(status_code=404)

        with open(file_path, "rb") as f:
            content = f.read()

        # get content type
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = "application/octet-stream"

        return HTTPResponse(body=content, content_type=content_type)

    def start(self):
        """Start server"""
        with self.server_socket:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            logging.info(f"server started >> {self.host}:{self.port}")
            while True:
                client_socket, address = self.server_socket.accept()
                logging.info(f"new connection: {address}")
                client_thread = threading.Thread(
                    target=self.handle_client, args=(client_socket, address)
                )
                client_thread.start()

    def handle_client(self, client_socket, address):
        """Handle client connections"""
        with client_socket:
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break

                    message = data.decode("utf-8")
                    logging.info(f"Received from {address}: {message}")

                    request = HTTPRequest(message)
                    if not request.is_valid:
                        response = HTTPResponse(400)
                    else:
                        # chain middlewares
                        handler = self.router.handle_request
                        for middleware_class in reversed(self.middlewares):
                            handler = middleware_class(handler)
                        response = handler(request)
                    return client_socket.sendall(response.to_bytes())

                except Exception as e:
                    client_socket.sendall(HTTPResponse(500).to_bytes())
                    raise RuntimeError("internal server error:", e)
