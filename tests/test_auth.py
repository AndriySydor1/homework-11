import unittest
from app.auth import get_password_hash, verify_password

class TestAuth(unittest.TestCase):

    def test_password_hashing(self):
        password = "securepassword123"
        hashed = get_password_hash(password)
        self.assertTrue(verify_password(password, hashed))

    def test_incorrect_password(self):
        password = "securepassword123"
        hashed = get_password_hash(password)
        self.assertFalse(verify_password("wrongpassword", hashed))

if __name__ == "__main__":
    unittest.main()
    