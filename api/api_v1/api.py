from fastapi import APIRouter
from api.api_v1.endpoints import admin_console
from api.api_v1.endpoints import print_label_service
from api.api_v1.endpoints import search_goods_service
from api.api_v1.endpoints import semat_game


api_router = APIRouter()
api_router.include_router(admin_console.router, tags=["Настройки системы, загрузка номенклатуры"])
api_router.include_router(print_label_service.router,tags=["Печать этикеток на принтеры этикеток"])
api_router.include_router(search_goods_service.router,tags=["Поиск товаров в базе данных"])
api_router.include_router(semat_game.router,tags=["Демо-игра для СЕМАТ Russia 2024"])

