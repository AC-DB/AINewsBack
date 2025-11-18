from ainewsback.config import settings
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ainewsback.utils.jwt import JWTUtils
from fastapi.security import OAuth2PasswordBearer

# 模拟验证码存储
fake_verification_codes = {"test_user": "123456"}

# OAuth2 依赖
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 登录请求模型
class LoginRequest(BaseModel):
    username: str
    code: str

# 登录响应模型
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/info")
async def info():
    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "app_description": settings.APP_DESCRIPTION,
        "app_license": settings.APP_LICENSE,
        "admin_name": settings.ADMIN_CONTACT.get("name"),
        "admin_email": settings.ADMIN_CONTACT.get("email"),
        "app_env": settings.APP_ENV,
        "debug": settings.DEBUG,
        "log_level": settings.LOG_LEVEL,
        "host": settings.HOST,
        "port": settings.PORT,
    }



# 示例接口：校验 JWT
@router.get("/protected")
async def protected(token: str = Depends(oauth2_scheme)):
    try:
        payload = JWTUtils.verify_token(token)
        return {"message": "访问成功", "data": payload}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))