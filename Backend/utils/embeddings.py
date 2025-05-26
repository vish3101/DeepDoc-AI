from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL

embedding_model=SentenceTransformer(EMBEDDING_MODEL)

def get_text_embedding(text):
    result=embedding_model.encode(text)
    return result