from pydantic import BaseModel

class User(BaseModel):
    ID: int
    Email: str
    Password: str
    First_connexion: str
    Last_change_password: str
    Admin: int