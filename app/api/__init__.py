from fastapi import APIRouter
from . import movie, epfile, genre, series, general
from . deps import templates

api_router = APIRouter()



api_router.include_router( movie.router,    prefix="/movie",    tags=["Movies"])
api_router.include_router( series.router,   prefix="/series",   tags=["TV Series"])
api_router.include_router( epfile.router,   prefix="/file",     tags=["Files"])
api_router.include_router( genre.router,    prefix="/genere",   tags=["Generes"])
api_router.include_router( general.router,  prefix='',          tags=["Generes"])