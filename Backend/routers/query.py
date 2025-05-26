import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from Backend.utils.chroma_db_client import chroma_client
from Backend.utils.search_pdf import search_pdf
from config import GOOGLE_API_KEY


class AskRequest(BaseModel):
    pdf_name: str
    question: str
    
    
router=APIRouter()
genai.configure(api_key=GOOGLE_API_KEY)

@router.post("/ask/")
async def ask_question(request:AskRequest):
    pdf_name = request.pdf_name
    question = request.question
    all_metadata = chroma_client.collection.get(include=["metadatas"])
    pdf_names_in_db = {meta["pdf_name"] for meta in all_metadata["metadatas"]}
    print("metadata of pdfs",pdf_names_in_db)
    if pdf_name not in pdf_names_in_db:
        raise HTTPException(status_code=404, detail=f"PDF '{pdf_name}' not found in database.")

    relavant_text=search_pdf(question,pdf_name)

    prompt = f"""
        You are an intelligent AI assistant designed to answer questions based on a specific document context.
        You will receive a set of relevant text excerpts from a pdf document and a user's question.
        Your task is to provide an accurate and concise answer using only the given context.

        Input:
        context
        {relavant_text}
        User's question
        {question}

        Instructions:
        1. Base your answers strictly on the provided context. Do not generate information that is not in the context.
        2. If the context does not contain enough information respond with: "No relevant information was found for this question"
        3. Keep the answer concise and to the point.
        """


    model=genai.GenerativeModel("gemini-2.0-flash")
    response=model.generate_content(prompt)
    return {"answer":response.text}