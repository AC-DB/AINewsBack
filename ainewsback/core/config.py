import tomllib
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import MySQLDsn, computed_field
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
    APP_ENV: str = "dev"
    DEBUG: bool = False
    LOG_LEVEL: str = "info"

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    MYSQL_SERVER: str = ""
    MYSQL_PORT: int = 0
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MySQLDsn:
        return MySQLDsn.build(
            scheme="mysql+pymysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_SERVER,
            port=self.MYSQL_PORT,
            path=self.MYSQL_DB,
        )

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
