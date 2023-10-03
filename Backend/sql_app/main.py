from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from . import CRUD, models, schemas
from .database import SessionLocal, engine
import json


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Connexion visualisation et création d'un utilisateur

@app.get("/Connexion/", response_model=schemas.UserBase)
def Connexion(email: str, password: str, db: Session = Depends(get_db)):
    user = CRUD.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="Email incorrect")
    else:
        if bcrypt.checkpw(password.encode('utf-8'), bytes(user.Password)):
            return schemas.UserBase(
                Email=user.Email,
                Admin=user.Admin
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


# Remplissage de la base de données Clients 

@app.post("/create_Clients/", response_model=schemas.Clients)
def client(client: schemas.Clients,  db: Session = Depends(get_db)):
        return CRUD.create_client(db, client)
        

@app.post("/upload_clients/")
def upload_clients(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = file.file.read()  # Utilisation de file.file.read() pour une lecture synchrone
    clients = json.loads(contents.decode("utf-8"))
    
    created_clients = []
    for client_data in clients:
        client = schemas.Clients(**client_data)
        created_client = CRUD.create_client(db, client)
        created_clients.append(created_client)
    return created_clients




