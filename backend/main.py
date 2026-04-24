import os
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from core import settings
from api.routes import ordinateur, user, auth, agent, ecran, licence, devis, bon_de_commande, facture, inventaire, model, log
from fastapi.middleware.cors import CORSMiddleware
from core.logger import setup_logger, logger

setup_logger()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)
Instrumentator().instrument(app).expose(app)
logger.info(f"Démarrage de l'application {settings.APP_NAME} version {settings.VERSION}")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(model, prefix="/models", tags=["models"])
app.include_router(log, prefix="/logs", tags=["logs"])

# @app.lifespan("startup")
# async def startup():
#     from db.seed import seed
#     seed()
#     logger.info(f"{settings.APP_NAME} démarré")