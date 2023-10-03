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
    db_user = models.users(Email=user.Email, Password=user.Password, Admin=user.Admin)
    db.add(db_user)
    db.commit()
    return db_user

#Clients
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



