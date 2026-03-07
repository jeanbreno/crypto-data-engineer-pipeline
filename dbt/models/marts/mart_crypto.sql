SELECT
    name,
    AVG(current_price) AS avg_price,
    SUM(total_volume) AS total_volume
FROM {{ ref('stg_crypto') }}
GROUP BY name