import PyPDF2
import docx2txt
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

def extract_text_from_file(path):
    """
    Extracts text from PDF, DOCX, or TXT files.
    Uses PyPDF2 → pdfplumber → OCR (Tesseract) for image PDFs.
    """
    # ---------- PDF HANDLING ----------
    if path.lower().endswith(".pdf"):
        text = ""

        # 1️⃣ Try PyPDF2
        try:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"[PyPDF2 Error] {e}")

        # 2️⃣ Try pdfplumber if PyPDF2 fails or returns empty
        if not text.strip():
            try:
                with pdfplumber.open(path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() or ""
            except Exception as e:
                print(f"[pdfplumber Error] {e}")

        # 3️⃣ Fallback: OCR (Tesseract) if still no text
        if not text.strip():
            print("[INFO] No extractable text found — using OCR fallback...")
            try:
                images = convert_from_path(path)
                for img in images:
                    text += pytesseract.image_to_string(img)
            except Exception as e:
                print(f"[OCR Error] {e}")

        return text.strip() or "NO_TEXT_EXTRACTED"

    # ---------- DOCX HANDLING ----------
    elif path.lower().endswith(".docx"):
        try:
            return docx2txt.process(path) or ""
        except Exception as e:
            print(f"[DOCX Error] {e}")
            return ""

    # ---------- TXT HANDLING ----------
    else:
        try:
            with open(path, "r", errors="ignore") as f:
                return f.read()
        except Exception as e:
            print(f"[TXT Error] {e}")
            return ""
