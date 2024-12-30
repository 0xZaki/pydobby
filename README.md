# PyDobby

Lightweight HTTP server framework built on Python's socket programming using TCP.

## Features

- Routing with path parameters support
- Query parameter parsing
- Middleware system for request/response processing
- Custom headers support


## Installation

```bash
pip install pydobby
```

## Usage

```python
from pydobby import PyDobby, HTTPRequest, HTTPResponse
import json
import logging

app = PyDobby()

# Custom middleware example
class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        logging.info(f"Response: {response.status_code}")
        return response

app.register_middleware(LoggingMiddleware)

# Basic route with path parameter
@app.get("/hello/<name>")
def hello(request: HTTPRequest, name: str) -> HTTPResponse:
    return HTTPResponse(body=f"Hello, {name}!")



# JSON handling example
@app.post("/submit")
def submit(request: HTTPRequest) -> HTTPResponse:
    data = json.loads(request.body)
    return HTTPResponse(status_code=201)

# Run the server
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

- [ ] Static File Serving
- [ ] CORS Support
- [ ] Cookie Handling
- [ ] Session Management
- [ ] File Upload
- [ ] SSL Support

## License

MIT License
