# 🚀🩺 Medical Data Migration (ETL)

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
| :... | :... |
| View logs | docker-compose logs -f |
| Stop services | docker-compose stop |
| Remove containers and network | docker-compose down |
| Rebuild after code changes | docker-compose up -d --build |
