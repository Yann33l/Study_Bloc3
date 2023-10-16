from datetime import date
from unittest.mock import Mock
import pytest

from sql_app import schemas, models
import sql_app.CRUD as CRUD

db = Mock()
user = schemas.UserCreate(
    Email="test@example.com",
    Last_change_password= date.fromisoformat("2022-10-10"),
    Password=b"password",
    Admin=False,
    Autorisation=True
)
user_from_db = schemas.UserCreate(
    Email="test@example.com",
    Last_change_password= date.fromisoformat("2022-10-10"),
    Password=b"password",
    Admin=False,
    Autorisation=True
)

user_not_from_db = schemas.UserCreate(
    Email="notindb@example.com",
    Last_change_password= date.fromisoformat("2022-10-10"),
    Password=b"password",
    Admin=False,
    Autorisation=True
)


def test_create_user():

    db_user = CRUD.create_user(db, user)
    
    assert db_user.Email == user.Email
    assert db_user.Last_change_password == user.Last_change_password
    assert db_user.Password == user.Password
    assert db_user.Admin == user.Admin
    assert db_user.Autorisation == user.Autorisation

def test_get_user_by_email():

    CRUD.get_user_by_email = Mock(return_value=user_from_db)
    db_user = CRUD.get_user_by_email(db, user.Email)

    assert db_user.Email == user.Email
    assert db_user.Last_change_password == user.Last_change_password
    assert db_user.Admin == user.Admin
    assert db_user.Autorisation == user.Autorisation

def test_get_users():

    CRUD.get_users = Mock(return_value=[user_from_db, user_from_db])
    db_user = CRUD.get_users(db)

    assert db_user[0].Email == user.Email
    assert db_user[0].Last_change_password == user.Last_change_password
    assert db_user[0].Admin == user.Admin
    assert db_user[0].Autorisation == user.Autorisation
    assert db_user[1].Email == user.Email
    assert db_user[1].Last_change_password == user.Last_change_password
    assert db_user[1].Admin == user.Admin
    assert db_user[1].Autorisation == user.Autorisation

def test_get_users_avec_un_none():

    CRUD.get_users = Mock(return_value=[user_from_db, None])
    db_user = CRUD.get_users(db)

    assert db_user[0].Email == user.Email
    assert db_user[0].Last_change_password == user.Last_change_password
    assert db_user[0].Admin == user.Admin
    assert db_user[0].Autorisation == user.Autorisation
    assert db_user[1] is None or isinstance(db_user[1], type(None))

