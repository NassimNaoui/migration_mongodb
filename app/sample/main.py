from extract.csv_reader import csv_reader
from transform.data_cleaning import data_transform
from db_manager import mongo_manager

def main():
    if mongo_manager.ping_server():
        print("✅ connexion to MongoDB succeed : The server is online")
    else:
        print("❌ connexion to mongoDB failed : The server is offline")
    

    reader = csv_reader(file_path='data/healthcare_dataset.csv')
    cleaner = data_transform()


    data = reader.read_data(1,100, 100)
    data_transformed = cleaner.transform_data(data)
    data_transformed = cleaner.count_admission_id(data_transformed)

    document_to_load = cleaner.convert_df_into_doc(data_transformed)

    users = mongo_manager.get_collection()

    users.insert_many(document_to_load)


if __name__ == "__main__":
    main()