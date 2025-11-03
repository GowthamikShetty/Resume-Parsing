import PyPDF2
import docx2txt

def extract_text_from_file(path):
    if path.lower().endswith(".pdf"):
        text = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                try:
                    text += page.extract_text() or ""
                except Exception:
                    continue
        return text
    elif path.lower().endswith(".docx"):
        return docx2txt.process(path) or ""
    else:
        # try plain read
        with open(path, "r", errors="ignore") as f:
            return f.read()
