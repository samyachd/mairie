from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional

from sqlalchemy.orm import Session
from core.settings import settings
from db.models.base import TokenBlacklist

if settings.SECRET_KEY is None:
    raise ValueError("JWT_KEY n'est pas définie dans les variables d'environnement")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hacher_mot_de_passe(mot_de_passe: str) -> str:
    return pwd_context.hash(mot_de_passe)

def verifier_mot_de_passe(mot_de_passe: str, hash: str) -> bool:
    return pwd_context.verify(mot_de_passe, hash)

def valider_force_mot_de_passe(mot_de_passe: str) -> tuple[bool, list[str]]:
    erreurs = []
    
    if len(mot_de_passe) < 8:
        erreurs.append("Minimum 8 caractères requis")
    if not any(c.isupper() for c in mot_de_passe):
        erreurs.append("Au moins une lettre majuscule requise")
    if not any(c.islower() for c in mot_de_passe):
        erreurs.append("Au moins une lettre minuscule requise")
    if not any(c.isdigit() for c in mot_de_passe):
        erreurs.append("Au moins un chiffre requis")
    
    caracteres_speciaux = "@$!%*?&"
    if not any(c in caracteres_speciaux for c in mot_de_passe):
        erreurs.append(f"Au moins un caractère spécial requis ({caracteres_speciaux})")
    
    return len(erreurs) == 0, erreurs

def creer_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)

    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verifier_email(token: str) -> Optional[str]:
    """Récupères l'email du user dans le login"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")

        if not email:
            return None
        return email
    
    except JWTError:
        return None