from pydantic import BaseModel

class User(BaseModel):
    ID: int
    Email: str
    Password: str
    First_connection: str
    Last_change_password: str
    Admin: int