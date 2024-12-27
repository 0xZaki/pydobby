from pydobby.server import HTTPServer
from pydobby.http import HTTPRequest, HTTPResponse
import json 

server = HTTPServer()

@server.get("/hello")
def home(request: HTTPRequest) -> HTTPResponse:
    data = "Jühn"
    return HTTPResponse(body=data)

@server.post("/submit")
def submit(request: HTTPRequest) -> HTTPResponse:
    data = json.loads(request.body)
    print(data)
    return HTTPResponse(status_code=201)

if __name__ == "__main__":
    server.start()
