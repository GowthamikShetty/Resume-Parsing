import PyPDF2
import docx2txt
import pdfplumber

def extract_text_from_file(path):
    text = ""

    if path.lower().endswith(".pdf"):
        # Try PyPDF2 first
        try:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
        except Exception as e:
            print("PyPDF2 error:", e)

        # If PyPDF2 fails or returns nothing, try pdfplumber
        if not text.strip():
            try:
                with pdfplumber.open(path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text
            except Exception as e:
                print("pdfplumber error:", e)

        # Still empty → likely scanned PDF
        if not text.strip():
            text = "No text extracted (PDF may be scanned or image-based)."

    elif path.lower().endswith(".docx"):
        try:
            text = docx2txt.process(path) or ""
        except Exception as e:
            print("DOCX extraction failed:", e)

    else:
        try:
            with open(path, "r", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            print("Plain text read failed:", e)

    return text
