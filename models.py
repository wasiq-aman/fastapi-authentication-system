from pydantic import BaseModel, EmailStr  # type: ignore

class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    username: str
    email: EmailStr

class LoginRequest(BaseModel):
    username: str
    password: str
