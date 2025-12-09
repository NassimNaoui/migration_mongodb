import pandas as pd

class data_transform:
    def __init__(self):
        pass

    def transform_data(self, df: pd.DataFrame):
        df_transformed = df.copy()
        
        try:
            # --- 1. drop duplicates rows ---
            df_transformed = df_transformed.drop_duplicates()

            # --- 2. return name in upper case ---
            df_transformed["name"] =  df_transformed["name"].str.upper()

            # --- 3. Round with 2 decimales the billing amout ---
            df_transformed["billing_amount"] = round(df_transformed["billing_amount"],2)

            # --- 4. return the first name col and last name col ---
            df_transformed[['first_name', 'last_name']] = df_transformed['name'].str.split(' ', expand=True)

            # --- 5. convert str to date format ---
            col_to_format = ["date_of_admission", "discharge_date"]
            for col in col_to_format:
                df_transformed[col] = pd.to_datetime(df_transformed[col])

            # --- 6. change column name ---
            col_name = df_transformed.columns.to_list()
            new_col_name = list(map(lambda x: x.replace(" ", "_"), col_name))
            new_col_name = list(map(lambda x: x.lower(), col_name))
            df_transformed.columns = new_col_name

            # --- 7. adding unique key for each patient 
            df_transformed['key'] = df_transformed["name"] + "_" +  df_transformed["age"] + "_" + df_transformed["gender"] + "_" + df_transformed["blood_type"]


            return df_transformed
        except Exception as e:
            print(f'error during the transformation process : {e}')

    def count_admission_id(self, df : pd.DataFrame):

        df_filtered = df.copy()

        # --- Count the number of admissions for each patient ---

        try:
            df_filtered.sort_values(['name','Age','gender','blood_type'], ascending=True)
            df_filtered['admission_id'] = df_filtered.groupby(['name','Age','gender','blood_type']).cumcount() + 1
            return df_filtered
        except Exception as e:
            print(f'error during the transformation process : {e}')

    
    def convert_df_into_doc(self, df: pd.DataFrame) -> list:
        if df.empty:
            return []

        # --- 1. Personal infos (Static cols) ---
        PERSONAL_COLS = [
            'first_name', 'last_name', 'gender', 'age', 'blood_type'
        ]
        
        # --- 2. Admissions infos ---
        ADMISSION_COLS = [
            'admission_id', 'date_of_admission', 'admission_type', 
            'room_number', 'medical_condition', 'medication', 
            'test_results', 'doctor', 'hospital'
        ]
        
        # --- 3. Billing infos ---
        BILLING_COLS = [
            'insurance_provider', 'billing_amount', 'discharge_date'
        ]

        # --- 4. Creates admission object with billing infos ---
        def Creates_admission_obj(admission_row):
            admission_dict = admission_row[ADMISSION_COLS].to_dict()
            

            billing_dict = admission_row[BILLING_COLS].to_dict()
            
            admission_dict['billing_infos'] = billing_dict
            return admission_dict

        # --- 5. Creates the final document ---
        def build_patient_doc(group):
            # group = all admissions for each patient
            
            
            patient_info = group.iloc[0]
            patient_id = patient_info['key']
            
            # Creates admission list with the function created above
            admissions_list = [
                Creates_admission_obj(row) 
                for _, row in group.iterrows()
            ]
            
            # Creates the structured object
            document = {
                patient_id: {
                    "personal_infos": {col: patient_info[col] for col in PERSONAL_COLS},
                    "admissions": admissions_list
                }
            }
            
            return [document]


        # --- 6. group by key ---
        grouped_data = df.groupby('key').apply(build_patient_doc)
        
        # --- 7 Flatten the object --- 
        final_docs = [doc for sublist in grouped_data.tolist() for doc in sublist]
        
        return final_docs








