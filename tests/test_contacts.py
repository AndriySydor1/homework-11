import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestContacts(unittest.TestCase):

    def test_create_contact_unauthorized(self):
        response = client.post("/contacts/", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "birthday": "1990-01-01"
        })
        self.assertEqual(response.status_code, 401)

    def test_get_contacts_unauthorized(self):
        response = client.get("/contacts/")
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
    