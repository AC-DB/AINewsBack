from typing import Optional, Tuple
from sqlmodel import Session

from ainewsback.models.user import ApUser
from ainewsback.repositories.user_repository import UserRepository
from ainewsback.services.verification import VerificationService
from ainewsback.utils.jwt import JWTUtils
from ainewsback.utils.password import PasswordUtil


class UserService:
    """用户业务逻辑层"""

    def __init__(self, session: Session, verification: VerificationService):
        self.repository = UserRepository(ApUser, session)
        self.verification = verification

    def get_user_by_id(self, user_id: int) -> Optional[ApUser]:
        """获取用户"""
        return self.repository.get(user_id)

    def get_user_by_phone(self, phone: str) -> Optional[ApUser]:
        """根据手机号获取用户"""
        return self.repository.get_by_phone(phone)

    def create_user_default(self, phone: str) -> ApUser:
        """创建默认用户"""
        name = "user_" + PasswordUtil.generate_random_password(6)
        random_password = PasswordUtil.generate_random_password(8)
        hashed_password, salt = PasswordUtil.create_password(
            random_password)

        user = ApUser(name=name, phone=phone, password=hashed_password, salt=salt)
        return self.repository.create(user)

    async def send_verification_code(self, phone: str, scene: str = "login") -> Tuple[bool, str, Optional[str]]:
        """
        发送验证码

        Returns:
            是否发送成功
        """
        return await self.verification.send_code(phone, scene)

    async def verify_verification_code(self, phone: str, code: str, scene: str = "login") -> Tuple[bool, str]:
        """
        验证验证码

        Returns:
            是否验证成功
        """
        return await self.verification.verify_code(phone, code, scene)

    def authenticate_by_password(self, phone: str, password: str) -> tuple[
        Optional[ApUser], Optional[str], str]:
        """
        密码登录认证

        Returns:
            (用户对象, token, 错误信息)
        """
        user = self.get_user_by_phone(phone)
        if not user:
            return None, None, "用户不存在"

        if not PasswordUtil.verify_password(password, user.password,
                                            user.salt):
            return None, None, "密码错误"

        token = JWTUtils.create_token(str(user.id))
        return user, token, ""

    async def authenticate_by_code(self, phone: str, code: str) -> tuple[
        ApUser, str]:
        """
        验证码登录认证(自动注册)

        Returns:
            (用户对象, token)
        """
        ok, msg = await self.verification.verify_code(phone, code, "login")

        if not ok:
            raise ValueError(msg)

        user = self.get_user_by_phone(phone)
        if not user:
            user = self.create_user_default(phone)

        token = JWTUtils.create_token(str(user.id))
        return user, token
