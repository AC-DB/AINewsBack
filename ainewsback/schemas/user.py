from pydantic import BaseModel


class User(BaseModel):
    id: int = 0,
    salt: str = "",
    name: str = "",
    password: str = "",
    phone: str = 0,
    image: str = None,
    sex: bool = True,
    certification: str = None,
    identityAuthentication: str = None,
    status: bool = True,
    flag: int = 0,
    createdTime: str = ""


class LoginAuthResponse(BaseModel):
    user: User = User()
    token: str = "token"


class LoginAuthRequest(BaseModel):
    phone: str
    password: str

class LoginCodeRequest(BaseModel):
    phone: str
    code: str