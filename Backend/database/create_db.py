from database import Base, engine
from database.models import Chunk, Document, Users


def create_all_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_all_tables()


    