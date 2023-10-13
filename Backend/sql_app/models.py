from sqlalchemy import Column, LargeBinary
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, DATE,Boolean, Float

from .database import Base

class users(Base):
    __tablename__ = "users"

    ID = Column(Integer,primary_key=True,index=True)
    Email = Column(String(45))
    Password = Column(LargeBinary)
    First_connexion = Column(DateTime)
    Last_change_password = Column(DATE)
    Admin = Column(Boolean)

class clients(Base):
    __tablename__ = "clients"

    ID = Column(Integer,primary_key=True,index=True)
    num_client = Column(Integer)
    nbr_enfants = Column(Integer)
    id_CSP = Column(Integer)

class cat_socio_pro(Base):
    __tablename__ = "cat_socio_pro"

    ID = Column(Integer,primary_key=True,index=True)
    libelle_CSP = Column(String(45))
    id_CSP = Column(Integer)

class articles(Base):
    __tablename__ = "articles"

    ID = Column(Integer,primary_key=True,index=True)
    libelle_article = Column(String(200))
    prix_vente = Column(Float)
    cout = Column(Float)
    id_categorie_article = Column(Integer)

class categories_articles(Base):
    __tablename__ = "categories_articles"

    ID = Column(Integer,primary_key=True,index=True)
    libelle_categorie = Column(String(45))
    code = Column(String(45))   

class paniers(Base):
    __tablename__ = "paniers"

    ID = Column(Integer,primary_key=True,index=True)
    date_achat = Column(DATE)
    id_client = Column(Integer)

class r_panier_article(Base):
    __tablename__ = "r_panier_article"

    ID = Column(Integer,primary_key=True,index=True)
    id_panier = Column(Integer)
    id_article = Column(Integer)
    quantite_article = Column(Integer)


