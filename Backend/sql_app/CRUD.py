from sqlalchemy.orm import Session

from . import models, schemas


"Fonctionne"
def Identification(db: Session, email: str, password: bytes):
    return db.query(models.users).filter(models.users.Email == email, models.users.Password == password).first()

"Fonctionne"
def get_user_by_ID(db: Session, id: int):
    return db.query(models.users).filter(models.users.ID == id).first()

"Fonctionne"
def get_user_by_email(db: Session, email: str):
    return db.query(models.users).filter(models.users.Email == email).scalar()

"Fonctionne"
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.users).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.users(Email=user.Email, Password=user.Password, Admin=user.Admin)
    db.add(db_user)
    db.commit()
    return db_user

