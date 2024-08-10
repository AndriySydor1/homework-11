from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL підключення до бази даних PostgreSQL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

# Створення об'єкта двигуна (engine)
engine = create_engine(DATABASE_URL)

# Створення фабрики сесій для роботи з базою даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для створення моделей SQLAlchemy
Base = declarative_base()

# Функція для отримання сесії бази даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        