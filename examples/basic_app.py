import json
import logging

from pydobby import HTTPRequest, HTTPResponse, PyDobby

app = PyDobby(port=8001)

# configure static folder
static_folder = "static"
app.serve_static(static_folder)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        logging.info(f"Response: {response.status_code}")
        return response


app.register_middleware(LoggingMiddleware)


# serve static files
@app.get("/static/<path>")
def serve_static(request: HTTPRequest, path: str) -> HTTPResponse:
    return app.get_static_file(path)


@app.get("/hello")
def home(request: HTTPRequest) -> HTTPResponse:
    if request.cookies.get("name"):
        data = f"hello {request.cookies['name']}!"
    else:
        data = "hello anon"
    headers = {"Server": "pydobby"}
    return HTTPResponse(body=data, headers=headers, content_type="text/plain")


@app.get("/hello/<name>")
def hello(request: HTTPRequest, name) -> HTTPResponse:
    data = f"hello {name}!"
    headers = {"Server": "pydobby"}
    res = HTTPResponse(body=data, headers=headers, content_type="text/plain")
    res.set_cookie(
        "name", name, max_age=3600, path="/", secure=True, httponly=True, samesite="Lax"
    )
    return res


@app.post("/submit")
def submit(request: HTTPRequest) -> HTTPResponse:
    data = json.loads(request.body)
    logging.info(data)
    return HTTPResponse(status_code=201)


if __name__ == "__main__":
    app.start()
