from pydobby.server import HTTPServer
from pydobby.http import HTTPRequest, HTTPResponse

server = HTTPServer()

@server.get("/hello")
def home(request: HTTPRequest) -> HTTPResponse:
    return HTTPResponse(body="hello")

if __name__ == "__main__":
    server.start()
