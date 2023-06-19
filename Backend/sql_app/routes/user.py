from fastapi import APIRouter
from config.database import SessionLocal
from models.index import users
from schemas.index import User

user = APIRouter() 


@user.post("/")
async def write_data(user: User):
    SessionLocal.execute(users.insert().values(
        ID=user.ID,
        Email=user.Email,
        Password=user.Password,
        First_connexion=user.First_connexion,
        Last_change_password=user.Last_change_password,
        Admin=user.Admin,
    ))
    return SessionLocal.execute(users.select()).fetchall()

@user.get("/{id}/")
async def read_data(id:int):
    return SessionLocal.execute(users.select()).where(user.c.id == id).fetchall()

@user.put("/{id}")
async def update_data(id:int, user: User):
    SessionLocal.execute(users.update(
        ID=user.ID,
        Email=user.Email,
        Password=user.Password,
        First_connexion=user.First_connexion,
        Last_change_password=user.Last_change_password,
        Admin=user.Admin,
    ).where(user.c.id == id))
    return SessionLocal.execute(users.select()).fetchall()

@user.delete("/{id}")
async def delete_data(id:int, user: User):
    SessionLocal.execute(users.delete(
        ID=user.ID,
        Email=user.Email,
        Password=user.Password,
        First_connexion=user.First_connexion,
        Last_change_password=user.Last_change_password,
        Admin=user.Admin,
    ).where(user.c.id == id))
    return SessionLocal.execute(users.select()).fetchall()