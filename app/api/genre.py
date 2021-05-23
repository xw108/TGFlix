from .deps import APIRouter,HTTPException,Request,CONFIG,crud,templates

router = APIRouter()


@router.get("/{slug}")
async def get_movie(request: Request, slug:str, page:int = 1):
    c, s = await crud.get_genre_id( slug)
    if not c:
        raise HTTPException(404, "Page not found")

    if page < 1:
        page = 1
    m = await crud.get_all_by_genre( c, (page-1)*CONFIG.MAX_ITEMS_PER_PAGE, CONFIG.MAX_ITEMS_PER_PAGE)
    title = f'All {s.title() } Movies/Series'
    return templates.TemplateResponse("movies.html", {
        "request": request,
        'movies' : m,
        'page' : page,
        'title' : title
    })

@router.get("")
async def get_movie(request: Request, page:int = 1):
    if page < 1:
        page = 1
    c = await crud.get_all_genres( (page-1)*CONFIG.MAX_ITEMS_PER_PAGE, CONFIG.MAX_ITEMS_PER_PAGE)
    return templates.TemplateResponse("genre.html", {
        "request": request,
        'cl' : c,
        'page' : page
    })