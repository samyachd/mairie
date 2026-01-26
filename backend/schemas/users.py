from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: EmailStr

class UserCreate(UserBase):
    mot_de_passe: str

class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str | None = None
    email: EmailStr | None = None
    mot_de_passe: str | None = None

class UserLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    mot_de_passe: str

class UserRead(UserBase):
    id: int
    created_at: datetime | None = None

class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str