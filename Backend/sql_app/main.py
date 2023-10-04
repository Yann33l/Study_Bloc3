from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from . import CRUD, models, schemas
from .database import SessionLocal, engine
import json, csv
from datetime import datetime

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


# Remplissage de la base de données Clients (json avec tableau )
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


# Remplissage de la base de données articles (json avec index)
@app.post("/upload_articles/")
def upload_articles(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:

        contents = file.file.read()
        articles = json.loads(contents.decode("utf-8"))

        created_articles = []
        for index in articles["ID"]:
            article_data = {
                "ID": articles["ID"][index],
                "libelle_article": articles["libelle_article"][index],
                "prix_vente": articles["prix_vente"][index],
                "cout": articles["cout"][index],
                "id_cathegorie_article": articles["id_cathegorie_article"][index]
            }
            article = schemas.articles(**article_data)
            created_article = CRUD.create_produit(db, article)
            created_articles.append(created_article)

        return created_articles
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Champ manquant dans le fichier JSON : {e}")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Erreur de décodage JSON : {}".format(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur : {}".format(e))
 

# Remplissage de la base de données panier (csv)
@app.post("/upload_paniers/")
def upload_paniers(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = file.file.read()
        paniers = csv.reader(contents.decode("utf-8").splitlines(), delimiter=";")
        next(paniers)  # Skip header

        created_paniers = []
        for panier in paniers:
            panier_data = {
                "ID": int(panier[0]),
                "id_client": int(panier[2]),
                "date_achat": datetime.strptime(panier[1], "%d/%m/%Y").date()
            }

            panier = schemas.paniers(**panier_data)
            created_panier = CRUD.create_panier(db, panier)
            created_paniers.append(created_panier)

        return created_paniers
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Champ manquant dans le fichier CSV : {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur : {}".format(e))

# Remplissage de la base de données r_panier_article (csv)
@app.post("/upload_r_panier_article/")
def upload_r_panier_articles(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = file.file.read()
        r_panier_articles = csv.reader(contents.decode("utf-8").splitlines(), delimiter=";")
        next(r_panier_articles)  # Skip header

        created_r_panier_articles = []
        for r_panier_article in r_panier_articles:
            r_panier_article_data = {
                "ID": int(r_panier_article[0]),
                "id_panier": int(r_panier_article[1]),
                "id_article": int(r_panier_article[2]),
                "quantite_article": int(r_panier_article[3])
            }

            r_panier_article = schemas.r_panier_article(**r_panier_article_data)
            created_r_panier_article = CRUD.create_r_panier_article(db, r_panier_article)
            created_r_panier_articles.append(created_r_panier_article)

        return created_r_panier_articles
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Champ manquant dans le fichier CSV : {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur : {}".format(e))