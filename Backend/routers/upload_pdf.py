import os

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "PDFs")
UPLOAD_DIR = os.path.abspath(UPLOAD_DIR)

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
    
@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    if os.path.exists(file_path):
        return JSONResponse(
            status_code=409,
            content={
                "filename": file.filename,
                "message": "A file with this name already exists. Please rename and try again.",
            },
        )
    
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        print(f"Saving to: {file_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save failed: {str(e)}")
    
    return JSONResponse(
        status_code=201,
        content={
            "filename": file.filename,
            "message": "File uploaded successfully.",
        },
    )


