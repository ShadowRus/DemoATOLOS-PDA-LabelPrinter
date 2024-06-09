import asyncio
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from models.Goods import Goods,AddGoodsRespone
from api import deps
from sqlalchemy.orm import Session
from sqlalchemy import or_,func
from api import deps
import re

import datetime

router = APIRouter()
now = datetime.datetime.now()

def get_value_or_none(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return None


@router.get("/barcode",summary="Поиск по идентификационному коду",
             description="Товар по идентификационному коду")
async def barcode(code, db: Session = Depends(deps.get_db)):
    goods_temp = db.query(Goods).filter((Goods.id_1 == str(code))|
                                             (Goods.id_2 == str(code))|
                                             (Goods.id_3 == str(code))|
                                             (Goods.id_4 == str(code))|(Goods.id_5 == str(code))).all()

    return goods_temp


@router.get("/search", summary="Поиск товара по названию или любому идентификатору",
             description="Ищет похожие совпадения в названии")
async def search(name:str, db: Session = Depends(deps.get_db)):
    name = name.strip()
    name = re.sub(r'[^\w\s]','',name)
    if name.isdigit():
        goods_temp = db.query(Goods).filter((Goods.id_1 == str(name)) |
                                            (Goods.id_2 == str(name)) |
                                            (Goods.id_3 == str(name)) |
                                            (Goods.id_4 == str(name)) | (Goods.id_5 == str(name))).all()
    else:
        name = name.lower()
        goods_temp = db.query(Goods).filter(func.lower(Goods.goods_name).like(f"%{name}%")).all()
    return goods_temp

# Добавление нового товара
@router.post("/goods", summary="Добавление нового товара",
             description="Добавляем в таблицу нового участника, ставим тэг is_manual = 1")
async def add_goods(goods_data:AddGoodsRespone, db: Session = Depends(deps.get_db)):
    goods = Goods(
        id_1=goods_data.id_1,
        id_2=goods_data.id_2,
        id_3=goods_data.id_3,
        id_4=goods_data.id_4,
        id_5=goods_data.id_5,
        goods_name=goods_data.goods_name,
        attr_1=goods_data.attr_1,
        attr_2=goods_data.attr_2,
        attr_3=goods_data.attr_3,
        attr_4=goods_data.attr_4,
        attr_5=goods_data.attr_5,
        attr_6=goods_data.attr_6,
        is_deleted=0, is_manual=1, is_add_at=datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S'))
    db.add(goods)
    db.commit()
    db.refresh(goods)
    return goods
