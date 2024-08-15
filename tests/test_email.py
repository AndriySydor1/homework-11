import unittest
from unittest.mock import patch
from app.email import send_verification_email, send_reset_password_email
from fastapi import BackgroundTasks
from pydantic import EmailStr

class TestEmail(unittest.TestCase):

    @patch("app.email.FastMail.send_message")
    def test_send_verification_email(self, mock_send):
        background_tasks = BackgroundTasks()
        email = EmailStr("test@example.com")
        token = "testtoken"
        send_verification_email(email, token, background_tasks)
        self.assertEqual(len(background_tasks.tasks), 1)
        mock_send.assert_called_once()

    @patch("app.email.FastMail.send_message")
    def test_send_reset_password_email(self, mock_send):
        background_tasks = BackgroundTasks()
        email = EmailStr("test@example.com")
        token = "testtoken"
        send_reset_password_email(email, token, background_tasks)
        self.assertEqual(len(background_tasks.tasks), 1)
        mock_send.assert_called_once()

if __name__ == "__main__":
    unittest.main()
    