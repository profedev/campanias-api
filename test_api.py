import hashlib
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from main import app


ORIGINAL_SHA256 = "9f1b5c1f890356cd3ff824e801119bfa853bd6c7f1ff107fa7372608da2855d3"


class ApiTests(unittest.TestCase):
    def test_root_redirects_to_original_document(self):
        with TestClient(app) as client:
            response = client.get("/", follow_redirects=False)
            self.assertEqual(response.status_code, 307)
            self.assertEqual(response.headers["location"], "/api/v1/campanias")
            followed = client.get("/")
        self.assertEqual(followed.status_code, 200)
        self.assertEqual(hashlib.sha256(followed.content).hexdigest(), ORIGINAL_SHA256)

    def test_original_file_and_response_are_identical(self):
        original = Path(__file__).with_name("campanias.json").read_bytes()
        self.assertEqual(hashlib.sha256(original).hexdigest(), ORIGINAL_SHA256)
        with TestClient(app) as client:
            response = client.get("/api/v1/campanias")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")
        self.assertEqual(response.content, original)

    def test_health(self):
        with TestClient(app) as client:
            response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_read_only(self):
        with TestClient(app) as client:
            for method in ("post", "put", "patch", "delete"):
                with self.subTest(method=method):
                    response = getattr(client, method)("/api/v1/campanias")
                    self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
