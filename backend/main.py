from fastapi import FastAPI
from backend.core.settings import settings
from backend.api.routes import users, ordinateurs, licenses, ecrans
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://mon-site-react.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "API Inventaire"}

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(ordinateurs.router, prefix="/ordinateurs", tags=["ordinateurs"])
app.include_router(licenses.router, prefix="/licenses", tags=["licenses"])
app.include_router(ecrans.router, prefix="/ecrans", tags=["ecrans"])