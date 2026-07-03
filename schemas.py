from pydantic import BaseModel
from datetime import datetime


##class to create task object 
class Task(BaseModel):
    title:str
    description:str
    done:bool
    createdAt: datetime
    updatedAt:datetime


##class to create task object containing data that can be sent to client
class TaskResponse(BaseModel):
    title:str
    description:str
    done:bool
    createdAt:datetime
    updatedAt:datetime

##Model to update email
class UpdateEmail(BaseModel):
    email:str

##Model to update password
class UpdatePassword(BaseModel):
    password:str


##class to create user object
class User(BaseModel):
    email:str
    password:str

##class to create user object containing data that can be sent to client
class UserResponse(BaseModel):
    email:str