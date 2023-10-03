from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


from . import CRUD, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"Fonctionne"
@app.get("/Connexion/", response_model=schemas.UserBase)
def Connexion(email: str, password: str, db: Session = Depends(get_db)):
    user = CRUD.Identification(db, email, password)
    if user is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return user

@app.get("/autentifiaction/", response_model=schemas.UserBase)
def authenticate_user(email: str, db: Session = Depends(get_db)):
    user = CRUD.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return user

@app.post("/create_users/", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exists = CRUD.get_user_by_email(db, email=user.Email)
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        return CRUD.create_user(db, user)

@app.get("/users/", response_model=list[schemas.UserBase])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = CRUD.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.UserBase)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = CRUD.get_user_by_ID(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user





""" from fastapi import FastAPI

@app.put("/users/{ID}")
async def update_data(id:int, user: User):
        ID=user.ID,
        Email=user.Email,
        Password=user.Password,
        First_connexion=user.First_connexion,
        Last_change_password=user.Last_change_password,
        Admin=user.Admin,
    ).where(user.c.id == id))
    return SessionLocal.execute(users.select()).fetchall()

@app.delete("/users/{ID}")
async def delete_data(id:int, user: User):
    SessionLocal.execute(users.delete(
        ID=user.ID,
        Email=user.Email,
        Password=user.Password,
        First_connexion=user.First_connexion,
        Last_change_password=user.Last_change_password,
        Admin=user.Admin,
    ).where(user.c.id == id))
    return SessionLocal.execute(users.select()).fetchall() """