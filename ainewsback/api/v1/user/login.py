from fastapi import APIRouter, Query

from ainewsback.schemas.base import resp_200, resp_500
from ainewsback.schemas.user import LoginAuthRequest, LoginAuthResponse, \
    LoginCodeRequest
from ainewsback.utils.jwt import JWTUtils

router = APIRouter(prefix="/login", tags=["login"])


# 用户密码登录
@router.post("/login_auth")
async def login_auth(item: LoginAuthRequest):
    item_dice = item.model_dump()
    back = LoginAuthResponse()
    return resp_200(back)


# 发送登录验证码
@router.get("/send_code")
async def send_code(phone: str = Query(
    ..., min_length=11, max_length=15, pattern=r"^\+?\d{11,15}$",
    title="手机号", description="11-15位，允许+开头")
):
    if phone is not None and phone != "":
        return resp_200(None, f"验证码发送成功")

    return resp_500(None, f"验证码发送失败")


# 用户验证码登录
@router.post("/code_login")
async def login_code(item: LoginCodeRequest):
    item_dice = item.model_dump()
    phone = item_dice["phone"]
    code = item_dice["code"]

    token = JWTUtils.create_token(phone)

    back = LoginAuthResponse(token=token)

    return resp_200(back)
