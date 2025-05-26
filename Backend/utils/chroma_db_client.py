import chromadb
from config import CHROMADB_PATH


class ChromaDBClient:
    def __init__(self):
        self.client=chromadb.PersistentClient(path=CHROMADB_PATH)
        self.collection=self.client.get_or_create_collection(name="pdf_embedding")

    def add_document(self,doc_id,embeddings,metadata):
        self.collection.add(ids=[doc_id],embeddings=[embeddings],metadatas=[metadata])

    def search(self,query_embedding,top_k=3,where=None):
        results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k,where=where)
        return results
chroma_client=ChromaDBClient()