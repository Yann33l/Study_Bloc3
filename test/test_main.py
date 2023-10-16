from unittest.mock import Mock

import bcrypt
from fastapi.testclient import TestClient

from Backend.sql_app import CRUD, models, schemas
from Backend.sql_app.database import engine
from main import app

models.Base.metadata.create_all(bind=engine)

client = TestClient(app)

# arrange
db = Mock()
salt = bcrypt.gensalt(12)
password_byte = b"password"
user = schemas.UserCreate(
    Email="test@test.com",
    Password=bcrypt.hashpw(password_byte, salt),
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

def test_read_users_exist():

    CRUD.get_users = Mock(return_value=[user, user])

    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["Email"] == user.Email
    assert response.json()[0]["Admin"] == user.Admin
    assert response.json()[1]["Email"] == user.Email
    assert response.json()[1]["Admin"] == user.Admin

def test_read_user_by_ID():

    CRUD.get_user_by_ID = Mock(return_value=user)

    response = client.get("/users/2")
    assert response.status_code == 200
    assert response.json()["Email"] == user.Email
    assert response.json()["Admin"] == user.Admin

def test_read_user_by_ID_not_found():
    
    db_user = None
    CRUD.get_user_by_ID = Mock(return_value=db_user)
    response = client.get("/users/55")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_connexion():

    CRUD.get_user_by_email = Mock(return_value=user)

    response = client.get(f"/Connexion/?email={user.Email}&password=password")
    
    assert response.status_code == 200
    assert response.json()["Email"] == user.Email
    assert response.json()["Admin"] == user.Admin
    assert response.json()["Autorisation"] == user.Autorisation

def test_connexion_incorrect_email():

    db_user = None
    CRUD.get_user_by_email = Mock(return_value=db_user)

    response = client.get("/Connexion/?email=incorrect@test.com&password=password")

    assert response.status_code == 404
    assert response.json()["detail"] == "Email incorrect"

def test_connexion_incorrect_password():

    CRUD.get_user_by_email = Mock(return_value=user)
    response = client.get("/Connexion/?email=test@test.com&password=incorrect")

    assert response.status_code == 404
    assert response.json()["detail"] == "Mot de passe incorrect"

