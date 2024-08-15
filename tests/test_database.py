import unittest
from app.database import get_db, engine
from sqlalchemy.orm import sessionmaker

class TestDatabase(unittest.TestCase):

    def test_get_db(self):
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = next(get_db())
        self.assertIsNotNone(session)
        session.close()

if __name__ == "__main__":
    unittest.main()
    