from pydantic import BaseModel
from datetime import date, datetime, time, timedelta


class UserBase(BaseModel):
    ID: int
    Email: str
    First_connexion: datetime | None = None
    Last_change_password: date | None = None
    Admin: int
        
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    Password: str

""" class User(UserBase):
    Password: str """

    