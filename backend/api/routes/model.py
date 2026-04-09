from fastapi import APIRouter, UploadFile, File, Depends
from requests import Session
from db.session import get_db
from core.dependencies import require_role

model = APIRouter()

@model.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(require_role("user", "admin"))
):
    contenu = await file.read()  # bytes bruts
    nom = file.filename
    type_mime = file.content_type  # "application/pdf"
    
    return {"nom": nom, "taille": len(contenu)}