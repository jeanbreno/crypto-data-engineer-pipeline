import requests
import json
import os
from datetime import datetime
from minio import Minio

# -----------------------------
# Configuração
# -----------------------------

MINIO_ENDPOINT = "minio:9000"

MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")

BUCKET_NAME = "raw"

API_URL = "https://api.coingecko.com/api/v3/simple/price"

PARAMS = {
    "ids": "bitcoin,ethereum,solana",
    "vs_currencies": "usd",
}

# -----------------------------
# Conectar no MinIO
# -----------------------------

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

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