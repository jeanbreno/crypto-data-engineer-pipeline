{{ config(materialized='table') }}

SELECT
    symbol,
    price_usd,
    volume_24h,
    market_cap,
    timestamp::timestamp as price_timestamp

FROM {{ ref('stg_crypto_prices') }}

WHERE price_usd IS NOT NULL