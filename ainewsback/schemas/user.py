from pydantic import BaseModel

from ainewsback.models.user import ApUser


class LoginAuthResponse(BaseModel):
    user: ApUser = ApUser()
    token: str = "token"


class LoginAuthRequest(BaseModel):
    phone: str
    password: str


class LoginCodeRequest(BaseModel):
    phone: str
    code: str
