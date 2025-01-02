from pydobby import HTTPResponse


class TestRouting:
    def test_basic_route_registration(self, app):
        @app.get("/test")
        def test_route(request):
            return HTTPResponse(body="test")

        assert "/test" in app.server.router.routes
        assert callable(app.server.router.routes["/test"]["GET"])

    def test_route_with_parameters(self, app, make_request):
        received_params = {}

        @app.get("/users/<user_id>")
        def get_user(request, user_id):
            received_params["user_id"] = user_id
            return HTTPResponse(body=f"User {user_id}")

        request = make_request(path="/users/123")
        response = app.server.router.handle_request(request)

        assert received_params["user_id"] == "123"
        assert response.body == b"User 123"

    def test_multiple_methods(self, app):
        @app.get("/resource")
        def get_resource(request):
            return HTTPResponse(body="get")

        @app.post("/resource")
        def create_resource(request):
            return HTTPResponse(body="post", status_code=201)

        assert "GET" in app.server.router.routes["/resource"]
        assert "POST" in app.server.router.routes["/resource"]
