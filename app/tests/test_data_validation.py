from app.sample.db_manager import mongo_manager
from app.sample.transform.data_cleaning import data_transform
import pandas as pd
from datetime import date

def test_data_validation_mongo():
    
    data = pd.read_csv('app/sample/data/healthcare_dataset.csv')
    cleaner = data_transform()
    data = cleaner.transform_data(data)

    len_doc_expected = data['key'].nunique()

    if mongo_manager.ping_server():
        users = mongo_manager.get_collection()
        docs = list(users.find())
        assert len(docs) == len_doc_expected

        first_doc = users.find_one()

        # --- checking the doc structure ---

        assert set(first_doc.keys()) == {"patient_id", "personal_infos", "admissions", '_id'}
        assert set(first_doc['personal_infos'].keys()) == {"first_name", "last_name", "age","gender", "blood_type"}
        assert set(first_doc['admissions'][0].keys()) == {"date_of_admission", "admission_type", "room_number", "medical_condition", "medication", "test_results", "doctor", "hospital", "billing_infos"}
        assert set(first_doc['admissions'][0]['billing_infos'].keys()) == {"insurance_provider", "billing_amount", "discharge_date"}

        # --- checking the data type ---
    
    expected_schema_first_level = {"patient_id" : str, "personal_infos" : dict, "admissions" : list}

    for key, expected_type in expected_schema_first_level.items():
        assert key in first_doc
        assert isinstance(first_doc[key], expected_type)

    expected_schema_second_level = {"first_name" : str, "last_name" : str, "age" : int,"gender" : str, "blood_type" : str}

    for key, expected_type in expected_schema_second_level.items():
        assert key in first_doc['personal_infos']
        assert isinstance(first_doc['personal_infos'][key], expected_type)

    expected_schema_third_level = {"date_of_admission" : date, "admission_type" : str , "room_number" : int , "medical_condition" : str , "medication" : str , "test_results" : str , "doctor" : str , "hospital" : str , "billing_infos" : dict }

    for key, expected_type in expected_schema_third_level.items():
        assert key in first_doc['admissions'][0]
        assert isinstance(first_doc['admissions'][0][key], expected_type)

    expected_schema_forth_level = {"insurance_provider" : str, "billing_amount" : float, "discharge_date" : date}

    for key, expected_type in expected_schema_forth_level.items():
        assert key in first_doc['admissions'][0]['billing_infos']
        assert isinstance(first_doc['admissions'][0]['billing_infos'][key], expected_type)