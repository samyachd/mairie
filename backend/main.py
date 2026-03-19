from fastapi import FastAPI
from api.routes import ecrans, ordinateurs
from core.settings import settings
from backend.api.routes import licence, user
from fastapi.middleware.cors import CORSMiddleware
from core.logger import setup_logger

setup_logger()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)

origins = [
    "https://castelnau-le-lez-inventaire.com",  # Ton site en production
    "http://localhost:3000",  # Pour le développement local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Domaines autorisés
    allow_credentials=True,  # Permet les cookies
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Méthodes HTTP autorisées
    allow_headers=["*"],  # Headers autorisés
)
@app.get("/")
def root():
    return {"status": "ok", "message": "API Inventaire"}

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(ordinateurs.router, prefix="/ordinateurs", tags=["ordinateurs"])
app.include_router(licence.router, prefix="/licenses", tags=["licenses"])
app.include_router(ecrans.router, prefix="/ecrans", tags=["ecrans"])