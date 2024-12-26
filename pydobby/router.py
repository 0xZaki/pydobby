from pydobby.http import HTTPRequest, HTTPResponse

class Router:
    def __init__(self):
        self.routes = {}
    
    def add_route(self, path: str, method: str, handler):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.upper()] = handler
        return handler
    
    def get(self, path: str):
        return lambda handler: self.add_route(path, 'GET', handler)
    
    def post(self, path: str):
        return lambda handler: self.add_route(path, 'POST', handler)
    
    def put(self, path: str):
        return lambda handler: self.add_route(path, 'PUT', handler)
    
    def delete(self, path: str):
        return lambda handler: self.add_route(path, 'DELETE', handler)
    
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        if request.path not in self.routes:
            return HTTPResponse(
                status_code=404,
            )
            
        handlers = self.routes[request.path]
        if request.method not in handlers:
            return HTTPResponse(
                status_code=405,
            )
            
        return handlers[request.method](request)
