import logging
import socket
import threading

from pydobby.request import HTTPRequest
from pydobby.response import HTTPResponse
from pydobby.router import Router


class HTTPServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port

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
