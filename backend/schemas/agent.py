from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class AgentCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom: str | None = None
    prenom: str | None = None
    service: str | None = None
    email: EmailStr | None = None
    telephone: str | None = None

class AgentUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom: str | None = None
    prenom: str | None = None
    service: str | None = None
    email: EmailStr | None = None
    telephone: str | None = None

class AgentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime | None = None