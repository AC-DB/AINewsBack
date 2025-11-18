import hashlib
import secrets
import string
from typing import Tuple


class PasswordUtil:
    """密码加密工具类"""

    @staticmethod
    def generate_salt(length: int = 16) -> str:
        """
        生成随机盐值

        Args:
            length: 盐值长度(字节数)

        Returns:
            十六进制格式的盐值字符串
        """

        return secrets.token_hex(length // 2)  # 每个字节对应两个十六进制字符

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """
        使用盐值对密码进行哈希加密

        Args:
            password: 原始密码
            salt: 盐值

        Returns:
            加密后的密码(MD5哈希值)
        """

        # 将密码和盐值组合
        salted_password = f"{password}{salt}"
        # 使用MD5进行哈希
        hashed = hashlib.md5(salted_password.encode('utf-8')).hexdigest()
        return hashed

    @staticmethod
    def create_password(password: str) -> Tuple[str, str]:
        """
        创建加密密码(生成盐值并加密)

        Args:
            password: 原始密码

        Returns:
            (加密后的密码, 盐值)
        """

        salt = PasswordUtil.generate_salt()
        hashed_password = PasswordUtil.hash_password(password, salt)
        return hashed_password, salt

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
        """
        验证密码是否正确

        Args:
            plain_password: 用户输入的明文密码
            hashed_password: 数据库中存储的加密密码
            salt: 数据库中存储的盐值

        Returns:
            密码是否匹配
        """

        # 使用相同的盐值对输入密码进行哈希
        input_hashed = PasswordUtil.hash_password(plain_password, salt)
        # 比较哈希值
        return input_hashed == hashed_password

    @staticmethod
    def generate_random_password(length: int = 8) -> str:
        """
        生成随机密码

        Args:
            length: 密码长度

        Returns:
            随机密码字符串
        """

        # 包含字母和数字的随机密码
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
