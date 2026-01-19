from fastapi import FastAPI
from backend.app.core.config import settings
from backend.app.api.routes import users, ordinateurs, licenses, ecrans

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(ordinateurs.router, prefix="/ordinateurs", tags=["ordinateurs"])
app.include_router(licenses.router, prefix="/licenses", tags=["licenses"])
app.include_router(ecrans.router, prefix="/ecrans", tags=["ecrans"])