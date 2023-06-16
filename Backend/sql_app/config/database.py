from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


# Configuration de la connexion à la base de données MySQL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://yannick:Study_projet3@127.0.0.1:3306/goldenline"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
meta = MetaData()