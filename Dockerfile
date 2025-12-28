# 1. 'python' version
FROM python:3.9-slim

# 2. working repo
WORKDIR /app

# 3. Dependecies installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy of the code
COPY . .

# 5. Running the app
CMD ["python", "-m", "app.sample.main"]