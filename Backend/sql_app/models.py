from sqlalchemy import Column, LargeBinary
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, DATE,Boolean

from .database import Base

class users(Base):
    __tablename__ = "users"

    ID = Column(Integer,primary_key=True,index=True)
    Email = Column(String(45))
    Password = Column(LargeBinary)
    First_connexion = Column(DateTime)
    Last_change_password = Column(DATE)
    Admin = Column(Boolean)

