import requests
import pandas as pd
from datetime import datetime

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame(data)

date = datetime.now().strftime("%Y%m%d_%H%M%S")

path = f"/opt/airflow/scripts/crypto_{date}.csv"

df.to_csv(path, index=False)

print("Arquivo salvo:", path)