import socket
import threading
import logging
from urllib.parse import urlparse, parse_qs

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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


class TCPServer:
    def __init__(self, host='0.0.0.0', port=8001):
        self.host = host
        self.port = port

        # refer to https://docs.python.org/3/library/socket.html (unix sockets)
        self.server_socket = socket.socket(family=socket.AF_INET,type = socket.SOCK_STREAM)

        # allow reuse of the same address if socket is in TIME_WAIT state
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        """Start TCP server"""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            logging.info(f"server started >> {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.server_socket.accept()
                logging.info(f"new connection: {address}")
                
                # start a thread to handle client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.start()
                
        except Exception as e:
            logging.error(f"server error: {e}")
            self.stop()

    def handle_client(self, client_socket, address):
        """Handle client connections"""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8')
                request = HTTPRequest(message)
                print(request.body,'====request body')
                print(request.query_params,'====query params')
                print(request.headers,'======headers')
                print(request.path,'======path')
                logging.info(f"Received from {address}: {message}")
                
                response = f"Server received: {message}"
                client_socket.send(response.encode('utf-8'))
                
        except Exception as e:
            logging.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed with {address}")

    def stop(self):
        """close server socket"""
        self.server_socket.close()
        logging.info("Server stopped")

if __name__ == "__main__":
    server = TCPServer()
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("Server shutdown requested")
        server.stop()
