from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: EmailStr
    mot_de_passe_hash: str

class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str | None = None
    email: EmailStr | None = None
    mot_de_passe_hash: str | None = None

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime | None = None