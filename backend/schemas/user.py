from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from db.models.user import RoleEnum


class UserCreate(BaseModel):
    """Créer un utilisateur (utilisé par les admins / le seed)."""
    
    nom: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: RoleEnum = RoleEnum.read


class UserUpdate(BaseModel):
    """Mettre à jour un utilisateur (tous champs optionnels)."""
    
    nom: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=128)
    role: RoleEnum | None = None


class UserRead(BaseModel):
    """Utilisateur retourné par l'API.
    
    IMPORTANT : ne contient PAS le mot de passe (hashé ou non).
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nom: str
    email: EmailStr
    role: RoleEnum