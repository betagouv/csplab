-- Creates the ingestion database and user.
-- Idempotent: safe to run multiple times.
-- Also executed automatically by the PostgreSQL Docker image on first boot
-- (files in /docker-entrypoint-initdb.d/ are run in alphabetical order).

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'ingestion') THEN
    CREATE USER ingestion WITH PASSWORD 'pass';
  END IF;
END
$$;

SELECT 'CREATE DATABASE ingestion OWNER ingestion'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ingestion')\gexec
