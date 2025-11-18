from typing import List, Optional

from sqlmodel import col, select

from ainewsback.models.user import ApUser
from ainewsback.repositories.base import BaseRepository


class UserRepository(BaseRepository[ApUser]):
    """用户数据访问层"""

    def get_by_phone(self, phone: str) -> Optional[ApUser]:
        """根据手机号查询用户"""
        statement = select(ApUser).where(ApUser.phone == phone)
        return self.session.exec(statement).first()

    def get_by_name(self, name: str) -> Optional[ApUser]:
        """根据用户名查询"""
        statement = select(ApUser).where(ApUser.name == name)
        return self.session.exec(statement).first()

    def search_users(self, keyword: str, skip: int = 0,
                     limit: int = 100) -> List[ApUser]:
        """搜索用户"""
        statement = select(ApUser).where(
            col(ApUser.name).contains(keyword) | col(ApUser.name).contains(
                keyword)
        ).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())
