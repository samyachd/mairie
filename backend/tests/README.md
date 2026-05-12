# Tests Structure

Organisation des tests du projet mairie.

## Structure

```
tests/
├── conftest.py           # Configuration pytest et fixtures partagées
├── unit/                 # Tests unitaires
│   ├── api/              # Tests des routes API
│   │   ├── test_users.py
│   │   ├── test_ordinateurs.py
│   │   ├── test_licenses.py
│   │   └── test_ecrans.py
│   └── db/               # Tests des modèles de données
│       └── test_models.py
└── integration/          # Tests d'intégration
    └── test_api_flow.py
```

## Utilisation

### Exécuter tous les tests
```bash
pytest
```

### Exécuter les tests unitaires uniquement
```bash
pytest tests/unit/
```

### Exécuter les tests d'intégration uniquement
```bash
pytest tests/integration/
```

### Exécuter avec couverture de code
```bash
pytest --cov=backend tests/
```

### Mode verbose
```bash
pytest -v
```

## Fixtures disponibles

### `db_engine`
Crée un moteur de base de données SQLite en mémoire (scope: session)

### `db_session`
Crée une nouvelle session de base de données pour chaque test avec rollback automatique

### `client`
Client de test FastAPI avec dépendances overridées pour utiliser la base de données de test

## Bonnes pratiques

1. **Tests unitaires** : Testent des fonctions/classes isolées
2. **Tests d'intégration** : Testent le comportement du système complet
3. **Nommage** : Les fichiers de test doivent commencer par `test_`
4. **Assertions** : Utiliser des assertions claires et explicites
5. **Fixtures** : Utiliser les fixtures pour setup et teardown

## Exemple de test complet

```python
def test_create_and_retrieve_user(client, db_session):
    """Test création et récupération d'un utilisateur."""
    # Arrange
    user_data = {"name": "John", "email": "john@example.com"}
    
    # Act
    response = client.post("/users/", json=user_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["name"] == "John"
```
