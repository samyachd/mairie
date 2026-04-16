from datetime import datetime
import pandas as pd
import json
from pathlib import Path

INPUT_DIR = Path("../data/raw_extracts")
OUTPUT_DIR = Path("../data/clean_extracts")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT = OUTPUT_DIR / f"seed_data_{TIMESTAMP}.json"

fichiers_json = sorted(INPUT_DIR.glob("seed_data_*.json"))

if not fichiers_json:
    print("Aucun fichier seed_data trouvé")
    exit()

dernier_fichier = fichiers_json[-1]

print(dernier_fichier.name)

data = json.loads(dernier_fichier.read_text(encoding="utf-8"))
df = pd.DataFrame(data["inventaire"])  # Remplacez "inventaire" par la clé appropriée si nécessaire
df = df.drop(df.index[[0,1]])
df = df.rename(columns={"Unnamed: 0": "SERVICE",
                        "Unnamed: 1": "EMPLACEMENT",
                        "Unnamed: 2": "UTILISATEUR PRINCIPAL",
                        "Unnamed: 3": "NOM RESEAU",
                        "Unnamed: 4": "N° SERIE\nPC",
                        "Unnamed: 5": "CLEF WIFI",
                        "Unnamed: 6": "LECTEUR DVD/CD EXTERNE",
                        "Unnamed: 7": "WEBCAM",
                        "Unnamed: 8": "CASQUE",
                        "Unnamed: 9": "TYPE",
                        "Unnamed: 10": "MAC ADRESSE\nETHERNET\n",
                        "Unnamed: 11": "MAC ADRESSE\nWIFI",
                        "Unnamed: 12": "DATE FIN GARANTIE\nPC",
                        "Unnamed: 13": "MARQUE\nPC",
                        "Unnamed: 14": "DATE ACHAT\nPC",
                        "Unnamed: 15": "FOURNISSEUR PC",
                        "Unnamed: 16": "N° BC\nPC",
                        "Unnamed: 17": "Adresse IP\nPC",
                        "Unnamed: 18": "eligible W10",
                        "Unnamed: 19": "OS",
                        "Unnamed: 20": "TYPE LICENCE PC",
                        "Unnamed: 21": "Clé OS\nPC",
                        "Unnamed: 22": "PROCESSEUR\nPC",
                        "Unnamed: 23": "RAM\nPC",
                        "Unnamed: 24": "ABSOLUTE DELL",
                        "Unnamed: 25": "DATE\nACHAT\nOFFICE",
                        "Unnamed: 26": "FOURNISSEUR\nOFFICE",
                        "Unnamed: 27": "BC\nOFFICE",
                        "Unnamed: 28": "VERSION\nOFFICE",
                        "Unnamed: 29": "TYPE LICENCE\nOFFICE",
                        "Unnamed: 30": "CLEF ACTIVATION",
                        "Unnamed: 31": "DATE\nACTIVATION",
                        "Unnamed: 32": "Mail\nACTIVATION",
                        "Unnamed: 33": "CLEF OFFICE",
                        "Unnamed: 34": "N° CONTRAT\nOPEN MICROSOFT",
                        "Unnamed: 35": "TYPE\nECRAN 1",
                        "Unnamed: 36": "MARQUE\nECRAN 1",
                        "Unnamed: 37": "MODELE\nECRAN 1",
                        "Unnamed: 38": "N° SERIE\nECRAN 1",
                        "Unnamed: 39": "FOURNISSEUR\nECRAN 1",
                        "Unnamed: 40": "N° BC\nECRAN 1",
                        "Unnamed: 41": "DATE ACHAT\nECRAN 1",
                        "Unnamed: 42": "DATE FIN\nGARANTIE\nECRAN 1",
                        "Unnamed: 43": "TYPE\nECRAN 2",
                        "Unnamed: 44": "MARQUE\nECRAN 2",
                        "Unnamed: 45": "MODELE\nECRAN 2",
                        "Unnamed: 46": "N° SERIE\nECRAN 2",
                        "Unnamed: 47": "FOURNISSEUR\nECRAN 2",
                        "Unnamed: 48": "N° BC\nECRAN 2",
                        "Unnamed: 49": "DATE ACHAT\nECRAN 2",
                        "Unnamed: 50": "DATE FIN\nGARANTIE\nECRAN 2",
                        "Unnamed: 51": "TYPE\nECRAN 3",
                        "Unnamed: 52": "MARQUE\nECRAN 3",
                        "Unnamed: 53": "MODELE\nECRAN 3",
                        "Unnamed: 54": "N° SERIE\nECRAN 3",
                        "Unnamed: 55": "FOURNISSEUR\nECRAN 3",
                        "Unnamed: 56": "N° BC\nECRAN 3",
                        "Unnamed: 57": "DATE ACHAT\nECRAN 3",
                        "Unnamed: 58": "DATE FIN\nGARANTIE\nECRAN 3",
                        "Unnamed: 59": "TYPE\nECRAN TELETRAVAIL",
                        "Unnamed: 60": "MARQUE ECRAN\nTELETRAVAIL",
                        "Unnamed: 61": "MODELE\nECRAN TELETRAVAIL",
                        "Unnamed: 62": "N° SERIE\nECRAN TELETRAVAIL",
                        "Unnamed: 63": "FOURNISSEUR\nECRAN TELETRAVAIL",
                        "Unnamed: 64": "N° BC\nECRAN TELETRAVAIL",
                        "Unnamed: 65": "DATE ACHAT\nECRAN TELETRAVAIL",
                        "Unnamed: 66": "DATE FIN\nGARANTIE\nECRAN TELETRAVAIL",
                        "Unnamed: 67": "TYPE\nECRAN TELETRAVAIL2",
                        "Unnamed: 68": "MARQUE ECRAN\nTELETRAVAIL3",
                        "Unnamed: 69": "MODELE\nECRAN TELETRAVAIL4",
                        "Unnamed: 70": "N° SERIE\nECRAN TELETRAVAIL5",
                        "Unnamed: 71": "FOURNISSEUR\nECRAN TELETRAVAIL6",
                        "Unnamed: 72": "N° BC\nECRAN TELETRAVAIL7",
                        "Unnamed: 73": "DATE ACHAT\nECRAN TELETRAVAIL8",
                        "Unnamed: 74": "DATE FIN\nGARANTIE\nECRAN TELETRAVAIL2"
                        })  # Renomme les colonnes
df.columns = df.columns.str.replace("\n", " ").str.strip()  # Supprime les sauts de ligne et les espaces
resultat = df.to_dict(orient="records")


with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(resultat, f, ensure_ascii=False, indent=2, default=str)

print(f"Nettoyage de {dernier_fichier.name} terminé")