import pandas as pd

class CsvReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def readData(self):
        data = pd.read_csv(self.file_path)
        return data

