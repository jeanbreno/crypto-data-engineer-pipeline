import json
import pandas as pd
from utils.minio_client import get_minio_client
from utils.postgres_client import get_connection
from minio.commonconfig import CopySource

BUCKET = "raw"
OBJECT_NAME = "crypto_prices_"
client = get_minio_client()


def list_raw_files(client, BUCKET, OBJECT_NAME):

    objects = client.list_objects(BUCKET, recursive=True)

    files = []

    for obj in objects:

        if obj.object_name.startswith("processed/"):
            continue

        if obj.object_name.startswith(OBJECT_NAME):
            files.append(obj.object_name)

    return files


def read_json_from_minio(client, BUCKET, file_name):

    response = client.get_object(BUCKET, file_name)

    data = json.loads(response.read().decode("utf-8"))

    return data


def load_to_postgres(df, file_name):

    import io
    import json

    conn = get_connection()
    cur = conn.cursor()

    df["source_file"] = file_name

    if "roi" in df.columns:
        df["roi"] = df["roi"].apply(lambda x: json.dumps(x) if x else None)

    buffer = io.StringIO()

    df.to_csv(
        buffer,
        index=False,
        header=False,
        sep=",",
        na_rep="\\N"
    )

    buffer.seek(0)

    copy_sql = """
        COPY bronze.crypto_prices (
            id,
            symbol,
            name,
            image,
            current_price,
            market_cap,
            market_cap_rank,
            fully_diluted_valuation,
            total_volume,
            high_24h,
            low_24h,
            price_change_24h,
            price_change_percentage_24h,
            market_cap_change_24h,
            market_cap_change_percentage_24h,
            circulating_supply,
            total_supply,
            max_supply,
            ath,
            ath_change_percentage,
            ath_date,
            atl,
            atl_change_percentage,
            atl_date,
            roi,
            last_updated,
            source_file
        )
        FROM STDIN WITH (
            FORMAT CSV,
            DELIMITER ',',
            NULL '\\N'
        )
    """

    cur.copy_expert(copy_sql, buffer)

    conn.commit()

    cur.close()
    conn.close()

def move_to_processed(client, bucket, file_name):

    destination = f"processed/{file_name}"

    client.copy_object(
        bucket,
        destination,
        CopySource(bucket, file_name)
    )

    client.remove_object(bucket, file_name)

    print(f"{file_name} movido para raw/processed/")

def main():

    files = list_raw_files(client, BUCKET, OBJECT_NAME)

    print(f"{len(files)} arquivos encontrados no RAW")

    for file_name in files:

        print(f"Processando {file_name}")

        data = read_json_from_minio(client, BUCKET, file_name)

        df = pd.DataFrame(data)

        load_to_postgres(df, file_name)

        print(f"{file_name} carregado para Postgres. Movendo para processed...")

        move_to_processed(client, BUCKET, file_name)


if __name__ == "__main__":
    main()