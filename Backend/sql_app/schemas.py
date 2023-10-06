from pydantic import BaseModel 
from datetime import date

#table users
class UserBase(BaseModel):
    Email: str
    First_connexion: date | None = None
    Last_change_password: date | None = None
    Admin: int
        
    class Config:
        orm_mode = True
class UserCreate(UserBase):
    Password: bytes

# table clients
class Clients(BaseModel):
    num_client: int
    nbr_enfants: int
    id_CSP: int

# table CSP
class cat_socio_pro(BaseModel):
    ID: int
    libelle_CSP: str
    id_CSP: int

# table articles
class articles(BaseModel):
    ID: int 
    libelle_article: str
    prix_vente: float
    cout: float
    id_categorie_article: int

# table categorie_articles
class categories_articles(BaseModel):
    ID: int
    libelle_categorie: str
    code: str

# table panier
class paniers(BaseModel):
    ID: int
    id_client: int
    date_achat: date

# table r_panier_article
class r_panier_article(BaseModel):
    ID: int
    id_panier: int
    id_article: int
    quantite_article: int
