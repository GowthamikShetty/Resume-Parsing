# app/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import spacy
import PyPDF2

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Resume Parser API is running"}

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file.file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return {"filename": file.filename, "content": text[:500]}  # short preview
