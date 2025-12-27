from app.sample.extract.csv_reader import csv_reader
import pandas as pd

def test_csv_reader():
    reader = csv_reader('app/sample/data/healthcare_dataset.csv')
    data = reader.read_data(100,100)

    assert len(data) > 1
    assert data.shape == (100, 15)