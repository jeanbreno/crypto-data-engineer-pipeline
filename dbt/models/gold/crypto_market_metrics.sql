{{ config(materialized='table') }}

SELECT
    symbol,

    AVG(price_usd) as avg_price,
    MAX(price_usd) as max_price,
    MIN(price_usd) as min_price,

    SUM(volume_24h) as total_volume

FROM {{ ref('crypto_prices_clean') }}

GROUP BY symbol