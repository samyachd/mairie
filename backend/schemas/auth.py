from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    """Réponse contenant le token"""
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Données extraites du token"""
    model_config = ConfigDict(from_attributes=True)
    email: str | None = None