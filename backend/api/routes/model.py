from time import time
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from core.dependencies import require_role
from services.ocr import extraire_document
from core.logger import logger
from db.models.ocr_stats import OcrStat

model = APIRouter()


@model.post("/extract")
async def extract_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "user")),
):
    """OCR-only — runs Mistral on the upload, returns the extracted fields.
    Caller is responsible for what to do with them (e.g. prefill a form).
    Nothing is persisted except an OCR stats row for monitoring."""
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Format non supporté — PDF, JPG ou PNG uniquement",
        )

    debut_total = time()
    contenu = await file.read()

    try:
        result = await extraire_document(contenu, file.content_type)
    except Exception as e:
        logger.error(f"Erreur OCR : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'extraction OCR")

    donnees = result["donnees"]   # list of items
    metriques = result["metriques"]
    duree_ms = int((time() - debut_total) * 1000)

    type_document = metriques.pop("_type_document", "inconnu") or "inconnu"

    stat = OcrStat(
        user_id=current_user.id,
        type_document=type_document,
        nom_fichier=file.filename,
        type_mime=file.content_type,
        taille_fichier=len(contenu),
        duree_ms=duree_ms,
        succes=True,
        **metriques,
    )
    db.add(stat)
    db.commit()

    logger.info(f"OCR réussi pour {file.filename} — {len(donnees)} équipement(s)")
    return {"donnees": donnees, "metriques": metriques}
