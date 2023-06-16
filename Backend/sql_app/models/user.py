from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, DATE,Boolean
from config.database import meta


users = Table(
    'users',meta,
    Column('ID',Integer,primary_key=True),
    Column('Email',String(45),unique=True),
    Column('Password',String(45)),
    Column('First_connexion',DateTime),
    Column('Last_change_password',DATE),
    Column('Admin',Boolean)
)