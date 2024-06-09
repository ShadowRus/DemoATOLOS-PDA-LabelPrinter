from fastapi import FastAPI, APIRouter,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.api_v1.api import api_router
from api import deps
import socket
from decouple import config


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


HOST = config('HOST', default=extract_ip())
PORT = config('PORT', default=8091)

root_router = APIRouter()
app = FastAPI(title="DemoATOL_OS_Solution")

app.include_router(api_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index_s1.html", {"request": request})


deps.Base.metadata.create_all(bind=deps.engine)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, log_level="debug")

