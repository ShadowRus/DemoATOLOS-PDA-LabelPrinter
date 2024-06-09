from sqlalchemy import Column, Integer, String
from api.deps import Base

from pydantic import BaseModel, HttpUrl, Field
from typing import Sequence, List, Optional

class Goods(Base):
    __tablename__="Goods"
    id = Column(Integer, primary_key=True, index=True)
    goods_name = Column(String)
    id_1 = Column(String,index=True)
    id_2 = Column(String,index=True)
    id_3 = Column(String)
    id_4 = Column(String)
    id_5 = Column(String)
    attr_1 = Column(String,index=True)
    attr_2= Column(String,index=True)
    attr_3 = Column(String)
    attr_4 = Column(String)
    attr_5 = Column(String)
    attr_6 = Column(String)
    is_deleted = Column(Integer)
    is_add_at = Column(String)
    is_manual = Column(Integer)

