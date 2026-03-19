from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas.inventaire import InventaireRead
from core.dependencies import get_current_user
from db.session import get_db
from db.models import Ecrans, OfficeLicenses, Ordinateurs

router = APIRouter(dependencies=[Depends(get_current_user)], prefix="/inventaire", tags=["inventaire"])

@router.get("/", response_model=list[InventaireRead])
def read_ecrans(db: Session = Depends(get_db)):
    return InventaireRead(
        ordinateurs=db.query(Ordinateurs).all(),
        ecrans=db.query(Ecrans).all(),
        licenses=db.query(OfficeLicenses).all()
    )