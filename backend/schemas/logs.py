from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    timestamp: datetime
    action: str
    table_cible: str
    item_id: int | None
    detail: str | None


class OcrStatRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    timestamp: datetime
    nom_fichier: str
    type_document: str
    type_mime: str
    taille_fichier: int
    nb_pages: int
    nb_champs_extraits: int
    nb_champs_vides: int
    taux_completude: float
    duree_ms: int
    duree_ocr_ms: int
    duree_extraction_ms: int
    succes: bool
    resultat_json: str | None
