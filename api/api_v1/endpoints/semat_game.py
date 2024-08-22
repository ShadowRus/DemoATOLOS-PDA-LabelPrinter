from fastapi import APIRouter,Depends, Security,Body,HTTPException, Body,Request,status
from fastapi.responses import JSONResponse,HTMLResponse,JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import SQLAlchemyError
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from api import deps
import datetime
import hashlib
import json
import time

from api.deps import get_db
from models.ModelUserOrg import ModelUser, UserResponse,SematResponse,SematActionRequest
from models.Goods import Goods,BarcodeRequest
from services.services import decode_or_return
from logger.logger_config import logger

router = APIRouter()

templates = Jinja2Templates(directory="templates")

router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/semat", response_class=HTMLResponse)
async def home(request: Request):
    logger.debug(f'/semat {request.client.host} is connected')
    return templates.TemplateResponse("semat_game_rev.html", {"request": request})


@router.post("/semat/reg", response_model=SematResponse)
def add_user(request: Request,user: UserResponse, db: Session = Depends(get_db)):
    logger.debug(f'/semat/reg data {user}')
    db_user = ModelUser(
        user_name = user.user_name,
        user_surname = user.user_surname,
        attr_1 = user.attr_1,
        attr_2 = user.attr_2,
        attr_3 = user.attr_3,
        attr_4 = user.attr_4,
        attr_5 = user.attr_5,
        added_at = int(time.time()),
        is_deleted = 0
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.debug(f'/semat/reg response {db_user.id} _ {db_user.user_name} _ {int(db_user.attr_1 if db_user.attr_1 else 0)} ')
    return SematResponse(user_id=db_user.id, name=db_user.user_name, count=int(db_user.attr_1 if db_user.attr_1 else 0))

@router.post("/semat/search")
async def barcode(request: BarcodeRequest, db: Session = Depends(deps.get_db)):
    logger.debug(f'/semat/search data {request.code}')
    try:
        # Декодирование кода
        code = decode_or_return(request.code)

        # Поиск в базе данных
        goods_temp = db.query(Goods).filter(
            (Goods.id_1 == str(code)) |
            (Goods.id_2 == str(code)) |
            (Goods.id_3 == str(code)) |
            (Goods.id_4 == str(code)) |
            (Goods.id_5 == str(code))
        ).first()
        # response = [{"goods_id": item.id, "goods_name": item.goods_name} for item in goods_temp]

        # Проверка, найден ли товар
        if not goods_temp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден")

        # Формирование ответа
        logger.debug(f'/semat/search response {goods_temp.id} _ {goods_temp.goods_name}')

        return JSONResponse(status_code=200, content= {"goods_id": goods_temp.id, "goods_name": goods_temp.goods_name})

    except ValueError as e:
        # Обработка ошибок декодирования
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except SQLAlchemyError as e:
        # Обработка ошибок базы данных
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка базы данных")

    except Exception as e:
        # Общая обработка прочих ошибок
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))





@router.post("/semat/action")
async def update_action(request: SematActionRequest, db: Session = Depends(get_db)):
# async def update_action(body=Body(), db: Session = Depends(get_db)):
    logger.debug(f'/semat/action data {request}')
    if 5 ==5 :
    #try:
        logger.debug(f'/semat/action data {request}')
        goods = db.query(Goods).filter(Goods.id == request.goods_id).first()


        user = db.query(ModelUser).filter(ModelUser.id == request.userId).first()


        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not goods:
            return JSONResponse(status_code=200, content={"count": user.attr_1})
        logger.debug(f'/semat/action goods.attr1 {goods.attr_1} and request.action {request.action}')
        logger.debug(f'/semat/action user.attr_1 {user.attr_1}')
        if int(goods.attr_1) == int(request.action):
            logger.debug(f'TRUE')
            user.attr_1 = str(int(user.attr_1) + 1)
        else:
            logger.debug(f'FALSE')
            user.attr_1 = str(int(user.attr_1) - 1)

        db.commit()
        db.refresh(user)


        logger.debug(f'/semat/action response {user.attr_1}')
        return JSONResponse(status_code=200, content={"count": user.attr_1})

    # except HTTPException as http_exc:
    #     logger.error(f'HTTP error: {http_exc.detail}')
    #     raise http_exc
    #
    # except SQLAlchemyError as db_exc:
    #     logger.error(f'Database error: {str(db_exc)}')
    #     # Откат изменений в случае ошибки базы данных
    #     db.rollback()
    #     raise HTTPException(status_code=500, detail="Database error")
    #
    # except Exception as exc:
    #     logger.error(f'Unexpected error: {str(exc)}')
    #     # Откат изменений в случае неожиданной ошибки
    #     db.rollback()
    #     raise HTTPException(status_code=500, detail="Internal server error")
