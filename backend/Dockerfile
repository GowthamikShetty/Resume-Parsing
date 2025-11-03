# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy English model
RUN python -m spacy download en_core_web_sm

# Copy the rest of your code
COPY . .

# Expose Render's expected port
EXPOSE 10000

# Run FastAPI app directly (no start.sh)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
