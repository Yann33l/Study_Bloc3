" Main file of the API."
import csv
import json
import os
import socket
from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from Backend.sql_app import CRUD, client_repository, models, schemas
from Backend.sql_app.database import ENV, SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

local_ip = socket.gethostbyname(socket.gethostname())

if local_ip == '192.168.1.64':
    ENV = "local"
else:
    # Environnement en ligne
    ENV = os.environ.get("ENV", "online")

if ENV == "local":
    SECRET_KEY = "B4AB1DBD6953186D3ABF5C8D5625CF06"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 50
else:
    SECRET_KEY = str(os.getenv("SECRET_KEY"))
    ALGORITHM = str(os.getenv("ALGORITHM"))
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 60)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


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
        allow_origins=["https://study-bloc3.vercel.app"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT"],
        allow_headers=["*"],)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------------------------------ #
# region Connexion par token


def create_access_token(data: dict, expires_delta: timedelta or None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub", None)
        if email is None:
            raise credentials_exception
        user = CRUD.get_user_by_email(db, email=email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise credentials_exception


async def get_current_active_user(current_user: schemas.UserBase = Depends(get_current_user)):
    return current_user


@app.post("/token/", response_model=schemas.Token)
async def login_for_access_token_docs(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = CRUD.get_user_by_email(db, form_data.username)
    if user is None:
        raise HTTPException(status_code=404, detail="Email incorrect")
    else:
        if bcrypt.checkpw(form_data.password.encode('utf-8'), bytes(user.Password)):
            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.Email}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=404, detail="Mot de passe incorrect")


@app.post("/Connexion/", response_model=schemas.Token)
async def login_for_access_token(current_user: schemas.UserForm, db: Session = Depends(get_db)):
    user = CRUD.get_user_by_email(db, current_user.Email)
    if user is None:
        raise HTTPException(status_code=404, detail="Email incorrect")
    else:
        if bcrypt.checkpw(current_user.Password.encode('utf-8'), bytes(user.Password)):
            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.Email}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=404, detail="Mot de passe incorrect")


@app.post("/user/info/", response_model=schemas.UserBase)
async def read_user_info(current_user: schemas.UserBase = Depends(get_current_active_user)):
    return schemas.UserBase(
        Email=current_user.Email,
        Admin=current_user.Admin,
        Autorisation=current_user.Autorisation,
    )

# endregion : Connexion par token

# region : Connexion visualisation et création d'un utilisateur
# Connexion d'un utilisateur sans token (back-up)
""" @app.post("/Connexion/", response_model=schemas.UserBase)
def Connexion(user: schemas.UserForm, db: Session = Depends(get_db)):
    db_user = CRUD.get_user_by_email(db, user.Email)
    if user is None:
        raise HTTPException(status_code=404, detail="Email incorrect")
    else:
        if bcrypt.checkpw(user.Password.encode('utf-8'), bytes(db_user.Password)):
            return schemas.UserBase(
                Email=db_user.Email,
                Admin=db_user.Admin,
                Autorisation=db_user.Autorisation,
            )
        else:
            raise HTTPException(status_code=404, detail="Mot de passe incorrect") """

# Creation d'un utilisateur
@app.post("/create_user/", response_model=schemas.UserCreate)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exists = CRUD.get_user_by_email(db, user.Email)
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        salt = bcrypt.gensalt(12)
        user.Password = bcrypt.hashpw(user.Password, salt)
        user.Last_change_password = datetime.now().date()
        return CRUD.create_user(db, user)


# Récupération de la liste des utilisateurs
@app.get("/users/", response_model=list[schemas.UserBase])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_active_user)):
    if current_user.Admin is True:
        users = CRUD.get_users(db, skip=skip, limit=limit)
        return users

"""
# Récupération d'un utilisateur par son ID
@app.get("/users/{user_id}", response_model=schemas.UserBase)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = CRUD.get_user_by_ID(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user"""

# Récupération d'un utilisateur par son email
@app.get("/userByEmail/", response_model=schemas.UserBase)
def read_user_email(email: str, db: Session = Depends(get_db)):
    db_user = CRUD.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Mise à jour du statu Admin d'un utilisateur
@app.put("/editUserAdmin/", response_model=schemas.UserBase)
def update_user_Admin(user_edit: schemas.UserEditAdmin, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_active_user)):
    if current_user.Admin is True:
        user = CRUD.edit_admin_status(db, user_edit.Email, user_edit.Admin)
        return user

# Mise à jour du statu Autorisation d'un utilisateur
@app.put("/editUserAutorisation/", response_model=schemas.UserBase)
def update_user_Autorisation(edit_user: schemas.UserEditAutorisation, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_active_user)):
    if current_user.Admin is True:
        user = CRUD.edit_autorisation_status(
            db, edit_user.Email, edit_user.Autorisation)
        return user
# endregion

# ------------------------------------------------------ #
"""
# region : Remplissage de la base de données Clients (json avec tableau )


@app.post("/create_Clients/", response_model=schemas.Clients)
def client(client: schemas.Clients,  db: Session = Depends(get_db)):
    return CRUD.create_client(db, client)


@app.post("/upload_clients/")
def upload_clients(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Utilisation de file.file.read() pour une lecture synchrone
    contents = file.file.read()
    clients = json.loads(contents.decode("utf-8"))

    created_clients = []
    for client_data in clients:
        client = schemas.Clients(**client_data)
        created_client = CRUD.create_client(db, client)
        created_clients.append(created_client)
    return created_clients
# endregion

# region : Remplissage de la base de données articles (json avec index)


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
        raise HTTPException(
            status_code=400, detail=f"Champ manquant dans le fichier JSON : {e}")
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400, detail="Erreur de décodage JSON : {}".format(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Erreur interne du serveur : {}".format(e))
 # endregion

# region : Remplissage de la base de données panier (csv)


@app.post("/upload_paniers/")
def upload_paniers(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = file.file.read()
        paniers = csv.reader(contents.decode(
            "utf-8").splitlines(), delimiter=";")
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
        raise HTTPException(
            status_code=400, detail=f"Champ manquant dans le fichier CSV : {e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Erreur interne du serveur : {}".format(e))
 # endregion

# region : Remplissage de la base de données r_panier_article (csv)


@app.post("/upload_r_panier_article/")
def upload_r_panier_articles(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = file.file.read()
        r_panier_articles = csv.reader(
            contents.decode("utf-8").splitlines(), delimiter=";")
        next(r_panier_articles)

        created_r_panier_articles = []
        for r_panier_article in r_panier_articles:
            r_panier_article_data = {
                "ID": int(r_panier_article[0]),
                "id_panier": int(r_panier_article[1]),
                "id_article": int(r_panier_article[2]),
                "quantite_article": int(r_panier_article[3])
            }

            r_panier_article = schemas.r_panier_article(
                **r_panier_article_data)
            created_r_panier_article = CRUD.create_r_panier_article(
                db, r_panier_article)
            created_r_panier_articles.append(created_r_panier_article)

        return created_r_panier_articles
    except KeyError as e:
        raise HTTPException(
            status_code=400, detail=f"Champ manquant dans le fichier CSV : {e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Erreur interne du serveur : {}".format(e))
 # endregion
"""
# ------------------------------------------------------ #

# region : Récupération des données pour la visualisation
# Dépenses par CSP et catégorie article
@app.get("/depenses_CSP_ClasseArticle/")
def depenses_CSP_ClasseArticle(current_user: schemas.UserBase = Depends(get_current_active_user)):
    if current_user.Autorisation is True:
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
    else:
        raise HTTPException(status_code=400, detail="Inactive user")


# Dépenses moyenne par pannier par CSP
@app.get("/moyenne_pannier_par_CSP/")
def moyenne_pannier_par_CSP(current_user: schemas.UserBase = Depends(get_current_active_user)):
    if current_user.Autorisation is True:
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
    else:
        raise HTTPException(status_code=400, detail="Inactive user")

# Collecte
@app.get("/Collecte/")
def Collecte(current_user: schemas.UserBase = Depends(get_current_active_user)):
    if current_user.Autorisation is True:
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
    else:
        raise HTTPException(status_code=400, detail="Inactive user")

# Vison globale
@app.get("/visu_ensemble/")
def visu_ensemble(current_user: schemas.UserBase = Depends(get_current_active_user)):
    if current_user.Autorisation is True:
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
    else:
        raise HTTPException(status_code=400, detail="Inactive user")
# endregion:
