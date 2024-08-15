import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestUsers(unittest.TestCase):

    def test_register_user(self):
        response = client.post("/users/register/", json={
            "email": "newuser@example.com",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        client.post("/users/register/", json={
            "email": "newuser@example.com",
            "password": "securepassword123"
        })
        response = client.post("/users/token/", data={
            "username": "newuser@example.com",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
    