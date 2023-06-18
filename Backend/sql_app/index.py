from fastapi import FastAPI
from routes.index import users

# Création de l'application FastAPI
app = FastAPI()


app.include_router(users)
#Exécution de l'application FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
