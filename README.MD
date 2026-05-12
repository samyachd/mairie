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


## Prérequis

- Docker et Docker Compose installés
- Git

## Installation

1. Cloner le dépôt :
   git clone <url>
   cd mairie

2. Créer le fichier .env à partir du template :
   cp .env.example .env
   # Éditer .env avec les valeurs appropriées (DB, JWT_SECRET, MISTRAL_API_KEY)

3. Lancer la stack :
   docker compose -f docker-compose.dev.yml up --build

4. Appliquer les migrations :
   docker compose -f docker-compose.dev.yml exec backend alembic upgrade head

5. Seeder les données initiales :
   docker compose -f docker-compose.dev.yml exec backend python -m utils.seed

L'API est disponible sur http://localhost:8000/docs
Grafana sur http://localhost:3001
Prometheus sur http://localhost:9090