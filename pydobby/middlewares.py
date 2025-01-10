from .response import HTTPResponse


class CORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_origins = self.app.conf.get("CORS_ALLOWED_ORIGINS", ["*"])
        self.allowed_methods = self.app.conf.get("CORS_ALLOWED_METHODS", ["*"])
        self.allowed_headers = self.app.conf.get("CORS_ALLOWED_HEADERS", ["*"])

    def __call__(self, request):
        # handle preflight request
        if request.method == "OPTIONS" and request.headers.get(
            "Access-Control-Request-Method"
        ):
            response = HTTPResponse(200)
            response.headers["Access-Control-Allow-Origin"] = ", ".join(
                self.allowed_origins
            )
            response.headers["Access-Control-Allow-Methods"] = ", ".join(
                self.allowed_methods
            )
            response.headers["Access-Control-Allow-Headers"] = ", ".join(
                self.allowed_headers
            )
            response.headers["Vary"] = "Origin"
            return response

        response = self.get_response(request)

        # set cors headers for actual requests
        origin = request.headers.get("Origin")
        if origin in self.allowed_origins or "*" in self.allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
        else:
            response.headers["Access-Control-Allow-Origin"] = ", ".join(
                self.allowed_origins
            )

        response.headers["Vary"] = "Origin"

        return response
