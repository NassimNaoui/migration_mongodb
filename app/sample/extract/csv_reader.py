import pandas as pd

class csv_reader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self, start,end, batch_size):

        data = pd.read_csv(self.file_path, skiprows=range(start,end),nrows=batch_size)
        return data

