from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Study_projet3@localhost:3310/goldenline"
SQLALCHEMY_DATABASE_URL_READ = "mysql+mysqlconnector://read:read@localhost:3310/goldenline"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
engine_read = create_engine(
    SQLALCHEMY_DATABASE_URL_READ
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
