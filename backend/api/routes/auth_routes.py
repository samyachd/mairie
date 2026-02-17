import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from core.dependencies import get_current_user
from core.security import (hacher_mot_de_passe,
                           valider_force_mot_de_passe,
                           verifier_mot_de_passe,
                           creer_access_token,
                           verifier_token)
from db.models import User
from db.session import get_db
from schemas.users import UserLogin

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])
    
# Route de connexion
@router.post("/connexion")
def connexion(user: UserLogin, db: Session = Depends(get_db)):
    
    utilisateur = db.query(User).filter(
        User.email == user.email
    ).first()
    
    if not utilisateur:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    if not verifier_mot_de_passe(user.mot_de_passe, utilisateur.mot_de_passe_hache):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    access_token = creer_access_token(data={"sub": utilisateur.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }, {"message": "Connexion réussie", "utilisateur_id": utilisateur.id}

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):

    print(f"Utilisateur {current_user.email} déconnecté")
    
    return {"message": "Déconnecté avec succès. Supprimez le token côté client."}