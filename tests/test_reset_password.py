import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestResetPassword(unittest.TestCase):

    def test_request_password_reset(self):
        response = client.post("/auth/reset-password/request/", json={"email": "test@example.com"})
        self.assertEqual(response.status_code, 404)

    def test_reset_password_invalid_token(self):
        response = client.post("/auth/reset-password/", json={"token": "invalidtoken", "new_password": "newpassword"})
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
    