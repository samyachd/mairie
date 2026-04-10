import base64
import json
from mistralai.client import Mistral
from core.settings import settings

client = Mistral(api_key=settings.MISTRAL_API_KEY)

async def extraire_document(contenu: bytes, type_mime: str) -> dict:
    # 1. Encoder le fichier en base64
    fichier_b64 = base64.standard_b64encode(contenu).decode("utf-8")
    
    # 2. Appel Mistral OCR
    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:{type_mime};base64,{fichier_b64}"
        },
        include_image_base64=False
    )
    
    # 3. Extraire le texte
    texte = "\n".join([page.markdown for page in response.pages])
    
    # 4. Extraire les données structurées avec un second appel
    extraction = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "user",
                "content": f"""Extrais les informations suivantes de ce document en JSON :
                - nom_client
                - marque
                - numéro_de_commande
                - fournisseur
                - montant_ht
                - montant_ttc
                - date_document
                - numero_document
                
                Document :
                {texte}
                
                Réponds UNIQUEMENT en JSON valide, sans texte autour."""
            }
        ]
    )
    
    # 5. Parser le JSON
    try:
        donnees = json.loads(extraction.choices[0].message.content)
    except json.JSONDecodeError:
        donnees = {}
    
    return donnees