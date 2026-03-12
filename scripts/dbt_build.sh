#!/bin/bash
set -e

cd /opt/airflow/dbt

echo "Instalando dependências do dbt (se houver packages)..."
dbt deps

echo "Executando dbt build (models + tests + seeds + snapshots)..."
dbt build --target dev

echo "Gerando documentação..."
dbt docs generate

echo "dbt build finalizado com sucesso."