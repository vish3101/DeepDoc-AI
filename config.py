import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path,override=True)
   
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
GITHUB_CLIENT_ID=os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET=os.getenv("GITHUB_CLIENT_SECRET")
CHROMADB_PATH="database/chroma_db"
EMBEDDING_MODEL="sentence-transformers/all-miniLM-L6-v2"