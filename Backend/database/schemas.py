from typing import List, Optional

from pydantic import BaseModel


class ChunkSchema(BaseModel):
    id: int
    content: str
    document_id: int
    faiss_index_id: int

    class Config:
        orm_mode = True


class DocumentSchema(BaseModel):
    id: int
    filename: str
    user_id: int
    chunks: Optional[List[ChunkSchema]] = []

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    github_id: str
    username: str
    documents: Optional[List[DocumentSchema]] = []

    class Config:
        orm_mode = True
