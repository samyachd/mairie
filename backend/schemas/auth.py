from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    """Réponse contenant le token"""
    access_token: str
    token_type: str = "bearer"