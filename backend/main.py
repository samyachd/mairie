from fastapi import FastAPI
from core import settings
from api.routes import ordinateur, user, auth, agent, ecran, licence, devis, bon_de_commande, facture, inventaire
from fastapi.middleware.cors import CORSMiddleware
from core.logger import setup_logger, logger

setup_logger()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)
logger.info(f"Démarrage de l'application {settings.APP_NAME} version {settings.VERSION}")

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

app.include_router(user, prefix="/users", tags=["users"])
app.include_router(ordinateur, prefix="/ordinateurs", tags=["ordinateurs"])
app.include_router(licence, prefix="/licenses", tags=["licenses"])
app.include_router(ecran, prefix="/ecrans", tags=["ecrans"])
app.include_router(auth, prefix="/auth", tags=["auth"])
app.include_router(inventaire, prefix="/inventaire", tags=["inventaire"])
app.include_router(agent, prefix="/agents", tags=["agents"])
app.include_router(devis, prefix="/devis", tags=["devis"])
app.include_router(bon_de_commande, prefix="/bons-de-commande", tags=["bons-de-commande"])
app.include_router(facture, prefix="/factures", tags=["factures"])
# app.include_router(model.router, prefix="/models", tags=["models"])