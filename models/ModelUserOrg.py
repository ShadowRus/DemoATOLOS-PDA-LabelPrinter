from sqlalchemy import Column, Integer, String,ForeignKey,JSON
from api.deps import Base

from pydantic import BaseModel, HttpUrl, Field
from typing import Sequence, List, Optional


class ModelUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    user_surname = Column(String)
    org_id = Column(Integer,ForeignKey("organization.id"))
    role_id = Column(Integer,ForeignKey("user_role.id"))
    attr_1 = Column(String)
    attr_2 = Column(String)
    attr_3 = Column(String)
    attr_4 = Column(String)
    attr_5 = Column(String)
    added_at = Column(Integer)
    is_deleted = Column(Integer)

class ModelOrg(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True, index=True)
    organization_name = Column(String)
    attr_1 = Column(String)
    attr_2 = Column(String)
    attr_3 = Column(String)
    attr_4 = Column(String)
    attr_5 = Column(String)
    added_at = Column(Integer)
    is_deleted = Column(Integer)

class ModelUserRole(Base):
    __tablename__="user_role"
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer,ForeignKey("role.id"))
    user_id = Column(Integer,ForeignKey("user.id"))
    access_by = Column(Integer,ForeignKey("user.id"))
    added_at = Column(Integer)
    is_deleted = Column(Integer)

class ModelRole(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    root = Column(Integer)
    auth = Column(Integer)
    access_endpoints = Column(JSON)
    is_deleted = Column(Integer)




class UserResponse(BaseModel):
    user_name:Optional[str]=Field(None)
    user_surname: Optional[str]=Field(None)
    organization: Optional[str]=Field(None)
    attr_1: Optional[str]=Field(None)
    attr_2: Optional[str]=Field(None)
    attr_3: Optional[str] = Field(None)
    attr_4: Optional[str] = Field(None)
    attr_5: Optional[str] = Field(None)

class SematResponse(BaseModel):
    user_id: Optional[int]=Field(None)
    name: Optional[str]=Field(None)
    count: Optional[int]=Field(None)


class SematActionRequest(BaseModel):
    userId: int
    goods_id: int
    action: int