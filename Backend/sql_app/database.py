" Ce fichier permet de se connecter à la base de données et de créer une session pour les requêtes "
import os
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv


load_dotenv()

local_ip = socket.gethostbyname(socket.gethostname())

if local_ip == '192.168.1.64':
    ENV = "local"
else:
    # Environnement en ligne
    ENV = os.environ.get("ENV", "online")

Login = os.getenv("Login")
Password = os.getenv("Password")
Server_Host = os.getenv("Server_Host")
Port = os.getenv("Port")
Database = os.getenv("Database")

print(Login, Password, Server_Host, Port, Database)

# scalingo
SCALINGO_MYSQL_URL = f"mysql://{Login}:{Password}@{Server_Host}:{Port}/{Database}"

# Local
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Study_projet3@localhost:3310/goldenline"
SQLALCHEMY_DATABASE_URL_READ = "mysql+mysqlconnector://read:read@localhost:3310/goldenline"


if ENV == "local":
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    engine_read = create_engine(SQLALCHEMY_DATABASE_URL_READ)
else:
    engine = create_engine(SCALINGO_MYSQL_URL)
    engine_read = create_engine(SCALINGO_MYSQL_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
