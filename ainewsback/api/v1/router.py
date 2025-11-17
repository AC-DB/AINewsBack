from fastapi import APIRouter
from ainewsback.api.v1.user import logon_router
from ainewsback.api.v1.base import root_router

# 用户端路由
user_router = APIRouter(prefix='/user/api/v1')
user_router.include_router(logon_router)

# 基础路由
base_router = APIRouter()
base_router.include_router(root_router)

# 总路由
router = APIRouter()
router.include_router(user_router)
router.include_router(base_router)