-- Creates the ingestion database, owned by the connected (super)user.
-- Idempotent: safe to run multiple times.
-- Also executed automatically by the PostgreSQL Docker image on first boot
-- (files in /docker-entrypoint-initdb.d/ are run in alphabetical order).

SELECT 'CREATE DATABASE ingestion'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ingestion')\gexec
