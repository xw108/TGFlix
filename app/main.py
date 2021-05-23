from fastapi import FastAPI,staticfiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from . import api, core,tg
import logging

logger   = logging.getLogger("uvicorn.error")

app = FastAPI( debug= core.CONFIG.DEBUG)

app.mount("/static", staticfiles.StaticFiles(directory="app/static"), name="static")
app.include_router( api.api_router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return api.templates.TemplateResponse("error.html",
        {"request" : request,'code' : exc.status_code,'m' : str(exc.detail)})


@app.on_event("startup")
async def startup_event():
    logger.info("Telegram client starting ...")
    await tg.client.start()
    await core.db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info('Telegram client stoping ...')
    await tg.client.disconnect()
    await core.db.disconnect()