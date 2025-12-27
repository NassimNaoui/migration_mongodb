from app.sample.extract.csv_reader import csvReader
from app.sample.transform.data_cleaning import dataTransform
from app.sample.load.mongo_loader import dataLoader
from app.sample.db_manager import mongo_manager

import pandas as pd

def main():
    if mongo_manager.ping_server():
        users = mongo_manager.get_collection()
        users.create_index("patient_id", unique=True)
        print("✅ connexion to MongoDB succeed : The server is online")
    else:
        print("❌ connexion to mongoDB failed : The server is offline")
        return  # On arrête si la connexion échoue

    reader = csvReader(file_path='app/sample/data/healthcare_dataset.csv')
    cleaner = dataTransform()
    loader = dataLoader(users)

    batch_size = 10000
    total_rows = len(pd.read_csv('app/sample/data/healthcare_dataset.csv'))

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
            print(f"✅ Loaded Batch #{batch_number}")
        except Exception as e:
            print(f"❌ Error Batch #{batch_number} : {e}")


if __name__ == "__main__":
    main()
