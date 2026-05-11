import base64
import json
import time
from mistralai.client import Mistral
import re
from core.settings import settings

client = Mistral(api_key=settings.MISTRAL_API_KEY)

CHAMPS = [
    "type_document", "fournisseur", "montant_ttc", "montant_ht",
    "date_document", "numero_document", "marque",
    "numero_de_commande", "tag", "date_achat", "fin_garantie",
    "type_equipement",
]


async def extraire_document(contenu: bytes, type_mime: str) -> dict:
    fichier_b64 = base64.standard_b64encode(contenu).decode("utf-8")

    if type_mime == "application/pdf":
        document = {
            "type": "document_url",
            "document_url": f"data:{type_mime};base64,{fichier_b64}",
        }
    else:
        document = {
            "type": "image_url",
            "image_url": f"data:{type_mime};base64,{fichier_b64}",
        }

    debut_ocr = time.time()
    response = await client.ocr.process_async(
        model="mistral-ocr-latest",
        document=document,
        include_image_base64=False,
    )
    duree_ocr_ms = int((time.time() - debut_ocr) * 1000)

    texte = "\n".join([page.markdown for page in response.pages])
    nb_pages = len(response.pages)

    debut_extraction = time.time()
    extraction = await client.chat.complete_async(
        model="mistral-small-latest",
        messages=[
            {
                "role": "user",
                "content": f"""Extrais TOUS les équipements listés dans ce document sous forme d'un tableau JSON.
Chaque élément du tableau représente UN équipement physique distinct.

Pour chaque équipement, extrais :
- type_document (UN SEUL parmi 'devis', 'bon_de_commande', 'facture')
- type_equipement (UN SEUL parmi 'PC FIXE', 'PC PORTABLE', 'ECRAN', 'AUTRE')
- marque
- tag (numéro de série ou référence individuelle de l'équipement — doit être UNIQUE par équipement)
- fournisseur
- date_document (format YYYY-MM-DD)
- numero_document
- numero_de_commande
- date_achat (format YYYY-MM-DD)
- fin_garantie (format YYYY-MM-DD)
- montant_ttc (prix unitaire TTC, pas le total de la ligne)
- montant_ht (prix unitaire HT)

Règles STRICTES :
- Chaque tag ne doit apparaître QU'UNE SEULE fois dans le tableau. Ne duplique jamais un tag.
- Si le document liste des tags individuels (ex: SN001, SN002, SN003), crée un élément par tag.
- Si une ligne indique une quantité sans tags individuels (ex: "6x Dell"), crée exactement autant d'éléments que la quantité, chacun avec tag null.
- Si un champ est commun à tous (fournisseur, date_document...), répète-le dans chaque élément.
- Mets null pour tout champ absent. Ne devine pas.
- Si aucun équipement n'est identifiable, retourne [].

Document :
{texte}

Réponds UNIQUEMENT avec un tableau JSON valide, sans texte autour.""",
            }
        ],
    )
    duree_extraction_ms = int((time.time() - debut_extraction) * 1000)

    try:
        contenu_json = extraction.choices[0].message.content
        contenu_json = re.sub(r"^```json\s*", "", contenu_json.strip())
        contenu_json = re.sub(r"\s*```$", "", contenu_json.strip())
        items = json.loads(contenu_json)
        if not isinstance(items, list):
            items = [items] if isinstance(items, dict) else []
    except (json.JSONDecodeError, AttributeError):
        items = []

    # Deduplicate by tag — keep first occurrence of each non-null tag
    seen_tags: set[str] = set()
    unique_items = []
    for item in items:
        tag = item.get("tag")
        if tag and tag in seen_tags:
            continue
        if tag:
            seen_tags.add(tag)
        unique_items.append(item)
    items = unique_items

    nb_items = len(items)
    nb_champs_total = nb_items * len(CHAMPS) if nb_items else len(CHAMPS)
    nb_champs_remplis = sum(
        len([k for k in CHAMPS if item.get(k)]) for item in items
    ) if items else 0
    type_document = items[0].get("type_document") if items else "inconnu"

    return {
        "donnees": items,
        "metriques": {
            "duree_ocr_ms": duree_ocr_ms,
            "duree_extraction_ms": duree_extraction_ms,
            "nb_pages": nb_pages,
            "nb_champs_extraits": nb_champs_remplis,
            "nb_champs_vides": nb_champs_total - nb_champs_remplis,
            "taux_completude": nb_champs_remplis / nb_champs_total if nb_champs_total else 0.0,
            "resultat_json": json.dumps(items, ensure_ascii=False),
            "_type_document": type_document,
        },
    }
