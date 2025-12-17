from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:admin@localhost:5432/my_db"
engine = create_engine(db_url)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
