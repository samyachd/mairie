import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.dependencies import get_current_user
from core.security import verifier_mot_de_passe,creer_access_token
from backend.db.models.models import User
from db.session import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/connexion", tags=["Authentication"])
    
# Route de connexion
@router.post("/connexion")
def connexion(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    utilisateur = db.query(User).filter(
        User.email == form.username,
    ).first()
    
    if not utilisateur:
        raise HTTPException(status_code=401, detail="L'utilisateur n'existe pas")

    if not verifier_mot_de_passe(form.password, utilisateur.mot_de_passe_hash):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    access_token = creer_access_token(data={"sub": utilisateur.email, "role":utilisateur.role})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }, {"message": "Connexion réussie", "utilisateur_id": utilisateur.id}

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):

    print(f"Utilisateur {current_user.email} déconnecté")
    
    return {"message": "Déconnecté avec succès. Supprimez le token côté client."}