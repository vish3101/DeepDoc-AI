from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL='sqlite:///./deepdoc.db'

engine=create_engine(DATABASE_URL,connect_args={'check_same_thread':False})

SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in the database:", tables)