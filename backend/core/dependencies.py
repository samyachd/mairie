from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from db.models.base import TokenBlacklist
from db.models.user import User as Utilisateur
from db.session import get_db
from core.security import verifier_email as verifier_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: Session = Depends(get_db)):
    """
    Récupère l'utilisateur à partir du JWT token
    Utilisable avec Depends() dans les routes protégées
    """
    token = credentials.credentials

    blacklisted = db.query(TokenBlacklist).filter(
        TokenBlacklist.token == token
    ).first()
    
    if blacklisted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalidé",
            headers={"WWW-Authenticate": "Bearer"}
        )

    email = verifier_token(token)

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"}
        )

    utilisateur = db.query(Utilisateur).filter(Utilisateur.email == email).first()

    if utilisateur is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé"
        )

    return utilisateur

def require_role(*roles: str):
    """Factory : crée une dépendance qui vérifie le rôle"""
    def dependency(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Accès refusé. Rôles requis : {roles}"
            )
        return current_user
    return dependency
