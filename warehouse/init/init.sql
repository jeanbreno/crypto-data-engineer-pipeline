CREATE DATABASE crypto_warehouse;

\c crypto_warehouse


-- criar schemas
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;


-- garantir usuario airflow
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles WHERE rolname = 'airflow'
   ) THEN
      CREATE ROLE airflow LOGIN PASSWORD 'airflow';
   END IF;
END
$$;


-- permissoes airflow
GRANT ALL PRIVILEGES ON DATABASE crypto_warehouse TO airflow;

GRANT USAGE ON SCHEMA bronze TO airflow;
GRANT USAGE ON SCHEMA silver TO airflow;
GRANT USAGE ON SCHEMA gold TO airflow;

GRANT CREATE ON SCHEMA bronze TO airflow;
GRANT CREATE ON SCHEMA silver TO airflow;
GRANT CREATE ON SCHEMA gold TO airflow;


-- permissoes postgres
GRANT ALL PRIVILEGES ON SCHEMA bronze TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA silver TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA gold TO postgres;


-- search path
ALTER ROLE airflow SET search_path TO bronze, silver, gold, public;


-- tabela bronze
CREATE TABLE IF NOT EXISTS bronze.crypto_prices (

    id TEXT,
    symbol TEXT,
    name TEXT,
    image TEXT,

    current_price NUMERIC,
    market_cap NUMERIC,
    market_cap_rank INTEGER,
    fully_diluted_valuation NUMERIC,

    total_volume NUMERIC,

    high_24h NUMERIC,
    low_24h NUMERIC,

    price_change_24h NUMERIC,
    price_change_percentage_24h NUMERIC,

    market_cap_change_24h NUMERIC,
    market_cap_change_percentage_24h NUMERIC,

    circulating_supply NUMERIC,
    total_supply NUMERIC,
    max_supply NUMERIC,

    ath NUMERIC,
    ath_change_percentage NUMERIC,
    ath_date TIMESTAMP,

    atl NUMERIC,
    atl_change_percentage NUMERIC,
    atl_date TIMESTAMP,

    roi JSONB,

    last_updated TIMESTAMP,

    source_file TEXT,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);