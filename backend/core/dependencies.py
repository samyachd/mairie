from fastapi import Depends, HTTPException, status
from fastapi import security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from db.models import User as Utilisateur
from db.session import get_db
from core.security import verifier_token

security = HTTPBearer()

def obtenir_utilisateur_actuel(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Récupère l'utilisateur à partir du JWT token
    Utilisable avec Depends() dans les routes protégées
    """
    # Récupérer le token
    token = credentials.credentials
    
    # Vérifier le token
    email = verifier_token(token)
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Trouver l'utilisateur
    utilisateur = db.query(Utilisateur).filter(Utilisateur.email == email).first()
    
    if utilisateur is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé"
        )
    
    return utilisateur