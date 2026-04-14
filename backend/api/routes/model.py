from time import time
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from core.dependencies import require_role
from services.ocr import extraire_document
from core.logger import logger
from db.models.documents import BonDeCommande, Facture, Devis
from db.models.ocr_stats import OcrStat

model = APIRouter()

@model.post("/upload/{type_document}/{equipement_id}")
async def upload_document(
    type_document: str,    # "facture", "devis", "bon_commande"
    equipement_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "user"))
):
    
    debut_total = time()
    # 1. Vérifier le type de fichier
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Format non supporté — PDF, JPG ou PNG uniquement")
    
    # 2. Lire en mémoire
    contenu = await file.read()
    
    # 3. OCR Mistral
    try:
        result = await extraire_document(contenu, file.content_type)
        donnees = result["donnees"]
        metriques = result["metriques"]
        logger.info(f"OCR réussi pour {file.filename}")
    except Exception as e:
        logger.error(f"Erreur OCR : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'extraction OCR")
    
    # 4. Stocker selon le type
    if type_document == "facture":
        doc = Facture(
            equipement_id=equipement_id,
            fournisseur=donnees.get("fournisseur"),
            montant=donnees.get("montant_ttc"),
            date_facture=donnees.get("date_document"),
            numero_facture=donnees.get("numero_document"),
        )

    elif type_document == "devis":
        doc = Devis(
            equipement_id=equipement_id,
            fournisseur=donnees.get("fournisseur"),
            date_devis=donnees.get("date_document"),
        )

    elif type_document == "bon_commande":
        doc = BonDeCommande(
            equipement_id=equipement_id,
            numero_bon=donnees.get("numero_document"),
            fournisseur=donnees.get("fournisseur"),
            date_commande=donnees.get("date_document"),
        )
    else:
        raise HTTPException(status_code=400, detail="Type de document invalide")

    duree_ms = int((time() - debut_total) * 1000)
    stat = OcrStat(
        user_id=current_user.id,
        type_document=type_document,
        nom_fichier=file.filename,
        type_mime=file.content_type,
        taille_fichier=len(contenu),
        duree_ms=duree_ms,
        **metriques  # ← dépaquète le dict du service
    )
    
    db.add(doc)
    db.add(stat)
    db.commit()
    db.refresh(doc)
    
    # 5. Fichier jamais stocké — détruit automatiquement
    return {
        "message": "Document traité avec succès",
        "donnees_extraites": donnees
    }