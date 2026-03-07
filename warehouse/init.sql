CREATE TABLE crypto_prices (
    id TEXT,
    symbol TEXT,
    name TEXT,
    current_price NUMERIC,
    market_cap NUMERIC,
    total_volume NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);