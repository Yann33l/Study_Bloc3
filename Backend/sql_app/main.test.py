# BEGIN: 1c2d3e4f5g6h

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from .routes import app, get_db
import bcrypt

models.Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_user():
    db = SessionLocal()
    user = schemas.UserCreate(
        Email="test@test.com",
        Password=b"password",
        Admin=False
    )
    response = client.post("/create_users/", json=user.dict())
    assert response.status_code == 200
    assert response.json()["Email"] == user.Email
    assert response.json()["Admin"] == user.Admin
    db_user = db.query(models.users).filter(models.users.Email == user.Email).scalar()
    assert db_user is not None
    assert db_user.Email == user.Email
    assert bcrypt.checkpw(user.Password, bytes(db_user.Password))

def test_create_user_already_exists():
    db = SessionLocal()
    user = schemas.UserCreate(
        Email="test@test.com",
        Password=b"password",
        Admin=False
    )
    db_user = models.users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = client.post("/create_users/", json=user.dict())
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_read_users():
    db = SessionLocal()
    user = schemas.UserCreate(
        Email="test@test.com",
        Password=b"password",
        Admin=False
    )
    db_user = models.users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["Email"] == user.Email
    assert response.json()[0]["Admin"] == user.Admin

def test_read_user():
    db = SessionLocal()
    user = schemas.UserCreate(
        Email="test@test.com",
        Password=b"password",
        Admin=False
    )
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
    db = SessionLocal()
    user = schemas.UserCreate(
        Email="test@test.com",
        Password=b"password",
        Admin=False
    )
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
    db = SessionLocal()
    user = schemas.UserCreate(
        Email="test@test.com",
        Password=b"password",
        Admin=False
    )
    db_user = models.users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = client.get("/Connexion/?email=test@test.com&password=incorrect")
    assert response.status_code == 404
    assert response.json()["detail"] == "Mot de passe incorrect"

# END: 1c2d3e4f5g6h