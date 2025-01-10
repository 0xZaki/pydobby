# PyDobby

Lightweight HTTP server framework built on Python's socket programming using TCP.

## Features

- Routing with path parameters support
- Query parameter parsing
- Middleware system for request/response processing
- Custom headers support
- Static file serving
- Cookie handling
- CORS support


## Installation

```bash
pip install pydobby
```

## Usage

### Basic Routing

```python
from pydobby import PyDobby, HTTPRequest, HTTPResponse
import json
import logging

app = PyDobby()

# custom middleware example
class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        logging.info(f"Response: {response.status_code}")
        return response

app.register_middleware(LoggingMiddleware)

### Basic Routing

```python
# Basic route
@app.get("/hello")
def home(request: HTTPRequest) -> HTTPResponse:

    return HTTPResponse(body="Hello World", content_type="text/plain")
```

### Path Parameters

```python
# route with path parameter and cookie setting
@app.get("/hello/<name>")
def hello(request: HTTPRequest, name: str) -> HTTPResponse:
    data = f"hello {name}!"
    headers = {"Server": "pydobby"}
    response = HTTPResponse(body=data, headers=headers, content_type="text/plain")
    # set a cookie
    response.set_cookie(
        "name", name,
        max_age=3600,
        path="/",
        secure=True,
        httponly=True,
        samesite="Lax"
    )
    return response
```

### Headers

```python
# setting custom headers
@app.get("/api/status")
def status(request: HTTPRequest) -> HTTPResponse:
    headers = {
        "Server": "pydobby",
        "X-Custom-Header": "custom value"
    }
    return HTTPResponse(
        body="OK",
        headers=headers,
        content_type="text/plain"
    )
```

### JSON Handling

```python
# POST route with JSON handling
@app.post("/submit")
def submit(request: HTTPRequest) -> HTTPResponse:
    try:
        data = json.loads(request.body)
        return HTTPResponse(
            status_code=201,
            body=json.dumps({"status": "success"}),
            content_type="application/json"
        )
    except json.JSONDecodeError:
        return HTTPResponse(
            status_code=400,
            body=json.dumps({"error": "Invalid JSON"}),
            content_type="application/json"
        )
```

### Cookie Handling

```python
# getting cookies
@app.get("/profile")
def profile(request: HTTPRequest) -> HTTPResponse:
    user_id = request.cookies.get("user_id")
    return HTTPResponse(body=f"User ID: {user_id}")

# setting cookies
@app.post("/login")
def login(request: HTTPRequest) -> HTTPResponse:
    response = HTTPResponse(body="Logged in")
    response.set_cookie("user_id", "123", max_age=3600)
    return response
```

### CORS Configuration

```python
# CORS configuration
app.conf = {
    "CORS_ALLOWED_ORIGINS": ["*"],
    "CORS_ALLOWED_METHODS": ["*"],
    "CORS_ALLOWED_HEADERS": ["*"],
}

# register CORS middleware
app.register_middleware(CORSMiddleware)
```

### Static File Serving

```python
# configure static file directory
app.serve_static("static")

# serve static files through a route
@app.get("/static/<path>")
def serve_static(request: HTTPRequest, path: str) -> HTTPResponse:
    return app.get_static_file(path)
```


# Run the server

```python
if __name__ == "__main__":
    app.start()
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pydobby.git
cd pydobby
```

2. Install in development mode:
```bash
pip install -e .
```

3. Run the example:
```bash
python examples/basic_app.py
```


## TODO

Improvements and features:

- [x] Static File Serving
- [x] CORS Support
- [x] Cookie Handling
- [ ] Session Management
- [ ] File Upload
- [ ] SSL Support

## License

MIT License
