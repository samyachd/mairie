from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Réponse contenant le token JWT."""
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    """Requête de connexion."""
    email: EmailStr
    password: str