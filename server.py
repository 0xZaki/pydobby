import socket
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
                print(data,'dataa')
                if not data:
                    break
                
                message = data.decode('utf-8')
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
