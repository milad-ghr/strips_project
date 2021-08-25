CREATE DATABASE strips;
CREATE USER strips_role WITH PASSWORD '123456789';
ALTER ROLE strips_role SET client_encoding TO 'utf8';
ALTER ROLE strips_role SET timezone TO 'UTC';
ALTER ROLE strips_role SET default_transaction_isolation TO 'read committed';
ALTER USER "strips_role" CREATEDB;
