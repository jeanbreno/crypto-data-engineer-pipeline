import requests
import json
from datetime import datetime
from minio import Minio

# -----------------------------
# Configuração
# -----------------------------

MINIO_ENDPOINT = "minio:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "password"
BUCKET_NAME = "crypto-data"

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

# criar bucket se não existir
if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)

# -----------------------------
# Buscar dados da API
# -----------------------------

response = requests.get(API_URL, params=PARAMS)
data = response.json()

payload = {
    "timestamp": datetime.utcnow().isoformat(),
    "data": data
}

# -----------------------------
# salvar local temporário
# -----------------------------

timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

file_name = f"crypto_prices_{timestamp}.json"

with open(file_name, "w") as f:
    json.dump(payload, f)

# -----------------------------
# upload para MinIO
# -----------------------------

client.fput_object(
    BUCKET_NAME,
    f"raw/{file_name}",
    file_name
)

print("Upload concluído:", file_name)