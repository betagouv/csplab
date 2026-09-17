#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import time

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s [s3-setup] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("s3-setup")

ENDPOINT_URL = os.getenv("WEB_S3_ENDPOINT_URL", "http://localhost:9000")
ACCESS_KEY = os.getenv("WEB_S3_ACCESS_KEY_ID", "rustfsadmin")
SECRET_KEY = os.getenv("WEB_S3_SECRET_ACCESS_KEY", "rustfsadmin")
REGION = os.getenv("WEB_S3_REGION_NAME", "us-east-1")


def client():
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION,
    )


def wait_for_s3(s3, max_retries: int = 30, delay: int = 2) -> bool:
    logger.info("🔍 Vérification de la disponibilité de RustFS sur %s...", ENDPOINT_URL)
    for attempt in range(max_retries):
        try:
            s3.list_buckets()
            logger.info("✅ RustFS est accessible")
            return True
        except EndpointConnectionError:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                logger.error(
                    "❌ RustFS n'est pas accessible après %d tentatives", max_retries
                )
                return False
    return False


def create_bucket_if_missing(s3, bucket_name: str) -> None:
    try:
        s3.head_bucket(Bucket=bucket_name)
        logger.info("✅ Le bucket '%s' existe déjà", bucket_name)
        return
    except ClientError:
        pass
    logger.info("🔧 Création du bucket '%s'...", bucket_name)
    s3.create_bucket(Bucket=bucket_name)
    logger.info("✅ Bucket '%s' créé avec succès", bucket_name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Crée le bucket S3 s'il n'existe pas")
    parser.add_argument(
        "--bucket-name",
        default=os.getenv(
            "WEB_S3_CANDIDATURE_DOCUMENTS_BUCKET_NAME",
            "csplab-candidature-documents-dev",
        ),
    )
    args = parser.parse_args()

    s3 = client()
    if not wait_for_s3(s3):
        sys.exit(1)
    create_bucket_if_missing(s3, args.bucket_name)


if __name__ == "__main__":
    main()
