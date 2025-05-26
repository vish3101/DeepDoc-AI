from Backend.utils.chroma_db_client import chroma_client
from Backend.utils.embeddings import get_text_embedding


def search_pdf(query, pdf_name):
    query_embedding = get_text_embedding(query)

    query_embedding = query_embedding.tolist()  # if not already
    results = chroma_client.search(
        query_embedding,
        top_k=3,
        where={"pdf_name": pdf_name} 
    )
    return results