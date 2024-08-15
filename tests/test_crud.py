import unittest
from sqlalchemy.orm import Session
from app import models, crud
from app.database import SessionLocal

class TestCRUD(unittest.TestCase):

    def setUp(self):
        self.db: Session = SessionLocal()
        self.test_user = models.User(email="test@example.com", hashed_password="hashed_password")
        self.db.add(self.test_user)
        self.db.commit()
        self.db.refresh(self.test_user)

    def tearDown(self):
        self.db.query(models.User).delete()
        self.db.commit()
        self.db.close()

    def test_create_user(self):
        new_user = models.User(email="new@example.com", hashed_password="hashed_password")
        crud.create_user(self.db, new_user)
        db_user = self.db.query(models.User).filter(models.User.email == "new@example.com").first()
        self.assertIsNotNone(db_user)

    def test_get_user(self):
        user = crud.get_user(self.db, self.test_user.id)
        self.assertEqual(user.email, self.test_user.email)

if __name__ == "__main__":
    unittest.main()
    