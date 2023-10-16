" Main file of the API."
import csv
import json
from datetime import datetime

import bcrypt
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from Backend.sql_app import CRUD, client_repository, models, schemas
from Backend.sql_app.database import ENV, SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
print("ENV", ENV)
if ENV == "local":
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["study-bloc3.vercel.app"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#region : Connexion visualisation et création d'un utilisateur

# Connexion d'un utilisateur
@app.get("/Connexion/", response_model=schemas.UserBase)
def Connexion(email: str, password: str, db: Session = Depends(get_db)):
    user = CRUD.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="Email incorrect")
    else:
        if bcrypt.checkpw(password.encode('utf-8'), bytes(user.Password)):
            return schemas.UserBase(
                Email=user.Email,
                Admin=user.Admin,
                Autorisation=user.Autorisation,
            )
        else:
            raise HTTPException(status_code=404, detail="Mot de passe incorrect")

# Creation d'un utilisateur
@app.post("/create_users/", response_model=schemas.UserCreate)
def create_users(email: str, password: str, db: Session = Depends(get_db)):
    user_exists = CRUD.get_user_by_email(db, email)
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        salt = bcrypt.gensalt(12)
        password_byte = password.encode('utf-8')
        user = schemas.UserCreate(
            Email=email,
            Password = bcrypt.hashpw(password_byte, salt),
            Autorisation = False,
            Admin = False,
            First_connexion = None,
            Last_change_password = datetime.now().date())
        return CRUD.create_user(db, user)


# Récupération de la liste des utilisateurs
@app.get("/users/", response_model=list[schemas.UserBase])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = CRUD.get_users(db, skip=skip, limit=limit)
    return users


# Récupération d'un utilisateur par son ID
@app.get("/users/{user_id}", response_model=schemas.UserBase)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = CRUD.get_user_by_ID(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Récupération d'un utilisateur par son email
@app.get("/userByEmail/", response_model=schemas.UserBase)
def read_user_email(email: str, db: Session = Depends(get_db)):
    db_user = CRUD.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#endregion

# ------------------------------------------------------ #

#region : Remplissage de la base de données Clients (json avec tableau )
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
#endregion

#region : Remplissage de la base de données articles (json avec index)
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
                "id_categorie_article": articles["id_categorie_article"][index]
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
 #endregion

#region : Remplissage de la base de données panier (csv)
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
                "date_achat": datetime.strptime(panier[1], "%d/%m/%Y").date(),
                "id_client": int(panier[2])
            }

            panier = schemas.paniers(**panier_data)
            created_panier = CRUD.create_panier(db, panier)
            created_paniers.append(created_panier)

        return created_paniers
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Champ manquant dans le fichier CSV : {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur : {}".format(e))
 #endregion

#region : Remplissage de la base de données r_panier_article (csv)
@app.post("/upload_r_panier_article/")
def upload_r_panier_articles(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = file.file.read()
        r_panier_articles = csv.reader(contents.decode("utf-8").splitlines(), delimiter=";")
        next(r_panier_articles) 

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
 #endregion

# ------------------------------------------------------ #

#region : Récupération des données pour la visualisation 
# Dépenses par CSP et catégorie article
@app.get("/depenses_CSP_ClasseArticle/")
def depenses_CSP_ClasseArticle():
    try:
        results = client_repository.get_depenses_CSP_ClasseArticle()
        formatted_results = []
        for row in results:
            formatted_results.append({
                "CSP": row[0],
                "depenses": row[1],
                "categorie_vetement": row[2]
            })
        return {"results": formatted_results}
    except Exception as e:
        return {"error": str(e)}

# Dépenses moyenne par pannier par CSP
@app.get("/moyenne_pannier_par_CSP/")
def moyenne_pannier_par_CSP():
    try:
        results = client_repository.get_moyenne_du_panier_par_CSP()        
        formatted_results = []
        for row in results:
            formatted_results.append({
                "CSP": row[0],
                "Moy_panier": row[1]
            })
        return {"results": formatted_results}
    except Exception as e:
        return {"error": str(e)}

# Collecte
@app.get("/Collecte/")
def Collecte():
    try:
        results = client_repository.get_Collecte()
        formatted_results = []
        for row in results:
            formatted_results.append({
                "collecte": row[0],
                "num_panier": row[1],
                "Prix_panier": row[2],
                "montant": row[3],
                "categorie_article": row[4]
                })
        return {"results": formatted_results}
    except Exception as e:
        return {"error": str(e)}

# Vison globale    
@app.get("/visu_ensemble/")
def visu_ensemble():
    try:
        results = client_repository.get_visu_ensemble()
        formatted_results = []
        for row in results:
            formatted_results.append({
                "Client": row[0],
                "Nbr enfants": row[1],
                "CSP": row[2],
                "id_panier": row[3],
                "date achat": row[4],
                "id_article": row[5],
                "quantite_article": row[6],
                "prix_vente": row[7],
                "cout": row[8],
                "categorie": row[9]
                })
        return {"results": formatted_results}
    except Exception as e:
        return {"error": str(e)} 
#endregion:
