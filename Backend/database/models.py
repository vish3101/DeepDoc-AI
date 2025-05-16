from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(String, unique=True)
    username = Column(String)

    documents = relationship("Document", back_populates="user")

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document")

class Chunk(Base):
    __tablename__ = 'chunks'
    id = Column(Integer, primary_key=True, index=True)
    chunk_text = Column(Text)
    document_id = Column(Integer, ForeignKey("documents.id"))

    document = relationship("Document", back_populates="chunks")

class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(Integer, ForeignKey("chunks.id"))
    faiss_index = Column(Integer)

    chunk = relationship("Chunk")
