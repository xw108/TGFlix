from fastapi import (
    HTTPException,
    APIRouter,
    Depends,
    HTTPException,
    Request,
)

from fastapi.responses import (
    HTMLResponse, 
    StreamingResponse,
    Response, 
    FileResponse,
    RedirectResponse,
)

from telethon.tl import types
from telethon import utils as tgUtils


from ..core import CONFIG
from ..tg import client, utils
from .. import crud

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["appc"] = CONFIG

class DwnloadManger:
    downloads:int = 0
