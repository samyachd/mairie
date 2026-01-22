# 📦 Mairie - Système d'Inventaire

Système de gestion d'inventaire pour les équipements informatiques (ordinateurs, écrans, licenses) d'une mairie.

## 🎯 Fonctionnalités

- **Gestion des Utilisateurs** : Création, lecture, mise à jour, suppression d'utilisateurs
- **Gestion des Ordinateurs** : Suivi complet des PC avec propriétaires, configurations, garanties
- **Gestion des Écrans** : Inventaire des moniteurs avec références aux ordinateurs
- **Gestion des Licenses** : Suivi des licenses Office avec associations aux PC
- **API RESTful** : FastAPI avec documentation automatique (Swagger)
- **Base de Données** : PostgreSQL avec SQLAlchemy ORM et migrations Alembic
- **Tests** : Suite de tests unitaires et d'intégration avec pytest

## 🛠️ Stack Technique

- **Backend** : FastAPI 0.128+
- **Base de Données** : PostgreSQL + SQLAlchemy 2.0
- **Migrations** : Alembic 1.17+
- **Validation** : Pydantic 2.12+
- **Tests** : pytest 9.0+
- **Linting** : ruff 0.14+
- **Typing** : mypy 1.19+
- **Frontend** : React 19.2 (en développement)

## 📋 Prérequis

- Python 3.12+
- PostgreSQL 12+
- pip ou uv (gestionnaire de paquets)

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/samyachd/mairie.git
cd mairie
```

### 2. Créer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances
```bash
pip install -e .
# ou
uv sync
```

### 4. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditer .env avec vos informations PostgreSQL
```

### 5. Créer la base de données
```bash
createdb mairie_db
```

### 6. Appliquer les migrations
```bash
alembic upgrade head
```

## 🚀 Démarrage

### Lancer le serveur
```bash
uvicorn backend.app.main:app --reload
```

L'API sera disponible sur `http://localhost:8000`

### Documentation Interactive
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 📚 Structure du Projet

```
mairie/
├── backend/
│   └── app/
│       ├── main.py              # Application FastAPI
│       ├── api/
│       │   └── routes/          # Routes API (users, ordinateurs, etc)
│       ├── db/
│       │   ├── models.py        # Modèles SQLAlchemy
│       │   ├── session.py       # Configuration DB
│       │   └── db.py            # Base class
│       ├── core/
│       │   ├── settings.py      # Configuration
│       │   ├── security.py      # Authentification/Sécurité
│       │   └── constants.py     # Constantes globales
│       └── schemas/             # Schémas Pydantic
├── tests/
│   ├── conftest.py             # Fixtures pytest
│   ├── unit/
│   │   ├── api/                # Tests des routes
│   │   └── db/                 # Tests des modèles
│   └── integration/            # Tests d'intégration
├── alembic/                     # Migrations DB
├── frontend/                    # Application React
├── notebooks/                   # Jupyter notebooks (RAG/CAG)
├── pyproject.toml              # Dépendances Python
└── .env.example                # Variables d'env exemple
```

## 🧪 Tests

### Lancer tous les tests
```bash
pytest
```

### Lancer avec couverture de code
```bash
pytest --cov=backend tests/
```

### Mode verbose
```bash
pytest -v
```

### Tests spécifiques
```bash
pytest tests/unit/api/test_users.py -v
pytest tests/integration/ -v
```

## 📝 Endpoints API

### Users
- `POST /users/` - Créer un utilisateur
- `GET /users/` - Lister les utilisateurs (pagination)
- `GET /users/{id}` - Détails d'un utilisateur
- `PUT /users/{id}` - Mettre à jour un utilisateur
- `DELETE /users/{id}` - Supprimer un utilisateur

### Ordinateurs
- `POST /ordinateurs/` - Créer un PC
- `GET /ordinateurs/` - Lister les PC
- `GET /ordinateurs/{id}` - Détails d'un PC
- `PUT /ordinateurs/{id}` - Mettre à jour un PC
- `DELETE /ordinateurs/{id}` - Supprimer un PC

### Écrans
- `POST /ecrans/` - Créer un écran
- `GET /ecrans/` - Lister les écrans
- `GET /ecrans/{id}` - Détails d'un écran
- `PUT /ecrans/{id}` - Mettre à jour un écran
- `DELETE /ecrans/{id}` - Supprimer un écran

### Licenses
- `POST /licenses/` - Créer une license
- `GET /licenses/` - Lister les licenses
- `GET /licenses/{id}` - Détails d'une license
- `PUT /licenses/{id}` - Mettre à jour une license
- `DELETE /licenses/{id}` - Supprimer une license

## 🔐 Sécurité

### Configurations actuelles
- CORS configuré pour localhost et domaines approuvés
- Validation des entrées avec Pydantic
- Gestion des erreurs HTTP cohérente
- Logging des opérations sensibles

### À implémenter
- [ ] Authentification JWT/OAuth2
- [ ] Système de rôles et permissions
- [ ] Rate limiting
- [ ] Audit trail des modifications
- [ ] Soft delete

## 📊 Modèles de Données

### User
```python
- id: int (PK)
- name: str
- email: str (unique)
- created_at: datetime
```

### Ordinateurs
```python
- id: int (PK)
- type_pc: str
- marque: str
- proprietaire: str
- service: str
- batiment: str
- ram: str
- os: str
- tag: str (unique)
- nom_reseau: str (unique)
- ip_address: str (unique)
- user_id: int (FK)
- office_license_id: int (FK)
```

### Écrans
```python
- id: int (PK)
- tag: str (unique)
- taille: str
- marque: str
- modele: str
- ordinateur_id: int (FK)
- slot: int (1-5)
```

### OfficeLicenses
```python
- id: int (PK)
- version: str
- type_license: str
- numero_bc: str
- achat: date
- fin_garantie: date
```

## 🔄 Migrations

### Créer une migration
```bash
alembic revision --autogenerate -m "description"
```

### Appliquer les migrations
```bash
alembic upgrade head
```

### Revenir en arrière
```bash
alembic downgrade -1
```

### Voir l'historique
```bash
alembic history
```

## 🐛 Dépannage

### Erreur de connexion DB
```bash
# Vérifier les variables d'env
cat .env

# Tester la connexion PostgreSQL
psql -U [DB_USER] -h [DB_HOST] -d [DB_NAME]
```

### Erreur de migration
```bash
# Réinitialiser la migration
alembic stamp head
alembic revision --autogenerate -m "new migration"
```

### Tests qui échouent
```bash
# Vérifier que pytest est installé
pip install pytest pytest-cov

# Nettoyer le cache
rm -rf .pytest_cache __pycache__

# Relancer les tests
pytest -v
```

## 📖 Développement

### Ajouter une nouvelle route
1. Créer le fichier dans `backend/app/api/routes/`
2. Définir le Pydantic schema dans `backend/app/schemas/`
3. Importer et inclure le router dans `main.py`
4. Ajouter les tests dans `tests/unit/api/`

### Code standards
- Utiliser logging pour les opérations
- Lever des `HTTPException` pour les erreurs
- Valider avec Pydantic
- Tester unitairement chaque fonction

### Linting & Formatage
```bash
# Linter avec ruff
ruff check backend/

# Formatter avec ruff
ruff format backend/

# Type checking avec mypy
mypy backend/
```

## 📞 Support

Pour les questions ou bugs :
1. Vérifier la [documentation FastAPI](https://fastapi.tiangolo.com/)
2. Consulter les tests existants
3. Créer une issue sur GitHub

## 📄 License

ISC

## 🤝 Contribuer

Les contributions sont bienvenues ! Veuillez :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/new-feature`)
3. Commiter les changements (`git commit -m 'Add feature'`)
4. Pousser vers la branche (`git push origin feature/new-feature`)
5. Ouvrir une Pull Request

---

**Version** : 0.1.0  
**Dernier update** : Janvier 2026
