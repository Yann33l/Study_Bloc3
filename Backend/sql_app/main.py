from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import bcrypt


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

@app.get("/Connexion/", response_model=schemas.UserCreate)
def Connexion2(email: str, password: str, db: Session = Depends(get_db)):
    print(password)
    user = CRUD.get_user_by_email(db, email)

    if user is None:
        raise HTTPException(status_code=404, detail="Email incorrect")
    else:
        if bcrypt.checkpw(password.encode('utf-8'), bytes(user.Password)):
            return schemas.UserCreate(
                Email=user.Email,
                Admin=user.Admin,
                Password=user.Password
            )
        else: 
            raise HTTPException(status_code=404, detail="Mot de passe incorrect")


@app.post("/create_users/", response_model=schemas.UserCreate)
def user(user: schemas.UserCreate,  db: Session = Depends(get_db)):
        user_exists = CRUD.get_user_by_email(db, email=user.Email)
        if user_exists:
           raise HTTPException(status_code=400, detail="Email already registered")
        else:       
            salt = bcrypt.gensalt(12)
            user.Password = bcrypt.hashpw(user.Password, salt)                       
            print(user.Password)
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
