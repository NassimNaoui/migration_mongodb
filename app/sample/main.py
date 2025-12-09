from extract.csv_reader import csv_reader
from db_manager import mongo_manager

def main():
    if mongo_manager.ping_server():
        print("✅ connexion to MongoDB succeed : The server is online")
    else:
        print("❌ connexion to mongoDB failed : The server is offline")

if __name__ == "__main__":
    main()