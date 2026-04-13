import asyncio
from services.ocr import extraire_document

async def main():
    with open("test_facture.pdf", "rb") as f:
        contenu = f.read()
    
    resultat = await extraire_document(contenu, "application/pdf")
    
    print("Données extraites:")
    print(resultat["donnees"])
    print("\nMétriques:")
    print(resultat["metriques"])

asyncio.run(main())