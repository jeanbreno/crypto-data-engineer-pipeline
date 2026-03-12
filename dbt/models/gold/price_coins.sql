CREATE MATERIALIZED VIEW gold.top_crypto_market_cap AS

SELECT
    symbol,
    name,
    market_cap,
    market_cap_rank
FROM {{ ref('crypto_prices_clean') }}
ORDER BY market_cap DESC
LIMIT 10;