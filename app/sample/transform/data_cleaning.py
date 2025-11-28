import pandas as pd

class data_transform:
    def __init__(self, file_path):
        self.file_path = file_path

    def transform_data(self, df):
        # --- 1. drop duplicates rows ---
        df = df.drop_duplicates()

        # --- 2. return name in upper case ---
        df["Name"] =  df["Name"].str.upper()

        # --- 3. Round with 2 decimales the billing amout ---
        df["Billing Amount"] = round(df["Billing Amount"],2)

        # --- 4. return the first name col and last name col ---
        df[['first_name', 'last_name']] = df['Name'].str.split(' ', expand=True)

        # --- 5. convert str to date format ---
        col_to_format = ["Date of Admission", "Discharge Date"]
        for col in col_to_format:
            df[col] = pd.to_datetime(df[col])




