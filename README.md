

# 🚀 Crypto Data Engineering Pipeline

Pipeline de **engenharia de dados end-to-end** que coleta dados do mercado de criptomoedas, armazena em um Data Lake, transforma para analytics e disponibiliza dashboards.

O objetivo do projeto é demonstrar uma **arquitetura moderna de dados**, simulando um ambiente real de produção.

---

# 🧠 Arquitetura

```text
API Crypto
   ↓
Airflow ingestion DAG (Python)
   ↓
Data lake MinIO (RAW)
   ↓
Airflow ingestion DAG (Python)
   ↓
Data Warehouse Postgres (Bronze)
   ↓
dbt
   ↓
Data Warehouse Postgres (Silver - dados tratados)
   ↓
dbt
   ↓
Data Warehouse Postgres (Gold - métricas analíticas)
   ↓
Metabase (Dashboard)
```

Ferramentas utilizadas:

* Orquestração → Apache Airflow
* Data Lake → MinIO
* Transformação → dbt
* Data Warehouse → PostgreSQL
* Visualização → Metabase
* Containerização → Docker

---

# 📊 Fonte de Dados

Os dados são coletados da API pública da CoinGecko.

Endpoint utilizado:

```
https://api.coingecko.com/api/v3/coins/markets
```

Dados coletados incluem:

* nome da criptomoeda
* símbolo
* preço atual
* market cap
* volume negociado
* ranking

---

# 📂 Estrutura do Projeto

```text
crypto-data-engineer-pipeline/
│
├── docker-compose.yml
│
├── airflow/
│   ├── dags/
│   │   └── crypto_pipeline.py
│   │
│   └── requirements.txt
│
├── ingestion/
│   └── extract_api.py
│
├── dbt/
│   ├── dbt_project.yml
│   └── models/
│       ├── staging/
│       │   └── stg_crypto.sql
│       │
│       └── marts/
│           └── mart_crypto.sql
│
├── warehouse/
│   └── init.sql
│
└── README.md
```

---

# 🔄 Pipeline de Dados

Fluxo do pipeline:

### 1️⃣ Ingestão

Um script Python coleta dados da API e salva no **Data Lake**.

### 2️⃣ Orquestração

Uma DAG do Apache Airflow executa a pipeline automaticamente.

### 3️⃣ Armazenamento

Os dados brutos são armazenados no Data Lake usando MinIO.

### 4️⃣ Transformação

Os dados são modelados utilizando dbt.

Modelos criados:

* staging layer
* analytics layer

### 5️⃣ Data Warehouse

Os dados transformados são armazenados no PostgreSQL.

### 6️⃣ Analytics

Dashboards são criados no Metabase para análise dos dados.

---

# 📈 Exemplos de Análises

O dashboard permite visualizar:

* Top 10 criptomoedas por market cap
* Volume de negociação
* Ranking de liquidez
* Média de preços
* Evolução de mercado

---

# ⚙️ Como executar o projeto

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/crypto-data-engineer-pipeline.git
cd crypto-data-engineer-pipeline
```

---

### 2️⃣ Iniciar os serviços

```bash
docker compose up -d
```

Isso iniciará:

* Airflow
* PostgreSQL
* MinIO
* Metabase

---

# 🌐 Interfaces

Airflow

```
http://localhost:8080
```

login

```
admin
admin
```

Metabase

```
http://localhost:3000
```

---

# 🧩 Arquitetura de Dados

Este projeto implementa um pipeline moderno de engenharia de dados baseado em:

* ingestão via API
* armazenamento em Data Lake
* modelagem analítica
* orquestração de workflows
* visualização de dados

Essa arquitetura é semelhante às utilizadas por empresas orientadas a dados como:

* Netflix
* Uber
* Airbnb

---

# 🎯 Objetivo do Projeto

Demonstrar habilidades em:

* construção de pipelines de dados
* ingestão de APIs
* orquestração com Airflow
* modelagem analítica com dbt
* construção de Data Warehouses
* visualização de dados

---

# 📌 Possíveis melhorias

* ingestão incremental
* arquitetura Medallion (Bronze / Silver / Gold)
* testes de qualidade de dados
* monitoramento de pipeline
* deploy em cloud

---