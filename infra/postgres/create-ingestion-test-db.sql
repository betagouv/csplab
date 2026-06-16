-- Creates the ingestion_test database, dropping it first if it exists.
-- The ingestion user (created by create-ingestion-db.sql) is reused as owner.

DROP DATABASE IF EXISTS ingestion_test;
CREATE DATABASE ingestion_test OWNER ingestion;
