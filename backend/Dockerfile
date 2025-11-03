FROM python:3.11-slim

WORKDIR /app
COPY ./app /app/app
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# (if you didn't use the wheel in requirements) ensure model installed:
RUN python -m spacy download en_core_web_sm

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
