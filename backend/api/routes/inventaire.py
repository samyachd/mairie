from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.inventaire import InventaireRead
from core.dependencies import get_current_user
from db.session import get_db
from db.models import Ecran, Ordinateur, OfficeLicense, Devis, BonDeCommande, Facture


router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[InventaireRead])
def read_ecrans(db: Session = Depends(get_db)):
    return InventaireRead(
        ordinateurs=db.query(Ordinateur).all(),
        ecrans=db.query(Ecran).all(),
        licenses=db.query(OfficeLicense).all(),
        devis=db.query(Devis).all(),
        bons_de_commande=db.query(BonDeCommande).all(),
        factures=db.query(Facture).all()
    )