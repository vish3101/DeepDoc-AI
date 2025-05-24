from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL='sqlite:///./deepdoc.db'

engine=create_engine(DATABASE_URL,connect_args={'check_same_thread':False})

SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()