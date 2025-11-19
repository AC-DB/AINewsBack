import redis
from fastapi import Depends
from sqlmodel import Session

from ainewsback.core.database import get_session
from ainewsback.core.reids import get_redis
from ainewsback.services.user_service import UserService
from ainewsback.services.verification import VerificationService


async def get_verification(
        r: redis.Redis = Depends(get_redis)) -> VerificationService:
    return VerificationService(r)


def get_user_service(
        session: Session = Depends(get_session),
        verification: VerificationService = Depends(get_verification)
) -> UserService:
    """获取用户服务依赖"""
    return UserService(session, verification)
