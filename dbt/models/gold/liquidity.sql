CREATE MATERIALIZED VIEW gold.crypto_liquidity AS

SELECT
    symbol,
    total_volume,
    market_cap,
    total_volume / market_cap AS liquidity_ratio
FROM {{ ref('crypto_prices_clean') }}
WHERE market_cap > 0;