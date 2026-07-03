from auth import hashPassword,verifyPassword, generateJwtToken
from fastapi import status, HTTPException, APIRouter
from schemas import User, UserResponse, Task, TaskResponse
from database import Base, sessionMaker
from models import TaskDB, UserDB
from datetime import datetime 


router = APIRouter()

##Post route to create task and store into database
@router.post("/Tasks", status_code = status.HTTP_201_CREATED,response_model = TaskResponse)
def createTask(task:Task):
    db = sessionMaker()
    newTask = TaskDB(title = task.title, description = task.description, done = task.done , createdAt = task.createdAt, updatedAt = task.updatedAt)
    db.add(newTask)
    db.commit()
    db.close()
    return task

##Get route to get task via id 
@router.get("/Tasks/{id}", response_model = TaskResponse )
def getTask(id:int):
    db = sessionMaker()
    foundTask = db.query(TaskDB).filter(TaskDB.id == id).first()
    if foundTask == None:
        raise HTTPException(status_code = 404, detail = "Task Not Found.")
    else:
        return foundTask 

##Delete route to delete task 
@router.delete("/Tasks/{id}")
def deleteTask(id:int):
    db = sessionMaker()
    foundTask = db.query(TaskDB).filter(TaskDB.id == id).first()
    if foundTask == None:
        raise HTTPException(status_code = 404, detail = "Task Not Found.")
    else:
        db.delete(foundTask)
        db.commit()
        db.close()
        return "Task titled "+foundTask.title + " is permenently deleted."

##Put route to update task
@router.put("/Tasks/{id}")
def updateTask(id:int, task:Task):
    db = sessionMaker()
    foundTask = db.query(TaskDB).filter(TaskDB.id == id).first()
    if foundTask == None:
        raise HTTPException(status_code = 404, detail = "Task Not Found.")
    else:
        title = foundTask.title
        foundTask.title = task.title
        foundTask.description = task.description
        foundTask.done = task.done
        foundTask.updatedAt = datetime.now()
        foundTask.createdAt = task.createdAt
        db.commit()
        db.close()
        return "Task titled "+title  + " has been updated."


                                            ########USER#########