from datetime import date
from unittest.mock import Mock

from sql_app import models, schemas
from sql_app.CRUD import create_user
from sqlalchemy.orm import Session



def test_create_user():
    db = Mock()
    user = schemas.UserCreate(
        Email="test@example.com",
        Last_change_password= date.fromisoformat("2022-10-10"),
        Password=b"password",
        Admin=False,
        Autorisation=True
    )
    db_user = create_user(db, user)
    assert db_user.Email == user.Email
    assert db_user.Last_change_password == user.Last_change_password
    assert db_user.Password == user.Password
    assert db_user.Admin == user.Admin
    assert db_user.Autorisation == user.Autorisation