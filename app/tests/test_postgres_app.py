from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi import status
from ..database import Base, SQLALCHEMY_DATABASE_URL
from ..main import app, get_db



engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/create_user",
        json={"username": "Hassan",
              "password": "Hassan",
              "user_email": "deadpool@example.com",
              "user_address": "Some Addreess",
              "user_identity_code":"11111111111",
              "user_phone": "0098999999999"},
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["user_email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["user_email"] == "deadpool@example.com"
    assert data["id"] == user_id
