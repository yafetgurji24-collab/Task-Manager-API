from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine("sqlite:///./tasks.db")
sessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
