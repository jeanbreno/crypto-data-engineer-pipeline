CREATE MATERIALIZED VIEW gold.avg_price_crypto AS

SELECT
    symbol,
    AVG(current_price) AS avg_price

FROM {{ ref('crypto_prices_clean') }}

GROUP BY symbol;