from app.extract.csv_reader import CsvReader
print("hello world")

reader = CsvReader("app/data/healthcare_dataset.csv")
data = reader.readData()