-- Creates the ingestion_test database.
-- Idempotent: safe to run multiple times.
-- The ingestion user (created by create-ingestion-db.sql) is reused as owner.

SELECT 'CREATE DATABASE ingestion_test OWNER ingestion'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ingestion_test')\gexec
