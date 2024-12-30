import json
import logging

from pydobby import HTTPRequest, HTTPResponse, PyDobby

app = PyDobby(port=8001)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        logging.info(f"Response: {response.status_code}")
        return response


app.register_middleware(LoggingMiddleware)


@app.get("/hello")
def home(request: HTTPRequest) -> HTTPResponse:
    data = "hello anon"
    headers = {"Server": "pydobby"}
    return HTTPResponse(body=data, headers=headers, content_type="text/plain")


@app.get("/hello/<name>")
def hello(request: HTTPRequest, name) -> HTTPResponse:
    data = f"hello {name}!"
    return HTTPResponse(body=data)


@app.post("/submit")
def submit(request: HTTPRequest) -> HTTPResponse:
    data = json.loads(request.body)
    logging.info(data)
    return HTTPResponse(status_code=201)


if __name__ == "__main__":
    app.start()
