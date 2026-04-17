### Inventaire projet

## Setup

- télécharger le dossier du projet projet
- setup un .env à la racine en utilisant le .env-example
- créer un dossier data à la racine, avec dedans :
    - excel_test : fichiers excel cibles à extraire
    - raw extracts : raw extracts du fichier excel
    - clean_extracts : clean extracts du fichier excel
    - seed : json de données qui sert actuellement de seed à la BDD

- mettre un fichier excel dans le dossier excel_test
- run la commande CLI make setup. elle extrait un json du test, run un npm install et un uv pip install.
- si les données du clean_extract correspond, mettre le fichier dans seed
- faire un make run : 
    - lance le dockerdev qui contient postgre/grafana/prometheus/loki/promtail
    - lance le backend
    - lance le frontend
    - ouvres la doc api et localhost:3000
