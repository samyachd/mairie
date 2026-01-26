from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()  # Charger les variables d'environnement depuis le fichier .env

# Configuration du contexte de hachage des mots de passe

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hacher_mot_de_passe(mot_de_passe: str) -> str:
    return pwd_context.hash(mot_de_passe)

def verifier_mot_de_passe(mot_de_passe_clair: str, mot_de_passe_hache: str) -> bool:
    return pwd_context.verify(mot_de_passe_clair, mot_de_passe_hache)

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

# ⚠️ IMPORTANT : Change cette clé en production !
# Génère-la avec : openssl rand -hex 32

SECRET_KEY = os.getenv("JWT_KEY")
if SECRET_KEY is None:
    raise ValueError("JWT_KEY n'est pas définie dans les variables d'environnement")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Le token expire après 30 minutes

def creer_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crée un JWT token
    
    Args:
        data: Les données à inclure dans le token (ex: {"sub": "user@example.com"})
        expires_delta: Durée de validité personnalisée (optionnel)
    
    Returns:
        Le token JWT sous forme de string
    
    Exemple:
        >>> token = creer_access_token({"sub": "user@example.com"})
        >>> print(token)
        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    # Copier les données pour ne pas modifier l'original
    to_encode = data.copy()
    
    # Définir l'expiration
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Ajouter l'expiration au payload
    to_encode.update({"exp": expire})
    
    # Créer le token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verifier_token(token: str) -> Optional[str]:
    """
    Vérifie et décode un JWT token
    
    Args:
        token: Le token JWT à vérifier
    
    Returns:
        L'email de l'utilisateur si le token est valide, None sinon
    
    Exemple:
        >>> email = verifier_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        >>> print(email)
        user@example.com
    """
    try:
        # Décoder le token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Récupérer l'email (subject)
        email: str = payload.get("sub")
        
        if email is None:
            return None
            
        return email
        
    except JWTError:
        # Token invalide, expiré, ou signature incorrecte
        return None

