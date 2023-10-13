" Ce fichier permet de se connecter à la base de données et de créer une session pour les requêtes "
import os
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



local_ip = socket.gethostbyname(socket.gethostname())

if local_ip == '192.168.1.64':
    ENV = "local"
else:
    # Environnement en ligne
    ENV = os.environ.get("ENV", "online")



# scalingo
SCALINGO_MYSQL_URL = "mysql://goldenline_7195:MLysrp1Px4WZhs0ZEJAV@94e79af0-02d8-4af3-862a-4516a9e45f09.goldenline-7195.mysql.a.osc-fr1.scalingo-dbs.com:30567/goldenline_7195"

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
