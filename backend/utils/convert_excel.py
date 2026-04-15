import pandas as pd
import json
from pathlib import Path

fichiers = {
    "ordinateurs": "data/inventaire_pc.xlsx",
    "ecrans": "data/inventaire_ecrans.xlsx",
}

resultat = {}
for cle, fichier in fichiers.items():
    df = pd.read_excel(fichier)
    df = df.where(pd.notna(df), None)  # remplace NaN par None
    resultat[cle] = df.to_dict(orient="records")

with open("data/seed_data.json", "w", encoding="utf-8") as f:
    json.dump(resultat, f, ensure_ascii=False, indent=2)

print("Conversion terminée")