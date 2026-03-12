import psycopg2
import sys
from utils.postgres_client import get_connection

conn = get_connection()

cur = conn.cursor()

checks = [
    {
        "name": "bronze table not empty",
        "query": "SELECT COUNT(*) FROM bronze.crypto_prices"
    },
    {
        "name": "no null timestamps",
        "query": "SELECT COUNT(*) FROM bronze.crypto_prices WHERE timestamp IS NULL"
    },
    {
        "name": "no null symbol",
        "query": "SELECT COUNT(*) FROM bronze.crypto_prices WHERE symbol IS NULL"
    }
]

for check in checks:

    cur.execute(check["query"])
    result = cur.fetchone()[0]

    print(f"Check: {check['name']} -> {result}")

    if check["name"] == "bronze table not empty" and result == 0:
        print("❌ Bronze table is empty")
        sys.exit(1)

    if check["name"] != "bronze table not empty" and result > 0:
        print("❌ Null values detected")
        sys.exit(1)

print("✅ Data Quality Passed")

cur.close()
conn.close()