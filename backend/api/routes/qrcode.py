import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.ordinateur import Ordinateur
from db.models.ecran import Ecran
from core.dependencies import require_role
from services.qrcode import generate_qr, generate_qr_zip

qrcode_router = APIRouter(dependencies=[Depends(require_role("read", "user", "admin"))])


# /all routes must be declared before /{id} so FastAPI doesn't try to cast "all" as int

@qrcode_router.get("/ordinateur/all", response_class=StreamingResponse)
def qr_all_ordinateurs(db: Session = Depends(get_db)):
    rows = db.query(Ordinateur).all()
    items = [(obj.tag or f"ORD-{obj.id}", obj.tag or f"ORD-{obj.id}") for obj in rows]
    return generate_qr_zip(items, "qrcodes-ordinateurs.zip")


@qrcode_router.get("/ecran/all", response_class=StreamingResponse)
def qr_all_ecrans(db: Session = Depends(get_db)):
    rows = db.query(Ecran).all()
    items = [(obj.tag or f"ECR-{obj.id}", obj.tag or f"ECR-{obj.id}") for obj in rows]
    return generate_qr_zip(items, "qrcodes-ecrans.zip")


@qrcode_router.get("/ordinateur/{id}", response_class=StreamingResponse)
def qr_ordinateur(id: int, db: Session = Depends(get_db)):
    obj = db.get(Ordinateur, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Ordinateur introuvable")
    return generate_qr(obj.tag or f"ORD-{obj.id}")


@qrcode_router.get("/ecran/{id}", response_class=StreamingResponse)
def qr_ecran(id: int, db: Session = Depends(get_db)):
    obj = db.get(Ecran, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Écran introuvable")
    return generate_qr(obj.tag or f"ECR-{obj.id}")
