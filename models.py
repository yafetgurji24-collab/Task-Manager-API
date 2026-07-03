from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base, engine, sessionMaker

##class to create Task database
class TaskDB(Base):
    __tablename__ = "Tasks"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    description = Column(String)
    done = Column(Boolean)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)


##Initialize database
Base.metadata.create_all(bind=engine)

##Class to create User Database
class UserDB(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key = True)
    email = Column(String)
    hashedPassword = Column(String)

##Initialize database
Base.metadata.create_all(bind=engine)