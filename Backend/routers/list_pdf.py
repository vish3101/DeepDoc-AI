import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

# Use consistent upload directory path
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "PDFs"))

@router.get("/list-pdfs")
async def list_pdfs():
    try:
        if not os.path.exists(UPLOAD_DIR):
            return JSONResponse(
                status_code=200,
                content={"pdf_files": []}
            )

        files = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(".pdf")]
        return JSONResponse(
            status_code=200,
            content={"pdf_files": files}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")
