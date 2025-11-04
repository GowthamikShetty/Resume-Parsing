from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import tempfile
from app.nlp import parse_resume
from app.utils import extract_text_from_file

app = FastAPI(title="Resume Parser API")

# Allow frontend origin (adjust in deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://resume-parsing-git-main-gowthami-k-shettys-projects.vercel.app"],
  # change to your frontend URL (e.g., https://your-site.vercel.app) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"):
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF or DOCX.")
    try:
        # save to temp file
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
