from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.Goods import Goods,AddGoodsRespone
from sqlalchemy.orm import Session
from sqlalchemy import func
from api import deps
import re
from services.services import decode_or_return,get_goods_name,BARCODE_API_NAME_GOODS,BARCODE_KEY,BARCODE_API_TOKEN

import datetime

router = APIRouter()
now = datetime.datetime.now()



@router.get("/barcode",summary="Поиск по идентификационному коду",
             description="Товар по идентификационному коду. Идентификационный код может быть передан как base64 или как обычное представление")
async def barcode(code, db: Session = Depends(deps.get_db)):
    code = decode_or_return(code)
    goods_temp = db.query(Goods).filter((Goods.id_1 == str(code))|
                                             (Goods.id_2 == str(code))|
                                             (Goods.id_3 == str(code))|
                                             (Goods.id_4 == str(code))|(Goods.id_5 == str(code))).all()

    return goods_temp


@router.get("/search", summary="Поиск товара по названию или любому идентификатору",
             description="Ищет похожие совпадения в названии")
async def search(name:str, db: Session = Depends(deps.get_db)):
    name = decode_or_return(name)
    name = name.strip()
    name = re.sub(r'[^\w\s]','',name)
    if name.isdigit():
        goods_temp = db.query(Goods).filter((Goods.id_1 == str(name)) |
                                            (Goods.id_2 == str(name)) |
                                            (Goods.id_3 == str(name)) |
                                            (Goods.id_4 == str(name)) | (Goods.id_5 == str(name))).all()
    else:
        #name = name.lower()
        print(name)
        goods_temp = db.query(Goods).filter((Goods.goods_name).like(f"%{name}%")).all()
    return goods_temp

# Добавление нового товара
@router.post("/goods", summary="Добавление нового товара",
             description="Добавляем в таблицу нового участника, ставим тэг is_manual = 1")
async def add_goods(goods_data:AddGoodsRespone, db: Session = Depends(deps.get_db)):
    try:
        goods = Goods(
            id_1=decode_or_return(goods_data.id_1),
            id_2=decode_or_return(goods_data.id_2),
            id_3=decode_or_return(goods_data.id_3),
            id_4=decode_or_return(goods_data.id_4),
            id_5=decode_or_return(goods_data.id_5),
            goods_name=decode_or_return(goods_data.goods_name),
            attr_1=decode_or_return(goods_data.attr_1),
            attr_2=decode_or_return(goods_data.attr_2),
            attr_3=decode_or_return(goods_data.attr_3),
            attr_4=decode_or_return(goods_data.attr_4),
            attr_5=decode_or_return(goods_data.attr_5),
            attr_6=decode_or_return(goods_data.attr_6),
            is_deleted=0, is_manual=1, is_add_at=datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S'))
        db.add(goods)
        db.commit()
        db.refresh(goods)
        return goods
    except:
        return JSONResponse(status_code=500, content={'status': 'Error'})


@router.get("/web_goods_name",summary="Получение информации о товаре по его штрихкоду",
             description="Используется платный сторронний сервис BarcodesOlegon")
def get_name(barcode:str):
    return get_goods_name(str(BARCODE_API_TOKEN),str(BARCODE_API_NAME_GOODS),str(BARCODE_KEY),str(barcode))
