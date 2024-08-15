import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def get_token():
    # Спочатку реєструємо нового користувача
    response = client.post("/users/register/", json={
        "email": "testuser@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 201

    # Отримуємо токен доступу для зареєстрованого користувача
    response = client.post("/users/token/", data={
        "username": "testuser@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 200
    return response.json()["access_token"]

def test_create_contact(get_token):
    access_token = get_token
    headers = {"Authorization": f"Bearer {access_token}"}

    # Надсилаємо запит на створення нового контакту
    response = client.post("/contacts/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "phone_number": "1234567890",
        "birthday": "1990-01-01",
        "additional_info": "Friend from college"
    }, headers=headers)

    # Перевіряємо, що контакт успішно створений
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "johndoe@example.com"

def test_create_contact_rate_limit(get_token):
    access_token = get_token
    headers = {"Authorization": f"Bearer {access_token}"}

    # Викликаємо створення контакту більше, ніж дозволено за часом
    for _ in range(6):
        response = client.post("/contacts/", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": f"janedoe{_}@example.com",
            "phone_number": "0987654321",
            "birthday": "1992-01-01",
            "additional_info": "Another friend from college"
        }, headers=headers)
        
    # Перевіряємо, що останній запит перевищує ліміт
    assert response.status_code == 429
    assert "rate limit exceeded" in response.text.lower()
    