from pydobby.server import HTTPServer
from pydobby.http import HTTPRequest, HTTPResponse
import json 
import logging

server = HTTPServer()

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        logging.info(f"Response: {response.status_code}")
        return response

server.register_middleware(LoggingMiddleware)


@server.get("/hello")
def home(request: HTTPRequest) -> HTTPResponse:
    data = f"hello anon"
    headers = {
        "Server": "pydobby"
    }
    return HTTPResponse(body=data, headers=headers, content_type="text/plain")

@server.get("/hello/<name>")
def home(request: HTTPRequest, name) -> HTTPResponse:
    data = f"hello {name}!"
    return HTTPResponse(body=data)

@server.post("/submit")
def submit(request: HTTPRequest) -> HTTPResponse:
    data = json.loads(request.body)
    print(data)
    return HTTPResponse(status_code=201)

if __name__ == "__main__":
    server.start()
