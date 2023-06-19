from fastapi import FastAPI
from routes.index import users

# Création de l'application FastAPI
app = FastAPI()


app.include_router(users)
