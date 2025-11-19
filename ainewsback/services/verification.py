from typing import Optional, Tuple

import redis

from ainewsback.core.config import settings
from ainewsback.utils.code_generator import CodeGenerator
from ainewsback.utils.dingtalk_robot import VerificationNotifier


class VerificationService:
    """验证码服务"""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.code_generator = CodeGenerator()
        self.notifier = VerificationNotifier()

    def _get_code_key(self, mobile: str, scene: str) -> str:
        """生成 Redis key"""
        return f"verification:code:{scene}:{mobile}"

    def _get_rate_limit_key(self, mobile: str) -> str:
        """生成频率限制 key"""
        return f"verification:rate_limit:{mobile}"

    def _get_attempt_key(self, mobile: str, scene: str) -> str:
        """生成尝试次数 key"""
        return f"verification:attempts:{scene}:{mobile}"

    async def check_rate_limit(self, mobile: str) -> Tuple[bool, Optional[int]]:
        """
        检查发送频率限制
        Returns: (是否允许发送, 剩余等待时间)
        """
        rate_key = self._get_rate_limit_key(mobile)
        ttl = await self.redis.ttl(rate_key)

        if ttl > 0:
            return False, ttl
        return True, None

    async def send_code(self, mobile: str, scene: str = "login") -> Tuple[
        bool, str, Optional[str]]:
        """
        发送验证码
        Returns: (成功状态, 消息, 验证码)
        """
        # 检查发送频率
        can_send, wait_time = await self.check_rate_limit(mobile)
        if not can_send:
            return False, f"发送过于频繁，请 {wait_time} 秒后再试", None

        # 生成验证码
        code = self.code_generator.generate_numeric_code()

        # 保存到 Redis
        code_key = self._get_code_key(mobile, scene)
        rate_key = self._get_rate_limit_key(mobile)
        # 重置验证尝试次数
        attempt_key = self._get_attempt_key(mobile, scene)

        async with self.redis.pipeline() as pipe:
            # 保存验证码，设置过期时间
            await pipe.setex(code_key, settings.CODE_EXPIRE_SECONDS, code)
            # 设置发送频率限制
            await pipe.setex(rate_key, settings.CODE_RATE_LIMIT, "1")
            await pipe.delete(attempt_key)
            await pipe.execute()

        # 发送钉钉通知
        success, message = await self.notifier.send_verification_code(mobile, code, scene)
        if not success:
            return False, message, None

        return True, "验证码发送成功", code

    async def verify_code(self, mobile: str, code: str, scene: str = "login") -> \
            Tuple[bool, str]:
        """
        验证验证码
        Returns: (验证结果, 消息)
        """
        code_key = self._get_code_key(mobile, scene)
        attempt_key = self._get_attempt_key(mobile, scene)

        # 检查验证码是否存在
        stored_code = self.redis.get(code_key)
        if not stored_code:
            return False, "验证码不存在或已过期"

        # 检查验证尝试次数
        attempts = self.redis.get(attempt_key)
        current_attempts = int(attempts) if attempts else 0

        if current_attempts >= settings.MAX_VERIFY_ATTEMPTS:
            # 超过最大尝试次数，删除验证码
            await self.redis.delete(code_key)
            return False, "验证失败次数过多，请重新获取验证码"

        # 验证码比对
        if code != stored_code:
            # 增加尝试次数
            await self.redis.incr(attempt_key)
            await self.redis.expire(attempt_key, settings.CODE_EXPIRE_SECONDS)
            remaining = settings.MAX_VERIFY_ATTEMPTS - current_attempts - 1
            return False, f"验证码错误，还有 {remaining} 次尝试机会"

        # 验证成功，删除验证码和尝试记录
        async with self.redis.pipeline() as pipe:
            await pipe.delete(code_key)
            await pipe.delete(attempt_key)
            await pipe.execute()

        return True, "验证成功"

    async def get_code_info(self, mobile: str, scene: str = "login") -> Optional[
        dict]:
        """获取验证码信息（调试用）"""
        code_key = self._get_code_key(mobile, scene)
        code = self.redis.get(code_key)
        ttl = self.redis.ttl(code_key)

        if code:
            return {
                "code": code,
                "expires_in": ttl,
                "mobile": mobile,
                "scene": scene
            }
        return None
