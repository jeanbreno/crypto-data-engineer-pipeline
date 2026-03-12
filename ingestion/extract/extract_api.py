import requests
import json
import os
from datetime import datetime
from minio import Minio
from utils.minio_client import get_minio_client

# -----------------------------
# Configuração
# -----------------------------

BUCKET_NAME = "raw"

API_URL = "https://api.coingecko.com/api/v3/coins/markets"

PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50
}

# -----------------------------
# Conectar no MinIO
# -----------------------------

client = get_minio_client()

# garantir que bucket existe
if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)


# -----------------------------
# Buscar dados da API
# -----------------------------

response = requests.get(API_URL, params=PARAMS)
data = response.json()

timestamp = datetime.utcnow()

payload = {
    "timestamp": timestamp.isoformat(),
    "data": data
}


# -----------------------------
# salvar local temporário
# -----------------------------

file_name = f"crypto_prices_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"

with open(file_name, "w") as f:
    json.dump(payload, f)


# -----------------------------
# caminho no data lake
# -----------------------------

object_path = (
    f"crypto/"
    f"year={timestamp.year}/"
    f"month={timestamp.month:02d}/"
    f"day={timestamp.day:02d}/"
    f"{file_name}"
)

# -----------------------------
# upload para MinIO
# -----------------------------

client.fput_object(
    BUCKET_NAME,
    object_path,
    file_name
)

print("Upload concluído:", object_path)