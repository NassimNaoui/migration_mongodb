from app.sample.extract.csv_reader import csvReader
import pandas as pd

def test_csv_reader():
    reader = csvReader('app/sample/data/healthcare_dataset.csv')
    data = reader.read_data(100,100)

    assert len(data) > 1
    assert data.shape == (100, 15)