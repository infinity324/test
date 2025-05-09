# models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

Base = declarative_base()


class User(Base):
    """数据库用户模型"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)


class UserCreate(BaseModel):
    """创建用户的Pydantic模型"""
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    """更新用户的Pydantic模型"""
    name: Optional[str]
    email: Optional[EmailStr]
