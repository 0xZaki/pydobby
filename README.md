# PyDobby

Lightweight HTTP server framework built on Python's socket programming using TCP.


## Features

- Routing
- Path parameter parsing
- Query parameter parsing
- Middleware system for request/response processing

## Installation

```bash
pip install pydobby2
```

## Quick Start

```python
from pydobby import PyDobby, HTTPRequest, HTTPResponse

app = PyDobby()

@app.get("/hello/<name>")
def hello(request: HTTPRequest, name: str) -> HTTPResponse:
    return HTTPResponse(body=f"Hello, {name}!")

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
