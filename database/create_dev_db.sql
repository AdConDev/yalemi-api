-- Database: yalemi-dev

-- DROP DATABASE IF EXISTS "yalemi-dev";

CREATE DATABASE "yalemi-dev"
    WITH
    OWNER = adcon
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Mexico.1252'
    LC_CTYPE = 'Spanish_Mexico.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE "yalemi-dev"
    IS 'Yalemi Project development database.';