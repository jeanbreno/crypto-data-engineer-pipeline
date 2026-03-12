CREATE DATABASE crypto_warehouse;

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

GRANT ALL PRIVILEGES ON DATABASE crypto_warehouse TO airflow;
grant all privileges on schema bronze to airflow;
grant all privileges on schema silver to airflow;
grant all privileges on schema gold to airflow;

CREATE TABLE IF NOT EXISTS crypto_warehouse.bronze.crypto_prices (
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