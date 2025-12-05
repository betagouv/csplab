# Commandes d'orchestration d'ingestion

Ce répertoire contient les commandes Django pour orchestrer les use cases d'ingestion de documents.

## Commandes disponibles

### 1. Charger les documents

```bash
./bin/manage load_documents --type CORPS
```

Utilise `LoadDocumentsUsecase` pour récupérer et persister les documents depuis l'API externe.

### 2. Nettoyer les documents

```bash
./bin/manage clean_documents --type CORPS
```

Utilise `CleanDocumentsUsecase` pour nettoyer les documents bruts et les transformer en entités métier.

### 3. Vectoriser les documents

```bash
./bin/manage vectorize_documents --type CORPS
```

Utilise `VectorizeDocumentsUsecase` pour générer les embeddings et les stocker dans la base vectorielle.

Options disponibles :

- `--limit N` : Limite le nombre de documents à vectoriser

## Pipeline complet

Pour exécuter le pipeline complet d'ingestion :

```bash
# 1. Charger les documents depuis l'API
./bin/manage load_documents --type CORPS

# 2. Nettoyer et transformer en entités
./bin/manage clean_documents --type CORPS

# 3. Générer les embeddings
./bin/manage vectorize_documents --type CORPS
```
