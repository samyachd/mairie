from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name:str | None = None
    email: EmailStr | None = None

class UserCreate(UserBase):
    name: str
    email: EmailStr

class UserUpdate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    created_at: datetime | None = None