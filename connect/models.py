from pydantic import BaseModel


class RegisterData(BaseModel):
    Username: str
    Password: str
    Fullname: str


class LoginData(BaseModel):
    Username: str
    Password: str
