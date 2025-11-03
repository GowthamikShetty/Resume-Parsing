# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app
# Install system-level dependencies
RUN apt-get update && apt-get install -y gcc g++

# Upgrade build tools
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy English model
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz

# Copy the rest of your code
COPY . .
# 5. Copy FastAPI app
COPY backend/app ./app

# Expose Render's expected port
EXPOSE 10000

# Run FastAPI app directly (no start.sh)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
