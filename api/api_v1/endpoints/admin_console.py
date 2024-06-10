import asyncio
from fastapi import APIRouter, UploadFile, File, Depends, Request
from fastapi.responses import JSONResponse
from models.Goods import Goods
from models.LabelPrinter import TemplateResponse,Template,PrinterService,PrinterRespone
from services.services import get_value_or_none
from sqlalchemy.orm import Session
from api import deps

import aiofiles as aiofiles
import os
import requests

from decouple import config

import pandas as pd
import datetime

UPLOAD = config('UPLOAD_DIR', default='./uploaded_files')

router = APIRouter()
now = datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')




@router.get("/getmyip", summary="Получить IP4 подключенного устройства",
             description="Реализуем регистрацию устройства")
async def get_my_ip(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}
#--Загрузка файла с номенклатурой
@router.post("/upload", summary="Загрузка файла с номенклатурой",
             description="Загружаем excel заданного формата")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(deps.get_db)):
    try:
        # Делаем что-то с загруженным файлом, например, сохраняем его на сервере
        async with aiofiles.open(os.path.join(UPLOAD, file.filename), 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)
        df = pd.read_excel(os.path.join(UPLOAD, file.filename), engine='openpyxl')
        data = df.to_dict(orient='index')
        for row in data:
            goods = Goods(
                id_1 = get_value_or_none(data[row],'Идентификатор_1'),
                id_2=get_value_or_none(data[row], 'Идентификатор_2'),
                id_3=get_value_or_none(data[row], 'Идентификатор_3'),
                id_4=get_value_or_none(data[row], 'Идентификатор_4'),
                id_5=get_value_or_none(data[row], 'Идентификатор_5'),
                goods_name= get_value_or_none(data[row],'Название товара'),
                attr_1 = get_value_or_none(data[row],'Атрибут_1'),
                attr_2=get_value_or_none(data[row], 'Атрибут_2'),
                attr_3=get_value_or_none(data[row], 'Атрибут_3'),
                attr_4=get_value_or_none(data[row], 'Атрибут_4'),
                attr_5=get_value_or_none(data[row], 'Атрибут_5'),
                attr_6=get_value_or_none(data[row], 'Атрибут_6'),
                is_deleted = 0,is_manual=0, is_add_at = datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S'))
            db.add(goods)
            db.commit()
        db.close()
        return {"filename": file.filename}
    except:
        return JSONResponse(status_code=500, content={'status': 'Error'})

#--Загрузка файла с номенклатурой
@router.post("/template", summary="Загружаем шаблон этикетки",
             description="Этикетка ZPL")
async def template(data:TemplateResponse,db: Session = Depends(deps.get_db)):
    try:
        template = Template(templ_data = data.label,
                            templ_name = data.name,
                            is_default = data.is_default,
                            is_deleted = 0)
        db.add(template)
        db.commit()
        db.close()
        return JSONResponse(status_code=200, content={'status': 'Success'})
    except:
        return JSONResponse(status_code=500, content={'status': 'Error'})



@router.post("/printer", summary="Добавляем принтер в БД",
             description="Отправка на сервер файла конфигурации ")
async def printer(data:PrinterRespone,db: Session = Depends(deps.get_db)):
    try:
        printer = PrinterService(print_name = data.name,url = data.url,is_default = data.is_default,
                                 port = data.port,type = data.type,is_deleted = 0)
        db.add(printer)
        db.commit()
        db.close()
        return JSONResponse(status_code=200, content={'status': 'Success'})
    except:
        return JSONResponse(status_code=500, content={'status': 'Error'})

#----Очистка БД
@router.get("/clear_db/goods", summary="Очистка БД с данными Номенклатуры",
             description="Очищаем таблицу с Номенклатурой")
async def clear_goods(db: Session = Depends(deps.get_db)):
    db.query(Goods).delete()
    db.commit()
    return JSONResponse(status_code=200, content={'status': 'Success'})

@router.get("/clear_db/label_templ", summary="Очистка БД с данными О шаблонах этикеток",
             description="Очищаем таблицу с Шаблонами этикеток")
async def clear_label(db: Session = Depends(deps.get_db)):
    db.query(Template).delete()
    db.commit()
    return JSONResponse(status_code=200, content={'status': 'Success'})

@router.get("/clear_db/printers", summary="Очистка БД с данными О подклбченных принтерах",
             description="Очищаем таблицу с Принтерами")
async def clear_printer(db: Session = Depends(deps.get_db)):
    db.query(PrinterService).delete()
    db.commit()
    return JSONResponse(status_code=200, content={'status': 'Success'})

@router.get("/clear_db", summary="Очистка БД с всеми данными",
             description="Очищаем таблицы с Номенклатурой, Шаблона, Принтерами")
async def clear_all(db: Session = Depends(deps.get_db)):
    db.query(Goods).delete()
    db.query(Template).delete()
    db.query(PrinterService).delete()
    db.commit()
    return JSONResponse(status_code=200, content={'status': 'Success'})