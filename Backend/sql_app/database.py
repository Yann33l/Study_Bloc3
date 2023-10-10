from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# scalingo
SCALINGO_MYSQL_URL= "mysql://goldenline_7195:MLysrp1Px4WZhs0ZEJAV@94e79af0-02d8-4af3-862a-4516a9e45f09.goldenline-7195.mysql.a.osc-fr1.scalingo-dbs.com:30567/goldenline_7195?useSSL=true&verifyServerCertificate=false"
""" DATABASE_URL=$SCALINGO_MYSQL_URL """

engine = create_engine(SCALINGO_MYSQL_URL)
engine_read = create_engine(SCALINGO_MYSQL_URL)


# Local
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Study_projet3@localhost:3310/goldenline"
SQLALCHEMY_DATABASE_URL_READ = "mysql+mysqlconnector://read:read@localhost:3310/goldenline"
""" engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine_read = create_engine(SQLALCHEMY_DATABASE_URL_READ) """


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()