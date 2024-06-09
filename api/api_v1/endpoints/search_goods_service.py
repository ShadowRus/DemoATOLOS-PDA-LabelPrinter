import asyncio
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from models.Goods import Goods
from api import deps
from sqlalchemy.orm import Session
from sqlalchemy import or_,func
from api import deps
import re

import datetime

router = APIRouter()
now = datetime.datetime.now()


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