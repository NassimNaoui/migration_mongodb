# 🚀🩺 Medical Data Migration (ETL)

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/mongodb-6.0-green)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/docker-enabled-blue)](https://www.docker.com/)

Python ETL pipeline designed to extract, clean, and load healthcare data into **MongoDB**. 
Features Docker containerization for seamless deployment and modular Python structure for easy maintenance.

## 🏗 Architecture
- **Source:** CSV (Kaggle Healthcare Dataset)
- **Processing:** Python (Cleaning & Transformation)
- **Destination:** MongoDB

---

## 🛠 Quick Start with Docker

### Prerequisites
* [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
* Healthcare Dataset: [Download from Kaggle](https://www.kaggle.com/datasets/prasad22/healthcare-dataset)

### 1. Clone the repository
```bash
git clone git@github.com:NassimNaoui/migration_mongodb.git
cd migration_mongodb
```

### 2. Data Setup
Place the downloaded CSV file into the following directory:

> app/sample/data/healthcare_dataset.csv

### 3. Launch 
```bash
docker-compose up -d
```

### 🔧 Useful Commands
| Description | Command |
| :--- | :--- |
| View logs | `docker-compose logs -f` |
| Stop services | `docker-compose stop` |
| Remove containers and network | `docker-compose down` |
| Rebuild after code changes | `docker-compose up -d --build` |

## ✨ Key Features & ETL Logic
The pipeline follows a modular Extract, Transform, Load process to ensure data quality:

- ✅ Data Extraction: Efficiently reads the healthcare CSV dataset.

- ✅ Data Cleaning:

    - Deduplication: Identification and removal of duplicate records.
    - Name Normalization: Names are converted to uppercase, and titles (Mr, Mrs, Dr, etc.) are stripped.
    - Financial Formatting: The Billing Amount column is rounded.
    - Type Conversion: Date columns are parsed into proper datetime objects.
    - Unique Mapping: Generation of a unique key for each patient record.

- ✅ Loading: Transformation into JSON-like documents and batch insertion into MongoDB.

*Performance: The ETL process is designed to handle data in batches to optimize memory usage and speed up the migration.*

<img src="assets/etl-process.gif">