from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import require_role
from schemas.ecran import EcranCreate, EcranRead, EcranUpdate
from db.session import get_db
from db.models import Ecrans

router = APIRouter(dependencies=[Depends(require_role("user","admin"))], prefix="/ecrans", tags=["ecrans"])

@router.post("/", response_model=EcranRead, status_code=status.HTTP_201_CREATED)
def create_ecran(ecran: EcranCreate, db: Session = Depends(get_db)):
    db_ecran = Ecrans(**ecran.model_dump(exclude_unset=True))
    db.add(db_ecran)
    db.commit()
    db.refresh(db_ecran)
    return db_ecran

@router.delete("/{ecran_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ecran(ecran_id: int, db: Session = Depends(get_db)):
    db_ecran = db.query(Ecrans).filter(Ecrans.id == ecran_id).first()
    if not db_ecran:
        raise HTTPException(status_code=404, detail="Ecran not found")
    db.delete(db_ecran)
    db.commit()
    return None

@router.put("/{ecran_id}", response_model=EcranRead)
def update_ecran(ecran_id: int, ecran: EcranUpdate, db: Session = Depends(get_db)):
    db_ecran = db.query(Ecrans).filter(Ecrans.id == ecran_id).first()
    if not db_ecran:
        raise HTTPException(status_code=404, detail="Ecran not found")

    data = ecran.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_ecran, key, value)

    db.commit()
    db.refresh(db_ecran)
    return db_ecran