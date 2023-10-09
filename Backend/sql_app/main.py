from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import bcrypt, json, csv
from . import CRUD, models, schemas
from .database import SessionLocal, engine, engine_read
from datetime import datetime
""" from .settings import settings """
from sqlalchemy.sql.expression import text


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

""" @app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    } """

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


#region : Connexion visualisation et création d'un utilisateur

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
           raise HTTPException(status_code=400, detail="Email déjà utilisé")
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
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
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
def get_depenses_CSP_ClasseArticle():
    try:
        with engine_read.connect() as connection:
            query = text("SELECT libelle_CSP as CSP, round(sum(quantite_article*prix_vente), 2) as depenses, libelle_categorie as categorie_vetement \
                            FROM goldenline.clients c \
                            LEFT JOIN goldenline.cat_socio_pro csp on csp.ID = c.id_CSP \
                            LEFT JOIN goldenline.paniers p on p.id_client = c.ID \
                            LEFT JOIN goldenline.r_panier_article r_pa on r_pa.id_panier = p.ID \
                            LEFT JOIN goldenline.articles a on a.ID = r_pa.id_article \
                            LEFT JOIN goldenline.categories_articles ca on a.id_categorie_article = ca.ID \
                            WHERE libelle_categorie IS NOT NULL \
                            GROUP BY libelle_CSP, libelle_categorie \
                            ORDER BY 1, 3;")
            result = connection.execute(query)

            results = result.fetchall()
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
def get_moyenne_pannier_par_CSP():
    try:
        with engine_read.connect() as connection:
            query = text("SELECT libelle_CSP as CSP, round(sum(quantite_article*prix_vente)/count(distinct id_panier),2) as Moy_panier \
                        FROM goldenline.clients c \
                        LEFT JOIN goldenline.cat_socio_pro csp on csp.ID = c.id_CSP \
                        left join goldenline.paniers p on p.id_client = c.ID \
                        left join goldenline.r_panier_article r_pa on r_pa.id_panier = p.ID \
                        left join goldenline.articles a on a.ID = r_pa.id_article \
                        where prix_vente is not null \
                        group by libelle_CSP \
                        ;")
            result = connection.execute(query)

            results = result.fetchall()
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
def get_Collecte():
    try:
        with engine_read.connect() as connection:
            query = text("SELECT ROW_NUMBER() OVER (ORDER BY id_panier, libelle_categorie) AS collecte, \
                        id_panier AS num_panier,  \
                        prix_panier.PPA as Prix_panier,  \
                        ROUND(SUM(quantite_article * prix_vente), 2) AS montant,  \
                        libelle_categorie AS categorie_article  \
                        FROM goldenline.clients c  \
                        LEFT JOIN goldenline.cat_socio_pro csp ON csp.ID = c.id_CSP \
                        LEFT JOIN goldenline.paniers p ON p.id_client = c.ID \
                        LEFT JOIN goldenline.r_panier_article r_pa ON r_pa.id_panier = p.ID \
                        LEFT JOIN goldenline.articles a ON a.ID = r_pa.id_article \
                        LEFT JOIN goldenline.categories_articles ca ON ca.id = a.id_categorie_article \
                        LEFT JOIN ( \
                            SELECT r_pa.id_panier AS panier_id, \
                                ROUND(SUM(quantite_article * prix_vente), 2) AS PPA \
                            FROM goldenline.paniers p \
                            LEFT JOIN goldenline.r_panier_article r_pa ON r_pa.id_panier = p.ID \
                            LEFT JOIN goldenline.articles a ON a.ID = r_pa.id_article \
                            WHERE prix_vente IS NOT NULL \
                            GROUP BY r_pa.id_panier) as prix_panier  \
                            ON r_pa.id_panier = prix_panier.panier_id \
                        WHERE prix_vente IS NOT NULL \
                        GROUP BY libelle_CSP, libelle_categorie, ca.ID, id_panier, prix_panier.PPA \
                        ORDER BY id_panier, libelle_categorie;") 
            result = connection.execute(query)

            results = result.fetchall()
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
def get_visu_ensemble():
    try:
        with engine_read.connect() as connection:
            query = text("SELECT num_client, nbr_enfants, libelle_CSP, id_panier, date_achat, id_article, quantite_article, prix_vente, cout, libelle_categorie \
                        FROM goldenline.clients c \
                        LEFT JOIN goldenline.cat_socio_pro csp on csp.ID = c.id_CSP \
                        LEFT JOIN goldenline.paniers p on p.id_client = c.ID \
                        LEFT JOIN goldenline.r_panier_article r_pa on r_pa.id_panier = p.ID \
                        LEFT JOIN goldenline.articles a on a.ID = r_pa.id_article \
                        LEFT JOIN goldenline.categories_articles ca on a.id_categorie_article = ca.ID \
                        ;") 
            result = connection.execute(query)

            results = result.fetchall()
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