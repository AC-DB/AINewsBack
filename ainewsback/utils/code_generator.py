import random
import string

from ainewsback.core.config import settings


class CodeGenerator:
    """验证码生成器"""

    @staticmethod
    def generate_numeric_code(length: int = None) -> str:
        """生成数字验证码"""
        length = length or settings.CODE_LENGTH
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])

    @staticmethod
    def generate_alphanumeric_code(length: int = 6) -> str:
        """生成字母数字混合验证码"""
        characters = string.ascii_uppercase + string.digits
        # 排除易混淆字符
        characters = characters.replace('O', '').replace('0', '').replace(
            'I', '').replace('1', '')
        return ''.join(random.choices(characters, k=length))

    @staticmethod
    def generate_mixed_code(length: int = 6) -> str:
        """生成包含小写字母的验证码"""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))
