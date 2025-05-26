from fastapi import APIRouter, File, Form, UploadFile

from Backend.utils.chroma_db_client import chroma_client
from Backend.utils.embeddings import get_text_embedding
from Backend.utils.pdf_processing import extract_text_from_pdf

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_path = f"Backend/PDFs/{file.filename}"

    with open(pdf_path, "wb") as f:
        file_content = file.file.read()
        f.write(file_content)

    text_chunks = extract_text_from_pdf(pdf_path)

    for i, chunk in enumerate(text_chunks):
        embedding = get_text_embedding(chunk)
        
        doc_id = f"{file.filename}_{i}"
        chroma_client.add_document(doc_id, embedding, {
            "text": chunk,
            "pdf_name": file.filename
        })

    return {"message": f"Your PDF {file.filename} successfully processed and stored in ChromaDB"}