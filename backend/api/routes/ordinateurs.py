from fastapi import APIRouter, Depends, HTTPException, status
from core.dependencies import  require_role
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.ordinateur import OrdinateurCreate, OrdinateurRead, OrdinateurUpdate
from db.session import get_db
from db.models import Ordinateurs

router = APIRouter(dependencies=[Depends(require_role("user","admin"))], prefix="/ordinateurs", tags=["ordinateurs"])

@router.post("/", response_model=OrdinateurRead, status_code=status.HTTP_201_CREATED)
def create_ordinateur(ordinateur: OrdinateurCreate, db: Session = Depends(get_db)):
    db_ordinateur = Ordinateurs(**ordinateur.model_dump(exclude_unset=True))
    db.add(db_ordinateur)
    try:
        db.commit()
        db.refresh(db_ordinateur)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un ordinateur avec ce tag, IP ou MAC existe déjà"
        )
    return db_ordinateur

@router.delete("/{ordinateur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pc(ordinateur_id: int, db: Session = Depends(get_db)):
    db_ordinateur = db.query(Ordinateurs).filter(Ordinateurs.id == ordinateur_id).first()
    if not db_ordinateur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ordinateur inexistant")
    db.delete(db_ordinateur)
    db.commit()
    return None

@router.put("/{ordinateur_id}", response_model=OrdinateurRead)
def update_ordinateur(ordinateur_id: int, ordinateur: OrdinateurUpdate, db: Session = Depends(get_db)):
    db_ordinateur = db.query(Ordinateurs).filter(Ordinateurs.id == ordinateur_id).first()
    if not db_ordinateur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ordinateur inexistant")

    data = ordinateur.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_ordinateur, key, value)

    db.commit()
    db.refresh(db_ordinateur)
    return db_ordinateur