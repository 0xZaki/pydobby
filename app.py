from pydobby.server import HTTPServer
from pydobby.http import HTTPRequest, HTTPResponse
import json 

server = HTTPServer()

@server.get("/hello")
def home(request: HTTPRequest) -> HTTPResponse:
    data = {
        "name": "John",
    }
    return HTTPResponse(body=json.dumps(data), content_type="application/json")

@server.post("/submit")
def submit(request: HTTPRequest) -> HTTPResponse:
    data = json.loads(request.body)
    print(data)
    return HTTPResponse(status_code=201)

if __name__ == "__main__":
    server.start()
