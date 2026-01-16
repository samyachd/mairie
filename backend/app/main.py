from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import users

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)

app.include_router(users.router, prefix="/users", tags=["users"])