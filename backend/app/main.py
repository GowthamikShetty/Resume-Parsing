from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import tempfile
from app.nlp import parse_resume
from app.utils import extract_text_from_file

app = FastAPI(title="Resume Parser API")

# ✅ FIXED CORS
# Add your frontend URL (Vercel) + localhost (for testing)
origins = [
    "https://resume-parsing-git-main-gowthami-k-shettys-projects.vercel.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # ✅ make sure this matches your actual domain
    allow_credentials=True,
    allow_methods=["*"],           # ✅ allow all request types (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],           # ✅ allow all headers, including Content-Type
)

@app.options("/upload")
async def preflight():
    # ✅ Handle preflight CORS OPTIONS requests
    return JSONResponse(status_code=200, content={"message": "CORS preflight success"})

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in (
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    ):
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF or DOCX.")

    try:
        suffix = ".pdf" if file.content_type == "application/pdf" else ".docx"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        text = extract_text_from_file(tmp_path)
        parsed = parse_resume(text)
        return JSONResponse(content={"success": True, "parsed": parsed})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
