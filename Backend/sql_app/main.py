from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# Création de l'application FastAPI
app = FastAPI()

# Configuration de la connexion à la base de données MySQL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://yannick:Study_projet3@127.0.0.1:3306/goldenline"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Modèle Pydantic pour représenter les données de l'utilisateur
class Utilisateur(BaseModel):
    ID: int
    Email: str
    Password: str
    First_connection: str
    Last_change_password: str
    Admin: int

# Route pour créer un nouvel utilisateur
@app.post("/users/")
def create_utilisateur(utilisateur: Utilisateur):
    db = SessionLocal()
    db.add(utilisateur)
    db.commit()
    db.refresh(utilisateur)

# Route pour obtenir les détails d'un utilisateur par email
@app.get("/users/{Email}", response_model=Utilisateur)
def get_utilisateur(Email: str):
    db = SessionLocal()
    data = db.query(Utilisateur).filter(Utilisateur.Email == Email).first()
    return data


# Exécution de l'application FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
