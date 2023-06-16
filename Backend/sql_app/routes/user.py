from fastapi import APIRouter
from config.database import SessionLocal
from models.index import users
from schemas.index import User

user = APIRouter() 


@user.get("/users/")
async def read_data():
    return SessionLocal.execute(users.select()).where(user.c.id == id).fetchall()

@user.post("/users/")
async def write_data(user: User):
    SessionLocal.execute(users.insert().values(
        Email=user.Email,
        Password=user.Password,
        First_connexion=user.First_connexion,
        Last_change_password=user.Last_change_password,
        Admin=user.Admin,
    ))