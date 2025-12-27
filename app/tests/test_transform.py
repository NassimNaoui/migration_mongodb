from app.sample.extract.csv_reader import csvReader
from app.sample.transform.data_cleaning import dataTransform
import pandas as pd
import numpy as np
from datetime import date

def test_transform_data():

    data = pd.read_csv('app/sample/data/healthcare_dataset.csv')
    cleaner = dataTransform()
    data_cleaned = cleaner.transform_data(data)

    expected_cols = ["name", "age", "gender", "blood_type", "medical_condition", "date_of_admission",
                     "doctor", "hospital", "insurance_provider", "billing_amount", "room_number",
                     "admission_type","discharge_date","medication","test_results","first_name",
                     "last_name", "key"]

    # --- cheking the columns --- 
    assert list(data_cleaned.columns) == expected_cols

    # --- checking uppercase in column name --- 
    assert data_cleaned["name"].str.isupper().all()

    # --- checking if there is no title in name ---
    assert (data_cleaned["name"].str.find("MRS.") < 0).all()
    assert (data_cleaned["name"].str.find("MR.") < 0).all()
    assert (data_cleaned["name"].str.find("MS.") < 0).all()
    assert (data_cleaned["name"].str.find("DR.") < 0).all()

    # --- checking na values in first and last name columns ---
    assert data_cleaned['first_name'].isna().all() == False
    assert data_cleaned['last_name'].isna().all() == False

    # --- checking data type of billing amount columns ---
    assert pd.api.types.is_float_dtype(data_cleaned["billing_amount"])

    # --- checking duplicated rows ---
    assert data_cleaned.duplicated().all() == False 

def test_convert_df_into_doc():

    data = pd.read_csv('app/sample/data/healthcare_dataset.csv', nrows=200)
    cleaner = dataTransform()
    data_cleaned = cleaner.transform_data(data)
    final_doc = cleaner.convert_df_into_doc(data_cleaned)
    final_doc = final_doc[0]

    # --- checking the doc structure ---

    assert set(final_doc.keys()) == {"patient_id", "personal_infos", "admissions"}
    assert set(final_doc['personal_infos'].keys()) == {"first_name", "last_name", "age","gender", "blood_type"}
    assert set(final_doc['admissions'][0].keys()) == {"date_of_admission", "admission_type", "room_number", "medical_condition", "medication", "test_results", "doctor", "hospital", "billing_infos"}
    assert set(final_doc['admissions'][0]['billing_infos'].keys()) == {"insurance_provider", "billing_amount", "discharge_date"}

    # --- checking the data type ---
    
    expected_schema_first_level = {"patient_id" : str, "personal_infos" : dict, "admissions" : list}

    for key, expected_type in expected_schema_first_level.items():
        assert key in final_doc
        assert isinstance(final_doc[key], expected_type)

    expected_schema_second_level = {"first_name" : str, "last_name" : str, "age" : int,"gender" : str, "blood_type" : str}

    for key, expected_type in expected_schema_second_level.items():
        assert key in final_doc['personal_infos']
        assert isinstance(final_doc['personal_infos'][key], expected_type)

    expected_schema_third_level = {"date_of_admission" : date, "admission_type" : str , "room_number" : int , "medical_condition" : str , "medication" : str , "test_results" : str , "doctor" : str , "hospital" : str , "billing_infos" : dict }

    for key, expected_type in expected_schema_third_level.items():
        assert key in final_doc['admissions'][0]
        assert isinstance(final_doc['admissions'][0][key], expected_type)

    expected_schema_forth_level = {"insurance_provider" : str, "billing_amount" : float, "discharge_date" : date}

    for key, expected_type in expected_schema_forth_level.items():
        assert key in final_doc['admissions'][0]['billing_infos']
        assert isinstance(final_doc['admissions'][0]['billing_infos'][key], expected_type)


