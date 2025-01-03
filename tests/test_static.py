import os
import tempfile


class TestStaticFiles:
    def test_serve_static_file(self, app, make_request):
        # create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"Hello from static file")
            static_file = f.name

        try:
            # configure static directory
            static_dir = os.path.dirname(static_file)
            app.serve_static(static_dir)

            filename = os.path.basename(static_file)
            make_request(path=f"/static/{filename}")
            response = app.get_static_file(filename)

            assert response.status_code == 200
            assert response.body == b"Hello from static file"
            assert response.headers["Content-Type"] == "text/plain"

        finally:
            os.unlink(static_file)

    def test_serve_nonexistent_file(self, app, make_request):
        app.serve_static("/tmp")
        response = app.get_static_file("test.txt")
        assert response.status_code == 404

    def test_directory_traversal_attempt(self, app, make_request):
        app.serve_static("/tmp")
        response = app.get_static_file("../etc/passwd")
        assert response.status_code == 403

    def test_different_content_types(self, app):
        with tempfile.TemporaryDirectory() as temp_dir:
            files = {
                "test.html": (b"<html>Test</html>", "text/html"),
                "test.json": (b'{"test": true}', "application/json"),
                "test.png": (b"fake-png-data", "image/png"),
                "test.js": (
                    b"function test() { return true; }",
                    ["application/javascript", "text/javascript"],
                ),
                "test.min.js": (
                    b"function t(){return!0}",
                    ["application/javascript", "text/javascript"],
                ),
                "script.mjs": (
                    b"export default function test() { return true; }",
                    ["application/javascript", "text/javascript"],
                ),
            }
            for filename, (content, expected_type) in files.items():
                file_path = os.path.join(temp_dir, filename)
                with open(file_path, "wb") as f:
                    f.write(content)

            app.serve_static(temp_dir)

            for filename, (content, expected_type) in files.items():
                response = app.get_static_file(filename)
                assert response.status_code == 200
                assert response.body == content
                if isinstance(expected_type, list):
                    assert response.headers["Content-Type"] in expected_type
                else:
                    assert response.headers["Content-Type"] == expected_type

    def test_no_static_folder_configured(self, app):
        response = app.get_static_file("test.txt")
        assert response.status_code == 404
