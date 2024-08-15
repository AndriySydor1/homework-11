import unittest
from app.utils import generate_verification_token, verify_verification_token

class TestUtils(unittest.TestCase):

    def test_generate_verification_token(self):
        email = "test@example.com"
        token = generate_verification_token(email)
        self.assertIsNotNone(token)

    def test_verify_verification_token(self):
        email = "test@example.com"
        token = generate_verification_token(email)
        verified_email = verify_verification_token(token)
        self.assertEqual(email, verified_email)

if __name__ == "__main__":
    unittest.main()
    