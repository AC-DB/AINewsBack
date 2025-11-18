from datetime import datetime
from enum import IntEnum
from typing import Optional

from sqlalchemy import Column, Integer
from sqlmodel import Field, SQLModel


# 枚举类定义
class SexEnum(IntEnum):
    """性别枚举"""
    MALE = 0
    FEMALE = 1
    UNKNOWN = 2


class CertificationStatus(IntEnum):
    """认证状态枚举"""
    NOT_CERTIFIED = 0
    CERTIFIED = 1


class UserStatus(IntEnum):
    """用户状态枚举"""
    NORMAL = 0
    LOCKED = 1


class UserFlag(IntEnum):
    """用户身份标识枚举"""
    NORMAL_USER = 0
    MEDIA_USER = 1
    VIP_USER = 2


class ApUser(SQLModel, table=True):
    """APP用户信息表模型"""

    __tablename__ = "ap_user"
    __table_args__ = {"comment": "APP用户信息表"}

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="主键"
    )

    salt: Optional[str] = Field(
        default=None,
        max_length=32,
        description="密码、通信等加密盐"
    )

    name: Optional[str] = Field(
        default=None,
        max_length=20,
        description="用户名"
    )

    password: Optional[str] = Field(
        default=None,
        max_length=32,
        description="密码,md5加密"
    )

    phone: Optional[str] = Field(
        default=None,
        max_length=11,
        description="手机号"
    )

    image: Optional[str] = Field(
        default=None,
        max_length=255,
        description="头像"
    )

    sex: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer),
        description="0 男 1 女 2 未知"
    )

    is_certification: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer),
        description="0 未 1 是"
    )

    is_identity_authentication: Optional[bool] = Field(
        default=None,
        description="是否身份认证"
    )

    status: int = Field(
        default=UserStatus.NORMAL,
        sa_column=Column(Integer),
        description="0正常 1锁定"
    )

    flag: int = Field(
        default=UserFlag.NORMAL_USER,
        sa_column=Column(Integer),
        description="0 普通用户 1 自媒体人 2 大V"
    )

    created_time: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="注册时间"
    )
