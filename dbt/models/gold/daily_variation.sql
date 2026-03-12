CREATE MATERIALIZED VIEW gold.daily_price_variation AS

SELECT
    symbol,
    AVG(price_change_percentage_24h) AS avg_daily_variation
FROM {{ ref('crypto_prices_clean') }}
GROUP BY symbol;