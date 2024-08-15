import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestMain(unittest.TestCase):

    def test_home_route(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome", response.text)

    def test_register_user(self):
        response = client.post("/users/register/", json={
            "email": "testuser@example.com",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()
    