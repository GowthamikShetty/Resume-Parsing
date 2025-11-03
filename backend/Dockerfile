FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements and install them
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install spaCy model (via pip for Render)
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz

# Copy your FastAPI app code
COPY app ./app

# Expose the port Render will use
EXPOSE 10000

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
