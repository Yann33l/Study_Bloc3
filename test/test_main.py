from unittest.mock import Mock

import bcrypt
from fastapi.testclient import TestClient

from Backend.sql_app import models, schemas, CRUD
from Backend.sql_app.database import engine
from main import app

models.Base.metadata.create_all(bind=engine)

client = TestClient(app)

# arrange
db = Mock()
user = schemas.UserCreate(
    Email="test@test.com",
    Password=b"password",
    Admin=False,
    Autorisation=True
)

def test_create_user_doesnt_exist():

    CRUD.get_user_by_email = Mock(return_value=False)
    CRUD.create_user = Mock(return_value=user)

    # act
    response = client.post(f"/create_users/?email={user.Email}&password=password")

    # assert
    assert response.status_code == 200
    assert response.json()["Email"] == user.Email
    assert response.json()["Admin"] == user.Admin


def test_create_user_already_exists():

    CRUD.get_user_by_email = Mock(return_value=True)

    response = client.post(f"/create_users/?email={user.Email}&password=password")

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_read_users():

    CRUD.get_users = Mock(return_value=[user, user])

    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["Email"] == user.Email
    assert response.json()[0]["Admin"] == user.Admin
    assert response.json()[1]["Email"] == user.Email
    assert response.json()[1]["Admin"] == user.Admin


def test_read_user():
    db_user = models.users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = client.get(f"/users/{db_user.id}")
    assert response.status_code == 200
    assert response.json()["Email"] == user.Email
    assert response.json()["Admin"] == user.Admin

def test_read_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_connexion():
    db_user = models.users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = client.get(f"/Connexion/?email={user.Email}&password={user.Password}")
    assert response.status_code == 200
    assert response.json()["Email"] == user.Email
    assert response.json()["Admin"] == user.Admin

def test_connexion_incorrect_email():
    response = client.get("/Connexion/?email=incorrect@test.com&password=password")
    assert response.status_code == 404
    assert response.json()["detail"] == "Email incorrect"

def test_connexion_incorrect_password():
    db_user = models.users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = client.get("/Connexion/?email=test@test.com&password=incorrect")
    assert response.status_code == 404
    assert response.json()["detail"] == "Mot de passe incorrect"

