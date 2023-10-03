from pydantic import BaseModel 
from datetime import date

class UserBase(BaseModel):
    Email: str
    First_connexion: date | None = None
    Last_change_password: date | None = None
    Admin: int
        
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    Password: bytes

    