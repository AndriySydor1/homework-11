import unittest
from app.models import User, Contact
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

class TestModels(unittest.TestCase):

    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = self.SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_create_user(self):
        user = User(email="test@example.com", hashed_password="hashedpassword")
        self.db.add(user)
        self.db.commit()
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test@example.com")

    def test_create_contact(self):
        user = User(email="test@example.com", hashed_password="hashedpassword")
        self.db.add(user)
        self.db.commit()

        contact = Contact(first_name="John", last_name="Doe", email="johndoe@example.com",
                          phone_number="1234567890", birthday="1990-01-01", owner_id=user.id)
        self.db.add(contact)
        self.db.commit()
        self.assertIsNotNone(contact.id)
        self.assertEqual(contact.email, "johndoe@example.com")

if __name__ == "__main__":
    unittest.main()
    