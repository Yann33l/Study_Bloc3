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

class clients(Base):
    __tablename__ = "clients"

    ID = Column(Integer,primary_key=True,index=True)
    num_client = Column(Integer)
    nbr_enfants = Column(Integer)
    id_CSP = Column(Integer)

class cath_socio_pro(Base):
    __tablename__ = "cath_socio_pro"

    ID = Column(Integer,primary_key=True,index=True)
    libelle_CSP = Column(String(45))
    id_CSP = Column(Integer)

class articles(Base):
    __tablename__ = "articles"

    ID = Column(Integer,primary_key=True,index=True)
    libelle_article = Column(String(45))
    prix_vente = Column(Integer)
    cout = Column(Integer)
    id_cathegorie_article = Column(Integer)

class cathegories_articles(Base):
    __tablename__ = "cathegories_articles"

    ID = Column(Integer,primary_key=True,index=True)
    libelle_cathegorie = Column(String(45))
    code = Column(String(45))   

class collectes(Base):
    __tablename__ = "collectes"

    ID = Column(Integer,primary_key=True,index=True)
    id_cat_article = Column(Integer)
    id_client = Column(Integer)

class paniers(Base):
    __tablename__ = "paniers"

    ID = Column(Integer,primary_key=True,index=True)
    id_collecte = Column(Integer)
    montant_vente = Column(Integer)
    cout_vente = Column(Integer)
    date_achat = Column(DATE)

class r_panier_article(Base):
    __tablename__ = "r_panier_article"

    ID = Column(Integer,primary_key=True,index=True)
    id_panier = Column(Integer)
    id_article = Column(Integer)

class r_panier_collecte(Base):
    __tablename__ = "r_pannier_collecte"

    ID = Column(Integer,primary_key=True,index=True)
    id_collecte = Column(Integer)
    id_panier = Column(Integer)

