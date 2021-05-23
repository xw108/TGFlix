from .deps import APIRouter,Request,crud,templates,CONFIG

router = APIRouter()

@router.get("/")
async def get_series_episodes(request: Request):
    m = await crud.get_movies( 0, 6)
    s = await crud.get_series( 0, 6)
    return templates.TemplateResponse("home.html", {"request": request,'movies' : m, 'series' : s})


@router.get("/search")
async def search(request: Request,m:str, page:int = 1):
    if page < 1:
        page = 1
    r = await crud.search_movies( m.lower(),(page-1)*CONFIG.MAX_ITEMS_PER_PAGE, CONFIG.MAX_ITEMS_PER_PAGE)
    return templates.TemplateResponse("movies.html",{
        "request"  : request,
        'title'     : f'Search results for {m}.',
        'movies'    : r,
        'prefix'    : f'm={m}',
        'page'      :page
    })

@router.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html",{"request"  : request})

@router.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html",{"request"  : request})