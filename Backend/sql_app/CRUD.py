from sqlalchemy.orm import Session

from . import models, schemas


"Fonctionne"
def get_user(db: Session, user_id: int):
    return db.query(models.users).filter(models.users.ID == user_id).first()

"Fonctionne"
def get_user_by_email(db: Session, email: str):
    return db.query(models.users).filter(models.users.Email == email).first()

"Fonctionne"
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.users).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.Password + "notreallyhashed"
    db_user = models.users(Email=user.Email, Password=fake_hashed_password, Admin=user.Admin,ID=user.ID)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

