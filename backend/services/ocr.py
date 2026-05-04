import base64
import json
import time
from mistralai.client import Mistral
import re
from core.settings import settings

client = Mistral(api_key=settings.MISTRAL_API_KEY)

async def extraire_document(contenu: bytes, type_mime: str) -> dict:
    # 1. Encoder le fichier en base64
    fichier_b64 = base64.standard_b64encode(contenu).decode("utf-8")
    
    # 2. Appel Mistral OCR
    debut_ocr = time.time()
    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:{type_mime};base64,{fichier_b64}"
        },
        include_image_base64=False
    )
    duree_ocr_ms = int((time.time() - debut_ocr) * 1000)
    
    # 3. Extraire le texte
    texte = "\n".join([page.markdown for page in response.pages])
    nb_pages = len(response.pages)
    
    # 4. Extraire les données structurées avec un second appel
    debut_extraction = time.time()
    extraction = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "user",
                "content": f"""Extrais les informations suivantes de ce document en JSON :
                - type_document (UN SEUL parmi 'devis', 'bon_de_commande', 'facture' — un devis propose un prix, un bon de commande l'engage, une facture le réclame après livraison)
                - marque
                - montant_ttc
                - montant_ht
                - numero_de_commande
                - fournisseur
                - date_document (format YYYY-MM-DD)
                - numero_document
                - tag
                - date_achat (format YYYY-MM-DD)
                - fin_garantie (format YYYY-MM-DD)
                - type_equipement (UN SEUL parmi 'PC FIXE', 'PC PORTABLE', 'ECRAN', 'AUTRE')

                Mets `null` pour tout champ absent du document. Ne devine pas.

                Document :
                {texte}

                Réponds UNIQUEMENT en JSON valide, sans texte autour."""
            }
        ]
    )
    duree_extraction_ms = int((time.time() - debut_extraction) * 1000)
    
    # 5. Parser le JSON
    try:
        contenu_json = extraction.choices[0].message.content
        contenu_json = re.sub(r"^```json\s*", "", contenu_json.strip())
        contenu_json = re.sub(r"\s*```$", "", contenu_json.strip())
        donnees = json.loads(contenu_json)
    except json.JSONDecodeError:
        donnees = {}
    
    champs_attendus = ["type_document", "fournisseur", "montant_ttc", "montant_ht",
                       "date_document", "numero_document", "marque",
                       "numero_de_commande", "tag", "date_achat", "fin_garantie",
                       "type_equipement"]
    champs_remplis = len([k for k in champs_attendus if donnees.get(k)])
    
    return {
        "donnees": donnees,
        "metriques": {
            "duree_ocr_ms": duree_ocr_ms,
            "duree_extraction_ms": duree_extraction_ms,
            "nb_pages": nb_pages,
            "nb_champs_extraits": champs_remplis,
            "nb_champs_vides": len(champs_attendus) - champs_remplis,
            "taux_completude": champs_remplis / len(champs_attendus),
            "resultat_json": json.dumps(donnees, ensure_ascii=False)
        }
    }