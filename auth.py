from passlib.context import CryptContext
from jose import jwt
from datetime import timedelta, datetime
from schemas import User, UserResponse, Task, TaskResponse


pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

##JWT
SECRET_KEY = "Zare_innovations"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 30

##Function to hash password
def hashPassword(password:str):
    return pwdContext.hash(password)

##Function to verify if hashed password and non-hashed password match
def verifyPassword(password,hashedPassword):
    return pwdContext.verify(password, hashedPassword)

##Function to generate jwt token
def generateJwtToken(data:dict):
    copyData = data.copy()
    time = datetime.now()
    time+= timedelta(minutes = EXPIRATION_MINUTES)
    copyData.update({"exp":EXPIRATION_MINUTES})
    token = jwt.encode(copyData, SECRET_KEY, algorithm = ALGORITHM)
    return token

