import pymupdf
import base64
from core.settings import settings
from mistralai.client import Mistral
from pydantic import BaseModel
from mistralai.extra import response_format_from_pydantic_model

class DocumentExtrait(BaseModel):
    numero: str | None
    date: str | None
    fournisseur: str | None
    montant_ht: float | None
    montant_ttc: float | None

def extraire_texte_ou_image(path: str):
    doc = pymupdf.open(path)
    page = doc[0]
    
    texte = page.get_text()
    
    if texte.strip():
        return {"type": "natif", "contenu": texte}
    else:
        image = page.get_pixmap()
        image.save("page.png")
        return {"type": "scan", "contenu": "page.png"}

def encode_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode("utf-8")

client = Mistral(api_key=settings.MISTRAL_API_KEY)
pdf_path = settings.EXEMPLE
base64_pdf = encode_pdf(pdf_path)

def ocr_et_extraire(contenu: bytes):
    import base64
    pdf_b64 = base64.b64encode(contenu).decode()
    
    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{pdf_b64}"
        },
        document_annotation_format=response_format_from_pydantic_model(DocumentExtrait),
        document_annotation_prompt="Extrais les informations de ce document"
    )
    
    return response.document_annotation