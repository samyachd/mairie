import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from core.constants import PAGINATION_LIMIT_DEFAULT, PAGINATION_SKIP_DEFAULT
from core.dependencies import get_current_user
from core.security import (hacher_mot_de_passe,
                           valider_force_mot_de_passe,)
from db.models import User
from db.session import get_db
from schemas.users import UserCreate, UserRead, UserUpdate

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/inscription", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def inscription(user: UserCreate, db: Session = Depends(get_db)):
    # On vérifier si l'email est déjà enregistré dans la DB
    utilisateur_existant = db.query(User).filter(
        User.email == user.email
    ).first()
    if utilisateur_existant:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    # On force la validation du mot de passe
    est_valide, erreurs = valider_force_mot_de_passe(user.mot_de_passe)
    if not est_valide:
        raise HTTPException(status_code=400, detail={"erreurs": erreurs})
    
    mot_de_passe_hache = hacher_mot_de_passe(user.mot_de_passe)
    
    try:
        db_user = User(
        email=user.email,
        nom=user.name,
        mot_de_passe_hache=mot_de_passe_hache
    )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User created: {db_user.id}")
        return {"message": "Compte créé avec succès", "id": db_user.id}
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=400, detail="Error creating user")
    
@router.get("/", response_model=list[UserRead])
def read_users(
    skip: int = PAGINATION_SKIP_DEFAULT,
    limit: int = PAGINATION_LIMIT_DEFAULT,
    db: Session = Depends(get_db),
):
    users = db.query(User).offset(skip).limit(limit).all()
    logger.debug(f"Retrieved {len(users)} users")
    return users

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        logger.warning(f"Delete user not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    logger.info(f"User deleted: {user_id}")
    return None


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        logger.warning(f"Update user not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    data = user.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    logger.info(f"User updated: {user_id}")
    return db_user
