from fastapi import Depends
from sqlmodel import Session

from ainewsback.core.database import get_session
from ainewsback.services.user_service import UserService


def get_user_service(
        session: Session = Depends(get_session)) -> UserService:
    """获取用户服务依赖"""
    return UserService(session)
