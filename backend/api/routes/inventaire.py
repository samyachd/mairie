from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.inventaire import InventaireRead
from core.dependencies import get_current_user
from db.session import get_db
from db.models.ecran import Ecran
from db.models.ordinateur import Ordinateur
from db.models.office_license import OfficeLicense

router = APIRouter(dependencies=[Depends(get_current_user)], prefix="/inventaire", tags=["inventaire"])

@router.get("/", response_model=list[InventaireRead])
def read_ecrans(db: Session = Depends(get_db)):
    return InventaireRead(
        ordinateurs=db.query(Ordinateur).all(),
        ecrans=db.query(Ecran).all(),
        licenses=db.query(OfficeLicense).all()
    )