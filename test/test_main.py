from datetime import datetime, timedelta
from unittest.mock import Mock

import bcrypt
import jwt
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from Backend.sql_app import CRUD, models, schemas
from Backend.sql_app.database import engine
from main import ALGORITHM, SECRET_KEY, app

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
email = "test@test.com"
password = "password"


def test_create_user_doesnt_exist():

    # arrange
    CRUD.get_user_by_email = Mock(return_value=False)
    CRUD.create_user = Mock(return_value=user)

    # act
    response = client.post('/create_user/', json={
        "Email": email,
        "Password": password,
        "First_connexion": None,
        "Last_change_password": None,
        "Admin": False,
        "Autorisation": False,
    })

    # assert
    assert response.status_code == 200
    assert response.json()["Email"] == email
    assert response.json()["Admin"] == False


def test_create_user_already_exists():

    # arrange
    CRUD.get_user_by_email = Mock(return_value=True)

    # act
    response = client.post('/create_user/', json={
        "Email": email,
        "Password": password,
        "First_connexion": None,
        "Last_change_password": None,
        "Admin": False,
        "Autorisation": False,
    })

    # assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

#test à corriger
"""    @app.get("/users/", response_model=list[schemas.UserBase])
    def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_active_user)):
>       if current_user.Admin is True:
E       AttributeError: 'bool' object has no attribute 'Admin'"""
def test_read_users_exist():
    token_payload = {"sub": "test@test.com",
                     "exp": datetime.utcnow() + timedelta(minutes=5)}
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    CRUD.get_users = Mock(return_value=[user, user])

    response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["Email"] == user.Email
    assert response.json()[0]["Admin"] == user.Admin
    assert response.json()[1]["Email"] == user.Email
    assert response.json()[1]["Admin"] == user.Admin
"""

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
"""

def test_connexion():
    # arrange
    # probleme datetime.utcnow() different entre le arrange et le act ce qui change la valeur du token
    # relancer pour valider le test (passe en fonction de la vitesse d'execution du test)
    token_payload = {"sub": "test@test.com",
                     "exp": datetime.utcnow() + timedelta(minutes=5)}
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    CRUD.get_user_by_email = Mock(return_value=user)

    # act
    response = client.post("/Connexion/", json={
        "Email": email,
        "Password": password, })

    # assert
    assert response.status_code == 200
    assert response.json()["access_token"] == token


def test_connexion_incorrect_email():

    # arrange
    db_user = None
    CRUD.get_user_by_email = Mock(return_value=db_user)

    # act
    response = client.post("/Connexion/", json={
        "Email": email,
        "Password": password, })

    # assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Email incorrect"


def test_connexion_incorrect_password():

    # arrange
    CRUD.get_user_by_email = Mock(return_value=user)

    # act
    response = client.post("/Connexion/", json={
        "Email": email,
        "Password": "wrong_password", })

    # assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Mot de passe incorrect"


def test_get_current_user_valid_token():

    # arrange
    token_payload = {"sub": "test@test.com",
                     "exp": datetime.utcnow() + timedelta(minutes=5)}
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    db_user = user

    # act
    response = client.post(
        '/user/info/', headers={"Authorization": f"Bearer {token}"})

    # assert
    assert response.status_code == 200
    assert response.json()["Email"] == db_user.Email
    assert response.json()["Admin"] == db_user.Admin
    assert response.json()["Autorisation"] == db_user.Autorisation


def test_get_current_user_invalid_token():

    # arrange
    token = "invalid_token"

    # act
    response = client.post(
        '/user/info/', headers={"Authorization": f"Bearer {token}"})

    # assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"


def test_get_current_user_user_not_found():
    # arrange
    token_payload = {"sub": "test@test.com",
                     "exp": datetime.utcnow() + timedelta(minutes=30)}
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    db_user = None
    CRUD.get_user_by_email = Mock(return_value=db_user)

    # act
    response = client.post(
        '/user/info/', headers={"Authorization": f"Bearer {token}"})

    # assert
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_current_user_missing_email():
    # arrange
    token_payload = {"exp": datetime.utcnow() + timedelta(minutes=30)}
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    db_user = None
    CRUD.get_user_by_email = Mock(return_value=db_user)

    # act
    response = client.post(
        '/user/info/', headers={"Authorization": f"Bearer {token}"})

    # assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"


def test_login_for_access_token_correct_credentials():

    # arrange
    current_user = schemas.UserForm(Email="test@test.com", Password="password")
    db_user = user
    CRUD.get_user_by_email = Mock(return_value=db_user)
    bcrypt.checkpw = Mock(return_value=True)
    access_token_expires = timedelta(minutes=5)
    access_token = jwt.encode(
        {"sub": db_user.Email, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # act
    response = client.post('/Connexion/', json=current_user.model_dump())

    # assert
    assert response.status_code == 200
    assert response.json()["access_token"] == access_token
    assert response.json()["token_type"] == "bearer"


def test_login_for_access_token_incorrect_email():

    # arrange
    current_user = schemas.UserForm(
        Email="incorrect@test.com", Password="password")
    db_user = None
    CRUD.get_user_by_email = Mock(return_value=db_user)

    # act
    response = client.post('/Connexion/', json=current_user.model_dump())

    # assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Email incorrect"


def test_login_for_access_token_incorrect_password():

    # arrange
    current_user = schemas.UserForm(
        Email="test@test.com", Password="incorrect")
    db_user = user
    CRUD.get_user_by_email = Mock(return_value=db_user)
    bcrypt.checkpw = Mock(return_value=False)

    # act
    response = client.post('/Connexion/', json=current_user.model_dump())

    # assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Mot de passe incorrect"
