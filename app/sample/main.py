from extract.csv_reader import csv_reader
from transform.data_cleaning import data_transform
from load.mongo_loader import data_loader
from db_manager import mongo_manager

import pandas as pd


if __name__ == "__main__":
    
    if mongo_manager.ping_server():
        users = mongo_manager.get_collection()
        users.create_index("patient_id", unique=True)
        print("✅ connexion to MongoDB succeed : The server is online")
    else:
        print("❌ connexion to mongoDB failed : The server is offline")
    

    reader = csv_reader(file_path='data/healthcare_dataset.csv')
    cleaner = data_transform()
    loader = data_loader(users)

    batch_size = 10000
    total_rows = len(pd.read_csv('data/healthcare_dataset.csv'))


    for batch_number, offset in enumerate(range(0, total_rows, batch_size), start=1):
        
        data = reader.read_data(offset, batch_size)

        if data.empty:
            print(f"⚠️ Batch #{batch_number} empty → stop")
            break

        print(f"🔄 Innitialisation : Batch #{batch_number} | offset={offset} | rows={len(data)}")

        data_transformed = cleaner.transform_data(data)
        document_to_load = cleaner.convert_df_into_doc(data_transformed)

        try:
            loader.load_many_docs(document_to_load)
            print(f"✅ Loaded  Batch #{batch_number}")
        except Exception as e:
            print(f"❌ Error Batch #{batch_number} : {e} ")