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
class cath_socio_pro(BaseModel):
    ID: int
    libelle_CSP: str
    id_CSP: int

# table articles
class articles(BaseModel):
    ID: int 
    libelle_article: str
    prix_vente: float
    cout: float
    id_cathegorie_article: int

# table cathegorie_articles
class cathegories_articles(BaseModel):
    ID: int
    libelle_cathegorie: str
    code: str

# table collecte
class collectes(BaseModel):
    ID: int
    id_cat_article: int
    id_client: int

# table panier
class paniers(BaseModel):
    ID: int
    id_collecte: int
    montant_vente: int
    cout_vente: int
    date_achat: date

# table r_panier_article
class r_panier_article(BaseModel):
    ID: int
    id_panier: int
    id_article: int
    quantite_article: int

# table r_panier_collecte
class r_panier_collecte(BaseModel):
    ID: int
    id_collecte: int
    id_panier: int
