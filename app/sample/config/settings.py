import os
from dotenv import load_dotenv
from pathlib import Path

# Charge le .env qui est à la racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Variables MongoDB
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

# Chemin vers le CSV source
CSV_PATH = os.getenv("CSV_PATH")

# TOKEN
KAGGLE_API_TOKEN = os.getenv("KAGGLE_API_TOKEN")

# Mode de l’application (dev / prod)
APP_ENV = os.getenv("APP_ENV", "development") 
