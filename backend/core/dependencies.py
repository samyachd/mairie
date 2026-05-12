from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from db.models.base import TokenBlacklist
from db.models.user import User as Utilisateur
from db.session import get_db
from core import verifier_email as verifier_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: Session = Depends(get_db)):
    # 1. Verify signature and expiry first — no DB hit for invalid tokens
    email = verifier_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Check blacklist only for structurally valid tokens, skip already-expired rows
    blacklisted = db.query(TokenBlacklist).filter(
        TokenBlacklist.token == credentials.credentials,
        TokenBlacklist.expire_at > datetime.now(timezone.utc),
    ).first()
    if blacklisted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalidé",
            headers={"WWW-Authenticate": "Bearer"},
        )

    utilisateur = db.query(Utilisateur).filter(Utilisateur.email == email).first()
    if utilisateur is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé",
        )

    return utilisateur

def require_role(*roles: str):
    def dependency(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Accès refusé. Rôles requis : {roles}",
            )
        return current_user
    return dependency
