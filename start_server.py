from fastapi import FastAPI, APIRouter,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.api_v1.api import api_router
from services.services import extract_ip
from api import deps
from decouple import config





HOST = config('HOST', default=extract_ip())
PORT = config('PORT', default=8091)

root_router = APIRouter()
app = FastAPI(title="DemoATOL_OS_Solution")

app.include_router(api_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index-T.html", {"request": request})


deps.Base.metadata.create_all(bind=deps.engine)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, log_level="debug")

