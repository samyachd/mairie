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
df.columns = df.columns.str.replace("\n", " ").str.strip()  # Supprime les sauts de ligne et les espaces
df = df.rename(columns={"Unnamed: 0": "SERVICE",
                        "Unnamed: 1": "EMPLACEMENT",
                        "Unnamed: 2": "UTILISATEUR PRINCIPAL",
                        "Unnamed: 3": "NOM RESEAU",
                        "Unnamed: 4": "N° SERIE PC",
                        "Unnamed: 5": "CLEF WIFI",
                        "Unnamed: 6": "LECTEUR DVD/CD EXTERNE",
                        "Unnamed: 7": "WEBCAM",
                        "Unnamed: 8": "CASQUE",
                        "Unnamed: 9": "TYPE",
                        "Unnamed: 10": "MAC ADRESSE ETHERNET",
                        "Unnamed: 11": "MAC ADRESSE WIFI",
                        "Unnamed: 12": "DATE FIN GARANTIE PC",
                        "Unnamed: 13": "MARQUE PC",
                        "Unnamed: 14": "DATE ACHAT PC",
                        "Unnamed: 15": "FOURNISSEUR PC",
                        "Unnamed: 16": "N° BC PC",
                        "Unnamed: 17": "Adresse IP PC",
                        "Unnamed: 18": "eligible W10",
                        "Unnamed: 19": "OS",
                        "Unnamed: 20": "TYPE LICENCE PC",
                        "Unnamed: 21": "Clé OS PC",
                        "Unnamed: 22": "PROCESSEUR PC",
                        "Unnamed: 23": "RAM PC",
                        "Unnamed: 24": "ABSOLUTE DELL",
                        "Unnamed: 25": "DATE ACHAT OFFICE",
                        "Unnamed: 26": "FOURNISSEUR OFFICE",
                        "Unnamed: 27": "BC OFFICE",
                        "Unnamed: 28": "VERSION OFFICE",
                        "Unnamed: 29": "TYPE LICENCE OFFICE",
                        "Unnamed: 30": "CLEF ACTIVATION",
                        "Unnamed: 31": "DATE ACTIVATION",
                        "Unnamed: 32": "Mail ACTIVATION",
                        "Unnamed: 33": "CLEF OFFICE",
                        "Unnamed: 34": "N° CONTRAT OPEN MICROSOFT",
                        "Unnamed: 35": "TYPE ECRAN 1",
                        "Unnamed: 36": "MARQUE ECRAN 1",
                        "Unnamed: 37": "MODELE ECRAN 1",
                        "Unnamed: 38": "N° SERIE ECRAN 1",
                        "Unnamed: 39": "FOURNISSEUR ECRAN 1",
                        "Unnamed: 40": "N° BC ECRAN 1",
                        "Unnamed: 41": "DATE ACHAT ECRAN 1",
                        "Unnamed: 42": "DATE FIN GARANTIE ECRAN 1",
                        "Unnamed: 43": "TYPE ECRAN 2",
                        "Unnamed: 44": "MARQUE ECRAN 2",
                        "Unnamed: 45": "MODELE ECRAN 2",
                        "Unnamed: 46": "N° SERIE ECRAN 2",
                        "Unnamed: 47": "FOURNISSEUR ECRAN 2",
                        "Unnamed: 48": "N° BC ECRAN 2",
                        "Unnamed: 49": "DATE ACHAT ECRAN 2",
                        "Unnamed: 50": "DATE FIN GARANTIE ECRAN 2",
                        "Unnamed: 51": "TYPE ECRAN 3",
                        "Unnamed: 52": "MARQUE ECRAN 3",
                        "Unnamed: 53": "MODELE ECRAN 3",
                        "Unnamed: 54": "N° SERIE ECRAN 3",
                        "Unnamed: 55": "FOURNISSEUR ECRAN 3",
                        "Unnamed: 56": "N° BC ECRAN 3",
                        "Unnamed: 57": "DATE ACHAT ECRAN 3",
                        "Unnamed: 58": "DATE FIN GARANTIE ECRAN 3",
                        "Unnamed: 59": "TYPE ECRAN TELETRAVAIL",
                        "Unnamed: 60": "MARQUE ECRAN TELETRAVAIL",
                        "Unnamed: 61": "MODELE ECRAN TELETRAVAIL",
                        "Unnamed: 62": "N° SERIE ECRAN TELETRAVAIL",
                        "Unnamed: 63": "FOURNISSEUR ECRAN TELETRAVAIL",
                        "Unnamed: 64": "N° BC ECRAN TELETRAVAIL",
                        "Unnamed: 65": "DATE ACHAT ECRAN TELETRAVAIL",
                        "Unnamed: 66": "DATE FIN GARANTIE ECRAN TELETRAVAIL",
                        "Unnamed: 67": "TYPE ECRAN TELETRAVAIL2",
                        "Unnamed: 68": "MARQUE ECRAN TELETRAVAIL3",
                        "Unnamed: 69": "MODELE ECRAN TELETRAVAIL4",
                        "Unnamed: 70": "N° SERIE ECRAN TELETRAVAIL5",
                        "Unnamed: 71": "FOURNISSEUR ECRAN TELETRAVAIL6",
                        "Unnamed: 72": "N° BC ECRAN TELETRAVAIL7",
                        "Unnamed: 73": "DATE ACHAT ECRAN TELETRAVAIL8",
                        "Unnamed: 74": "DATE FIN GARANTIE ECRAN TELETRAVAIL2"
                        })  # Renomme les colonnes
resultat = df.to_dict(orient="records")


with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(resultat, f, ensure_ascii=False, indent=2, default=str)

print(f"Nettoyage de {dernier_fichier.name} terminé")