" Ce fichier permet de se connecter à la base de données et de créer une session pour les requêtes "
import os
import socket

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Détection de l'environnement
local_ip = socket.gethostbyname(socket.gethostname())

if local_ip == '192.168.1.64':
    ENV = "local"
else:
    # Environnement en ligne
    ENV = os.environ.get("ENV", "online")

# Récupération des variables d'environnement pour scalingo
Login = os.getenv("Login")
Password = os.getenv("Password")
Server_Host = os.getenv("Server_Host")
Port = os.getenv("Port")
Database = os.getenv("Database")


# scalingo
SCALINGO_MYSQL_URL = f"mysql://{Login}:{Password}@{Server_Host}:{Port}/{Database}"

# Local
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Study_projet3@localhost:3310/goldenline"

# Local_test
SQLALCHEMY_DATABASE_URL_TEST = "mysql+mysqlconnector://root:Study_projet3@localhost:3310/goldenline_test"


if ENV == "local":
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
elif ENV == "local_test":
    engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)
else:
    engine = create_engine(SCALINGO_MYSQL_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
