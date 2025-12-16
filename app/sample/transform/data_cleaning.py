import pandas as pd

class data_transform:
    def __init__(self):
        pass

    def transform_data(self, df: pd.DataFrame):
        df_transformed = df.copy()
        
        try:
            # --- drop duplicates rows ---
            df_transformed = df_transformed.drop_duplicates()

            # --- change column name ---
            col_name = df_transformed.columns.to_list()
            new_col_name = list(map(lambda x: x.replace(" ", "_"), col_name))
            new_col_name = list(map(lambda x: x.lower(), new_col_name))
            df_transformed.columns = new_col_name

            # --- return name in upper case ---
            df_transformed["name"] =  df_transformed["name"].str.upper()

            # --- Delete title in Name
            df_transformed['name'] = df_transformed['name'].str.upper().str.replace(r'\b(MRS|MR|MS|DR)\.?\s*', '', regex=True).str.strip()

            # --- return the first name col and last name col ---
            df_transformed[['first_name', 'last_name']] = df_transformed['name'].str.strip().str.split(r'\s+', n=1, expand=True)

            # --- Round with 2 decimales the billing amout ---
            df_transformed["billing_amount"] = df_transformed["billing_amount"].astype(float)
            df_transformed["billing_amount"] = round(df_transformed["billing_amount"],2)

            # --- convert str to date format ---
            col_to_format = ["date_of_admission", "discharge_date"]
            for col in col_to_format:
                df_transformed[col] = pd.to_datetime(df_transformed[col])

            # --- adding unique key for each patient 
            df_transformed['key'] = df_transformed["name"] + "_" +  df_transformed["age"].astype(str) + "_" + df_transformed["gender"] + "_" + df_transformed["blood_type"]


            return df_transformed
        except Exception as e:
            print(f'error during the transformation process : {e}')

    
    def convert_df_into_doc(self, df: pd.DataFrame) -> list:
        if df.empty:
            return []

        
        # --- Admissions infos ---
        ADMISSION_COLS = [
            'date_of_admission', 'admission_type', 
            'room_number', 'medical_condition', 'medication', 
            'test_results', 'doctor', 'hospital'
        ]
        
        # --- Billing infos ---
        BILLING_COLS = [
            'insurance_provider', 'billing_amount', 'discharge_date'
        ]

        # ---  Creates admission object with billing infos ---
        def Creates_admission_obj(admission_row):
            admission_dict = admission_row[ADMISSION_COLS].to_dict()
            

            billing_dict = admission_row[BILLING_COLS].to_dict()
            
            admission_dict['billing_infos'] = billing_dict
            return admission_dict

        # ---  Creates the final document ---
        def build_patient_doc(group):
            # group = all admissions for each patient
            
            
            patient_info = group.iloc[0]
            patient_id = patient_info['key']

            #personal infos object with numpy conversion

            personal_infos = {
                "first_name": patient_info['first_name'],
                "last_name": patient_info['last_name'],
                "gender": patient_info['gender'],
                "age": int(patient_info['age']), 
                "blood_type": patient_info['blood_type']
            }
            
            # Creates admission list with the function created above
            admissions_list = [
                Creates_admission_obj(row) 
                for _, row in group.iterrows()
            ]
            
            # Creates the structured object
            document = {
                "patient_id" : patient_id, 
                "personal_infos": personal_infos,
                "admissions": admissions_list
            }
            
            return [document]


        # ---  group by key ---
        grouped_data = df.groupby('key').apply(build_patient_doc)
        
        # --- Flatten the object --- 
        final_docs = [doc for sublist in grouped_data.tolist() for doc in sublist]
        
        return final_docs








