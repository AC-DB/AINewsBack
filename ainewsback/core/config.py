import tomllib
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Literal, Optional

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PyProjectConfig:
    """读取 pyproject.toml 的辅助类"""

    _cache: Optional[Dict[str, Any]] = None

    @classmethod
    def load(cls) -> Dict[str, Any]:
        """加载并缓存 pyproject.toml"""
        if cls._cache is not None:
            return cls._cache

        pyproject_path = Path(
            __file__).parent.parent.parent / "pyproject.toml"

        if not pyproject_path.exists():
            raise FileNotFoundError(
                f"pyproject.toml not found at {pyproject_path}")

        with open(pyproject_path, "rb") as f:
            cls._cache = tomllib.load(f)

        return cls._cache

    @classmethod
    def get_poetry_config(cls) -> Dict[str, Any]:
        """获取 Poetry 配置"""
        return cls.load().get("project", {})

    @classmethod
    def get_name(cls) -> str:
        """获取项目名称"""
        return cls.get_poetry_config().get("name", "Unknown")

    @classmethod
    def get_version(cls) -> str:
        """获取项目版本"""
        return cls.get_poetry_config().get("version", "0.0.0")

    @classmethod
    def get_description(cls) -> str:
        """获取项目描述"""
        return cls.get_poetry_config().get("description", "Unknown")

    @classmethod
    def get_first_author_contact(cls) -> dict:
        """
        获取项目第一个作者的 name 和 email（用于 FastAPI contact）
        """
        authors = cls.get_poetry_config().get("authors", [])
        author_obj = authors[0] if authors else {}
        if isinstance(author_obj, dict):
            return {
                "name": author_obj.get("name"),
                "email": author_obj.get("email"),
            }
        return {}

    @classmethod
    def get_license(cls) -> dict:
        """获取项目许可证"""
        license_info = cls.get_poetry_config().get("license", "Unknow")

        return {
            "name": license_info,
            "identifier": license_info,
        }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore',
                                      case_sensitive=False,
                                      env_file_encoding="utf-8")

    # 项目元数据
    APP_NAME: str = PyProjectConfig.get_name()
    APP_VERSION: str = PyProjectConfig.get_version()
    APP_DESCRIPTION: str = PyProjectConfig.get_description()
    ADMIN_CONTACT: dict = PyProjectConfig.get_first_author_contact()
    APP_LICENSE: dict = PyProjectConfig.get_license()

    # 应用配置
    APP_ENV: Literal["dev", "pro", "test"] = "dev"
    DEBUG: bool = False

    # Logging
    LOG_LEVEL: str = "info"
    LOG_TO_CONSOLE: bool = True
    LOG_TO_FILE: bool = True
    LOG_FILE_PATH: str = "logs"
    LOG_FILE_MAX_BYTES: int = 10485760  # 10MB
    LOG_FILE_BACKUP_COUNT: int = 10
    LOG_FORMAT: Literal["json", "text", "colored"] = "json"

    # Access Log
    ENABLE_ACCESS_LOG: bool = True
    ACCESS_LOG_PATH: str = "logs/access.log"

    # SQL Log
    ENABLE_SQL_LOG: bool = False
    SQL_LOG_LEVEL: str = "INFO"

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    DB_SERVER: str = ""
    DB_PORT: int = 0
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_SERVER,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    # 钉钉机器人配置
    DINGTALK_WEBHOOK_URL: str = ""
    DINGTALK_SECRET: str = ""

    # 验证码设置
    CODE_LENGTH: int = 0
    CODE_EXPIRE_SECONDS: int = 0
    CODE_RATE_LIMIT: int = 0
    MAX_VERIFY_ATTEMPTS: int = 0

    # Redis
    REDIS_HOST: str = ""
    REDIS_PORT: int = 0
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    REDIS_DECODE_RESPONSES: bool = True

    # JWT 配置
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0
    CURRENT_ISSUER: str = ""
    TOKEN_AUDIENCE: list[str] = []
    ACCESS_TOKEN_ISSUER: list[str] = []


# 创建全局配置实例
settings = Settings()


# 导出便捷函数
@lru_cache
def get_settings() -> Settings:
    return Settings()
