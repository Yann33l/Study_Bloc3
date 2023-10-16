from sqlalchemy.orm import Session

from . import models, schemas


# Users
def get_user_by_ID(db: Session, id: int):
    return db.query(models.users).filter(models.users.ID == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.users).filter(models.users.Email == email).scalar()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.users).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.users(Email=user.Email,First_connexion=None,Last_change_password=user.Last_change_password , Password=user.Password, Admin=user.Admin, Autorisation=user.Autorisation)
    db.add(db_user)
    db.commit()
    return db_user

# Clients
def get_client_by_ID(db: Session, id: int):
    return db.query(models.clients).filter(models.clients.ID == id).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.clients).offset(skip).limit(limit).all()

def create_client(db: Session, client: schemas.Clients):
    db_client = models.clients(num_client=client.num_client, nbr_enfants=client.nbr_enfants, id_CSP=client.id_CSP)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    client_response_dict = {
        "num_client": db_client.num_client,
        "nbr_enfants": db_client.nbr_enfants,
        "id_CSP": db_client.id_CSP
    }
    return client_response_dict

# Produits
def create_produit(db: Session, articles: schemas.articles):
    db_articles = models.articles(ID=articles.ID, libelle_article=articles.libelle_article, prix_vente=articles.prix_vente, cout=articles.cout, id_categorie_article=articles.id_categorie_article)
    db.add(db_articles)
    db.commit()
    db.refresh(db_articles)
    produit_response_dict = {
        "ID": db_articles.ID,
        "libelle_article": db_articles.libelle_article,
        "prix_vente": db_articles.prix_vente,
        "cout": db_articles.cout,
        "id_categorie_article": db_articles.id_categorie_article
    }
    return produit_response_dict

# Paniers
def create_panier(db: Session, paniers: schemas.paniers):
    db_paniers = models.paniers(ID=paniers.ID, id_client=paniers.id_client, date_achat=paniers.date_achat)
    db.add(db_paniers)
    db.commit()
    db.refresh(db_paniers)
    panier_response_dict = {
        "ID": db_paniers.ID,
        "id_client": db_paniers.id_client,
        "date_achat": db_paniers.date_achat
    }
    return panier_response_dict

# r_panier_article
def create_r_panier_article(db: Session, r_panier_article: schemas.r_panier_article):
    db_r_panier_article = models.r_panier_article(ID=r_panier_article.ID, id_panier=r_panier_article.id_panier, id_article=r_panier_article.id_article, quantite_article=r_panier_article.quantite_article)
    db.add(db_r_panier_article)
    db.commit()
    db.refresh(db_r_panier_article)
    r_panier_article_response_dict = {
        "ID": db_r_panier_article.ID,
        "id_panier": db_r_panier_article.id_panier,
        "id_article": db_r_panier_article.id_article,
        "quantite_article": db_r_panier_article.quantite_article
    }
    return r_panier_article_response_dict
