from fastapi import APIRouter, Depends, Query

from ainewsback.api.v1.deps import get_user_service
from ainewsback.schemas.base import resp, resp_200, resp_500
from ainewsback.schemas.user import LoginAuthRequest, LoginAuthResponse, \
    LoginCodeRequest
from ainewsback.services.user_service import UserService

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/login_auth")
async def login_auth(
        item: LoginAuthRequest,
        user_service: UserService = Depends(get_user_service)
):
    """用户密码登录"""
    user, token, error_msg = user_service.authenticate_by_password(
        phone=item.phone,
        password=item.password
    )

    if error_msg:
        return resp(code=500, message=error_msg)

    return resp_200(LoginAuthResponse(user=user, token=token))


@router.get("/send_code")
async def send_code(
        phone: str = Query(
            ..., min_length=11, max_length=15, pattern=r"^\+?\d{11,15}$",
            title="手机号", description="11-15位,允许+开头"
        ),
        user_service: UserService = Depends(get_user_service),
):
    """发送登录验证码"""
    success = await user_service.send_verification_code(phone)

    if success:
        return resp_200(None, "验证码发送成功")

    return resp_500(None, "验证码发送失败")


@router.post("/code_login")
async def login_code(
        item: LoginCodeRequest,
        user_service: UserService = Depends(get_user_service)
):
    """用户验证码登录"""
    user, token = user_service.authenticate_by_code(
        phone=item.phone,
        code=item.code
    )

    return resp_200(LoginAuthResponse(user=user, token=token))
