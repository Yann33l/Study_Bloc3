from fastapi import FastAPI

# Création de l'application FastAPI
app = FastAPI()

# Exécution de l'application FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
