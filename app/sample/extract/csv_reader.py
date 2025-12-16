import pandas as pd

class csv_reader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self, offset, batch_size):
        return pd.read_csv(
            self.file_path,
            skiprows=range(1, offset + 1),
            nrows=batch_size
        )
