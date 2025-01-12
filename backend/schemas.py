from pydantic import BaseModel ,EmailStr
from typing import Optional 


############# user ##############

class UserCreate(BaseModel):
    first_name : str
    last_name : str 
    email : EmailStr
    password : str

class UserRespond(BaseModel):
    first_name : str
    last_name : str 
    email : EmailStr
    id : Optional[int] = None
    
    class config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str




######### feedback ##################


class UserFeedback(BaseModel):
    title: str
    email: EmailStr  # Ensure the email field is defined and validated
    content: str

    class Config:
        orm_mode = True




########token #############

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str]= None
    

##### voice #########

class VoiceCommandResponse(BaseModel):
    message: str