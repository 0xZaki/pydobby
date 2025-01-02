from pydobby import HTTPResponse


class TestMiddleware:
    def test_single_middleware(self, app, make_request):
        middleware_called = {"pre": False, "post": False}

        class TestMiddleware:
            def __init__(self, get_response):
                self.get_response = get_response

            def __call__(self, request):
                middleware_called["pre"] = True
                response = self.get_response(request)
                middleware_called["post"] = True
                return response

        app.register_middleware(TestMiddleware)

        @app.get("/test")
        def test_route(request):
            return HTTPResponse(body="test")

        request = make_request(path="/test")

        # build middleware chain like server
        handler = app.server.router.handle_request
        for middleware_class in reversed(app.server.middlewares):
            handler = middleware_class(handler)
        handler(request)

        assert middleware_called["pre"]
        assert middleware_called["post"]

    def test_multiple_middleware_order(self, app, make_request):
        execution_order = []

        class FirstMiddleware:
            def __init__(self, get_response):
                self.get_response = get_response

            def __call__(self, request):
                execution_order.append("first_pre")
                response = self.get_response(request)
                execution_order.append("first_post")
                return response

        class SecondMiddleware:
            def __init__(self, get_response):
                self.get_response = get_response

            def __call__(self, request):
                execution_order.append("second_pre")
                response = self.get_response(request)
                execution_order.append("second_post")
                return response

        app.register_middleware(FirstMiddleware)
        app.register_middleware(SecondMiddleware)

        @app.get("/test")
        def test_route(request):
            execution_order.append("handler")
            return HTTPResponse(body="test")

        request = make_request(path="/test")

        # build middleware chain like the server
        handler = app.server.router.handle_request
        for middleware_class in reversed(app.server.middlewares):
            handler = middleware_class(handler)
        handler(request)

        expected_order = [
            "first_pre",
            "second_pre",
            "handler",
            "second_post",
            "first_post",
        ]
        assert execution_order == expected_order
