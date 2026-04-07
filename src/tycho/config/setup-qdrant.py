#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import time

import requests
from requests.exceptions import ConnectionError, RequestException, Timeout

# Constantes HTTP
HTTP_OK = 200
HTTP_CREATED = 201
REQUEST_TIMEOUT = 5

# Configuration simple du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s [qdrant-setup] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("qdrant-setup")
vector_size = int(os.getenv("TYCHO_EMBEDDING_DIMENSION", "1024"))


def wait_for_qdrant(url: str, max_retries: int = 30, delay: int = 2) -> bool:
    logger.info(f"🔍 Vérification de la disponibilité de Qdrant sur {url}...")

    for attempt in range(max_retries):
        try:
            response = requests.get(f"{url}/", timeout=REQUEST_TIMEOUT)
            if response.status_code == HTTP_OK:
                logger.info("✅ Qdrant est accessible")
                return True
        except (ConnectionError, Timeout):
            if attempt < max_retries - 1:
                retry_msg = (
                    f"⏳ Tentative {attempt + 1}/{max_retries} - "
                    f"Qdrant n'est pas encore prêt, attente de {delay}s..."
                )
                logger.debug(retry_msg)
                time.sleep(delay)
            else:
                error_msg = (
                    f"❌ Qdrant n'est pas accessible après {max_retries} tentatives"
                )
                logger.error(error_msg)
                return False
        except RequestException as e:
            logger.error(f"❌ Erreur lors de la connexion à Qdrant: {e}")
            return False

    return False


def collection_exists(base_url: str, collection_name: str) -> bool:
    try:
        response = requests.get(
            f"{base_url}/collections/{collection_name}", timeout=REQUEST_TIMEOUT
        )
        return response.status_code == HTTP_OK
    except RequestException:
        return False


def create_collection(base_url: str, collection_name: str) -> bool:
    logger.info(f"🔧 Création de la collection '{collection_name}'...")

    # Configuration de la collection
    collection_config = {"vectors": {"size": vector_size, "distance": "Cosine"}}

    try:
        # Créer la collection
        response = requests.put(
            f"{base_url}/collections/{collection_name}",
            json=collection_config,
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code not in [HTTP_OK, HTTP_CREATED]:
            error_msg = (
                f"❌ Erreur lors de la création de la collection: "
                f"{response.status_code} - {response.text}"
            )
            logger.error(error_msg)
            return False

        logger.info(f"✅ Collection '{collection_name}' créée avec succès")
        return True

    except RequestException as e:
        logger.error(f"❌ Erreur lors de la création de la collection: {e}")
        return False


def create_field_index(
    base_url: str, collection_name: str, field_name: str, field_type: str = "keyword"
) -> bool:
    logger.info(f"🔧 Création de l'index pour le champ '{field_name}'...")

    index_config = {"field_name": field_name, "field_schema": field_type}

    try:
        response = requests.put(
            f"{base_url}/collections/{collection_name}/index",
            json=index_config,
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code not in [HTTP_OK, HTTP_CREATED]:
            warning_msg = (
                f"⚠️  Avertissement: Impossible de créer l'index pour "
                f"'{field_name}': {response.status_code} - {response.text}"
            )
            logger.info(warning_msg)
            return False

        logger.info(f"✅ Index créé pour le champ '{field_name}'")
        return True

    except RequestException as e:
        error_msg = f"❌ Erreur lors de la création de l'index pour '{field_name}': {e}"
        logger.error(error_msg)
        return False


def setup_collection_indexes(base_url: str, collection_name: str) -> None:
    logger.info("🔧 Configuration des index pour les filtres...")

    # Index simples (keyword)
    simple_indexes = ["document_type", "category", "verse"]

    # Index pour les champs de localisation imbriqués
    nested_indexes = [
        "localisation.region",
        "localisation.country",
        "localisation.department",
    ]

    all_indexes = simple_indexes + nested_indexes

    success_count = 0
    for field_name in all_indexes:
        if create_field_index(base_url, collection_name, field_name):
            success_count += 1

    logger.info(f"✅ {success_count}/{len(all_indexes)} index créés avec succès")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Configure Qdrant collection automatically"
    )
    parser.add_argument(
        "--collection-name",
        default="fonction_publique",
        help="Name of the collection to create (default: fonction_publique)",
    )
    args = parser.parse_args()

    # Configuration
    QDRANT_URL = "http://localhost:6333"
    COLLECTION_NAME = args.collection_name

    logger.info("🚀 Démarrage de la configuration automatique de Qdrant")
    logger.info(f"📍 URL Qdrant: {QDRANT_URL}")
    logger.info(f"📦 Collection: {COLLECTION_NAME}")
    logger.info(f"📏 Dimension des vecteurs: {vector_size}")

    # Étape 1: Attendre que Qdrant soit disponible
    if not wait_for_qdrant(QDRANT_URL):
        error_msg = (
            "❌ Impossible de se connecter à Qdrant. "
            "Assurez-vous que le service est démarré."
        )
        logger.error(error_msg)
        sys.exit(1)

    # Étape 2: Vérifier si la collection existe
    if collection_exists(QDRANT_URL, COLLECTION_NAME):
        logger.info(f"✅ La collection '{COLLECTION_NAME}' existe déjà")
        logger.info("🎉 Configuration Qdrant terminée - aucune action nécessaire")
        sys.exit(0)

    logger.info(f"📝 La collection '{COLLECTION_NAME}' n'existe pas")

    # Étape 3: Créer la collection
    if not create_collection(QDRANT_URL, COLLECTION_NAME):
        logger.info("❌ Échec de la création de la collection")
        sys.exit(1)

    # Étape 4: Configurer les index
    setup_collection_indexes(QDRANT_URL, COLLECTION_NAME)

    logger.info("🎉 Configuration Qdrant terminée avec succès!")
    logger.info(
        f"🌐 Vous pouvez maintenant accéder à l'interface web: {QDRANT_URL}/dashboard"
    )


if __name__ == "__main__":
    main()
