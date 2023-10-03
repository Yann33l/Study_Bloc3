from sqlalchemy.orm import Session

from . import models, schemas


"Fonctionne"
def Identification(db: Session, email: str, password: str):
    return db.query(models.users).filter(models.users.Email == email, models.users.Password == password).first()

"Fonctionne"
def get_user_by_ID(db: Session, id: int):
    return db.query(models.users).filter(models.users.ID == id).first()

"Fonctionne"
def get_user_by_email(db: Session, email: str):
    return db.query(models.users).filter(models.users.Email == email).first()

"Fonctionne"
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.users).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.Password + "123"
    db_user = models.users(Email=user.Email, Password=fake_hashed_password, Admin=user.Admin,ID=user.ID)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

