from auth import hashPassword,verifyPassword, generateJwtToken
from fastapi import status, HTTPException, APIRouter
from schemas import User, UserResponse, Task, TaskResponse, UpdateEmail, UpdatePassword
from database import Base, sessionMaker
from models import TaskDB, UserDB
from datetime import datetime 
from typing import List

router = APIRouter()


                                                     ########TASK#########

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

##Get all tasks
@router.get("/Tasks",response_model = List[TaskResponse])
def getAllTasks(page: int = 1, limit: int = 10):
    db = sessionMaker()
    offset = (page - 1)* limit
    task = db.query(TaskDB).offset(offset).limit(limit).all()
    db.close()
    return task


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

##Post route to create and sign up user to the database
@router.post("/signup",response_model = UserResponse, status_code = status.HTTP_201_CREATED)
def signUp(user:User):
    db = sessionMaker()
    newUser = UserDB(email = user.email, hashedPassword = hashPassword(user.password))
    db.add(newUser)
    db.commit()
    db.close()
    return user

##Route to log in user
@router.post("/Login")
def login(user:User):
    db = sessionMaker()
    foundUser = db.query(UserDB).filter(UserDB.email == user.email).first()
    if foundUser != None:
        if verifyPassword(user.password, foundUser.hashedPassword) == False:
            raise HTTPException(status_code = 401, detail= "Unauthorized user.")
        else:
            return generateJwtToken({"sub":user.email})
    else:
        raise HTTPException(status_code = 404, detail = "User Not Found.")
    
##Get route to get user via id
@router.get("/Users/{id}", response_model = UserResponse)
def getUser(id:int):
    db = sessionMaker()
    foundUser = db.query(UserDB).filter(UserDB.id == id).first()
    if foundUser == None:
        raise HTTPException(status_code = 404, detail = "User Not Found.")
    else:
        return foundUser

##Get route to get user via email
@router.get("/Users/email/{email}", response_model = UserResponse)
def getUser(email:str):
    db = sessionMaker()
    foundUser = db.query(UserDB).filter(UserDB.email == email).first()
    if foundUser == None:
        raise HTTPException(status_code = 404, detail = "User Not Found.")
    else:
        return foundUser
    

##Delete route to delete user from database
@router.delete("/Users/{id}")
def deleteUser(id:int):
    db = sessionMaker()
    foundUser = db.query(UserDB).filter(UserDB.id == id).first()
    if foundUser == None:
        raise HTTPException(status_code = 404, detail = "User Not Found.")
    else:
        email = foundUser.email
        db.delete(foundUser)
        db.commit()
        db.close()
        return "User with email "+email+" has been permenently deleted."
    

##Put route to change user's email in the database
@router.put("/Users/{id}/email")
def changeEmail(id:int,emailData:UpdateEmail):
    db = sessionMaker()
    foundUser = db.query(UserDB).filter(UserDB.id == id).first()
    if foundUser == None:
        raise HTTPException(status_code = 404, detail = "User Not Found.")
    else:
        foundUser.email = emailData.email
        db.commit()
        db.close()
        return "User's email has been changed."
    
##Put route to update user's password in the database
@router.put("/Users/{id}/password")
def changePassword(id:int, passwordData:UpdatePassword):
    db = sessionMaker()
    foundUser = db.query(UserDB).filter(UserDB.id == id).first()
    if foundUser == None:
        raise HTTPException(status_code = 404, detail = "User Not Found.")
    else:
        foundUser.hashedPassword = hashPassword(passwordData.password)
        db.commit()
        db.close()
        return "User's password has been changed."
    
    

